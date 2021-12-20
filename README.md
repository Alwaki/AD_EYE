# AD_EYE
This respository includes a Platooning package, object detection package, system identification package as well as GNU-RADIO (ITS-G5) interfacing script with ROS.

# Important comment on how to build the workspace

* Get into the workspace: cd catkin_ws in the terminal
* Then build the workspace with the following command: catkin_make -DCMAKE_BUILD_TYPE=Release

# How to launch the whole system

**Launch the turtlebots with namespace**

In order to make the launch process of the turlebots smoother modified launchfile needs to be 
put inside the respective turtlebot.

On **each turtlebot** put the adeye_tbX.launch, where X is either 0 or 1 for respective turtlebot, file inside of this directory:

/catkin_ws/src/.../turtlebot3_bringup/launch

Then on the RSU computer open up four terminals, two will be used for each turtlebot.

**ssh into respective turtlebot**

* ssh pi@(ip adress of turtlebot 0) (do this in two of the terminals)
* ssh pi@(ip adress of turtlebot 1) (do this in two of the terminals)

The IP adress of the turtlebot and the master IP adress might have to be changed inside
the bashrc file inside the turtlebots.

**Launch the scripts to start and configure the turtlebots and the raspicam camera**

* ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup adeyetb0.launch multi_robot_name:="tb3_0" set_lidar_frame_id:="tb3_0/base_scan"
  ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch

* ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_bringup adeyetb1.launch multi_robot_name:="tb3_1" set_lidar_frame_id:="tb3_1/base_scan"
  ROS_NAMESPACE=tb3_1 roslaunch turtlebot3_bringup turtlebot3_rpicamera.launch


**Launch the platooning package, object detection package, and the GNU-RADIO client script to interface ITS-G5 with ROS.**

Open up additionaly 3 terminals and in each terminal type:

* roslaunch platooning multi_robot.launch
* roslaunch object_detection object_detection_main.launch

For the GNU-RADIO client script first get into the correct folder by typing:
* cd catkin_ws/src/platooning/scripts/
* Then in the same terminal type: python gnuradio_client.py

*The RQT-graph shoud look like this:**

![RQT](https://github.com/Alwaki/AD_EYE/blob/main/rqt.png)

# A comment about using darknet_ros package with name space

To use darknet ros with name space some modifications to the darknet_ros package had to be made.

* In darknet_ros/launch/, the yolo_v3.launch and darknet_ros.launch were altered slightly.
* In darknet_ros/config, tb3_0ros.yaml and tb3_1ros.yaml were added so the package would publish
and subscribe within the corresponding namespace of the turtlebots which is tb3_0 and tb3_1.


