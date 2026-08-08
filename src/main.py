from config.config import config
from src.screen import capture_screen, get_average_color
from src.backend import start, process_frame, stop
import time


fps = config["capture"]["fps"]
frame_interval = 1.0 / fps

print(f"Capturing screen at {fps} FPS, frame interval: {frame_interval} seconds")
print("Press Ctrl+C to stop the program.")

try:
    start()

    while True:
        frame = capture_screen()
        average_color = get_average_color(frame)

        process_frame(average_color)

        time.sleep(frame_interval)

except KeyboardInterrupt:
    pass

finally:
    stop()