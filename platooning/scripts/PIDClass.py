'''
Class which is inherited, provides PID controller methods and 
stores control parameters.
'''

from libraries import *

class PID:

    def __init__(self):
        self.Kp_v = 2                       # Controller gain longitudianl controller
        self.Kp_w = 1.5                     # Controller gain lateral controller
        self.limit_v = 0.26                 # Saturation limit velocity
        self.limit_w = 1.82                 # Saturation limit yaw angle

    def longitudinal_PI_control(self, error):
        pass

    def lateral_PI_control(self, error):
        pass