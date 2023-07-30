import pyvesc
from lib.utils import JSONManager

class VESC(JSONManager):
    def __init__(self):
        super().__init__()
        self.vesc = pyvesc.VESC(self.port)

    def run(self, steering, throttle:0.0):
        self.vesc.set_servo(steering * self.steering_multiplier)
        self.vesc.set_rpm(throttle * self.throttle_multiplier)


if __name__ == '__main__':
    v = VESC()