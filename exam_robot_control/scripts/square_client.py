#!/usr/bin/env python3

import rospy
from exam_robot_control.srv import RobotMotion

rospy.init_node('square_client')

rospy.wait_for_service('draw_square')

client = rospy.ServiceProxy('draw_square', RobotMotion)

response = client(1.0, 2)

print(response.success)
