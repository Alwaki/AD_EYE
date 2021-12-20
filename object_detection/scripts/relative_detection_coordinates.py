#! /usr/bin/env python
import math
import rospy
#import tf
#import tf2_ros

from sensor_msgs.msg import LaserScan
#from darknet_ros_msgs.msg import BoundingBox 
from darknet_ros_msgs.msg import BoundingBoxes
from object_detection.msg import objectpixels
from std_msgs.msg import String

#Change name of the script to relative_detection_coordinates
#Previously object_location_test

"""
The RelativeCoordinates class retrieves bounding box information from the darknet ros package.
Calculates the midpont of the bounding box, transforms it into a angle relative
to the midpoint of the Lidar which is then used to get the corresponding range value 
provided by the LaserScan message.

The relative coordinates of the detected object to the Lidar frame is then 
calculated and published.
"""
#Subscribes to:
#/darknet_ros/bounding_boxes
#/scan

#Publish to:
#/Relative_coordinates_info

class RelativeCoordinates:
    def __init__(self):
        self.lidar_angle = None
        self.ranges = []
        self.ObjectClass = None
        
    def Detection_rel_to_lidar_cb(self, BoundingBoxInfo): 
        
        #Sets an angle scale based on the width in pixels and the viewing angle
        #of the raspicam.
        anglescale = 320/31.1
        
        try:
            objectType = str(BoundingBoxInfo.bounding_boxes[0].Class)

            if objectType in ['car','truck']: 
              
                self.ObjectClass = str(BoundingBoxInfo.bounding_boxes[0].Class)
                x_max = BoundingBoxInfo.bounding_boxes[0].xmax
                x_min = BoundingBoxInfo.bounding_boxes[0].xmin

                #Calculate the midpoint of the detected boundary box.
                x_midpoint = (x_max + x_min)/2 

                #Transforms the midpoint of the boundary box to degrees, relative to the midpoint of the Lidar.
                self.x_angle = (x_midpoint/anglescale)-31.1
                self.x_angle = round(self.x_angle)
                
                #Attempt to only retrieve information from bounding boxes which are fully inside 
                #the vieving angle of the camera, this is to get more accurate coordinates of the 
                #detected coordinates
                if (x_min + 50) <= x_midpoint <= (x_max - 50):

                    if self.x_angle <0:
                        self.lidar_angle = int(-self.x_angle)
                    else:
                        self.lidar_angle = int(359-self.x_angle)

                    self.calculate_relative_coordinates() 

                else:
                    return 
            else:
                return

        except (IndexError):
            return

    def laserdata_cb(self, LidarData): 
        """
        Retrieves ranges provided by the Lidar.
        """

        self.ranges = LidarData.ranges 
        

    def calculate_relative_coordinates(self):
        

        objectDistance = self.ranges[self.lidar_angle]
 
        x_coord = math.cos(math.radians(self.lidar_angle))*objectDistance
        y_coord = math.sin(math.radians(self.lidar_angle))*objectDistance

        object_coord_info = objectpixels()
        object_coord_info.object_x = x_coord 
        object_coord_info.object_y = y_coord
        object_coord_info.mid_bb_angle = self.x_angle
        object_coord_info.objecttag = self.ObjectClass

        try:
            pub.publish(object_coord_info) 

        except rospy.ROSInterruptException:
            pass

if __name__ == '__main__':

    rospy.init_node('relative_detection_coordinates',anonymous = False)
    lidar = RelativeCoordinates()
    sub1 = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes , lidar.Detection_rel_to_lidar_cb)
    sub2 = rospy.Subscriber('/scan', LaserScan , lidar.laserdata_cb)
    pub = rospy.Publisher('/Relative_coordinates_info', objectpixels, queue_size=10)
    rospy.spin()
