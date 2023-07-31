import cv2

from lib.camera import OAKDCamera
from lib.hsv_filter import detectLine
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = detectLine(camera)

while True:
    steering, throttle = detector.get_actuator_values()
    print(f'Steering: {steering}, Throttle: {throttle}')
    vehicle.run(steering, throttle)

    # Wait for q keypress or KeyboardInterrupt event to occur
    if cv2.waitKey(1) & 0xFF == ord('q'):
        detector.save_settings() # Choose to save settings if in calibration mode
        if detector.calibration_mode:
            cv2.destroyAllWindows()
        break