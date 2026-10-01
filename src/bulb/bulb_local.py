import tinytuya
import time
from config.config import config
from src.logger import logger

DEFAULT_WHITE_TEMPERATURE = 1000

def _create_bulb():
    bulb = tinytuya.BulbDevice(
        config["tuya"]["DEVICE_ID"],
        config["tuya"]["IP"],
        config["tuya"]["LOCAL_KEY"],
    )

    bulb.set_version(3.5)
    bulb.set_socketPersistent(True)
    bulb.set_socketTimeout(0.5)
    # Avoid TinyTuya's default five attempts with five-second gaps (~22.5s).
    bulb.set_socketRetryLimit(1)
    bulb.set_socketRetryDelay(0.1)
    bulb.detect_bulb(nowait=True)

    return bulb

bulb = _create_bulb()

def reconnect():
    global bulb

    reconnect_start = time.perf_counter()
    logger.info("Reconnect: starting")

    try:
        if bulb is not None and bulb.socket:
            logger.debug("Reconnect: closing old bulb socket")
            bulb.socket.close()
    except Exception as e:
        logger.debug(f"Reconnect: error closing old socket: {e}")

    logger.debug("Reconnect: creating new BulbDevice")

    try:
        new_bulb = _create_bulb()

        detect_start = time.perf_counter()

        logger.debug("Reconnect: running detect_bulb()")
        new_bulb.detect_bulb(nowait=False)

        detect_time = time.perf_counter() - detect_start

        logger.debug(
            f"Reconnect: detect_bulb completed in {detect_time:.3f}s"
        )

        logger.debug(f"Reconnect: dpset={new_bulb.dpset}")
        logger.debug(f"Reconnect: have_status={new_bulb._have_status}")

        if not new_bulb.dpset.get("colour"):
            raise RuntimeError("Fresh bulb connection is not configured.")

        logger.info(
            f"Reconnect: fresh bulb configured in "
            f"{time.perf_counter() - reconnect_start:.3f}s"
        )

        # Only make it active AFTER configuration succeeds.
        bulb = new_bulb

    except Exception as e:
        reconnect_time = time.perf_counter() - reconnect_start

        logger.error(
            f"Reconnect failed after {reconnect_time:.3f}s: {e}"
        )

        raise

def set_power(is_on: bool):
    '''Set the power state of the device.'''
    response = bulb.turn_on() if is_on else bulb.turn_off()

    if response is None:
        return True

    return "Err" not in response


def set_color(h: int, s: int, v: int):
    '''Set the color of the device.'''

    h = max(0, min(h, 360)) / 360 #hue must be between 0 and 360, 0 is red, 120 is green, 240 is blue
    s = max(0, min(s, 1000)) / 1000 #saturation must be between 0 and 1000, 0 is no color, 1000 is full color
    v = max(0, min(v, 1000)) / 1000 #value must be between 0 and 1000, 0 is off, 1000 is full brightness

    command_start = time.perf_counter()

    logger.debug(
        f"COLOR command started: "
        f"h={h * 360:.1f}, s={s * 1000:.0f}, v={v * 1000:.0f}"
    )

    try:
        # Color changes arrive continuously; do not wait for a reply on every
        # frame. TinyTuya still returns immediate send errors in nowait mode.
        response = bulb.set_hsv(h, s, v, nowait=True)

        if response is not None and "Err" in response:
            raise RuntimeError(f"TinyTuya rejected COLOR command: {response}")

    except Exception as e:
        elapsed = time.perf_counter() - command_start

        logger.error(
            f"COLOR command failed after {elapsed:.3f}s: {e}"
        )

        raise

    else:
        elapsed = time.perf_counter() - command_start

        logger.debug(
            f"COLOR command completed: latency={elapsed:.3f}s"
        )

        if elapsed >= 0.5:
            logger.warning(
                f"Slow COLOR command: latency={elapsed:.3f}s"
            )

        return True


def set_white(brightness: int, temperature: int = DEFAULT_WHITE_TEMPERATURE):
    '''Set the white light of the device.'''
    global bulb

    brightness = max(10, min(brightness, 1000)) #brightness must be between 10 and 1000
    temperature = max(0, min(temperature, 1000)) #color temperature must be between 0 and 1000

    command_start = time.perf_counter()

    logger.info(
        f"WHITE command started: "
        f"brightness={brightness}, temperature={temperature}"
    )

    white_bulb = tinytuya.BulbDevice(
        config["tuya"]["DEVICE_ID"],
        config["tuya"]["IP"],
        config["tuya"]["LOCAL_KEY"],
    )

    try:
        white_bulb.set_version(3.5)
        white_bulb.set_socketPersistent(True)
        white_bulb.set_socketTimeout(0.5)
        white_bulb.set_socketRetryLimit(1)
        white_bulb.set_socketRetryDelay(0.1)
        white_bulb.detect_bulb(nowait=False)

        if not white_bulb.bulb_configured:
            raise RuntimeError("Fresh white-command connection is not configured.")

        response = white_bulb.set_white(
            brightness,
            temperature,
            nowait=False,
        )

        if response is not None and "Err" in response:
            raise RuntimeError(f"TinyTuya rejected WHITE command: {response}")

        # Adopt the acknowledged connection so its cached mode matches the
        # bulb. This also leaves any fire-and-forget color replies behind on
        # the old socket, which is closed below.
        previous_bulb = bulb
        bulb = white_bulb
        white_bulb = None

        try:
            if previous_bulb is not None and previous_bulb.socket:
                previous_bulb.socket.close()
        except Exception as e:
            logger.debug(f"Previous bulb socket close failed: {e}")

    except Exception as e:
        elapsed = time.perf_counter() - command_start

        logger.error(
            f"WHITE command failed after {elapsed:.3f}s: {e}"
        )

        raise

    else:
        elapsed = time.perf_counter() - command_start

        logger.info(
            f"WHITE command completed: latency={elapsed:.3f}s"
        )

        if elapsed >= 0.5:
            logger.warning(
                f"Slow WHITE command: latency={elapsed:.3f}s"
            )

        return True

    finally:
        if white_bulb is not None:
            try:
                white_bulb.close()
            except Exception as e:
                logger.debug(f"White command connection close failed: {e}")


def check_connection():
    '''Check whether the bulb is reachable.'''

    check_start = time.perf_counter()

    logger.debug("Watchdog: connection check started")

    try:
        # Probe through a separate short-lived device so a health check cannot
        # consume a reply queued on the worker's persistent command socket.
        health_bulb = tinytuya.BulbDevice(
            config["tuya"]["DEVICE_ID"],
            config["tuya"]["IP"],
            config["tuya"]["LOCAL_KEY"],
        )
        health_bulb.set_version(3.5)
        health_bulb.set_socketTimeout(0.5)
        health_bulb.set_socketRetryLimit(1)
        health_bulb.set_socketRetryDelay(0.1)
        response = health_bulb.status()

        elapsed = time.perf_counter() - check_start
        health_bulb.close()

        if response and "Err" not in response:
            logger.debug(
                f"Watchdog: connection OK "
                f"latency={elapsed:.3f}s"
            )
            return True

        logger.warning(
            f"Watchdog: status failed "
            f"latency={elapsed:.3f}s, response={response}"
        )

        logger.warning(
            "Watchdog: worker bulb state: "
            f"id={id(bulb)}, "
            f"socket_exists={bulb.socket is not None}, "
            f"socket_persistent={bulb.socketPersistent}, "
            f"socket_timeout={bulb.connection_timeout}, "
            f"have_status={bulb._have_status}, "
            f"configured={bulb.bulb_configured}, "
            f"bulb_type={bulb.bulb_type}"
        )

        return False

    except Exception as e:
        elapsed = time.perf_counter() - check_start

        logger.warning(
            f"Watchdog: status exception "
            f"latency={elapsed:.3f}s, error={e}"
        )

        logger.warning(
            "Watchdog: worker bulb state after exception: "
            f"id={id(bulb)}, "
            f"socket_exists={bulb.socket is not None}, "
            f"socket_persistent={bulb.socketPersistent}, "
            f"socket_timeout={bulb.connection_timeout}, "
            f"have_status={bulb._have_status}, "
            f"configured={bulb.bulb_configured}, "
            f"bulb_type={bulb.bulb_type}"
        )

        return False
