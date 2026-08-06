import cv2
import numpy as np

H_THRESHOLD = 3      # out of 360
S_THRESHOLD = 30     # out of 1000
V_THRESHOLD = 30     # out of 1000
WHITE_SATURATION_THRESHOLD = 40     # out of 1000
WHITE_VALUE_THRESHOLD = 500         # out of 1000(temperature)
BLACK_VALUE_THRESHOLD = 30         # out of 1000


def bgr_to_hsv(bgr):
    '''Convert a BGR color to HSV format.'''
    bgr=np.uint8([[bgr]])

    # Convert BGR to HSV
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)[0][0]

    h, s, v = map(int, hsv)
    h = int(h * 2)  # Scale hue to 0-360
    s = int(s * 1000 / 255)  # Scale saturation to 0-1000
    v = int(v * 1000 / 255)  # Scale value to 0-1000

    return h, s, v

def has_significant_change(current_hsv, last_hsv):  
    '''Returns True if the HSV difference exceeds the thresholds, otherwise returns False'''
    h_diff = abs(current_hsv[0] - last_hsv[0])
    s_diff = abs(current_hsv[1] - last_hsv[1])
    v_diff = abs(current_hsv[2] - last_hsv[2])

    return h_diff >= H_THRESHOLD or s_diff >= S_THRESHOLD or v_diff >= V_THRESHOLD

def is_white(hsv):
    '''Returns True if the HSV value should use the bulb's white light mode, otherwise returns False'''
    _, s, v = hsv
    return s <= WHITE_SATURATION_THRESHOLD and v >= WHITE_VALUE_THRESHOLD

def is_black(hsv):
    '''Returns True if the HSV value should use the bulb's black light mode, otherwise returns False'''
    _, _, v = hsv
    return v <= BLACK_VALUE_THRESHOLD