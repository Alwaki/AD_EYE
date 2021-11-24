'''
Class which is inherited, provides waypoint methods for cleaning
the waypoint list, and adding waypoints. Also stores parameters and lists
related to waypoints.
'''

class Waypoint():
    def __init__(self):
        self.local_pose = []                # The current pose of the robot
        self.waypoint_list = []           # List of goals for the robot to reach
        self.waypoints_tolerance = 0.4      # Tolerance threshhold for removing achieved goals
        self.waypoints_tolerance_sqrd = self.waypoints_tolerance ** 2


    def clear_waypoints(self, current_pose):
        '''
        Checks that the current vehicle pose has values, and that
        the list of waypoints is not empty. If both are fine, then
        checks the distance for each waypoint in the list, and
        compares it with the current vehicle pose. If any waypoints
        are less than a certain tolerance threshhold, they are removed.
        If the distance is greater than the tolerance threshhold, the
        loop is broken. Note that squared distance is used for speed.
        '''
        distance_sqrd = 0
        while (distance_sqrd < self.waypoints_tolerance_sqrd) and (len(self.waypoint_list) > 0):
            distance_sqrd = (self.waypoint_list[0][0] - self.local_pose[0]) ** 2 \
            + (self.waypoint_list[0][1] - self.local_pose[1]) ** 2
            print(distance_sqrd,'dist_sqrd')
            if distance_sqrd < self.waypoints_tolerance_sqrd:
                self.waypoint_list.pop(0)

    def add_waypoint(self, waypoint):
        '''
        Checks that the current vehicle pose has values. If yes, then
        takes a waypoint in the format [x,y] and compares it with the current
        pose of the vehicle. If the distance is found to be greater than
        a certain tolerance, then the waypoint is added to a list
        of waypoints. Note that squared distance is used for speed.
        '''
        if len(self.local_pose) != 0:
            distance_sqrd = (waypoint[0] - self.local_pose[0]) ** 2 \
                    + (waypoint[1] - self.local_pose[1]) ** 2
            if distance_sqrd > self.waypoints_tolerance_sqrd:
                self.waypoint_list.append(waypoint)
