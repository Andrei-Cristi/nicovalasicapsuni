#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

pub = None

def callback(scan):
    global pub

    move = Twist()

    front = scan.ranges[0]
    left = scan.ranges[90]
    right = scan.ranges[270]

    limit = 1.0

    if front < limit:
        move.linear.x = 0.0
        move.angular.z = 0.5
        rospy.loginfo("Obstacle in front - turning left")

    elif left < limit:
        move.linear.x = 0.0
        move.angular.z = -0.5
        rospy.loginfo("Obstacle on left - turning right")

    elif right < limit:
        move.linear.x = 0.0
        move.angular.z = 0.5
        rospy.loginfo("Obstacle on right - turning left")

    else:
        move.linear.x = 0.25
        move.angular.z = 0.0
        rospy.loginfo("Free path - moving forward")

    pub.publish(move)

rospy.init_node("lidar_guard_node")

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

sub = rospy.Subscriber("/scan", LaserScan, callback)

rospy.spin()
