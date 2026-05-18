#! /usr/bin/env python3

import rospy
import actionlib
from geometry_msgs.msg import Twist
from ardrone_as.msg import ArdroneAction, ArdroneGoal

nImage = 1

def feedback_callback(feedback):
    global nImage
    print('[Feedback] image n.%d received' % nImage)
    nImage += 1

rospy.init_node('drone_action_client')

client = actionlib.SimpleActionClient('/ardrone_action_server', ArdroneAction)
client.wait_for_server()

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

goal = ArdroneGoal()
goal.nseconds = 10

client.send_goal(goal, feedback_cb=feedback_callback)

rate = rospy.Rate(10)

move = Twist()
move.linear.x = 0.5
move.angular.z = 0.5

while not rospy.is_shutdown() and not client.wait_for_result(rospy.Duration(0.1)):
    pub.publish(move)
    rate.sleep()

stop = Twist()
pub.publish(stop)

print('[Result] State: %d' % client.get_state())
