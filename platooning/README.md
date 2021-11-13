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

* **amcl_parameters.yaml:** Parameters for AMCL package, used for localization with lidar.
* **sensor_filter.yaml:** Parameters for robot_localization package, used for sensor fusion to filter odometry data.

### Launch files

* **amcl.launch** Launch file for AMCL package.
* **sensor_filter.launch:** Launch file for robot_localization package.
* **single_robot.launch:** Used to launch a single robot instance, using parameters passed from multi launch.
* **multi_robot.launch:** Used to launch several robots, and deciding parameters passed to each robot.

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
### Import Turtlebot Model in Prescan
https://community.sw.siemens.com/s/article/Import-3-D-model-with-Model-Preparation-Tool-MPT

https://cad.onshape.com/documents/179d4ba2a1f9231f93cae6e2/w/71e9066aee42d5039f880e2f/e/3cb7d487c93655e7067a3d5f?fbclid=IwAR1RUqGc8uZ0Gc7hAdDFxJSulvsWcBhz3JirojNLNmd525iloat9MULHanc
