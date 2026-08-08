from config.config import config
import cv2
import numpy as np

# #RGB Thresholds
# R_THRESHOLD = config["rgb"]["r_threshold"]     # out of 255
# G_THRESHOLD = config["rgb"]["g_threshold"]      # out of 255
# B_THRESHOLD = config["rgb"]["b_threshold"]      # out of 255

#HSV Thresholds
H_THRESHOLD = config["hsv"]["h_threshold"]      # out of 360
S_THRESHOLD = config["hsv"]["s_threshold"]     # out of 1000
V_THRESHOLD = config["hsv"]["v_threshold"]     # out of 1000

#WHITE/BLACK Detection Thresholds
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


# def bgr_to_rgb(bgr):
#     '''Convert a BGR color to RGB format.'''
#     b, g, r = map(int, bgr)
#     return r, g, b


# def has_significant_rgb_change(current_rgb, target_rgb):
#     '''Returns True if the RGB difference exceeds the thresholds, otherwise returns False'''
#     r1, g1, b1 = current_rgb
#     r2, g2, b2 = target_rgb
#     r_diff = abs(r1 - r2)
#     g_diff = abs(g1 - g2)
#     b_diff = abs(b1 - b2)

#     return r_diff >= R_THRESHOLD or g_diff >= G_THRESHOLD or b_diff >= B_THRESHOLD


def has_significant_color_change(current_color, target_color):  
    '''Returns True if the color difference exceeds the thresholds, otherwise returns False'''
    h_diff = abs(current_color[0] - target_color[0])
    h_diff = min(h_diff, 360 - h_diff)  # Account for hue wrap-around
    s_diff = abs(current_color[1] - target_color[1])
    v_diff = abs(current_color[2] - target_color[2])

    return h_diff >= H_THRESHOLD or s_diff >= S_THRESHOLD or v_diff >= V_THRESHOLD


def is_white(hsv):
    '''Returns True if the HSV value should use the bulb's white light mode, otherwise returns False'''
    _, s, v = hsv
    return s <= WHITE_SATURATION_THRESHOLD and v >= WHITE_VALUE_THRESHOLD

# def is_white_rgb(rgb):
#     '''Returns True if the RGB value should use the bulb's white light mode, otherwise returns False'''
#     r, g, b = rgb
#     return r >= R_THRESHOLD and g >= G_THRESHOLD and b >= B_THRESHOLD

def is_black(hsv):
    '''Returns True if the HSV value should turn the bulb off, otherwise returns False'''
    _, _, v = hsv
    return v <= BLACK_VALUE_THRESHOLD

# def is_black_rgb(rgb):
#     '''Returns True if the RGB value should turn the bulb off, otherwise returns False'''
#     r, g, b = rgb
#     return r <= R_THRESHOLD and g <= G_THRESHOLD and b <= B_THRESHOLD
