from screen import capture_screen, get_average_color

while True:
    frame = capture_screen()

    average_color = get_average_color(frame)

    print(average_color)

    if input("Press Enter to capture again (or type q to quit): ").lower() == "q":
        break