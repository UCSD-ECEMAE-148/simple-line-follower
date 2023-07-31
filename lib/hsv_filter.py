from lib.utils import JSONManager
import cv2
import numpy as np

class detectLine(JSONManager):
    # Helper functions
    def update_lower_hue(self, value): self.lower_hue = value
    def update_lower_sat(self, value): self.lower_sat = value
    def update_lower_val(self, value): self.lower_val = value
    def update_upper_hue(self, value): self.upper_hue = value
    def update_upper_sat(self, value): self.upper_sat = value
    def update_upper_val(self, value): self.upper_val = value
    def update_left_crop(self, value): self.left_crop = value/100
    def update_right_crop(self, value): self.right_crop = value/100
    def update_top_crop(self, value): self.top_crop = value/100
    def update_bottom_crop(self, value): self.bottom_crop = value/100
    
    def __init__(self, camera, windowName='Camera'):
        ''' This method is encharged of correctly initiallizing the detect Line objects'''
        print("Starting... Please wait...")

        self.cX, self.cY = 0, 0

        self.windowName = windowName

        # Inherit parent properties
        super().__init__()

        # Initialize the Oak-D camera
        self.camera = camera

        if self.calibration_mode:
            # Create named windows
            cv2.namedWindow(windowName)
            cv2.namedWindow('Mask')

            # Create trackbars
            cv2.createTrackbar('Lower Hue', 'Mask', self.lower_hue, 254, self.update_lower_hue)
            cv2.createTrackbar('Lower Sat', 'Mask', self.lower_sat, 254, self.update_lower_sat)
            cv2.createTrackbar('Lower Val', 'Mask', self.lower_val, 254, self.update_lower_val)
            cv2.createTrackbar('Upper Hue', 'Mask', self.upper_hue, 255, self.update_upper_hue)
            cv2.createTrackbar('Upper Sat', 'Mask', self.upper_sat, 255, self.update_upper_sat)
            cv2.createTrackbar('Upper Val', 'Mask', self.upper_val, 255, self.update_upper_val)

            # Create buttons
            cv2.createTrackbar('Invert', 'Mask', self.invert_mask, 1, lambda x: setattr(self, 'invert_mask', x))
            cv2.createTrackbar('Run Motor', 'Mask', self.run_motor, 1, lambda x: setattr(self, 'run_motor', x))

            # Create trackbars for region of interest
            cv2.createTrackbar('Left Crop', 'Mask', int(self.left_crop*100), 100, self.update_left_crop)
            cv2.createTrackbar('Right Crop', 'Mask', int(self.right_crop*100), 100, self.update_right_crop)
            cv2.createTrackbar('Top Crop', 'Mask', int(self.top_crop*100), 100, self.update_top_crop)
            cv2.createTrackbar('Bottom Crop', 'Mask', int(self.bottom_crop*100), 100, self.update_bottom_crop)

        print("Done initializing...")

    def get_actuator_values(self):
        ''' Update image from video source and fid centroid of mask.'''

        # Capture new image from source
        self.frame = np.copy(self.camera.get_frame())
        mask = self.filter_frame()

        self.moment_search(mask) # Sets self.cX, self.cY

        # Print translate to steering and throttle
        if self.cX is not None and self.cY is not None:
            # Limit the steering angle from 0 to 1
            self.steering = max(min(1-(self.frame.shape[1]-self.cX)/(self.frame.shape[1]),1),0)

            if self.run_motor:
                # Clamp the steering angle from 0 to 1
                if self.steering > 0.5:
                    self.throttle = abs(1.0-self.steering)
                else:
                    self.throttle = abs(self.steering)

                # Clamp the throttle
                self.throttle = max(2*self.max_throttle*self.throttle,self.min_throttle)
            else:
                self.throttle = 0.0

            

        if self.calibration_mode:
            # Show centroid on image
            cv2.circle(self.frame, (self.cX, self.cY), 5, (255, 255, 255), -1)
            cv2.putText(self.frame, "centroid", (self.cX - 25, self.cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Show windows
            cv2.imshow(self.windowName, self.frame)
            cv2.imshow('Mask', mask)

        return self.steering, self.throttle

    def filter_frame(self):
        mask = self.hsv_filter(self.frame)

        if self.invert_mask:
            mask = cv2.bitwise_not(mask)
        
        # Crop the image
        # The crop values are in percentage of the original image, convert to pixels
        left_crop = int(self.left_crop * self.frame.shape[1])
        right_crop = int(self.right_crop * self.frame.shape[1])
        top_crop = int(self.top_crop * self.frame.shape[0])
        bottom_crop = int(self.bottom_crop * self.frame.shape[0])

        # zero out pixels not in the mask
        mask[0:top_crop,:] = 0
        mask[(mask.shape[0]-bottom_crop):mask.shape[0],:] = 0
        mask[:,0:left_crop] = 0
        mask[:,(mask.shape[1]-right_crop):mask.shape[1]] = 0

        return mask

    def moment_search(self, mask):
        '''Calculate the centroid of the mask'''
        # Calculate the moments of the mask
        M = cv2.moments(mask)
        # Calculate x,y coordinate of center
        if M["m00"] != 0:
            self.cX = int(M["m10"] / M["m00"])
            self.cY = int(M["m01"] / M["m00"])     

        return self.cX, self.cY

    def hsv_filter(self, frame):
        ''' This method is encharged of searching for the line in the HSV color space'''
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (self.lower_hue, self.lower_sat, self.lower_val),
                                (self.upper_hue, self.upper_sat, self.upper_val))
    
        return mask
 