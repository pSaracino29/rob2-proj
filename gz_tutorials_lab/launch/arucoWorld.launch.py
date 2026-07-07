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

    sdf_file_path = os.path.join(
        get_package_share_directory('gz_tutorials_lab'),
        'sdf_ws',
        'joint_pub.sdf'
    )

    file_sdf_model = os.path.join(
         get_package_share_directory('gz_tutorials_lab'),
         'worlds',
         'mondoProva.world'
    )

    with open(sdf_file_path, 'r') as f:
        robot_description = f.read()

    with open(file_sdf_model, 'r') as f:
        simple_model_description = f.read()

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path],
        remappings=[
            ('/tf', '/tf_ros_mapped'),
            ('/tf_static', '/tf_static_ros_mapped'),
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

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={
                'gz_args': ['-r ', os.path.join(pkg_share, 'worlds', 'mondoProva.world')],
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
                '/model/blueCar/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                '/joint_states@sensor_msgs/msg/JointState@gz.msgs.Model',
                #'/model/vehicle_blue/pose@geometry_msgs/msg/PoseArray@gz.msgs.Pose_V'
            ],
            remappings=[
                ('/camera/camera_info', '/camera_info_ros_mapped'),
                ('/camera/image', '/camera_image_ros_mapped'),
                ('/cmd_vel', '/cmd_vel_ros_mapped'),
                ('/imu', '/imu_ros_mapped'),
                ('/lidar', '/lidar_ros_mapped'),
                ('/model/blueCar/tf', '/tf_ros_mapped'),
                ('/model/blueCar/pose', '/pose_ros_mapped'),
                ('/joint_states', '/joint_states_ros_mapped')
            ],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'robot_description': simple_model_description
            }]
        ),

        Node(
            package='gz_tutorials_lab',
            executable='odom_tf_broadcaster',
            output='screen',
            parameters=[{
                'use_sim_time': True
            }]
        ),
    
    auto_drive_node,
    rviz_node

    ])