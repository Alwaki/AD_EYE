#ifndef ROBOT_NODE_H
#define ROBOT_NODE_H

#include "ros/ros.h"
#include <geometry_msgs/Pose2D.h>
#include <vector>

/*!
* Main class for object instantiation in ROS interface.
*/
class RobotNode
{
   public:
        /*!
        * Constructor.
        */
        RobotNode();

        /*!
         * Destructor.
        */
        virtual ~RobotNode();

    private:
        /*!
         * Ros node handle.
        */
        ros::NodeHandle nh_;

        /*!
         * Parameters and/or variables.
        */
        bool leader_flag_;
        geometry_msgs::Pose2D current_pose_;
        std::vector<geometry_msgs::Pose2D> waypoints_;

        /*!
         * Subscribers, publishers, services.
        */
        ros::Subscriber waypoint_sub_;
        ros::Publisher  pose_pub_;

        /*!
         * Method declarations.
        */
        bool init_node();

        void run_node();

        void waypoint_callback(geometry_msgs::Pose2D point);
};

#endif