# Controller Explainer

This document explains the current `LivMach Walker` setup in practical terms.

## What Exists

The project is a Webots quadruped with:

- one rigid torso
- four single-joint legs
- one Python controller
- direct keyboard control

There is no external app, no TCP bridge, and no model-in-the-loop control path.

## Main Files

- [controllers/livmach_walker/livmach_walker.py](/home/shreyak/programming/robotics/livmach_walker/controllers/livmach_walker/livmach_walker.py)
- [worlds/livmach_walker.wbt](/home/shreyak/programming/robotics/livmach_walker/worlds/livmach_walker.wbt)
- [README.md](/home/shreyak/programming/robotics/livmach_walker/README.md)

## Controller Structure

The controller does four jobs:

1. Reads keyboard input from Webots.
2. Converts that input into `forward`, `turn`, or `stand` intent.
3. Computes target joint angles for all four legs.
4. Applies simple IMU-based stabilization using roll and pitch.

## Key Concepts

The controller is easiest to understand if you separate three layers:

- `stance`: the baseline joint angles that keep the body off the floor
- `stride`: the periodic motion that creates walking
- `stabilization`: small corrections from the IMU that keep the torso level

Those layers are combined each step before sending the final motor targets.

## Gait Model

The gait is intentionally simple.

- Each leg has one phase offset.
- The controller advances a shared gait phase over time.
- Each leg uses `sin(...)` of that phase to create a repeating stride.
- Forward/backward comes from stride direction.
- Left/right turning comes from adding side-dependent bias.

This is not a full dynamic walking controller. It is a lightweight procedural gait.

Backward motion is not a separate gait. The controller reverses the phase progression, which makes the same crawl pattern run in the opposite direction.

Turning is also not a separate steering system. It is a bias added on top of the crawl so one side loads differently from the other.

## Stabilization

The controller reads `imu.getRollPitchYaw()` and uses:

- pitch to bias front vs rear legs
- roll to bias left vs right legs

That helps the robot resist tipping without adding more joints or a more complex balance controller.

The stabilization is intentionally small. Its job is not to stand the robot up by itself. Its job is to nudge the stance toward level while the gait is running.

## Why The World Geometry Matters

The world file defines whether the gait has any chance to work.

Important details:

- leg anchor positions
- foot size
- foot direction
- body height above ground
- friction material
- torso collision shape

If these are wrong, the controller can be logically correct and the robot will still just tip or drag.

In this project, the world geometry and the controller are designed together. The stance angles in code assume the leg anchors, foot direction, and friction setup from the world file.

## Keyboard Commands

- `Up`: forward
- `Down`: backward
- `Left`: turn left
- `Right`: turn right
- `Space`: stand still

## Common Tuning Points

In [controllers/livmach_walker/livmach_walker.py](/home/shreyak/programming/robotics/livmach_walker/controllers/livmach_walker/livmach_walker.py), the main tuning constants are:

- `NEUTRAL_STANCE`
- `FORWARD_AMPLITUDE`
- `TURN_AMPLITUDE`
- `GAIT_HZ`
- `PITCH_GAIN`
- `ROLL_GAIN`

Practical effect of the main constants:

- `NEUTRAL_STANCE` moves the default body pose.
- `FORWARD_AMPLITUDE` changes how far each stride swings.
- `TURN_AMPLITUDE` changes how strongly the robot biases left or right.
- `GAIT_HZ` changes how quickly the crawl repeats.
- `PITCH_GAIN` and `ROLL_GAIN` change how aggressively the robot corrects lean.

In [worlds/livmach_walker.wbt](/home/shreyak/programming/robotics/livmach_walker/worlds/livmach_walker.wbt), the main physical tuning points are:

- joint anchor positions
- foot dimensions
- robot spawn height
- friction values
- body mass and leg mass

## When To Change What

- If keys work but motion is weak: tune gait amplitude or gait frequency.
- If motion happens in the wrong direction: tune phase order or sign.
- If the robot tips forward/backward: tune stance, pitch gain, or foot placement.
- If turning does nothing: tune `TURN_AMPLITUDE`.
- If the robot drags badly: inspect foot geometry and collision placement in the world.

## Read This First

If you only remember three things, remember these:

1. The controller is a crawl, not a trot.
2. Backward motion is phase reversal, not a separate mirrored machine.
3. Small physical geometry changes in the world file can matter more than big code changes.
