#!/usr/bin/env python3

import rospy
import actionlib
from std_msgs.msg import Empty
from actions_pkg.msg import DroneCommandAction, DroneCommandFeedback, DroneCommandResult

class DroneCommandServer(object):

    _feedback = DroneCommandFeedback()
    _result = DroneCommandResult()

    def __init__(self):
        self.takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)

        self._as = actionlib.SimpleActionServer(
            "drone_command_as",
            DroneCommandAction,
            self.goal_callback,
            False
        )
        self._as.start()

    def goal_callback(self, goal):
        command = goal.goal.upper()

        rate = rospy.Rate(1)

        if command == "TAKEOFF":
            self._feedback.feedback = "take off"
            self._as.publish_feedback(self._feedback)

            rospy.loginfo("Taking off...")
            self.takeoff_pub.publish(Empty())

            rate.sleep()

            self._result.result = True
            self._as.set_succeeded(self._result)

        elif command == "LAND":
            self._feedback.feedback = "landing"
            self._as.publish_feedback(self._feedback)

            rospy.loginfo("Landing...")
            self.land_pub.publish(Empty())

            rate.sleep()

            self._result.result = True
            self._as.set_succeeded(self._result)

        else:
            rospy.loginfo("Invalid command. Use TAKEOFF or LAND.")
            self._result.result = False
            self._as.set_succeeded(self._result)


if __name__ == '__main__':
    rospy.init_node('drone_command_server')
    DroneCommandServer()
    rospy.spin()
