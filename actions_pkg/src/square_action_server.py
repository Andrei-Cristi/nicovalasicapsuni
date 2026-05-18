#!/usr/bin/env python3

import rospy
import actionlib
import time

from geometry_msgs.msg import Twist
from actionlib.msg import TestAction, TestFeedback, TestResult

class SquareActionServer():

    _feedback = TestFeedback()
    _result = TestResult()

    def __init__(self):

        self._as = actionlib.SimpleActionServer(
            "square_as",
            TestAction,
            execute_cb=self.goal_callback,
            auto_start=False
        )

        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        self._as.start()

    def goal_callback(self, goal):

        rospy.loginfo("Square action started")

        start_time = time.time()

        move = Twist()

        rate = rospy.Rate(10)

        side_size = goal.goal

        for side in range(1, 5):

            if self._as.is_preempt_requested():
                rospy.loginfo("Preempted")
                self._as.set_preempted()
                return

            self._feedback.feedback = side
            self._as.publish_feedback(self._feedback)

            rospy.loginfo("Moving side %d" % side)

            move.linear.x = 0.5
            move.angular.z = 0.0

            duration = side_size * 2

            start_side = time.time()

            while time.time() - start_side < duration:
                self.pub.publish(move)
                rate.sleep()

            move.linear.x = 0.0
            move.angular.z = 0.8

            turn_start = time.time()

            while time.time() - turn_start < 2:
                self.pub.publish(move)
                rate.sleep()

        stop = Twist()
        self.pub.publish(stop)

        total_time = int(time.time() - start_time)

        self._result.result = total_time

        rospy.loginfo("Square completed in %d seconds" % total_time)

        self._as.set_succeeded(self._result)


if __name__ == '__main__':

    rospy.init_node('square_action_server')

    SquareActionServer()

    rospy.spin()
