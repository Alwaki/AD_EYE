#!/usr/bin/env python
import rospy
import tf2_ros
import tf2_msgs.msg
import geometry_msgs.msg

from object_detection.msg import objectpixels

"""
This script creates a tag frame corresponding
to the detected object.
"""
#Subscribes to:
#/Relative_coordinates_info
#Publish:
#Tag frame cooresponding to the detected object.
 
def retrieve_objectcoordinates_relative_to_lidar_cb(relative_coordinates):

    x = relative_coordinates.object_x
    y = relative_coordinates.object_y  
   
    tfb = FixedTFBroadcaster(x,y)

class FixedTFBroadcaster:

    def __init__(self,x,y):
        self.pub_tf = rospy.Publisher("/tf", tf2_msgs.msg.TFMessage, queue_size=10)
 
        t = geometry_msgs.msg.TransformStamped()
        t.header.frame_id = header_id
        t.header.stamp = rospy.Time.now()
        t.child_frame_id = detection_tag
        t.transform.translation.x = x
        t.transform.translation.y = y
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1

        tfm = tf2_msgs.msg.TFMessage([t])
        self.pub_tf.publish(tfm)

if __name__ == '__main__':
    rospy.init_node('fixed_tf2_broadcaster')
    #Retrieve parameters provided by the launch file
    detection_tag = rospy.get_param("~detection_tag_transform")
    header_id = rospy.get_param("~header")
   
    pub = rospy.Subscriber('/Relative_coordinates_info', objectpixels , retrieve_objectcoordinates_relative_to_lidar_cb)
    rospy.spin()

