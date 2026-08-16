import cv2
import numpy as np
import mss

sct = mss.mss()
monitor = sct.monitors[1]


def capture_screen():
    '''Capture the screen and return the frame.'''

    screenshot = sct.grab(monitor)

    frame = np.asarray(screenshot)

    # BGRA to BGR
    frame = frame[:, :, :3]

    frame = cv2.resize(
        frame,
        (640, 360),
        interpolation=cv2.INTER_AREA
    )

    return frame


def get_average_color(frame):
    '''Get the average color of the frame.'''

    average_color = frame.mean(axis=(0, 1)).astype(int)

    return average_color