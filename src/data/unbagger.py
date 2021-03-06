#!/usr/bin/python

# Start up ROS pieces.
PKG = 'object_detection'
import roslib; roslib.load_manifest(PKG)
import rosbag
import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Reading bag filename from command line or roslaunch parameter.
import os
import sys

class ImageCreator():
    # Must have __init__(self) function for a class, similar to a C++ class constructor.
    def __init__(self):
        # Get parameters when starting node from a launch file.
        if len(sys.argv) < 2:
            #save_dir = rospy.get_param('save_dir')
            #filename = rospy.get_param('filename')

            save_dir = './images/'
            filename = './bagfiles/positive.bag'

            rospy.loginfo("Bag filename = %s", filename)
        # Get parameters as arguments to 'rosrun my_package bag_to_images.py <save_dir> <filename>', where save_dir and filename exist relative to this executable file.
        else:
            save_dir = os.path.join(sys.path[0], sys.argv[1])
            filename = os.path.join(sys.path[0], sys.argv[2])
            rospy.loginfo("Bag filename = %s", filename)

        # Use a CvBridge to convert ROS images to OpenCV images so they can be saved.
        self.bridge = CvBridge()

        # Open bag file.
        with rosbag.Bag(filename, 'r') as bag:
            for topic, msg, t in bag.read_messages():
                try:
                    cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
                    timestr = "%.6f" % msg.header.stamp.to_sec()
                    image_name = str(save_dir)+timestr+".png"
                    print ("saving image:" + image_name)
                    cv.imwrite(image_name, cv_image)
                except CvBridgeError, e:
                    print (e)


# Main function.    
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node(PKG)
    # Go to class functions that do all the heavy lifting. Do error checking.
    try:
        image_creator = ImageCreator()
    except rospy.ROSInterruptException: pass
