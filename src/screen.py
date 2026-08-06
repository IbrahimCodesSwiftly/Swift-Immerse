import cv2
import numpy as np
import mss

def capture_screen():
    '''Capture the screen and return the frame.'''
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor

        while True:
            screenshot = sct.grab(monitor)

            frame = np.array(screenshot)

            # Convert BGRA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            return frame

def get_average_color(frame):
    '''Get the average color of the frame.'''
    average_color = frame.mean(axis=(0, 1)).astype(int)

    return average_color