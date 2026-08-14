from config.config import config
from src.screen import capture_screen, get_average_color
from src.backend import start, process_frame, stop
from src.instance_lock import SingleInstance
import time


instance = SingleInstance()

if not instance.acquire():
    print("Swift Immerse is already running.")
    raise SystemExit(1)

# existing Swift Immerse startup...


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
    try:
        stop()
    finally:
        instance.release()