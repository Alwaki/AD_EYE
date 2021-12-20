#!/usr/bin/env python2

import rospy
#Import needed messages to use markers in RVIZ
import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseWithCovarianceStamped


"""
The markerclass_prescan retrieves the coordinates from the prescan vehicle, and publish them
as an red sphere in rviz to show its contionous trajectory.
"""
#Subscribe to:
#/vehicle/amcl_pose
#pulish to:
#/visualization_prescan

class markerclass_prescan:
    def __init__(self):
        self.x = None
        self.y = None
        self.yaw = 0

    def retrieve_prescan_coordinates(self,prescan):
        """
        Retrieve coordinates of the prescan vehicle.
        """
        self.x = prescan.pose.pose.position.x
        self.y = prescan.pose.pose.position.y
        
        orientation = prescan.pose.pose.orientation
        self.w = orientation.w
        #orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        #(roll, pitch, yaw) = euler_from_quaternion(orientation_list)
       

    def Detection_visualization_rviz_prescan(self):
     
        count = 0
        MARKERS_MAX = 1
        markerArray = MarkerArray()
        while not rospy.is_shutdown():
            marker = Marker()
            marker.header.frame_id = "/map"
            
            if self.x:
                marker.type = marker.SPHERE
                marker.action = marker.ADD
                marker.scale.x = 0.2
                marker.scale.y = 0.2
                marker.scale.z = 0.2
                marker.color.a = 1.0
                marker.color.r = 1.0
                marker.color.g = 0.0
                marker.color.b = 0.0
                marker.pose.orientation.w = self.w
                marker.pose.position.x = self.x
                marker.pose.position.y = self.y
                marker.pose.position.z = 0 
 
            #Add the new marker to the MarkerArray, removing the oldest marker from it when necessary
            if(count > MARKERS_MAX):
                markerArray.markers.pop(0)

            markerArray.markers.append(marker)

            #Renumber the marker IDs
            id = 0
            for m in markerArray.markers:
                m.id = id
                id += 1
 
            #Publish the MarkerArray
            pub.publish(markerArray)

            count += 1
            rospy.sleep(0.01)

if __name__ == '__main__':

    rospy.init_node('Marker_Prescan',anonymous = True)

    markerclass = markerclass_prescan()
    sub1 = rospy.Subscriber('/vehicle/amcl_pose', PoseWithCovarianceStamped, markerclass.retrieve_prescan_coordinates)
    pub = rospy.Publisher('visualization_prescan', MarkerArray, queue_size=10) 
    markerclass.Detection_visualization_rviz_prescan()
    rospy.spin()
