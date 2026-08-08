from config.config import config

LERP_FACTOR = config["smoothing"]["factor"]  # Smoothing factor for linear interpolation

def smooth_color(current_color, target_color):
    """Smoothly transition from the current color to the target color."""
    current_h, current_s, current_v = current_color
    target_h, target_s, target_v = target_color

    h_diff = (target_h - current_h + 180) % 360 - 180

    smoothed_h = (current_h + h_diff * LERP_FACTOR) % 360
    smoothed_s = current_s + (target_s - current_s) * LERP_FACTOR
    smoothed_v = current_v + (target_v - current_v) * LERP_FACTOR

    return int(smoothed_h), int(smoothed_s), int(smoothed_v)