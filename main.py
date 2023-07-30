import cv2

from lib.camera import ImageCamera
from lib.hsv_filter import detectLine
       
camera = ImageCamera(path='test_images/test1.jpg')
detector = detectLine(camera)

while True:
    detector.update_image()
    print(detector.steering, detector.throttle)
    # Wait for q keypress or KeyboardInterrupt event to occur
    if cv2.waitKey(1) & 0xFF == ord('q'):
        detector.save_settings() # Choose to save settings if in calibration mode
        if detector.calibration_mode:
            cv2.destroyAllWindows()
        break