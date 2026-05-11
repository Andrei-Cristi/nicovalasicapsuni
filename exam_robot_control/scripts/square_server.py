#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from exam_robot_control.srv import RobotMotion, RobotMotionResponse
import time
import math

pub = None

def move_forward(distance):
    vel = Twist()
    vel.linear.x = 0.3

    duration = distance / 0.3

    start = time.time()

    while time.time() - start < duration:
        pub.publish(vel)
        rospy.sleep(0.1)

    vel.linear.x = 0
    pub.publish(vel)

def rotate_90():
    vel = Twist()
    vel.angular.z = 0.5

    duration = (math.pi / 2) / 0.5

    start = time.time()

    while time.time() - start < duration:
        pub.publish(vel)
        rospy.sleep(0.1)

    vel.angular.z = 0
    pub.publish(vel)

def handle_square(req):

    for _ in range(req.repetitions):

        for i in range(4):

            move_forward(req.side)

            rotate_90()

    return RobotMotionResponse(True)

def server():

    global pub

    rospy.init_node('square_server')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.Service('draw_square', RobotMotion, handle_square)

    rospy.loginfo("Square server started")

    rospy.spin()

if __name__ == '__main__':
    server()
