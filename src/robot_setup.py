#!/usr/bin/env python
import roslib
roslib.load_manifest('rtabmap_slam')
import rospy
import tf
from tf.transformations import quaternion_from_euler
from std_msgs.msg import Header, String
from geometry_msgs.msg import Quaternion, Twist, Vector3
from nav_msgs.msg import Odometry

'''
1. Publish odometry information
2. Publish robot transform configuration
'''

class Robot(object):
    def __init__(self):
        rospy.init_node('robot_setup')
        self.tfBroadcaster = tf.TransformBroadcaster()
        rospy.Subscriber("/kobuki/odom", Odometry, self.subOdom)
        self.odomPublisher = rospy.Publisher('/odom',Odometry, queue_size=10)
        self.position, self.orientation = (0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)
        self.linearX, self.angularZ = 0.0, 0.0
#-------------------------------------------------------------------------------
    def subOdom(self, odom):
        self.position = (odom.pose.pose.position.x, odom.pose.pose.position.y, 0.0)
        self.orientation = (odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w)
        self.linearX = odom.twist.twist.linear.x
        self.angularZ = odom.twist.twist.angular.z
#-------------------------------------------------------------------------------
    def broadcastTF(self,data=None):
        self.tfBroadcaster.sendTransform(self.position,
                         self.orientation,
                         rospy.Time.now(),
                         "base_link",
                         "odom")
        self.tfBroadcaster.sendTransform((0.0, 0.0, 0.2),
                         quaternion_from_euler(0, 0, 0),
                         rospy.Time.now(),
                         "camera_link",
                         "base_link")
        self.tfBroadcaster.sendTransform((0, 0, 0.2),
                         quaternion_from_euler(0, 0, 0),
                         rospy.Time.now(),
                         "base_laser",
                         "base_link")

    def publishOdometry(self,data=None):
        odom = Odometry()
        odom.header.seq = 0
        odom.header.stamp = rospy.Time.now()
        odom.header.frame_id = "odom"
        odom.pose.pose.position.x = self.position[0]
        odom.pose.pose.position.y = self.position[1]
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = Quaternion(self.orientation[0], self.orientation[1], self.orientation[2], self.orientation[3])
        odom.twist.twist.linear.x = self.linearX
        odom.twist.twist.angular.z = self.angularZ
        self.odomPublisher.publish(odom)

    def start(self):
        rate = rospy.Rate(50.0)
        rospy.loginfo("Start publishing required tf")
        while not rospy.is_shutdown():
            self.broadcastTF()
            self.publishOdometry()
            rate.sleep()


if __name__ == '__main__':
    kai = Robot()
    kai.start()
