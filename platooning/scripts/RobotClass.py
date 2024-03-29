from PlannerClass import *
from std_msgs.msg import String

class Robot(Planner):
    '''
    Class which inherits all other classes. Creates functionality for
    ROS communication.
    '''

    def __init__(self):
        Planner.__init__(self)
        self.local_pose_sub = rospy.Subscriber('/odom', PoseWithCovarianceStamped, \
                                                self.local_pose_update_cb, queue_size=10)
        self.follower_sub   = rospy.Subscriber('/vehicle/odom', PoseWithCovarianceStamped,\
                                                self.waypoint_update_cb, queue_size=10)
        self.speed_pub      = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.stop_srv       = rospy.Service('stop', SetBool, self.stop_service)

    def publish_speed(self, msg):
        '''
        Used as a virtual method in PlannerClass, implemented here.
        Simply uses the ROS publish functionality to publish a message.
        '''
        self.speed_pub.publish(msg)

    def stop_service(self, req):
        '''
        Callback method for the stop service. Passes the request as an argument,
        which is a boolean representing stop type.
        '''
        self.stop(req.data)
        
       # x = SetBool()
        #x.message = "heyman"
        #x.success = 1
        
        return (1 ,"yo")
