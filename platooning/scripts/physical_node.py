#!/usr/bin/env python2

from RobotClass import *

if __name__ == '__main__':
    """Initiate node for turtlebot 1"""
    rospy.init_node('control_node', anonymous = False)

    """Instanciate the robot class"""
    turtlebot = Robot()

    """Waken callback when there is a message available, otherwise sleep"""
    rospy.spin()
