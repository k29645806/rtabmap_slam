#!/usr/bin/env python
import roslib
roslib.load_manifest('rtabmap_slam')
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Point, Quaternion
import tf

import time


class Navigation(object):

    label_list = {}

    Room = PoseStamped()
    Room.pose.position = Point(55,66,0)
    Room.pose.orientation = Quaternion(0,0,0,1)

    Kitchen = PoseStamped()
    Kitchen.pose.position = Point(77,88,0)
    Kitchen.pose.orientation = Quaternion(0,0,0,1)

    label_list["room"] = Room
    label_list["kitchen"] = Kitchen


    def __init__(self):
        rospy.init_node('sendGoal')
        self.pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.tf_listener = tf.TransformListener()

    def sendGoal(self,cmd):
        goal = self.label_list[cmd]
        goal.header.stamp = rospy.Time.now()
        goal.header.frame_id = "map"
        self.pub.publish(goal)

    def label_location(self,cmd):
        location_label = cmd.split(" ")[1]
        rospy.loginfo("Location label: %s"%location_label)
        location = self.subTF()

        try:
            self.label_list[location_label] = location
        except:
            rospy.loginfo("Error are you sure tf transform being published? ")

    def subTF(self):
        # Subscribe /map -> /base_link transform
        self.tf_listener.waitForTransform("map", "base_link", rospy.Time(), rospy.Duration(1.0))
        (trans,rot) = self.tf_listener.lookupTransform("map", "base_link", rospy.Time())
        rospy.loginfo("Translation:%s  Orientation:%s"%(trans, rot))
        location = PoseStamped()
        location.pose.position = Point(trans[0], trans[1], trans[2])
        location.pose.orientation = Quaternion(rot[0], rot[1], rot[2], rot[3])
        return location


    def parser(self,cmd):
        if "label" in cmd:
            self.label_location(cmd)

        elif cmd in self.label_list:
            rospy.loginfo("Heading to %s"%cmd)
            self.sendGoal(cmd)
        else:
            rospy.loginfo("The labeled list")
            rospy.loginfo(self.label_list.keys())

if __name__ == '__main__':
    try:
        nav = Navigation()
        while not rospy.is_shutdown():
            cmd = raw_input("Where do you want to go?  ")
            nav.parser(cmd)
    except rospy.ROSInterruptException:
        rospy.loginfo("Error rospy")
    finally:
        rospy.loginfo("Publish_nav_cmd stopped")
