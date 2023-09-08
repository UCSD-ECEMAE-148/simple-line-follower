import cv2
import numpy as np

class DepthFilter():
    def __init__(self, camera) -> None:
        self.camera = camera

        # Custom filter
        array = cv2.getGaussianKernel(640, 0)

        # Negate the second half of the array
        self.array = np.concatenate((array[:320], -array[320:]), axis=0)

    def get_actuator_values(self):
        depth = self.camera.get_depth()
        steer = depth @ self.array
        steer = np.sum(steer/(640*10))
        
        return steer, 0.0