import cv2
import numpy as np

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = DepthFilter(camera)

# 1D array gausian kernel
array = np.linspace(0, 2.5, 320)
array = np.concatenate((array, -np.flip(array)), axis=0)

while True:
    depth = camera.get_depth()

    depth_norm = depth/255 # Normalize depth to 0-1
    depth_exp = 1 - np.exp(-5*depth_norm) # Apply exponential function

    steer = depth_exp @ array
    steer = steer[:320]
    steer = np.sum(steer)/(640*500)

    # clamp between -1 to 1
    steer = np.clip(steer, -1, 1)

    # print(steer)
    # map to from -1 to 1 to 0 to 1
    steer = (steer + 1)/2

    vehicle.run(steer, -0.03)