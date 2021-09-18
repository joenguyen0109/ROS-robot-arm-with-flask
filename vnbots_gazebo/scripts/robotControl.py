# Control robot and pickup objects base on website command


import rospy
import math
import moveit_commander
from std_srvs.srv import Empty
from vnbots_gazebo.srv import EndPosition

class robotControl:

    def __init__(self):
        self.server = rospy.Service('MoveRobot', EndPosition, self.moveRobot) 
        self.move_group = moveit_commander.MoveGroupCommander('manipulator')
        self.waitPosition()

    def waitPosition(self):

        print("Move to wait position")
        joint_goal = self.move_group.get_current_joint_values()

        joint_goal[0] = math.radians(90) 
        joint_goal[1] = math.radians(-90)
        joint_goal[2] = math.radians(90)
        joint_goal[3] = math.radians(-132) 
        joint_goal[4] = math.radians(-90) 
        joint_goal[5] = math.radians(0) 
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

    
    def readyPosition(self):
        print("Move to ready position")
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[0] = math.radians(0);       
        joint_goal[1] = math.radians(-61.58);  
        joint_goal[2] = math.radians(104.42);  
        joint_goal[3] = math.radians(-132.84); 
        joint_goal[4] = math.radians(-90);     
        joint_goal[5] = math.radians(0);      
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

        self.moveVertical(0.3)

    def moveRobot(self,data):
        print(data)
        self.readyPosition()
        self.moveToDesiredPosition(data.xStart,data.yStart,data.zStart)
        self.moveToContainer(data.containerName)

    def moveToDesiredPosition(self,x,y,z):
        # Move on top of the object
        print('Move on top of object')
        curPose = self.move_group.get_current_pose().pose
        curPose.position.x = x-0.8
        curPose.position.y = y
        self.move_group.set_pose_target(curPose)
        self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()

        # Make the EE point down
        print('Move gripper vertical')
        joint_goal = self.move_group.get_current_joint_values()
        joint_goal[4] = math.radians(-90) 
        self.move_group.go(joint_goal, wait=True)
        self.move_group.stop()

        # Go down and pick it up
        print("Move down and pick object")
        self.moveVertical(z)
        rospy.ServiceProxy('/ur5e_epick/epick/on', Empty)()

        # Move back up again
        print('Move back up')
        self.moveVertical(0.3)

    def moveVertical(self,height):
        curPose = self.move_group.get_current_pose().pose
        curPose.position.z = height
        self.move_group.set_pose_target(curPose)
        self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()


    def moveToContainer(self,container):
        print("Move to container")
        if container == 'Container 1':

            joint_goal = self.move_group.get_current_joint_values()
            joint_goal[0] = math.radians(-110) 
            self.move_group.go(joint_goal, wait=True)
            self.move_group.stop()

            curPose = self.move_group.get_current_pose().pose
            curPose.position.y = -0.5

        else:
            joint_goal = self.move_group.get_current_joint_values()
            joint_goal[0] = math.radians(90) 
            self.move_group.go(joint_goal, wait=True)
            self.move_group.stop()

            curPose = self.move_group.get_current_pose().pose
            curPose.position.y = 0.8

        self.move_group.set_pose_target(curPose)
        self.move_group.go(wait=True)
        self.move_group.stop()
        self.move_group.clear_pose_targets()
        rospy.ServiceProxy('/ur5e_epick/epick/off', Empty)()


if __name__ == '__main__':
    rospy.init_node('robot_controller')
    robotController = robotControl()
    rospy.spin()