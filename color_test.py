from screen import capture_screen, get_average_color
from colors import bgr_to_hsv

while True:
    frame = capture_screen()

    average_color = get_average_color(frame)

    h, s, v = bgr_to_hsv(average_color)

    print(f"BGR : {average_color}")
    print(f"H   : {h}")
    print(f"S   : {s}")
    print(f"V   : {v}")
    print()

    if input("Press Enter to capture again (or q to quit): ").lower() == "q":
        break