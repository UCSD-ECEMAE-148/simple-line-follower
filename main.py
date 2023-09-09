import cv2
import numpy as np

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = DepthFilter(camera)

# 1D array gausian kernel
array = cv2.getGaussianKernel(640, 0)

# Negate the second half of the array
array = np.concatenate((array[:320], -array[320:]), axis=0)

while True:
    depth = camera.get_depth()

    steer = depth @ array
    steer = np.sum(steer)/(640*15)

    vehicle.run(steer, 0.0)