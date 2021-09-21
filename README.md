# Introduction
This is the project for MTRN4230 in UNSW. Control robot arm through a web interface with a machine learning algorithm to classify objects.
# Requirement 
run in ubunutu 20.04 or WSL2 on window
(not recommend run in virtualbox)

python 3.8

install flask and sklearn

install ros noetic http://wiki.ros.org/noetic/Installation/Ubuntu

	install moveIt:

	sudo apt install ros-noetic-moveit
	sudo apt-get install ros-noetic-joint-trajectory-controller



# Setup 
Clone the repo then setup and link git repo
```bash
mkdir -p ~/ROS_workspaces/vnbots_ws/src

cd ~/ROS_workspaces/vnbots_ws/src
ln -s gitRepo/vnbots_gazebo .
ln -s gitRepo/ur5e_epick_moveit_config .
ln -s gitRepo/ur_description .
ln -s gitRepo/ur_kinematics .
```

# build & run
run each command in seperate termnial with source devel/setup.bash
```bash
cd ~/ROS_workspaces/vnbots_ws
catkin_make
source devel/setup.bash
```
Run gazebo simulation
```bash
roslaunch vnbots_gazebo demo.launch
```
Run robot control
```bash
rosrun vnbots_gazebo robotControl.py
```
Spawn object in gazebo world
```bash
cd ~/ROS_workspaces/vnbots_ws
rosrun vnbots_gazebo spawn_object.py
```
Run camera server
```bash
rosrun vnbots_gazebo sever.py
```
Run flask website
```bash
python3 ~/ROS_workspaces/vnbots_ws/src/camera_processing/app.py 
```
