from libraries import *

class Identify():
    '''
    Class which can handle testing the unknown dynamics of the
    turtlebot. When initialized, publishes a step output and 
    records the results. This is repeated for linear
    velocity as well as angular velocity.
    '''
    def __init__(self):
        self.type = 0                     # 0: linear step, 1: angular step
        self.counter = 0                  # Used to count up to when the step begins
        self.linear_step = 0              # Should saturate at 0.26
        self.angular_step = 0             # Should saturate at 1.82
        self.linear_vel_data = []         # Stores data
        self.linear_step_data = []
        self.angular_step_data = []
        self.angular_vel_data = []
        self.time_data = []

        # Publisher and subscriber initializations (match namespace!)
        self.robot_vel_sub = rospy.Subscriber('/odom', Odometry, \
                                                self.step, queue_size=1)
        self.speed_pub      = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    
    def step(self, msg):
        '''
        Callback function that creates a step, and samples the information
        available of the system.
        '''

        # Setup step at reasonable time
        self.counter += 1
        if self.counter > 50:
            self.linear_step = 0.5
            self.angular_step = 3
        
        # Store data values
        t = time.time()
        self.time_data.append(t)
        if self.type == 0:
            self.linear_vel_data.append(msg.twist.twist.linear.x)
            self.linear_step_data.append(self.linear_step)
        else:
            self.angular_vel_data.append(msg.twist.twist.linear.x)
            self.angular_step_data.append(self.angular_step)

        # Publish speed message (either zero or step value)
        twist = Twist()
        if self.type == 0:
            twist.linear.x = self.linear_step; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        else:
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = self.angular_step
        
        self.publish_speed(twist)

        # At a reasonable time, write data to file and shutdown node
        if self.counter == 100:
            results = open("results.txt", "w")
            for i in range(len(self.time_data)):
                '''
                results.write(str(self.time_data[i]) + ';' + str(self.linear_step_data[i]) + ';' \
                              + str(self.linear_vel_data[i]) + ';' + str(self.angular_step_data[i])\
                              + ';' + str(self.angular_vel_data[i]) + "\n")
                '''
                results.write(str(self.linear_step_data[i]))
                
            results.close()
            rospy.signal_shutdown('done')
