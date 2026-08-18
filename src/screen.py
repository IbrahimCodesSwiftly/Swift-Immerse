import cv2
import numpy as np
import mss

_sct = mss.mss()
_monitor = _sct.monitors[1]

_CAPTURE_WIDTH = 640
_CAPTURE_HEIGHT = 360


def capture_screen():
    """Capture and downscale the primary screen."""

    screenshot = _sct.grab(_monitor)

    frame = np.asarray(screenshot)

    frame = cv2.resize(
        frame,
        (_CAPTURE_WIDTH, _CAPTURE_HEIGHT),
        interpolation=cv2.INTER_AREA
    )

    # Remove alpha channel.
    frame = frame[:, :, :3]

    return frame


def get_average_color(frame):
    '''Get the average color of the frame.'''

    average_color = frame.mean(axis=(0, 1)).astype(int)

    return average_color