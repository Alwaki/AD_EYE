from PIDClass import *
from WaypointClass import *

class Planner(PID, Waypoint):
    '''
    Class that inherits the PID controller and Waypoint functionality.
    Uses these to generate planning sequences in the form of speed messages,
    and stop commands.
    '''

    def __init__(self):
        PID.__init__(self)
        Waypoint.__init__(self)
        self.running_flag = True            # Boolean logic used to indicate if follower
                                            # logic should continue
        self.longitudinal_ref = 0.35         # Used as reference to create longitudinal error
        self.local_speed = []               # Stores current speed of robot as [linear, angular]
        self.deceleration_constant = 0.1    # Deceleration constant used to simulate stop with inertia

    def msg_2_list(self, msg):
        '''
        Recieves a geometry message, and converts it to list format
        with [x,y,theta]. Can use either nav_msgs/Odometry or
        geometry_msgs/PoseWithCovarianceStamped.
        '''
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        orientation = msg.pose.pose.orientation
        orientation_list = [orientation.x, orientation.y, orientation.z, orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        return [x,y,yaw]

    def speed_2_twist(self, linear_speed, angular_speed):
        '''
        Recieves two scalar values, and converts them to a twist message format,
        to represent velocity in the 2D use case.
        '''
        twist = Twist()
        twist.linear.x = linear_speed; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = angular_speed
        return twist

    def local_pose_update_cb(self, msg):
        '''
        Recieves a geometry message, converts it to list format
        and updates the local pose of the vehicle with it.
        '''
        [x,y,yaw] = self.msg_2_list(msg)
        self.local_pose = [x,y,yaw]
    
    def waypoint_update_cb(self, msg):
        '''
        Recieves a geometry message, converts it to list format
        and tries to add it to the list of waypoints.
        '''
        [x,y,yaw] = self.msg_2_list(msg)
        self.add_waypoint([x,y])
    
    def scheduled_follower_logic(self):
        '''
        This method is meant to be called at a fixed rate.
        Will attempt to clear waypoints close to the robot,
        and calculate a control sequence based on existing
        waypoints and the vehicle's current pose. Also
        publishes a speed command based on this control.
        '''

        # Get the time between callbacks, i.e the sampling time
        self.sample_time()

        # Check that the vehicle has not been stopped
        if self.running_flag:

            # Check that the robot has a current pose
            if len(self.local_pose) != 0:

                # Clear all waypoints nearby
                self.clear_waypoints(self.local_pose)

                # If there are waypoints, calculate control sequence for latest waypoint
                if len(self.waypoint_list) > 0:

                    # Calculate longitudinal control
                    distance = math.hypot(self.waypoint_list[-1][0] - self.local_pose[0], \
                                        self.waypoint_list[-1][1] - self.local_pose[1])
                    longitudinal_error = distance - self.longitudinal_ref
                    longitudinal_control = self.longitudinal_PI_control(longitudinal_error)

                    # Calculate lateral control
                    x1 = self.waypoint_list[0][0] - self.local_pose[0]
                    y1 = self.waypoint_list[0][1] - self.local_pose[1]
                    theta = math.atan2(y1,x1)
                    dtheta = theta - self.local_pose[2]
                    dtheta = ((dtheta + math.pi)%(2*math.pi)) - math.pi
                    lateral_control = self.lateral_PI_control(dtheta)

                    # Publish control sequence to velocity topic
                    speed_msg = self.speed_2_twist(longitudinal_control, lateral_control)
                    self.publish_speed(speed_msg)

                    # Update current speed information
                    self.local_speed = [longitudinal_control, lateral_control]
                
                # If there are no waypoints
                else:

                    # Kill the engines until new waypoints
                    speed_msg = self.speed_2_twist(0,0)

                    # Publish zero velocity sequence to velocity topic
                    self.publish_speed(speed_msg)

                    # Update current speed information
                    self.local_speed = [0, 0]

    def stop(self, type = 0):
        '''
        A function which is called to immediately stop the vehicle, both
        in longitudinal and lateral directions. This function supports
        both immediate stops and simulated stops with inertia. The type
        of stop is chosen with the type parameter. Unsupported types
        also lead to immediate stop.

        0: immediate stop (default)
        1: stop with inertia

        Note that the stop with inertia is calculated with a reaction time
        of 0.7 seconds, and an assumed deceleration of 1 m/s^2.
        '''
        # Flag for follower logic to stop
        self.running_flag = False

        # Stop immediately
        if type == 0:
            msg = self.speed_2_twist(0, 0)
            self.publish_speed(msg)

        # Stop with inertia
        elif type == 1:
            time.sleep(0.7)
            while self.local_speed[0] > 0.1:
                self.local_speed[0] = self.local_speed[0] - self.deceleration_constant
                msg = self.speed_2_twist(self.local_speed[0], 0)
                self.publish_speed(msg)
                time.sleep(0.1)
            msg = self.speed_2_twist(0, 0)
            self.publish_speed(msg)

        # For any undefined argument, also stop immediately
        else:
            msg = self.speed_2_twist(0, 0)
            self.publish_speed(msg)

    def publish_speed(self, msg):
        '''Virtual method, implemented by inheriting class'''
        pass
