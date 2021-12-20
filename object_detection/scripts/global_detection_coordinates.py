#! /usr/bin/env python
import rospy
import tf
import tf2_ros
#from std_msgs.msg import String
from object_detection.msg import objectcoord
from object_detection.msg import objectpixels
from std_msgs.msg import String


"""
This script performs a transform from the global map frame
to the detection_tag_frame in order to get the coordinates
of the detected object in the global coordinatesystem
"""
#Subscribes to:
#tb3_id/Relative_coordinates_info

#Publish to:
#tb3_id/Global_coordinates_info

def global_coordinates_cb(Relative_coord_info):

    #Retrieve the detected objects class
    objecttag = Relative_coord_info.objecttag

    try:
        #Waiting to let the frames initialize
        list.waitForTransform(robot_odom, detection_tag,rospy.Time(), rospy.Duration(1))

        #Perform a transformation between map frame and detection frame to retrieve the coordinates
        #of the detection in the global coordinatesystem 
        (trans,rot) = list.lookupTransform( '/map', detection_tag , rospy.Time(0)) 

        x = trans[0]
        y = trans[1]

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, IndexError):
        return

    global_coordinate_info = objectcoord()
    global_coordinate_info.x_coord = x
    global_coordinate_info.y_coord = y
    global_coordinate_info.objecttag = objecttag

    try:   
        pub.publish(global_coordinate_info)  
    except rospy.ROSInterruptException:
        pass



if __name__ == '__main__':

    rospy.init_node('global_detection_coordinates',anonymous = True)
    list = tf.TransformListener()

    #Retrieve parameters from launch file
    detection_tag = rospy.get_param("~detect_tag")
    robot_odom = rospy.get_param("~robot_odom")

    sub = rospy.Subscriber('/Relative_coordinates_info', objectpixels , global_coordinates_cb)
    pub = rospy.Publisher('/Global_coordinates_info', objectcoord, queue_size=10)  
    rospy.spin()
