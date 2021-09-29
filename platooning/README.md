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

Currently no standalone config files. 

### Launch files

TO BE ADDED!

* **mcl.launch:** Only simple launch which starts the single mcl node.


### Subscribed Topics

TO BE ADDED!

* **`/temperature`** ([sensor_msgs/Temperature])

	The temperature measurements from which the average is computed.


### Published Topics

TO BE ADDED!


### Services

TO BE ADDED!

* **`get_average`** ([std_srvs/Trigger])

	Returns information about the current average. For example, you can trigger the computation from the console with

		rosservice call /ros_package_template/get_average


### Parameters

TO BE ADDED!

* **`subscriber_topic`** (string, default: "/temperature")

	The name of the input topic.

* **`cache_size`** (int, default: 200, min: 0, max: 1000)

	The size of the cache.

### Map making (For future)
https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/
https://learn.turtlebot.com/2015/02/03/8/