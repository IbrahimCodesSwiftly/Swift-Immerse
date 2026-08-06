from config.config import config

LERP_FACTOR = config["smoothing"]["factor"]  # Smoothing factor for linear interpolation

def smooth_hsv(current_hsv, target_hsv):
    """Smoothly transitions from the current HSV values to the target HSV values using a smoothing factor."""
    current_h, current_s, current_v = current_hsv
    target_h, target_s, target_v = target_hsv

    smoothed_h = current_h + (target_h - current_h) * LERP_FACTOR
    smoothed_s = current_s + (target_s - current_s) * LERP_FACTOR
    smoothed_v = current_v + (target_v - current_v) * LERP_FACTOR

    return int(smoothed_h), int(smoothed_s), int(smoothed_v)