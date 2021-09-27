import math
import rospy
import tf
import tf2_ros
import numpy as np

from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class Robot:
    def __init__(self):

        """ Initiate parameters """
        self.stamped_waypoints = [[0,0,0,0]]     #Holds time stamped waypoints of the preceeding vehicle.
        self.last_odom = [0, 0]                  #List used to check if the Prescan simulation is at its end.
        self.t_ref = 2                           #Allowed "distance" in seconds between the the vehicles
        self.Kp_v = 2                            #Controller gain longitudianl controller
        self.Kp_w = 1.5                          #Controller gain lateral controller
        self.limit_v = 0.26                      #Saturation limit velocity
        self.limit_w = 1.82                      #Saturation limit yaw angle
        self.waypoints_tolerance = 0.8           #Waypoint tolerance to clean out old values from the stamped_waypoints list.

        """Initiate turtlebots current pose"""
        self.robotCurrentPose = [0,0,0,0]

        """Initiate parameters to calculate time between callbacks, i.e samplingtime"""
        self.last_callback_time = 0
        self.not_first_callback = False
        self.time_since_last_callback = 0

        """Create subscribers and publishers"""
        sub1 = rospy.Subscriber('/odom', Odometry, self.pose_cb)
        sub2  = rospy.Subscriber('/vehicle/odom', Odometry, self.controller_cb)
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    def pose_cb(self, Odometry):

            """Get the current pose of the turtlebot"""
            x = Odometry.pose.pose.position.x
            y = Odometry.pose.pose.position.y
            orientation = Odometry.pose.pose.orientation
            orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
            """Convert from quaternion to euler coordinates to match the coordinates of the /cmd_vel topic"""
            (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

            self.robotCurrentPose = [x,y,yaw]

    def controller_cb(self, Odometry):

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
        if self.last_odom[0] != x and self.last_odom[1] != y:
            self.stamped_waypoints.append([x,y,yaw,time])
            self.last_odom[0] = x
            self.last_odom[1] = y

        if self.stamped_waypoints:

            """Longitudinal P controller"""
            t1 = self.stamped_waypoints[0][3]
            t2 = self.stamped_waypoints[-1][3]
            dt = t2 - t1
            error_longitudinal = dt - self.t_ref

            #Integrator_v = Integrator_v + error_longitudinal * time
            control_output_v = self.Kp_v * error_longitudinal #+ Integrator_v * Ki_v

            """Saturation and anti-windup for longitudinal controller"""
            if control_output_v > self.limit_v:
                control_output_v = self.limit_v
                #Integrator_v = 0;
            elif control_output_v < 0:
                control_output_v = 0
                #Integrator_v = 0;

            """Lateral P controller"""
            x1 = self.stamped_waypoints[0][0] - self.robotCurrentPose[0] #[0[0]]
            y1 = self.stamped_waypoints[0][1] - self.robotCurrentPose[1] #[0][1]
            theta = math.atan2(y1,x1)
            dtheta = theta - self.robotCurrentPose[2]
            dtheta = ((dtheta + math.pi)%(2*math.pi)) - math.pi

            #Integrator_w = Integrator_w + dtheta*samplingtime
            control_output_w = self.Kp_w * dtheta # + Ki_w * Integrator_w

            """Saturation and anti-windup for lateral controller"""
            if control_output_w > self.limit_w:
                control_control_w = self.limit_w
                #Integrator_w = 0;
            elif control_output_w < -self.limit_w:
                control_output_w = -self.limit_w
                #Integrator_w = 0;

            """Send control commands to the turtlebot"""
            twist = Twist()
            twist.linear.x = control_output_v; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_output_w
            pub.publish(twist)

            """Clean out old values from the stamped_waypoints list"""
            for i in range(len(self.stamped_waypoints)):
                p1 = np.array(self.robotCurrentPose[0:2])
                p2 = np.array(self.stamped_waypoints[0][0:2])
                distanceToWaypoints = np.linalg.norm(p1 - p2)
                if distanceToWaypoints < self.waypoints_tolerance:
                    self.stamped_waypoints.pop(0)

        else:
            twist = Twist()
            """Stop the turtlebot"""
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            pub.publish(twist)