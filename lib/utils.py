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

        # Set steering and throttle
        self.steering_multiplier = self.settings['vesc_settings']['steering_multiplier']
        self.throttle_multiplier = self.settings['vesc_settings']['throttle_multiplier']
        self.port = self.settings['vesc_settings']['port']

    def save_settings(self):
        if self.calibration_mode:
            # Save color detection parameters
            self.settings['color_detection']['lower_hue'] = self.lower_hue
            self.settings['color_detection']['lower_sat'] = self.lower_sat
            self.settings['color_detection']['lower_val'] = self.lower_val
            self.settings['color_detection']['upper_hue'] = self.upper_hue
            self.settings['color_detection']['upper_sat'] = self.upper_sat
            self.settings['color_detection']['upper_val'] = self.upper_val

            # Save steering and throttle
            self.settings['vesc_settings']['steering_multiplier'] = self.steering_multiplier
            self.settings['vesc_settings']['throttle_multiplier'] = self.throttle_multiplier
            self.settings['vesc_settings']['port'] = self.port

            f = open('settings.json','w')
            f.write(json.dumps(self.settings, indent=4))
            f.close()