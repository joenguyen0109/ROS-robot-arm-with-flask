from ImageProcessing import ImageProcessing
import os
import cv2
import struct
import socket
import pickle
from base_camera import BaseCamera

from Snapshot import Snapshot
        
class Camera(BaseCamera):
    snapshot = False

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source


    @staticmethod
    def frames():

        # Establish TCP connection to recieve image from camera

        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_ip = '127.0.1.1'# Standard loopback interface address (localhost)
        port = 10050 # Port to listen on (non-privileged ports are > 1023)
        # now connect to the web server on the specified port number
        client_socket.connect((host_ip,port)) 
        #'b' or 'B'produces an instance of the bytes type instead of the str type
        #used in handling binary data from network connections
        data = b""
        # Q: unsigned long long integer(8 bytes)
        payload_size = struct.calcsize("Q")



        while True:
            # Read data from TCP
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)

            # Handle SnapShot command
            if (Camera.snapshot):
                Snapshot.currentSnapshot = frame
                
            yield cv2.imencode('.jpg', frame)[1].tobytes()
