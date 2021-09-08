#pragma once



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
         * Parameters/variables.
        */

        /*!
         * Subscribers, publishers, services.
        */

        /*!
         * Method declarations.
        */
}