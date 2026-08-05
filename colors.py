import cv2
import numpy as np

def bgr_to_hsv(bgr):
    bgr=np.uint8([[bgr]])

    # Convert BGR to HSV
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0][0]

    h, s, v = map(int, hsv)
    h = int(h * 2)  # Scale hue to 0-360
    s = int(s * 1000 / 255)  # Scale saturation to 0-1000
    v = int(v * 1000 / 255)  # Scale value to 0-1000

    return h, s, v