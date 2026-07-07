import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_ros_gz_sim = FindPackageShare('ros_gz_sim')
    ros_gz_sim_pkg_path = get_package_share_directory('ros_gz_sim')
    example_pkg_path = FindPackageShare('gz_tutorials_lab')
    gz_launch_path = PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
    pkg_share = get_package_share_directory('gz_tutorials_lab')
    rviz_config_path = os.path.join(pkg_share, 'rviz_ws', 'primaConf_tf.rviz')

    models_path = os.path.join(pkg_share, 'models')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        remappings=[
            ('/tf', '/tf_ros_mapped'),
            ('/tf_static', '/tf_static_ros_mapped'),
            #('/model/vehicle_blue/pose', '/pose_ros_mapped')
            
        ]
    )

    auto_drive_node = Node(
        package='gz_tutorials_lab',
        executable='auto_drive',
        name='auto_drive',
        output='screen'
    )

    return LaunchDescription([
        
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            models_path
        ),

        SetEnvironmentVariable(
            'GZ_SIM_PLUGIN_PATH',
            PathJoinSubstitution([example_pkg_path, 'plugins'])
        ),

        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(gz_launch_path),
        #     launch_arguments={
        #         #'gz_args': ['-r', ' ',PathJoinSubstitution([example_pkg_path, 'sdf_ws/buildingRobot.sdf'])],
        #         'gz_args': ['-r', ' ', PathJoinSubstitution([example_pkg_path, 'worlds', 'arucoWorld.world'])],
        #         'on_exit_shutdown': 'True'
        #     }.items(),
        # ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': ['-r ', os.path.join(pkg_share, 'sdf_ws', 'buildingRobot.sdf')],
                'on_exit_shutdown': 'True'
            }.items(),
        
        ),

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
                '/camera/image@sensor_msgs/msg/Image@gz.msgs.Image',
                '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                '/imu@sensor_msgs/msg/Imu@gz.msgs.IMU',
                '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                '/model/vehicle_blue/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                #'/model/vehicle_blue/pose@geometry_msgs/msg/PoseArray@gz.msgs.Pose_V'
            ],
            remappings=[
                ('/camera/camera_info', '/camera_info_ros_mapped'),
                ('/camera/image', '/camera_image_ros_mapped'),
                ('/cmd_vel', '/cmd_vel_ros_mapped'),
                ('/imu', '/imu_ros_mapped'),
                ('/lidar', '/lidar_ros_mapped'),
                ('/model/vehicle_blue/tf', '/tf_ros_mapped'),
                ('/model/vehicle_blue/pose', '/pose_ros_mapped')
            ],
            output='screen'
        ),

        # 2. Inseriamo la variabile del nodo dentro la lista di return
        auto_drive_node,
        rviz_node
    ])