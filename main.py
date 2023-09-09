import cv2
import numpy as np

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = DepthFilter(camera)

# 1D array gausian kernel
array = np.linspace(0.5, 1, 320)
array = np.concatenate((array, -array), axis=0)


# Negate the second half of the array
# array = np.concatenate((array[:320], -array[320:]), axis=0)

while True:
    depth = camera.get_depth()

    steer = depth @ array
    steer = steer[:320]
    steer = np.sum(steer)/(640*100)

    # clamp between -1 to 1
    steer = np.clip(steer, -1, 1)

    # print(steer)
    # map to from -1 to 1 to 0 to 1
    steer = (steer + 1)/2
    # print(steer)
    vehicle.run(steer, -0.03)