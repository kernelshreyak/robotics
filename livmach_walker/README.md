# LivMach Walker

Webots quadruped walker with a single local keyboard controller.

## Overview

The project now uses one controller only:

- [controllers/livmach_walker/livmach_walker.py](/home/shreyak/programming/robotics/livmach_walker/controllers/livmach_walker/livmach_walker.py): keyboard-controlled quadruped gait controller
- [worlds/livmach_walker.wbt](/home/shreyak/programming/robotics/livmach_walker/worlds/livmach_walker.wbt): 4-legged Webots world and robot definition

The older external TCP bridge and Ollama-based controller were removed. The current setup is intentionally simpler: open the world in Webots and drive the robot directly with arrow keys.

## Controls

- `Up`: move forward
- `Down`: move backward
- `Left`: turn left
- `Right`: turn right
- `Space`: stand still / settle

## Running

From this project directory:

```bash
webots worlds/livmach_walker.wbt
```

Inside Webots, make sure the robot controller is `livmach_walker`, then start or reset the simulation.

## Current Design

- 4 legs with one hinge joint per leg
- front feet point forward
- rear feet point backward
- simple crawl-style gait
- IMU-based pitch and roll stabilization in the controller
- no external processes required

## Files

- [worlds/livmach_walker.wbt](/home/shreyak/programming/robotics/livmach_walker/worlds/livmach_walker.wbt): arena and robot body/joint geometry
- [controllers/livmach_walker/livmach_walker.py](/home/shreyak/programming/robotics/livmach_walker/controllers/livmach_walker/livmach_walker.py): gait logic, keyboard input, stabilization
- [docs/controller-explainer.md](/home/shreyak/programming/robotics/livmach_walker/docs/controller-explainer.md): more detailed explanation of how the controller works

## Notes

- If the robot behaves unexpectedly after edits, reset the world in Webots so the controller and world changes are reloaded.
- If forward and backward behavior diverge, check the gait phase logic in `livmach_walker.py`.
- If the robot tips, tune stance angles, gait amplitude, or stabilization gains before changing the whole structure.

## Current Limitations

- The robot uses one hinge joint per leg, so the gait is necessarily simple.
- Walking is procedural, not dynamically optimized, so stability still depends heavily on geometry and tuning.
- Turning works by gait bias rather than a dedicated steering model, so it may be coarse.
- The controller is best treated as a compact experimental baseline, not a finished locomotion stack.
