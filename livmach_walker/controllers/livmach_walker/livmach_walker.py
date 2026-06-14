"""
LivMach quadruped keyboard controller.

Single-controller setup. Attach this controller to the robot in Webots and use:
  Up: move forward
  Down: move backward
  Left: turn left
  Right: turn right
  Space: stand still
"""

from __future__ import annotations

import math

from controller import Keyboard, Robot

NEUTRAL_STANCE = {
    "front_left": 0.55,
    "front_right": 0.55,
    "rear_left": -0.55,
    "rear_right": -0.55,
}

MIN_ANGLE = -1.2
MAX_ANGLE = 1.2
MAX_MOTOR_VELOCITY = 7.0

FORWARD_AMPLITUDE = 0.6
TURN_AMPLITUDE = 0.7
GAIT_HZ = 1.1
STANCE_RETURN_RATE = 0.10
PITCH_GAIN = 0.45
ROLL_GAIN = 0.24
LOG_EVERY_STEPS = 40

LEG_ORDER = ("front_left", "front_right", "rear_left", "rear_right")
CRAWL_PHASE = {
    "front_left": 0.0,
    "rear_right": math.pi / 2.0,
    "front_right": math.pi,
    "rear_left": 3.0 * math.pi / 2.0,
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


robot = Robot()
timestep = int(robot.getBasicTimeStep())

keyboard = Keyboard()
keyboard.enable(timestep)

motors = {
    "front_left": robot.getDevice("front_left_leg_motor"),
    "front_right": robot.getDevice("front_right_leg_motor"),
    "rear_left": robot.getDevice("rear_left_leg_motor"),
    "rear_right": robot.getDevice("rear_right_leg_motor"),
}
sensors = {
    "front_left": robot.getDevice("front_left_leg_sensor"),
    "front_right": robot.getDevice("front_right_leg_sensor"),
    "rear_left": robot.getDevice("rear_left_leg_sensor"),
    "rear_right": robot.getDevice("rear_right_leg_sensor"),
}
imu = robot.getDevice("imu")

for sensor in sensors.values():
    sensor.enable(timestep)

imu.enable(timestep)

for leg_name, motor in motors.items():
    motor.setVelocity(MAX_MOTOR_VELOCITY)
    motor.setPosition(NEUTRAL_STANCE[leg_name])

print("LivMach quadruped controller ready.")
print("  Up/Down: forward/backward")
print("  Left/Right: turn left/right")
print("  Space: stand still")

targets = dict(NEUTRAL_STANCE)
phase = 0.0
step_count = 0
last_mode = "idle"


def gather_keys() -> set[int]:
    pressed: set[int] = set()
    while True:
        key = keyboard.getKey()
        if key == -1:
            return pressed
        pressed.add(key)


def resolve_motion(pressed: set[int]) -> tuple[int, int, bool]:
    forward = 0
    turn = 0
    hold_still = ord(" ") in pressed

    if Keyboard.UP in pressed and Keyboard.DOWN not in pressed:
        forward = 1
    elif Keyboard.DOWN in pressed and Keyboard.UP not in pressed:
        forward = -1

    if Keyboard.LEFT in pressed and Keyboard.RIGHT not in pressed:
        turn = -1
    elif Keyboard.RIGHT in pressed and Keyboard.LEFT not in pressed:
        turn = 1

    return forward, turn, hold_still


def stabilization_offsets() -> dict[str, float]:
    roll, pitch, _ = imu.getRollPitchYaw()
    # Pitch pushes the front and rear legs in opposite directions to keep the torso level.
    front_bias = -pitch * PITCH_GAIN
    rear_bias = pitch * PITCH_GAIN
    # Roll uses the same idea, but across left vs right legs.
    left_bias = -roll * ROLL_GAIN
    right_bias = roll * ROLL_GAIN
    return {
        "front_left": front_bias + left_bias,
        "front_right": front_bias + right_bias,
        "rear_left": rear_bias + left_bias,
        "rear_right": rear_bias + right_bias,
    }


while robot.step(timestep) != -1:
    step_count += 1
    pressed = gather_keys()
    forward_cmd, turn_cmd, hold_still = resolve_motion(pressed)
    offsets = stabilization_offsets()

    if hold_still or (forward_cmd == 0 and turn_cmd == 0):
        # Relax back toward the current stabilized stance instead of snapping to zero.
        for leg_name in LEG_ORDER:
            neutral = NEUTRAL_STANCE[leg_name] + offsets[leg_name]
            targets[leg_name] += (neutral - targets[leg_name]) * STANCE_RETURN_RATE
        mode = "idle" if not hold_still else "stand"
    else:
        # Reverse the phase progression for backward motion so the crawl pattern actually runs in reverse.
        phase += 2.0 * math.pi * GAIT_HZ * (timestep / 1000.0)
        phase_direction = 1.0 if forward_cmd >= 0 else -1.0
        for leg_name in LEG_ORDER:
            wave = math.sin(phase_direction * phase + CRAWL_PHASE[leg_name])
            stride = forward_cmd * FORWARD_AMPLITUDE * wave

            # Turning is implemented as a side-dependent bias on top of the crawl stride.
            if turn_cmd < 0:
                if "left" in leg_name:
                    turn_bias = -TURN_AMPLITUDE * abs(wave)
                else:
                    turn_bias = TURN_AMPLITUDE * abs(wave)
            elif turn_cmd > 0:
                if "right" in leg_name:
                    turn_bias = -TURN_AMPLITUDE * abs(wave)
                else:
                    turn_bias = TURN_AMPLITUDE * abs(wave)
            else:
                turn_bias = 0.0

            targets[leg_name] = clamp(
                NEUTRAL_STANCE[leg_name] + stride + turn_bias + offsets[leg_name],
                MIN_ANGLE,
                MAX_ANGLE,
            )

        if forward_cmd > 0 and turn_cmd == 0:
            mode = "forward"
        elif forward_cmd < 0 and turn_cmd == 0:
            mode = "backward"
        elif forward_cmd == 0 and turn_cmd < 0:
            mode = "turn-left"
        elif forward_cmd == 0 and turn_cmd > 0:
            mode = "turn-right"
        elif forward_cmd > 0 and turn_cmd < 0:
            mode = "forward-left"
        elif forward_cmd > 0 and turn_cmd > 0:
            mode = "forward-right"
        elif forward_cmd < 0 and turn_cmd < 0:
            mode = "backward-left"
        else:
            mode = "backward-right"

    if mode != last_mode:
        print(f"MODE {mode}")
        last_mode = mode

    # Apply the final target to each joint; Webots handles the interpolation.
    for leg_name, motor in motors.items():
        motor.setPosition(clamp(targets[leg_name], MIN_ANGLE, MAX_ANGLE))

    if step_count % LOG_EVERY_STEPS == 0:
        legs_text = ", ".join(f"{name}={sensors[name].getValue():+.3f}" for name in LEG_ORDER)
        print(f"GAIT mode={mode} {legs_text}")
