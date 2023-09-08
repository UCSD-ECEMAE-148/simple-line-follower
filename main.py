import cv2

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
# from lib.actuator import VESC
       
camera = OAKDCamera()
# vehicle = VESC()
detector = DepthFilter(camera)

while True:
    steering, throttle = detector.get_actuator_values()
    # print steering to 3 decimal places
    print(f'Steering: {steering:.3f}, Throttle: {throttle:.3f}')
    # vehicle.run(steering, throttle)

    # Wait for q keypress or KeyboardInterrupt event to occur
    if cv2.waitKey(1) & 0xFF == ord('q'):
        detector.save_settings() # Choose to save settings if in calibration mode
        if detector.calibration_mode:
            cv2.destroyAllWindows()
        break