from screen import capture_screen, get_average_color
from colors import bgr_to_hsv
from bulb import set_color, set_power
import time

print("Starting Swift Immerse...")

power_response = set_power(True)
print("Power response:", power_response)

try:
    while True:
        frame = capture_screen()

        average_color = get_average_color(frame)

        h, s, v = bgr_to_hsv(average_color)

        set_color(h, s, v)

        time.sleep(0.05)

except KeyboardInterrupt:                 #press Ctrl+C to stop the program
    print("\nStopping Swift Immerse...")

    print("Turning off bulb...")
    response = set_power(False)

    if response["success"]:
        print("Bulb turned off.")
    else:
        print("Failed to turn off bulb.")