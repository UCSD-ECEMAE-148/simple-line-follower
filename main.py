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
    depth_exp = 1 - np.exp(-5*depth_norm) # Apply exponential function, 0-1

    depth_thresh = 0.25
    depth_exp[depth_exp < depth_thresh] = 0 # Threshold depth

    # Get histogram in the horizontal direction
    hist = np.sum(depth_exp, axis=0)

    # Smooth the histogram
    hist = np.convolve(hist, np.ones(50)/200, mode='same')

    # Crop the left and right edges
    hist[:50] = 200
    hist[-50:] = 200

    # Find the lastest minimum continous value
    steer = np.argmin(hist)/640

    vehicle.run(steer, -0.03)