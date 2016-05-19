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
Publish robot transform configuration
'''

class Robot(object):
    def __init__(self):
        rospy.init_node('robot_setup_v')
        self.tfBroadcaster = tf.TransformBroadcaster()
        #rospy.Subscriber("/rtabmap/odom", Odometry, self.subOdom)
        #self.odomPublisher = rospy.Publisher('/odom',Odometry, queue_size=10)
        self.position, self.orientation = (0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 0.0)
#-------------------------------------------------------------------------------
    def subOdom(self, odom):
        self.position = (odom.pose.pose.position.x, odom.pose.pose.position.y, 0.0)
        self.orientation = (odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z, odom.pose.pose.orientation.w)
#-------------------------------------------------------------------------------
    def broadcastTF(self,data=None):
        #self.tfBroadcaster.sendTransform(self.position,
        #                 self.orientation,
        #                 rospy.Time.now(),
        #                 "base_link",
        #                 "odom")
        #self.tfBroadcaster.sendTransform((0, 0, 0),
        #                 quaternion_from_euler(0, 0, 0),
        #                 rospy.Time.now(),
        #                 "base_link",
        #                 "base_footprint")
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

    def start(self):
        rate = rospy.Rate(50.0)
        rospy.loginfo("Start publishing required tf")
        while not rospy.is_shutdown():
            self.broadcastTF()
            rate.sleep()


if __name__ == '__main__':
    kai = Robot()
    kai.start()
