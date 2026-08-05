from src.screen import capture_screen, get_average_color
from src.colors import bgr_to_hsv
from src.bulb import set_color, set_power
import time

print("Starting Swift Immerse...")

power_response = set_power(True)
print("Power response:", power_response)

last_hsv = None

try:
    while True:
        frame = capture_screen()

        average_color = get_average_color(frame)

        h, s, v = bgr_to_hsv(average_color)

        current_hsv = (h, s, v)

        if current_hsv != last_hsv:      #if the color has changed since the last frame, send a command to the bulb to change its color
            set_color(h, s, v)
            last_hsv = current_hsv       #check if the color has changed since the last frame to avoid sending unnecessary commands

        time.sleep(0.05)

except KeyboardInterrupt:                 #press Ctrl+C to stop the program
    print("\nStopping Swift Immerse...")

    print("Turning off bulb...")
    response = set_power(False)

    if response["success"]:
        print("Bulb turned off.")
    else:
        print("Failed to turn off bulb.")