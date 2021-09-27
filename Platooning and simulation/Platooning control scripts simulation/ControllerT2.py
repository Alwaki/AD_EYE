import math
import rospy
import tf
import tf2_ros
import numpy as np

from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


rospy.init_node('Vehicle2_node', anonymous = False)

""" Init parameters """
stamped_waypoints = [[0,0,0,0]]
last_odom = [0, 0]
theta1 = 0
t_ref = 2                   #Allowed "Distance" between the two turtlebots
Kp_v = 2                  #Controller gain longitudianl controller
Kp_w = 1.5             #Controller gain lateral controller
limit_v = 0.26       #Saturation limit velocity
limit_w = 1.82              #Saturation limit yaw angle
waypoints_tolerance = 0.8  #Tolerence set in order to clear clean out values out of stamped_waypoints
#speed = 0.5

class controller:
    def __init__(self):

        #print(self.robotCurrentPose, "Robots start position")
        self.robotCurrentPose = [0,0,0,0]
        self.last_ballback_time = 0
        self.not_first_callback = False
        self.time_since_last_callback = 0

        self.speed = 0.5

    def TurtleBotPose(self,Odometry):

        """Get current pose of the turtlebot and publish it to the preceeding vehicle"""
        """Might use this callback to get turtlebots current velocity instead"""
        x = Odometry.pose.pose.position.x
        y = Odometry.pose.pose.position.y
        orientation = Odometry.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        self.robotCurrentPose = [x,y,yaw]

        #print(self.robotCurrentPose)
        #print(len(self.robotCurrentPose))

        """Publisher to preceeding vehicle, custom message Vehicle_pose needed?"""
        #pub = rospy.Publisher('Vehicle1_odometry', Vehicle1_pose, queue_size=10)
        #Pose =  Vehicle1_pose()
        #pub.publish(Pose)

        """Example rospy.Rate:"""
         #pub = rospy.Publisher('topic_name', String, queue_size=10)
         #rospy.init_node('node_name')
         #r = rospy.Rate(10) # 10hz
         #while not rospy.is_shutdown():
            #pub.publish("hello world")
            #r.sleep()

    def Controller(self,Odometry):

        """ Caulculate time between callbacks, i.e Samplingtime """
        callback_time = rospy.get_time()
        if self.not_first_callback:
            self.time_since_last_callback = rospy.get_time() - self.last_callback_time
        self.not_first_callback = True
        self.last_callback_time = callback_time

        """This should be the pose from Prescan here, atm Odometry as a placeholder to test the code."""
        x = Odometry.pose.pose.position.x
        y = Odometry.pose.pose.position.y
        orientation = Odometry.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        """Could use rospy.get_time() below instead when we have the Prescan odometry"""
        time = callback_time#Odometry.header.stamp.secs

        if last_odom[0] != x and last_odom[1] != y:
            stamped_waypoints.append([x,y,yaw,time])
            last_odom[0] = x
            last_odom[1] = y

        if stamped_waypoints:
            """Store most recent waypoint values in the end of the list."""
            #stamped_waypoints.insert(0, [x,y,w,time])

            #list[-1][0] get first item of last vector in list!
            """Longitudinal controller based on time"""
            t1 = stamped_waypoints[0][3]
            t2 = stamped_waypoints[-1][3]

            #print(t2,"t2")

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

            """Lateral controller PI"""
            x1 = stamped_waypoints[0][0] - self.robotCurrentPose[0] #[0[0]]
            y1 = stamped_waypoints[0][1] - self.robotCurrentPose[1] #[0][1]
            theta = math.atan2(y1,x1)
            dtheta = theta - self.robotCurrentPose[2]
            dtheta = ((dtheta + math.pi)%(2*math.pi)) - math.pi
            print(dtheta)
            #print(dtheta,"dtheta")

            #Integrator_w = Integrator_w + dtheta*samplingtime
            control_output_w = Kp_w * dtheta # + Ki_w * Integrator_w
            print(control_output_w,"Thetacontrol")

            """Saturation and anti-windup for lateral controller"""
            if control_output_w > limit_w:
                control_control_w = limit_w
                #Integrator_w = 0;
            elif control_output_w < -limit_w:
                control_output_w = -limit_w
                #Integrator_w = 0;

            """Send control commands to the turtlebot"""
                #TO DO:
                #control_output_v
                #control_output_w

            twist = Twist()
            twist.linear.x = control_output_v; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_output_w
            pub.publish(twist)

            """ Placeholder if poses needs to be updated by calculation"""
            #self.robotCurrentPose[0] += self.speed*self.time_since_last_callback
            #self.robotCurrentPose[1] += self.speed*self.time_since_last_callback
            #print(self.RobotCUrrentPose)


            """Clean out old values from the waypoints list"""
            for i in range(len(stamped_waypoints)):
                p1 = np.array(self.robotCurrentPose[0:2])#[0][0:2]
                p2 = np.array(stamped_waypoints[0][0:2])

                #print(p1,"p1")
                #print(p2,"p2")
                #distanceToWaypoints = math.dist(robotCurrentPose[0][0:2], stamped_waypoints[0][0:2])
                distanceToWaypoints = np.linalg.norm(p1 - p2)
                #print(distanceToWaypoints)


                #print(distanceToWaypoints)
                if distanceToWaypoints < waypoints_tolerance:
                    stamped_waypoints.pop(0)  #May not be the most efficient way to do this


            print(len(stamped_waypoints))

        else:
            twist = Twist()
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            pub.publish(twist)

if __name__ == '__main__':

    """Initiate the class"""
    controller = controller()

    """ Set up subscribers """
    sub1 = rospy.Subscriber('/robot2/odom', Odometry, controller.TurtleBotPose)
    sub2  = rospy.Subscriber('/robot1/odom', Odometry, controller.Controller)
    pub = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=10)

    """Waken callback when there is a message available, otherwise sleep"""
    rospy.spin()
