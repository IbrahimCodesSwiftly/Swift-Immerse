from mss import mss
import numpy as np
import cv2

with mss() as sct:
    monitor = sct.monitors[1]  # Primary monitor

    while True:
        screenshot = sct.grab(monitor)

        frame = np.array(screenshot)

        # Convert BGRA to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        average_color = frame.mean(axis=(0, 1))
        print(int(average_color[0]), int(average_color[1]), int(average_color[2]))

        cv2.imshow("Swift Immerse - Screen Capture", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()