# object detection

## Overview

This is a object detection package intended for detection of trucks or car's along the road.
However, other types of objects can also be detected by changing the code.
This package use the darknet_ros package to enable the use of YOLOv3 for object detection.
The darknet_ros package is available here: https://github.com/leggedrobotics/darknet_ros
Furthermore, the object detection package use pre-trained weights also available in the darknet_ros package.

**Keywords:** Object detection, YOLOv3, darknet_ros, ROS

### License

The source code is currently not licensed.

**Author: Niclas Määttä, Youchen Sun, Alexander Wallén Kiessling<br />
Affiliation: [KTH AD-EYE](https://www.adeye.se/)<br />
Maintainer: Niclas Määttä, nmaatta@kth.se**

The object detection is currently being tested under [ROS] Kinetic on respectively Ubuntu 16.04.
This is academic code, expect that it changes often and any fitness for a particular purpose is disclaimed.

## Installation

By installing the object detection package from the AD-EYE repo and fulfilling dependencies.
In order to be able to use the GPU when performing object detection CUDA needs to be installed, 
see appendix E.2.2 in AD-EYES final report on how to install this.

### Dependencies

* **darknet_ros**: https://github.com/leggedrobotics/darknet_ros

## Detailed description

## Usage details

To launch this package type: roslaunch object_detection object_detection_main.launch in a terminal.

* This will launch the object detection algorithm for each turtlbots as well as one instance of darknet ros
for each turtlebot.

### Launch files

* object_detection_main.launch 
* object_detection.launch






