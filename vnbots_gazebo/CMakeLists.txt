cmake_minimum_required(VERSION 3.0.2)
project(vnbots_gazebo)

add_compile_options(-std=c++17)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(catkin REQUIRED COMPONENTS
      roscpp
      rospy
      moveit_core
      moveit_ros_planning
      moveit_ros_planning_interface
      roslaunch
      message_generation
)

add_service_files(
  FILES
  EndPosition.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

# Perform checks on launch files too
roslaunch_add_file_check(launch)

catkin_package(
  LIBRARIES
  INCLUDE_DIRS
  CATKIN_DEPENDS
      moveit_core
      moveit_ros_planning_interface
  DEPENDS message_runtime
      
)

###########
## Build ##
###########

include_directories(${catkin_INCLUDE_DIRS} ${Boost_INCLUDE_DIR} ${EIGEN3_INCLUDE_DIRS})




catkin_install_python(PROGRAMS scripts/robotControl.py scripts/spawn_object.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)