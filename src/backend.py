from src.colors import bgr_to_hsv, has_significant_color_change, is_white, is_black
from src.bulb import set_color, set_power, set_white
from src.smoothing import smooth_color

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
            set_white(v)  # Set brightness
            current_mode = "white"

    elif is_black(current_color):
            set_color(0, 0, 0)  # Set to black
            current_mode = "color"

    else:
        set_color(h, s, v)
        current_mode = "color"

def stop():
    '''Stop the Swift Immerse program.'''
    print("\nStopping Swift Immerse...")

    print("Turning off bulb...")
    power_success = set_power(False)

    if power_success:
        print("Bulb turned off.")
    else:
        print("Failed to turn off bulb.")