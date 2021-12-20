#!/usr/bin/env python

from __future__ import print_function
import rospy
from std_msgs.msg import String
from std_srvs.srv import SetBool

import socket 

UDP_IP = "127.0.0.1"
UDP_PORT = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

def gnuradio_server():
    print("the socket is intialized...")
    while(1):
        data, addr = sock.recvfrom(1024)
        data = data[24:]
        rospy.loginfo(data)
        rospy.wait_for_service('/tb3_0/stop')
        try:
            emergency_stop0 = rospy.ServiceProxy('/tb3_0/stop', SetBool)
            if data == "STOP":
                emergency_stop0(0)
            elif data == "STOP SLOW":
                emergency_stop0(1)
            elif data == "START":
                emergency_stop0(0)
            else:
                print("Didn't know what to do")		
        except rospy.ServiceException as e:
            print("Service call failed: %s" %e)

        rospy.wait_for_service('/tb3_1/stop')
        try:
            emergency_stop1 = rospy.ServiceProxy('/tb3_1/stop', SetBool)
            if data == "STOP":
                emergency_stop1(0)
            elif data == "STOP SLOW":
                emergency_stop1(1)
            elif data == "START":
                emergency_stop1(0)
            else:
                print("Didn't know what to do")
        except rospy.ServiceException as e:
            print("Service call failed: %s" %e)

        print("Received data: %s", data)

    #while not rospy.is_shutdown():
        #data, addr = sock.recvfrom(1024)
        #data = data[24:]
        #rospy.loginfo(data)
        #if data == "STOP":

            #emerengcy_stop0(0)
            #emerengcy_stop1(0)
            #print("Received data: %s", data)
            #print("data_len: %d", data_len)
            #break
        #rate.sleep()
        #rospy.spin()

if __name__ == "__main__":
    #rospy.init_node('gnuradio_client',anonymous = True)
    gnuradio_server()
