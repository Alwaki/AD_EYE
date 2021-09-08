#include "robot_node.h"

RobotNode::RobotNode(geometry_msgs::Pose2D initial_pose):
    nh_("~")
    {init_node(initial_pose);}

RobotNode::~RobotNode() = default;

void RobotNode::init_node(geometry_msgs::Pose2D initial_pose)
{
    waypoint_sub_  = nh_.subscribe<geometry_msgs::Pose2D>("waypoints", 1, &RobotNode::waypoint_callback_, this);
    pose_pub_      = nh_.advertise<geometry_msgs::Pose2D>("pose_output", 100);
}

void run_node_();