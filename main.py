import cv2
import numpy as np

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = DepthFilter(camera)

# 1D array gausian kernel
array = np.linspace(-1, 1, 640//2)
array = np.concatenate((array[:320], -array[320:]), axis=0)

print(array)

# Negate the second half of the array
# array = np.concatenate((array[:320], -array[320:]), axis=0)

while True:
    depth = camera.get_depth()

    steer = depth @ array
    steer = np.sum(steer)/(640*15)

    # clamp between -1 to 1
    steer = np.clip(steer, -1, 1)
    # map to from -1 to 1 to 0 to 1
    steer = (steer + 1)/2

    vehicle.run(steer, 0.02)