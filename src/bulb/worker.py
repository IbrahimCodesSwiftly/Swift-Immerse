import threading
import time

from src.bulb import set_color, set_white


OUTPUT_FPS = 10
OUTPUT_INTERVAL = 1 / OUTPUT_FPS

_latest_state = None
_last_sent_state = None

_lock = threading.Lock()

_running = False
_thread = None


def start():
    """Start the bulb output worker."""
    global _running, _thread, _latest_state, _last_sent_state

    if _running:
        return

    _latest_state = None
    _last_sent_state = None

    _running = True

    _thread = threading.Thread(
        target=_run,
        daemon=True
    )

    _thread.start()


def stop():
    """Stop the bulb output worker."""
    global _running, _thread

    _running = False

    if _thread is not None:
        _thread.join()

    _thread = None


def set_state(mode, value):
    """Replace the current desired bulb state."""
    global _latest_state

    with _lock:
        _latest_state = (mode, value)


def _run():
    """Send the latest desired state at a controlled rate."""
    global _last_sent_state

    while _running:

        with _lock:
            state = _latest_state

        # Nothing to send.
        if state is None:
            time.sleep(OUTPUT_INTERVAL)
            continue

        # Doesn't send the exact same state repeatedly.
        if state == _last_sent_state:
            time.sleep(OUTPUT_INTERVAL)
            continue

        mode, value = state

        print(f"WORKER sending: {mode} {value}")

        if mode == "color":
            set_color(*value)

        elif mode == "white":
            set_white(value)

        _last_sent_state = state

        time.sleep(OUTPUT_INTERVAL)