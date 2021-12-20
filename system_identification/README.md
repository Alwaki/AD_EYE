# system_identification

## Overview

This is a system identification package, intended for checking unknown dynamics of a robot
for automatic tuning of automatic control methods.

**Keywords:** Control, system identification, ROS

### License

The source code is currently not licensed.

**Author: Alexander Wallén Kiessling<br />
Affiliation: [KTH AD-EYE](https://www.adeye.se/)<br />
Maintainer: Alexander Wallén Kiessling, akie@kth.se**

The platooning package is currently being tested under [ROS] Kinetic on respectively Ubuntu 16.04.
This is academic code, expect that it changes often and any fitness for a particular purpose is disclaimed.

## Installation

By installing the system_indentification package from the AD-EYE repo and fulfilling dependencies.

### Dependencies

See the package.xml for dependencies.

## Detailed description


## Usage details

### Subscribed Topics

* **`/tb3_id/odom`** ([nav_msgs/Odometry])

	The current state of the robot, in terms of pose and speed.


### Published Topics

* **`/tb3_id/cmd_vel`** ([geometry_msgs/Twist])

	Control output to robot, in terms of speed.
