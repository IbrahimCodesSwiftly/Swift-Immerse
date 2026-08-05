from src.screen import capture_screen
import cv2

while True:
    frame = capture_screen()

    cv2.imshow("Screen Capture", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()