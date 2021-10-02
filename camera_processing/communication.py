from ImageProcessing import ImageProcessing
import cv2
from sensor_msgs.msg import Image
from Snapshot import Snapshot
from cv_bridge import CvBridge
import numpy as np
import rospy

class ROS:
    snapshot = False
    def __init__(self):
        self.queue = []
        self.prev = np.zeros((800,800,3), np.uint8) 
        self.sub = rospy.Subscriber('/camera/image_raw', Image,self.callback)

    def callback(self,image):
        br = CvBridge()
        current_frame = br.imgmsg_to_cv2(image)
        self.queue.append(current_frame)
        if ROS.snapshot:
            ROS.snapshot = False
            Snapshot.currentSnapshot = current_frame


    def get_frame(self):
        if not self.queue:
            frame = self.prev 
        else:
            frame = self.queue.pop(0)
            self.prev = frame
        return cv2.imencode('.jpg', frame)[1].tobytes()
 