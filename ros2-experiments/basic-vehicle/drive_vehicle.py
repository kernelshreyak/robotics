#!/usr/bin/env python3

import argparse
import select
import sys
import termios
import tty

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


INSTRUCTIONS = """
Keyboard control:
  w: increase forward speed
  s: increase reverse speed
  a: increase left turn rate
  d: increase right turn rate
  x or space: stop
  q: quit
"""


class KeyboardTeleop(Node):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__("basic_vehicle_teleop")
        self.publisher = self.create_publisher(Twist, args.topic, 10)
        self.linear_step = args.linear_step
        self.angular_step = args.angular_step
        self.max_linear = args.max_linear
        self.max_angular = args.max_angular
        self.linear = 0.0
        self.angular = 0.0
        self.create_timer(0.1, self.publish_command)
        self.get_logger().info(f"Publishing Twist commands on {args.topic}")

    def clamp(self, value: float, limit: float) -> float:
        return max(-limit, min(limit, value))

    def handle_key(self, key: str) -> bool:
        if key == "w":
            self.linear = self.clamp(self.linear + self.linear_step, self.max_linear)
        elif key == "s":
            self.linear = self.clamp(self.linear - self.linear_step, self.max_linear)
        elif key == "a":
            self.angular = self.clamp(self.angular + self.angular_step, self.max_angular)
        elif key == "d":
            self.angular = self.clamp(self.angular - self.angular_step, self.max_angular)
        elif key in {"x", " "}:
            self.linear = 0.0
            self.angular = 0.0
        elif key == "q":
            self.linear = 0.0
            self.angular = 0.0
            self.publish_command()
            return False
        else:
            return True

        self.get_logger().info(
            f"linear={self.linear:.2f} m/s angular={self.angular:.2f} rad/s"
        )
        return True

    def publish_command(self) -> None:
        msg = Twist()
        msg.linear.x = self.linear
        msg.angular.z = self.angular
        self.publisher.publish(msg)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Keyboard teleop for the Gazebo basic vehicle")
    parser.add_argument("--topic", default="/cmd_vel", help="ROS 2 topic to publish Twist commands on")
    parser.add_argument("--linear-step", type=float, default=0.15, help="Linear speed increment in m/s")
    parser.add_argument("--angular-step", type=float, default=0.25, help="Angular speed increment in rad/s")
    parser.add_argument("--max-linear", type=float, default=1.2, help="Maximum linear speed in m/s")
    parser.add_argument("--max-angular", type=float, default=2.0, help="Maximum angular speed in rad/s")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rclpy.init()
    node = KeyboardTeleop(args)
    print(INSTRUCTIONS)

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        running = True
        while running and rclpy.ok():
            rclpy.spin_once(node, timeout_sec=0.1)
            ready, _, _ = select.select([sys.stdin], [], [], 0.0)
            if ready:
                key = sys.stdin.read(1).lower()
                running = node.handle_key(key)
    finally:
        stop_msg = Twist()
        node.publisher.publish(stop_msg)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
