import cv2
import numpy as np
import mss

# Capture the screen and return the frame
def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary monitor

        while True:
            screenshot = sct.grab(monitor)

            frame = np.array(screenshot)

            # Convert BGRA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            return frame

# Get the average color of the frame
def get_average_color(frame):
    average_color = frame.mean(axis=(0, 1)).astype(int)

    return average_color