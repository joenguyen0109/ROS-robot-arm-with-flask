# Introduction
This is the project for MTRN4230 in UNSW. Control robot arm through a web interface and ROS with a machine learning algorithm to classify objects. 

![grab-landing-page](https://github.com/joenguyen0109/ROS-robot-arm-with-flask/blob/main/gif.gif)
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
Install tutorial: https://www.youtube.com/watch?v=sNZTlIOxwEo

Clone the repo then setup repo
```bash
mkdir -p ~/ROS_workspaces/vnbots_ws/src
cd ~/ROS_workspaces/vnbots_ws/src
git clone link
```

# build & run
```bash
cd ~/ROS_workspaces/vnbots_ws
catkin_make
source devel/setup.bash
```
run each command in seperate termnial with  
cd ~/ROS_workspaces/vnbots_ws  
source devel/setup.bash  



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
rosrun vnbots_gazebo spawn_object.py
```
Run camera server
```bash
rosrun vnbots_gazebo sever.py
```
Run flask website
```bash
cd ~/ROS_workspaces/vnbots_ws/src/ROS-robot-arm-with-flask/camera_processing
python3 app.py 
```
