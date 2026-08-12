from src.colors import bgr_to_hsv, has_significant_color_change, is_white, is_black
from src.bulb import set_color, set_power, set_white
from src.smoothing import smooth_color
from src.bulb.worker import start as start_worker
from src.bulb.worker import stop as stop_worker
from src.bulb.worker import set_state
import time

target_color = None
output_color = None
current_mode = None

def start():
    '''Start the Swift Immerse program.'''

    global target_color, output_color, current_mode

    target_color = None
    output_color = None
    current_mode = None

    print("Starting Swift Immerse...")
    power_success = set_power(True)
    print("Power success:", power_success)

    start_worker()

def process_frame(average_color):
    '''Process a single frame of the screen capture.'''

    global target_color, output_color, current_mode

    current_color = bgr_to_hsv(average_color)

    if target_color is None:
        target_color = current_color
        output_color = current_color

    if has_significant_color_change(current_color, target_color):
        target_color = current_color

    output_color = smooth_color(output_color, target_color)
    h, s, v = output_color

    if is_white(current_color):
        if current_mode != "white":
            set_state("white", v)  # Set brightness
            
            current_mode = "white"

    elif is_black(current_color):
            if current_mode != "black":
                set_state("color", (0, 0, 0))  # Set to black

                current_mode = "black"

    else:
        if current_mode != "color":
            set_state("color", (h, s, v))
            
            current_mode = "color"
        else:
            set_state("color", (h, s, v))

def stop():
    '''Stop the Swift Immerse program.'''
    print("\nStopping Swift Immerse...")

    stop_worker()

    print("Turning off bulb...")
    power_success = set_power(False)

    if power_success:
        print("Bulb turned off.")
    else:
        print("Failed to turn off bulb.")