#pragma once

#include <geometry_msgs.h>
#include <vector.h>

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
        bool leader_flag;
        geometry_msgs::Pose2D current_pose;
        std::vector<geometry_msgs::Pose2D> waypoints;

        /*!
         * Subscribers, publishers, services.
        */
        ros::Subscriber waypoint_sub_;
        ros::Publisher  pose_pub_;

        /*!
         * Method declarations.
        */
        bool init(geometry_msgs::Pose2D initial_pose);

        void waypoint_callback(const geometry_msgs::Pose2D new_map);

        void publish_pose();
}