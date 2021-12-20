#!/usr/bin/env python2

'''
Code for creating the node and handing control to ROS network.
'''

from RobotClass import *

if __name__ == '__main__':
    """ Initiate node for turtlebot """
    rospy.init_node('control_node', anonymous = False)

    """ Set the scheduled rate (10 Hz) """
    rate = rospy.Rate(100) 

    """ Instanciate the robot class """
    turtlebot = Robot()

    """ Sleep at a scheduled rate, handling callbacks """
    while not rospy.is_shutdown():
        turtlebot.scheduled_follower_logic()
        rate.sleep()
