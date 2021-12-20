#!/usr/bin/env python2

'''
Code for creating the node and handing control to ROS network.
'''

from IdentifyClass import *

if __name__ == '__main__':
    """ Initiate node for turtlebot """
    rospy.init_node('identifier_node', anonymous = False)

    """ Set the scheduled rate (10 Hz) """
    rate = rospy.Rate(10) 

    """ Instanciate the identifier class """
    id = Identify()

    """ Sleep at a scheduled rate, hand over node control to ROS """
    while not rospy.is_shutdown():
        rate.sleep()
