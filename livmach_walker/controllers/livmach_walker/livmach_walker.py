"""
LivMach walker Webots controller.

Streams IMU + leg state over TCP each step and applies leg commands received
from the external Python app. Keyboard trim still works as a local fallback.

TCP binary protocol: livmach_walker/bridge/protocol.py
Default port: 5555 (override via controllerArgs in the world file).
"""

from __future__ import annotations

import sys
from pathlib import Path

from controller import Keyboard, Robot

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bridge.tcp_link import SimulationTcpServer

NEUTRAL_ANGLE = 0.0
ANGLE_STEP = 0.05
MIN_ANGLE = -1.5
MAX_ANGLE = 1.5
DEFAULT_PORT = 5555


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_port() -> int:
    if len(sys.argv) > 1:
        return int(sys.argv[1])
    return DEFAULT_PORT


robot = Robot()
timestep = int(robot.getBasicTimeStep())
port = parse_port()

left_motor = robot.getDevice("left_leg_motor")
right_motor = robot.getDevice("right_leg_motor")
left_sensor = robot.getDevice("left_leg_sensor")
right_sensor = robot.getDevice("right_leg_sensor")
imu = robot.getDevice("imu")
accelerometer = robot.getDevice("accelerometer")
gyro = robot.getDevice("gyro")

for sensor in (left_sensor, right_sensor):
    sensor.enable(timestep)

imu.enable(timestep)
accelerometer.enable(timestep)
gyro.enable(timestep)

keyboard = Keyboard()
keyboard.enable(timestep)

bridge = SimulationTcpServer(port=port)

left_target = NEUTRAL_ANGLE
right_target = NEUTRAL_ANGLE

for motor in (left_motor, right_motor):
    motor.setPosition(NEUTRAL_ANGLE)

print("LivMach walker controller ready.")
print(f"  TCP bridge on 127.0.0.1:{port}")
print("  Run: python livmach_walker/external_app.py")
print("  Keyboard fallback: UP/DOWN both legs, LEFT/RIGHT single leg, R reset")

last_status = None

while robot.step(timestep) != -1:
    status = bridge.status_message()
    if status and status != last_status:
        print(status)
        last_status = status

    key = keyboard.getKey()
    if key == ord("R"):
        left_target = NEUTRAL_ANGLE
        right_target = NEUTRAL_ANGLE
    elif key == Keyboard.UP:
        left_target += ANGLE_STEP
        right_target += ANGLE_STEP
    elif key == Keyboard.DOWN:
        left_target -= ANGLE_STEP
        right_target -= ANGLE_STEP
    elif key == Keyboard.LEFT:
        left_target -= ANGLE_STEP
    elif key == Keyboard.RIGHT:
        right_target += ANGLE_STEP

    remote_cmd = bridge.poll()
    if remote_cmd is not None:
        left_target, right_target = remote_cmd

    left_target = clamp(left_target, MIN_ANGLE, MAX_ANGLE)
    right_target = clamp(right_target, MIN_ANGLE, MAX_ANGLE)

    left_motor.setPosition(left_target)
    right_motor.setPosition(right_target)

    roll, pitch, yaw = imu.getRollPitchYaw()
    ax, ay, az = accelerometer.getValues()
    gx, gy, gz = gyro.getValues()

    bridge.send_imu(
        time_s=robot.getTime(),
        roll=roll,
        pitch=pitch,
        yaw=yaw,
        ax=ax,
        ay=ay,
        az=az,
        gx=gx,
        gy=gy,
        gz=gz,
        left_leg=left_sensor.getValue(),
        right_leg=right_sensor.getValue(),
    )

bridge.close()
