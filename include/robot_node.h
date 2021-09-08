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
        double gain_kp_;
        double gain_ki_;
        double gain_kd_;
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
        bool init_node_(geometry_msgs::Pose2D initial_pose);

        void run_node_();

        void waypoint_callback_(const geometry_msgs::Pose2D new_map);

        void publish_pose_();
}