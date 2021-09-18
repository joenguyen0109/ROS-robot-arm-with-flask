#!/usr/bin/python
# This file spawns object into gazebo world


import rospy
import tf

from gazebo_msgs.srv import SpawnModel

from geometry_msgs.msg import *

def spawn_object(pose,name,path):
    
    model_xml = ''

    with open (path, 'r') as xml_file:
        model_xml = xml_file.read().replace('\n', '')

    spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
    spawn_model_prox(name, model_xml, '', pose, 'world')

def main():

    rospy.init_node('spawn_object')

    print("Generate Objects")

    ot = tf.transformations.quaternion_from_euler(0,0,0)

    # Object location
    xPose = [1.2,1.3,1.4,1.8,1.5]
    yPose = [0.1,-0.2,0.5,0.4,0]
    # Object file path
    path = [r'/home/joe/Documents/gazeboModel/gear_part/model.sdf',r'/home/joe/Documents/gazeboModel/box/box.sdf',r'/home/joe/Documents/gazeboModel/ball/ball.sdf',r'/home/joe/Documents/ROS_ws/VNBot_ws/src/vnbots_gazebo/models/bowl/model.sdf',r'/home/joe/Documents/ROS_ws/VNBot_ws/src/vnbots_gazebo/models/gear_part/model.sdf']

    
    i =0 
    for x in xPose:
        pose = Pose(position = Point(x=x, y=yPose[i], z=0.775), orientation = Quaternion(x=ot[0], y=ot[1], z=ot[2], w=ot[3]))
        spawn_object(pose, "object" + str(i),path[i])
        i += 1


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        print ("Program interrupted before completion")
