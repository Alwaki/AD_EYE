#!/usr/bin/env python

from __future__ import print_function

from beginner_tutorials.srv import AddTwoInts,AddTwoIntsResponse
import rospy
from std_msgs.msg import String

import socket 

UDP_IP = "127.0.0.1"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

def gnuradio_server():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('gnuradio_server')
    rate = rospy.Rate(10) # 10hz

    print("the socket is intialized...")
    while not rospy.is_shutdown():
        data, addr = sock.recvfrom(1024)
        data = data[24:]
        rospy.loginfo(data)
        pub.publish(data)
        data_len = len(data)
        print("Received data: %s", data)
        print("data_len: %d", data_len)
        rate.sleep()

if __name__ == "__main__":
    
    gnuradio_server()