#! /usr/bin/env python3   # execurte it using the python 3 interpreter
import xacro     #  For processing Xacro (XML Macros) robot description files
# ROS 2 launch system components for creating launch descriptions
# Utilities for finding package directories and handling launch configurations

import os
# from os.path import join
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
# The get_package_share_directory function, part of the ament_index_cpp library, is used in ROS 2 to locate 
# the share directory of a given package. This function efficiently helps you find the directory containing 
# resources like configuration files, scripts, and other assets associated with a specific ROS 2 package. 
from launch.substitutions import LaunchConfiguration, Command, PythonExpression
from launch.conditions import IfCondition
from launch_ros.descriptions import ParameterValue
# this function is the entry point for the ros2 launch files 
# it must contain the launch description so like it execute all the nodes 

def generate_launch_description():
    # Declares a runtime-configurable parameter named with_bridge.
    # Allows dynamically passing values (e.g., true/false) when launching the file.
    with_bridge = LaunchConfiguration('with_bridge')
    
    #  argument to specify if bridge needs to be launched
    arg_with_bridge = DeclareLaunchArgument('with_bridge', 
                                            default_value='true',
                                            description="Set true to bridge ROS 2 & Gz topics")
                                            
                                            
    #path to xacro file
    # get_package_share_directory() is crucial for finding resources regardless of where the package is installed
    pkg_mr_robot_desc=get_package_share_directory("mr_robot_description")
    world_path= get_package_share_directory("mr_robot_description")+"/worlds/world.sdf"
    
    print(f"{pkg_mr_robot_desc}")  # outputs /home/dev/BOT/Mr_robot./install/mr_robot_description/share/mr_robot_description
    print(f"{world_path}")        # /home/dev/BOT/Mr_robot./install/mr_robot_description/share/mr_robot_description/worlds/world.sdf
    print(f"{with_bridge}")  # outputs <launch.substitutions.launch_configuration.LaunchConfiguration object at 0x77861992cf10>

        
    # Include the gazebo.launch.py file
    gazebo=IncludeLaunchDescription(
        # ros_gz_sim includes the gazebo sim launch file 
                # ros2 launch ros_gz_sim gz_sim.launch.py
                PythonLaunchDescriptionSource([get_package_share_directory('ros_gz_sim'), '/launch/gz_sim.launch.py']),
                    launch_arguments={
                        'gz_args' : [world_path + " -v 4"] , 
                        'on_exit_shutdown' : 'true',
                    }.items()
        )
      
    # spawn robot with rviz
    robot = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    # get_package_share_directory('mr_robot_description'),
                    # '/launch',
                    # '/display.launch.py'
                    os.path.join(pkg_mr_robot_desc, 'launch', 'display.launch.py')
                    # (f"{pkg_mr_robot_desc}/launch/display.launch.py)
                    ]),
                    launch_arguments={
                        'rviz': 'true',
                        'with_bridge': 'true'
                    }.items()
            )
    
     
    return LaunchDescription([
        gazebo,
        robot,
    ])

