from libraries import *

class PID:
    '''
    Class which is inherited, provides PID controller methods and
    stores control parameters.
    '''

    def __init__(self):
        self.Kp_v = 2                     # Proportional controller gain longitudinal controller
        self.Ki_v = 0.8                     # Integral controller gain longitudinal controller
        self.Kp_w = 1.5   #1                  # Proportional controller gain lateral controller
        self.Ki_w = 0.8                   #Integral controller gain longitudinal controller

        self.max_limit_v = 0.26             # Maximum saturation limit velocity
        self.min_limit_v = 0                # Minimum saturation limit velocity
        self.max_limit_w = 1.82             # Maxamium saturation limit yaw angle
        self.min_limit_w = -1.82            # Minimum saturation limit yaw angle

        self.Iterm_v = 0                         #Inititate the integral part of the longitudinal PI controller
        self.Iterm_w = 0                         #Inititate the integral part of the lateral PI controller

        self.dt = 0                         #Initiate sampling time i.e time between callbacks
        self.previous_callback_time = 0     #Inititate parameter used to store previous callback time
        
    def longitudinal_PI_control(self, error):

        #Integral part of the controller
        #self.Iterm_v += self.Ki_v * error * self.dt
        #Control output
        longitudinal_control_output = self.Kp_v * error #+ self.Iterm_v

        #Saturation and anti-windup for the longitudinal controller
        if longitudinal_control_output > self.max_limit_v:

            #self.Iterm_v -= longitudinal_control_output - self.max_limit_v
            longitudinal_control_output = self.max_limit_v

        elif longitudinal_control_output < self.min_limit_v:

            #self.Iterm_v += self.min_limit_v - longitudinal_control_output
            longitudinal_control_output = self.min_limit_v
        #print(longitudinal_control_output,'v')
        return longitudinal_control_output

    def lateral_PI_control(self, error):

        #Integral part of the controller
        #self.Iterm_w += self.Ki_w * error * self.dt
        #Control output
        lateral_control_output = self.Kp_v * error #+ self.Iterm_w

        #Saturation and anti-windup for the longitudinal controller
        if lateral_control_output > self.max_limit_w:

            #self.Iterm_w -= lateral_control_output - self.max_limit_w
            lateral_control_output = self.max_limit_w

        elif lateral_control_output <  self.min_limit_w:

            #self.Iterm_w += self.min_limit_w - lateral_control_output
            lateral_control_output = self.min_limit_w
        #print(lateral_control_output,'w')
        return lateral_control_output

        #If we want to add D part to the controller:
        #previous_error = error
        # Kd * (error - previous_error)/self.dt
    
    def sample_time(self):
        #Get current time
        current_time = rospy.get_time()
        #Calculate callback time since last callback i.e the samplingtime dt
        if self.not_first_callback:
            self.dt = rospy.get_time() - self.previous_callback_time
        self.not_first_callback = True
        self.previous_callback_time = current_time

