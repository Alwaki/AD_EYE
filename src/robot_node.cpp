#include "robot_node.h"

RobotNode::RobotNode():
    nh_("~")
    {init_node();}

RobotNode::~RobotNode() = default;

bool RobotNode::init_node()
{
    waypoint_sub_  = nh_.subscribe<geometry_msgs::Pose2D>("waypoints", 1, &RobotNode::waypoint_callback, this);
    pose_pub_      = nh_.advertise<geometry_msgs::Pose2D>("pose_output", 100);
}

void RobotNode::run_node(){}

void RobotNode::waypoint_callback(geometry_msgs::Pose2D point){}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "RobotNode");
    RobotNode robot_node_object;
    ros::Rate loop_rate(10);
    while(ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
}