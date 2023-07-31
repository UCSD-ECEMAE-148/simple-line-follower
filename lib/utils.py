import json

class JSONManager():
    def __init__(self):
        f = open('settings.json')
        self.settings = json.load(f)
        f.close

        # Set global parameters
        self.calibration_mode = self.settings['calibration_mode']

        # Set Color detection paramenters
        self.lower_hue = self.settings['color_detection']['lower_hue']
        self.lower_sat = self.settings['color_detection']['lower_sat']
        self.lower_val = self.settings['color_detection']['lower_val']
        self.upper_hue = self.settings['color_detection']['upper_hue']
        self.upper_sat = self.settings['color_detection']['upper_sat']
        self.upper_val = self.settings['color_detection']['upper_val']
        self.invert_mask = self.settings['color_detection']['invert_mask']

        # Set steering and throttle
        self.steering_multiplier = self.settings['vesc_settings']['steering_multiplier']
        self.throttle_multiplier = self.settings['vesc_settings']['throttle_multiplier']
        self.port = self.settings['vesc_settings']['port']
        self.run_motor = self.settings['vesc_settings']['run_motor']

        # Region of interest
        self.left_crop = self.settings['roi']['left_crop']
        self.right_crop = self.settings['roi']['right_crop']
        self.top_crop = self.settings['roi']['top_crop']
        self.bottom_crop = self.settings['roi']['bottom_crop']

    def save_settings(self):
        if self.calibration_mode:
            # Save color detection parameters
            self.settings['color_detection']['lower_hue'] = self.lower_hue
            self.settings['color_detection']['lower_sat'] = self.lower_sat
            self.settings['color_detection']['lower_val'] = self.lower_val
            self.settings['color_detection']['upper_hue'] = self.upper_hue
            self.settings['color_detection']['upper_sat'] = self.upper_sat
            self.settings['color_detection']['upper_val'] = self.upper_val
            self.settings['color_detection']['invert_mask'] = self.invert_mask

            # Save steering and throttle
            self.settings['vesc_settings']['steering_multiplier'] = self.steering_multiplier
            self.settings['vesc_settings']['throttle_multiplier'] = self.throttle_multiplier
            self.settings['vesc_settings']['port'] = self.port
            self.settings['vesc_settings']['run_motor'] = self.run_motor

            # Save region of interest
            self.settings['roi']['left_crop'] = self.left_crop
            self.settings['roi']['right_crop'] = self.right_crop
            self.settings['roi']['top_crop'] = self.top_crop
            self.settings['roi']['bottom_crop'] = self.bottom_crop

            f = open('settings.json','w')
            f.write(json.dumps(self.settings, indent=4))
            f.close()