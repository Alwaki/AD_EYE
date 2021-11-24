'''
Class which calculates the time between callbacks i.e the sampling time which will be used by the
PI controllers.
'''

from libraries import *

class Samplingtime:
    def __init__(self):
        self.previous_callback_time = 0     #Inititate parameter used to store previous callback time
        self.not_first_callback = False     #Boolean logic used to determine if the first callback has happened or not
        self.dt = 0                         #Initiate sampling time i.e time between callbacks

    def sampling_time(self):

        #Get current time
        current_time = rospy.get_time()
        #Calculate callback time since last callback i.e the samplingtime dt
        if self.not_first_callback:
            self.dt = rospy.get_time() - self.previous_callback_time
        self.not_first_callback = True
        self.previous_callback_time = current_time
