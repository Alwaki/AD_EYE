#!/usr/bin/env python2

import rospy
from std_msgs.msg import String
from object_detection.msg import objectcoord

#Import needed messages to use markers in RVIZ
import roslib; roslib.load_manifest('visualization_marker_tutorials')
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

"""
The markerclass retrieves the coordinates of the detected
object in the global coordinate system. Calculates the mean value
of these coordinates to get a more accurate visualization in RVIZ.
These mean x and y values are then published to RVIZ.

"""
#subscribes to:
#tb3_id/Global_coordinates_info

#Publish to:
#tb3_id/visualization_marker_array

class markerclass:
    def __init__(self):
   
        self.marker_x = None
        self.marker_y = None
        self.count_x = 0
        self.count_y = 0
        self.sum_x = 0
        self.sum_y = 0
        self.previous_average_x = 0
        self.previous_average_y = 0
        self.x = None
        self.y = None
        self.cal_num=0
      
        self.counter = 0
        self.marker_average = []
        self.threshhold = 1

        self.detect_tag = ""
    

    def retrieve_detection_coord_cb(self,global_coordinates):
        """
        Retrieve coordinates of the detection relative to 
        the global coordinate system.
        """
        self.detect_tag = global_coordinates.objecttag
        self.x = global_coordinates.x_coord
        self.y = global_coordinates.y_coord
       
        self.average_coordinates()

    def average_coordinates1(self):
        """
        Calculates the mean x and y coordinates of the detected object
        in the global coordinate system within a certain interval to
        distinguish between different detections.

        """
        self.count_x += 1
        self.count_y += 1

        self.sum_x += self.x
        average_x = self.sum_x / self.count_x
        self.sum_y += self.y
        average_y = self.sum_y / self.count_x

        #Check if the average is within a specified interval othervise
        #reset the sum and counter.
        if self.count_x > 1 and self.cal_num<20:

            if (abs(self.previous_average_x) - 0.25) <= abs(average_x) <= (abs(self.previous_average_x) + 0.25):
                self.marker_x = average_x
                
            else:
                self.count_x = 0
                self.sum_x = 0
                self.cal_num =0
            self.previous_average_x = average_x
        elif self.cal_num>20:
            self.cal_num = 0
            average_x=0
            self.count_x = 0
        else:
            self.previous_average_x = average_x
            

        if self.count_y > 1 and self.cal_num<20:

            if (abs(self.previous_average_y) - 0.25) <= abs(average_y) <= (abs(self.previous_average_y) + 0.25):
                self.marker_y = average_y
            else:
                self.count_y = 0
                self.sum_y = 0
                self.cal_num =0
            self.previous_average_y = average_y
        elif self.cal_num>20:
            self.cal_num = 0
            average_y=0
            self.count_y = 0
        else:
            self.previous_average_y = average_y

        self.cal_num += 1
       

    def average_coordinates(self):
        """
        Calculates the mean x and y coordinates of the detected object
        in the global coordinate system within a certain interval to
        distinguish between different detections.
        """
        self.counter += 1
        if self.marker_average and self.counter > 1:
            if ((self.x-self.marker_average[0])** 2 + (self.y-self.marker_average[1])** 2) < self.threshhold:
                self.marker_average = [(self.marker_average[0]*(self.counter-1)+self.x)/self.counter, \
                                        (self.marker_average[1]*(self.counter-1)+self.y/self.counter)]
            else:
                # Reset
                self.marker_average = [self.x, self.y]
                counter = 1
        else:
            # Initialize
            self.marker_average = [self.x, self.y] 

    def Detection_visualization_rviz(self):
        """
        Visualizes detections made by yolov3 (darknet ros package) in rviz.
        car: SPEHRE, green colour
        person: CYLINDER, yellow colour
        tuck: CUBE, blue colour
        """
        count = 0
        MARKERS_MAX = 100
        markerArray = MarkerArray()
        while not rospy.is_shutdown():
            marker = Marker()
            marker.header.frame_id = "/map"
            

            #Switch between marker types depending of detection type.
            if self.detect_tag == "car":
                marker.type = marker.SPHERE
                #Green colour
                marker.color.a = 1.0
                marker.color.r = 0
                marker.color.g = 1.0
                marker.color.b = 0.0
            if self.detect_tag == "person":
                marker.type = marker.CYLINDER
                #Yellow colour
                marker.color.a = 1.0
                marker.color.r = 1.0
                marker.color.g = 1.0
                marker.color.b = 0.0
            if self.detect_tag == "truck":
                marker.type = marker.CUBE
                #Blue colour
                marker.color.a = 1.0
                marker.color.r = 0
                marker.color.g = 1.0
                marker.color.b = 1.0

            if self.marker_average:
                marker.action = marker.ADD
                marker.scale.x = 0.2
                marker.scale.y = 0.2
                marker.scale.z = 0.2
                marker.pose.orientation.w = 1.0
                marker.pose.position.x = self.marker_average[0]
                marker.pose.position.y = self.marker_average[1]
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

    rospy.init_node('Marker_node',anonymous = True)
    markerclass = markerclass()
    sub1 = rospy.Subscriber('/Global_coordinates_info', objectcoord , markerclass.retrieve_detection_coord_cb)
    pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10) 
    markerclass.Detection_visualization_rviz()
    rospy.spin()
