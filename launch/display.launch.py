#! /usr/bin/env python3
import xacro
from os.path import join
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument, TimerAction, LogInfo
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration, Command, PythonExpression
from launch.conditions import IfCondition
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    
    xacro_file=get_package_share_directory('mr_robot_description')+'/urdf/mr_robot_description.xacro'
    bridge_config=get_package_share_directory('mr_robot_description')+ '/config/bridge.yaml'
    rviz_config=get_package_share_directory("mr_robot_description")+"/config/display.rviz"
    #publishing robot_state into topic robot_description
    
    # Purpose converts the URDF/XACRO description into a ros topic /robot_description
    # Working :- uses the xacro to process the mr_robot_description.xacro , publishees the kinematic structure for TF and other nodes 
    # creates anode that publishes the state of the robot fot thr ros2 
    robot_state=Node(
                    package = 'robot_state_publisher',
                    executable = 'robot_state_publisher',  
                    name='robot_state_publisher',                    # for the system reference 
                    parameters = [{'robot_description': ParameterValue(   # pramater vslue os created dynamically by parameter value to wrap the description 
                                  Command(['xacro ', xacro_file,       # xacro to the URDF
                                # ' kinect_enabled:=', "true",
                                # ' lidar_enabled:=', "true",           # They allow you to enable/disable parts of the robot model without modifying the Xacro file directly.
                                # ' camera_enabled:=', camera_enabled,
                                 # basically it is the dynamic configs 
                                # works k=like this 
                                # <xacro:if value="${lidar_enabled}">
                                #     <!-- LiDAR sensor is included in URDF -->
                                #     <xacro:include filename="lidar_sensor.xacro" />
                                # </xacro:if>
                                ]),
                                value_type=str)}]   # cz it ts the lomg urdf file to make sure ros node process ti as the srting 
                            )
    
    joint_state=Node(
                package = 'joint_state_publisher',
                executable = 'joint_state_publisher',  
                name='joint_state_publisher',                    # for the system reference 
        
                        )
    
    #spawn mr_robot using the topic "/mr_robot_description" in the gazebo 
    robot_spawn=Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',    # prints the logs on the screen 
        arguments=[
                    '-name', 'mr_robot',    # name in the gazebo 
                    '-topic', '/robot_description',   # specifies the topic where to get the robot description 
                    "-allow_renaming", "true",
                    '-x', '0.0',  # Set the initial X position
                    '-y', '0.0',  # Set the initial Y position
                    '-z', '0.0' ,  # Set the initial Z position
                    '-Y', '0.0'   # Set the initial Z position
                    # '-x', '2.0',  # Set the initial X position
                    # '-y', '0.0',  # Set the initial Y position
                    # '-z', '0.0' ,  # Set the initial Z position
                    # '-Y', '-1.57'   # Set the initial Z position
    ]
    )

    # parameter bridge node to bridge different gz and tos 2 topics   ros_gz bridge 
    ros_gz_bridge = Node(
                package="ros_gz_bridge", 
                executable="parameter_bridge",
                parameters = [
                    {'config_file': bridge_config}],    # config_file is the key that points toh the file 
                # condition=IfCondition(with_bridge)
                )
    
    # launch rviz node if rviz parameter was set to true  but now not if launches bcz with_rviz is commented 
    rviz = Node(package='rviz2',
                executable='rviz2',
                name='rviz',
    			output='screen',
                arguments=['-d' + rviz_config],
                # condition=IfCondition(with_rviz)
                )
    
    # map_stf = Node(package="tf2_ros",
    #                executable="static_transform_publisher",
    #                arguments=["0","0","0","0.0","0.0","0.0","map","odom"])
    
    arg_use_sim_time = DeclareLaunchArgument('use_sim_time',    # usesimtime is thr ros define pram
											default_value='true',
											description="Enable sim time from /clock")
    
    return LaunchDescription([
        robot_state,
        robot_spawn,
        arg_use_sim_time,
        ros_gz_bridge,
        rviz,
        joint_state,
        # map_stf
        # arg_with_bridge
    ])