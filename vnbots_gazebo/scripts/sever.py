#!/usr/bin/python3
# Host sever to send image from camera to website

import socket
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import pickle
import struct
class SeverCamera:

    def __init__(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_name  = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print('HOST IP:',host_ip)
        port = 10050
        socket_address = (host_ip,port)
        print('Socket created')
        # bind the socket to the host. 
        #The values passed to bind() depend on the address family of the socket
        server_socket.bind(socket_address)
        print('Socket bind complete')
        #listen() enables a server to accept() connections
        #listen() has a backlog parameter. 
        #It specifies the number of unaccepted connections that the system will allow before refusing new connections.
        server_socket.listen(5)
        print('Socket now listening')
        self.client_socket,addr = server_socket.accept()
        self.sub = rospy.Subscriber('/camera/image_raw', Image, self.callback)

    # Everytime rostopic send a new image, sever will send it to website via socket programming
    def callback(self,image):
        br = CvBridge()
        current_frame = br.imgmsg_to_cv2(image)
        if self.client_socket:
            a = pickle.dumps(current_frame)
            message = struct.pack("Q",len(a))+a
            self.client_socket.sendall(message)

if __name__ == '__main__':
    rospy.init_node('Simple_node_camera',anonymous=True)
    camera = SeverCamera()
    rospy.spin()
