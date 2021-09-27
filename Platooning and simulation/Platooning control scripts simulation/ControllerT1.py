"""Controller script for turtlebot 1"""

import math
import rospy
import tf
import tf2_ros
import numpy as np

from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

"""Initiate node for turtlebot 1"""
rospy.init_node('Vehicle1_node', anonymous = False)

""" Initiate parameters """
stamped_waypoints = [[0,0,0,0]]     #Holds time stamped waypoints of the preceeding vehicle.
last_odom = [0, 0]                  #List used to check if the Prescan simulation is at its end.
t_ref = 2                           #Allowed "distance" in seconds between the the vehicles
Kp_v = 2                            #Controller gain longitudianl controller
Kp_w = 1.5                          #Controller gain lateral controller
limit_v = 0.26                      #Saturation limit velocity
limit_w = 1.82                      #Saturation limit yaw angle
waypoints_tolerance = 0.8           #Waypoint tolerance to clean out old values from the stamped_waypoints list.

class controller:
    def __init__(self):

        """Initiate turtlebots current pose"""
        self.robotCurrentPose = [0,0,0,0]

        """Initiate parameters to calculate time between callbacks, i.e samplingtime"""
        self.last_ballback_time = 0
        self.not_first_callback = False
        self.time_since_last_callback = 0

    def TurtleBotPose(self,Odometry):

        """Get the current pose of the turtlebot"""
        x = Odometry.pose.pose.position.x
        y = Odometry.pose.pose.position.y
        orientation = Odometry.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        """Convert from quaternion to euler coordinates to match the coordinates of the /cmd_vel topic"""
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        self.robotCurrentPose = [x,y,yaw]

    def Controller(self,Odometry):

        """Get Current time"""
        callback_time = rospy.get_time()

        """Get time between callbacks, i.e samplingtime, will be used if we implement a PI controller later"""
        if self.not_first_callback:
            self.time_since_last_callback = rospy.get_time() - self.last_callback_time
        self.not_first_callback = True
        self.last_callback_time = callback_time

        """Retrieve the pose of the Prescan vehicle"""
        x = Odometry.pose.pose.position.x
        y = Odometry.pose.pose.position.y
        orientation = Odometry.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        time = callback_time

        """If statement checking if the presan simulation is at its end, stop the turtlebot if it is"""
        if last_odom[0] != x and last_odom[1] != y:
            stamped_waypoints.append([x,y,yaw,time])
            last_odom[0] = x
            last_odom[1] = y

        if stamped_waypoints:

            """Longitudinal P controller"""
            t1 = stamped_waypoints[0][3]
            t2 = stamped_waypoints[-1][3]
            dt = t2 - t1
            error_longitudinal = dt - t_ref

            #Integrator_v = Integrator_v + error_longitudinal * time
            control_output_v = Kp_v * error_longitudinal #+ Integrator_v * Ki_v

            """Saturation and anti-windup for longitudinal controller"""
            if control_output_v > limit_v:
                control_output_v = limit_v
                #Integrator_v = 0;
            elif control_output_v < 0:
                control_output_v = 0
                #Integrator_v = 0;

            """Lateral P controller"""
            x1 = stamped_waypoints[0][0] - self.robotCurrentPose[0] #[0[0]]
            y1 = stamped_waypoints[0][1] - self.robotCurrentPose[1] #[0][1]
            theta = math.atan2(y1,x1)
            dtheta = theta - self.robotCurrentPose[2]
            dtheta = ((dtheta + math.pi)%(2*math.pi)) - math.pi

            #Integrator_w = Integrator_w + dtheta*samplingtime
            control_output_w = Kp_w * dtheta # + Ki_w * Integrator_w

            """Saturation and anti-windup for lateral controller"""
            if control_output_w > limit_w:
                control_control_w = limit_w
                #Integrator_w = 0;
            elif control_output_w < -limit_w:
                control_output_w = -limit_w
                #Integrator_w = 0;

            """Send control commands to the turtlebot"""
            twist = Twist()
            twist.linear.x = control_output_v; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_output_w
            pub.publish(twist)

            """Clean out old values from the stamped_waypoints list"""
            for i in range(len(stamped_waypoints)):
                p1 = np.array(self.robotCurrentPose[0:2])
                p2 = np.array(stamped_waypoints[0][0:2])
                distanceToWaypoints = np.linalg.norm(p1 - p2)
                if distanceToWaypoints < waypoints_tolerance:
                    stamped_waypoints.pop(0)

        else:
            twist = Twist()
            """Stop the turtlebot"""
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            pub.publish(twist)

if __name__ == '__main__':

    """Initiate the controller class"""
    controller = controller()

    """Subscribe to turtlebots 1 odom topic """
    sub1 = rospy.Subscriber('/robot1/odom', Odometry, controller.TurtleBotPose)

    """Subscribe to the Precsan vehicles odom topic"""
    sub2  = rospy.Subscriber('/vehicle/odom', Odometry, controller.Controller)

    """Publisher to send linear speed and yaw angle to the turtlebot 1"""
    pub = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)

    """Waken callback when there is a message available, otherwise sleep"""
    rospy.spin()
