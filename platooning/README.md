# platooning

## Overview

This is a platooning package, intended for simulation and physical demonstration with turtlebots.

**Keywords:** Platooning, driverless, ROS

### License

The source code is currently not licensed.

**Author: Alexander Wallén Kiessling, Niclas Määttä, Youchen Sun<br />
Affiliation: [KTH AD-EYE](https://www.adeye.se/)<br />
Maintainer: Alexander Wallén Kiessling, akie@kth.se**

The platooning package is currently being tested under [ROS] Kinetic on respectively Ubuntu 16.04.
This is academic code, expect that it changes often and any fitness for a particular purpose is disclaimed.

## Installation

By installing the platooning package from the AD-EYE repo and fulfilling dependencies.

### Dependencies

See the package.xml for dependencies.

## Detailed description

## Usage details
### Config files

navigation.rviz

### Launch files

* multi_robot.launch (this launch file launch all the other launch files)
* single_robot.launch
* amcl_tb3_0.launch
* amcl_tb3_1.launch


### Subscribed Topics

TO BE ADDED!

* **`/temperature`** ([sensor_msgs/Temperature])

	The temperature measurements from which the average is computed.


### Published Topics

TO BE ADDED!


### Services

* **`stop`** ([std_srvs/SetBool])

	Service used to be triggered by ITS-G5, will stop the turtlebots in the platoon.

		

### Parameters

TO BE ADDED!


