#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from exam_robot_control.srv import RobotMotion, RobotMotionResponse

pub = None

def stop_robot():
    twist = Twist()
    pub.publish(twist)
    rospy.sleep(1)

def move_forward():
    rate = rospy.Rate(10)

    twist = Twist()
    twist.linear.x = 0.3
    twist.angular.z = 0.0

    for i in range(30):
        pub.publish(twist)
        rate.sleep()

    stop_robot()

def turn_left():
    rate = rospy.Rate(10)

    twist = Twist()
    twist.linear.x = 0.0
    twist.angular.z = 0.6

    for i in range(20):
        pub.publish(twist)
        rate.sleep()

    stop_robot()

def handle_request(req):
    command = req.command.lower()

    if command == "inainte":
        move_forward()
        return RobotMotionResponse(True, "Robotul a mers inainte")

    elif command == "stanga":
        turn_left()
        return RobotMotionResponse(True, "Robotul s-a rotit la stanga")

    elif command == "opreste":
        stop_robot()
        return RobotMotionResponse(True, "Robotul s-a oprit")

    else:
        return RobotMotionResponse(False, "Comanda necunoscuta")

if __name__ == "__main__":
    rospy.init_node("robot_motion_server")

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.sleep(2)

    service = rospy.Service("robot_motion", RobotMotion, handle_request)

    rospy.loginfo("Serverul /robot_motion este pornit")

    rospy.spin()
