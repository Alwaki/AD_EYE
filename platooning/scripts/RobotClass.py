from PlannerClass import *

class Robot(Planner):

    def __init__(self):
        Planner.__init__(self)
        self.local_pose_sub = rospy.Subscriber('/odom', PoseWithCovarianceStamped, \
                                                self.local_pose_update_cb)
        self.follower_sub   = rospy.Subscriber('/vehicle/amcl_pose', PoseWithCovarianceStamped,\
                                                self.follower_logic_cb)
        self.speed_pub      = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.stop_srv       = rospy.Service('stop', SetBool, self.stop_service)
    
    def publish_speed(self, msg):
        self.speed_pub.publish(msg)
    
    def stop_service(self, req):
        self.stop(req.data)
