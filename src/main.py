from config.config import config
from src.screen import capture_screen, get_average_color
from src.colors import bgr_to_hsv, has_significant_change, is_white, is_black
from src.bulb import set_color, set_power, set_white
from src.smoothing import smooth_hsv
import time

print("Starting Swift Immerse...")

power_response = set_power(True)
print("Power response:", power_response)

target_hsv = None
output_hsv = None
fps = config["capture"]["fps"]
frame_interval = 1.0 / fps

print(f"Capturing screen at {fps} FPS, frame interval: {frame_interval} seconds")
print("Press Ctrl+C to stop the program.")

try:
    while True:
        frame = capture_screen()

        average_color = get_average_color(frame)

        h, s, v = bgr_to_hsv(average_color)

        current_hsv = (h, s, v)

        if target_hsv is None:
            target_hsv = current_hsv
            output_hsv = current_hsv

        if has_significant_change(current_hsv, target_hsv):
            target_hsv = current_hsv

        output_hsv = smooth_hsv(output_hsv, target_hsv)
        h, s, v = output_hsv

        if is_white(output_hsv):
            set_white(v)  # Set brightness
        elif is_black(output_hsv):
            set_color(0, 0, 0)  # Set to black
        else:
            set_color(h, s, v)
        
        time.sleep(frame_interval)

except KeyboardInterrupt:                 #press Ctrl+C to stop the program
    print("\nStopping Swift Immerse...")

    print("Turning off bulb...")
    response = set_power(False)

    if response["success"]:
        print("Bulb turned off.")
    else:
        print("Failed to turn off bulb.")