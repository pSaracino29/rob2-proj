#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class AutoDrive(Node):
    def __init__(self):
        super().__init__('auto_drive')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel_ros_mapped', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5  # Move forward at 0.5 m/s
        msg.angular.z = 0.0  # Rotate at 0.1 rad/s
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = AutoDrive()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)  # Stop the robot
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()