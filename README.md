# Requirement 
	run in ubunutu 20.04
	python 3.8
	install flask and sklearn
	install ros noetic
	install moveIt:
sudo apt install ros-noetic-moveit
sudo apt-get install ros-noetic-joint-trajectory-controller



# make src folder
```bash
mkdir -p ~/ROS_workspaces/vnbots_ws/src
```

# clone the git repo 
# run these to apply links 
```bash
cd ~/ROS_workspaces/vnbots_ws/src
ln -s your dir/vnbots_gazebo .
ln -s your dir/ur5e_epick_moveit_config .
ln -s your dir/ur_description .
ln -s your dir/ur_kinematics .
```

# to build & run
```bash
cd ~/ROS_workspaces/vnbots_ws
catkin_make
source devel/setup.bash

run in order

run the gazebo in different terminal with source devel/setup.bash 
roslaunch vnbots_gazebo demo.launch

run robot control in different terminal with source devel/setup.bash
rosrun vnbots_gazebo robotControl.py

spawn object into gazebo in different terminal with source devel/setup.bash
rosrun vnbots_gazebo spawn_object.py

run camera sever in different terminal with source devel/setup.bash
rosrun vnbots_gazebo sever.py

run website in different terminal with source devel/setup.bash
python3 /your dir/cameraprocessing/app.py 

```
