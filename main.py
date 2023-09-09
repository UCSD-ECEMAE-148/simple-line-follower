import cv2
import numpy as np

from lib.camera import OAKDCamera
from lib.depth_fitler import DepthFilter
from lib.actuator import VESC
       
camera = OAKDCamera()
vehicle = VESC()
detector = DepthFilter(camera)

while True:
    depth = camera.get_depth()

    depth_norm = depth/255 # Normalize depth to 0-1
    depth_exp = 1 - np.exp(-5*depth_norm) # Apply exponential function

    # Horizontal histogram of the depth image
    hist = np.sum(depth_exp, axis=0)

    # Low pass filter, kernel size 5
    hist = np.convolve(hist, np.ones(5)/5, mode='same')

    # Left side sum negative and right side sum positive
    new_hist = np.copy(hist)/40000
    new_hist[:320] = new_hist[:320]
    new_hist[320:] = -new_hist[320:]

    # Apply 1D gausian kernel
    steer = np.sum(new_hist)
    steer = np.clip(steer, -1, 1)
    steer = (steer + 1)/2

    vehicle.run(steer, -0.03)