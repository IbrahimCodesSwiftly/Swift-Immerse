import threading
import time

from src.bulb import set_color, set_white, check_connection, reconnect
from src.logger import logger

_WATCHDOG_INTERVAL = 1.0
_WATCHDOG_CONFIRM_DELAY = 0.1
_WATCHDOG_FAILURE_LIMIT = 2

OUTPUT_FPS = 10
OUTPUT_INTERVAL = 1 / OUTPUT_FPS

_latest_state = None
_last_sent_state = None
_retry_state = None
_retry_after = 0.0
_RETRY_DELAY = 0.5

_lock = threading.Lock()
_bulb_io_lock = threading.Lock()

_running = False
_thread = None

_watchdog_thread = None
_watchdog_running = False

_recovery_thread = None
_recovery_running = False
_recovering = False

_recovery_event = threading.Event()


def start():
    '''Start the bulb output worker.'''
    global _running, _thread, _latest_state
    global _last_sent_state, _watchdog_running, _watchdog_thread
    global _recovery_thread, _recovery_running, _recovering
    global _retry_state, _retry_after

    if _running:
        return

    _recovering = False
    _recovery_event.clear()

    logger.info("Worker starting")

    _latest_state = None
    _last_sent_state = None
    _retry_state = None
    _retry_after = 0.0

    _running = True

    _thread = threading.Thread(
        target=_run,
        daemon=True
    )

    _thread.start()

    _watchdog_running = True

    _watchdog_thread = threading.Thread(
        target=_watchdog,
        daemon=True
    )

    _watchdog_thread.start()

    _recovery_running = True

    _recovery_thread = threading.Thread(
        target=_recovery_worker,
        daemon=True
    )

    _recovery_thread.start()

    logger.info("Worker started")


def stop():
    '''Stop the bulb output worker.'''
    global _running, _thread
    global _watchdog_running, _watchdog_thread
    global _recovery_thread, _recovery_running

    logger.info("Worker stopping")

    _running = False
    _watchdog_running = False
    _recovery_running = False

    if _thread is not None:
        _thread.join()

    if _watchdog_thread is not None:
        _watchdog_thread.join()

    if _recovery_thread is not None:
        _recovery_thread.join()

    _thread = None
    _watchdog_thread = None
    _recovery_thread = None

    logger.info("Worker stopped")


def set_state(mode, value):
    '''Replace the current desired bulb state.'''
    global _latest_state

    with _lock:
        _latest_state = (mode, value)


def _run():
    '''Send the latest desired state at a controlled rate.'''
    global _last_sent_state, _retry_state, _retry_after

    while _running:

        if _recovering:
            time.sleep(OUTPUT_INTERVAL)
            continue

        # Serialize output with recovery, and re-read the desired state after
        # taking the lock so a command queued before recovery cannot go stale.
        with _bulb_io_lock:
            if _recovering:
                state = None
            else:
                with _lock:
                    state = _latest_state

            retry_ready = (
                state != _retry_state
                or time.monotonic() >= _retry_after
            )

            if state is not None and state != _last_sent_state and retry_ready:
                mode, value = state
                send_start = time.perf_counter()

                try:
                    if mode == "color":
                        command_succeeded = set_color(*value)

                    elif mode == "white":
                        command_succeeded = set_white(value)

                    else:
                        command_succeeded = False

                    if not command_succeeded:
                        _retry_state = state
                        _retry_after = time.monotonic() + _RETRY_DELAY
                        logger.warning(
                            f"Worker command not confirmed: mode={mode}; "
                            f"retrying in {_RETRY_DELAY:.1f}s"
                        )
                    else:
                        send_time = time.perf_counter() - send_start

                        logger.debug(
                            f"Command sent: mode={mode}, value={value}, latency={send_time:.3f}s"
                        )
                        if send_time >= 0.5:
                            logger.warning(
                                f"Slow bulb command: mode={mode}, "
                                f"value={value}, latency={send_time:.3f}s"
                            )

                        _last_sent_state = state
                        _retry_state = None
                        _retry_after = 0.0

                except Exception as e:
                    send_time = time.perf_counter() - send_start
                    _retry_state = state
                    _retry_after = time.monotonic() + _RETRY_DELAY

                    logger.error(
                        f"Worker command failed: mode={mode}, "
                        f"value={value}, latency={send_time:.3f}s, error={e}; "
                        f"retrying in {_RETRY_DELAY:.1f}s"
                    )

        time.sleep(OUTPUT_INTERVAL)


def _watchdog():
    '''Periodically check whether the bulb is reachable.'''

    consecutive_failures = 0

    while _watchdog_running:
        time.sleep(_WATCHDOG_INTERVAL)

        if not _watchdog_running:
            break

        if _recovering:
            consecutive_failures = 0
            continue

        # Health checks use a separate connection, so they do not contend
        # with commands sent over the worker's persistent socket.
        healthy = check_connection()

        if healthy:
            consecutive_failures = 0
            continue

        consecutive_failures += 1
        logger.warning(
            f"Watchdog failure "
            f"({consecutive_failures}/{_WATCHDOG_FAILURE_LIMIT})"
        )

        # Confirm the failure before declaring the connection unhealthy.
        if consecutive_failures < _WATCHDOG_FAILURE_LIMIT:
            time.sleep(_WATCHDOG_CONFIRM_DELAY)
            continue

        logger.error("Watchdog failure confirmed; requesting recovery")

        _recovery_event.set()

        # Reset the counter.
        # Recovery thread is now responsible for repairing the connection.
        consecutive_failures = 0


def _send_state(state):
    '''Send a complete bulb state.'''
    mode, value = state

    if mode == "color":
        set_color(*value)

    elif mode == "white":
        set_white(value)


def _recovery_worker():
    '''Handle connection recovery requests.'''

    global _recovering, _last_sent_state

    while _recovery_running:

        if not _recovery_event.wait(timeout=0.5):
            continue

        if not _recovery_running:
            break

        logger.warning("Recovery requested")
        _recovery_event.clear()

        _recovering = True
        logger.info("Recovery: output paused")

        recovery_start = time.perf_counter()

        try:

            logger.info("Recovery: creating fresh connection")

            with _bulb_io_lock:
                reconnect()

                logger.info("Recovery: fresh connection ready")

                with _lock:
                    latest_state = _latest_state

                logger.debug(f"Recovery: latest state = {latest_state}")

                if latest_state is not None:
                    logger.info("Recovery: restoring latest state")

                    _send_state(latest_state)

                    _last_sent_state = latest_state

                    logger.info("Recovery: latest state restored")

        except Exception as e:
            recovery_time = time.perf_counter() - recovery_start

            logger.error(
                f"Recovery failed after {recovery_time:.3f}s: {e}"
            )

        finally:
            recovery_time = time.perf_counter() - recovery_start

            logger.info(
                f"Recovery finished in {recovery_time:.3f}s"
            )

            _recovering = False
            logger.info("Recovery: output resumed")
