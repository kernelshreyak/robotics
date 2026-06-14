# Robotics Project Portfolio

A collection of robotics experiments spanning Webots, CoppeliaSim, embedded control, industrial IoT, CAD, and circuit simulation. Most directories are independent projects, so you can work inside one subsystem without pulling in the rest of the repository.

## Repository Layout

| Path | Contents |
| ---- | -------- |
| `livmach_walker/` | Webots quadruped walker with a local keyboard controller and IMU-based stabilization. |
| `turret_simulation/` | Webots project for a manually driven turret with custom PROTO and shared tripod assets. |
| `turret_targeting_system/` | Arduino manual turret pan controller driven by left/right buttons and a Servo motor. |
| `shooter_mechanism/` | Webots arena for a dual-wheel shooter plus its controller sources and build outputs. |
| `conveyor_belt/` | Webots conveyor demos, package handling controllers, and supporting assets. |
| `sorting_machine/` | Webots WIP conveyor that will sort incoming boxes by color and size. |
| `spikewheel_bot/` | Webots spike-wheeled robot with a simple manual Python drive controller. |
| `roller_vehicle/` | Webots roller vehicle starter scene with a placeholder Python controller. |
| `newtons_cradle_mechanism/` | Webots Newton's cradle scene with a custom `PendulumBall` PROTO. |
| `ipr/` | Webots project with C/C++ controllers and a shared `libipr` library. |
| `copelliasim/` | Ready-to-run `.ttt` scenes and Lua scripts for Pioneer, Robotnik, and conveyor experiments. |
| `industrial-iot/` | Python OPC UA ingestion examples for Codesys and Kepware-style servers. |
| `4wd_robot_car/` | ESP32 sketch serving a browser-based control page for a 4WD robot car. |
| `circuit_simulations/` | SimulIDE `.sim1` circuits for regulator and basic measurement experiments. |
| `part_design_cad/` | FreeCAD, Blender, OBJ, MTL, and STL assets reused across simulator projects. |
| `Skeleton_male/` | Blender skeleton asset and a related rig UI script. |
| `panda-reach-and-pick/` | MP4 clips and still frames from a Panda reach-and-pick RL experiment. |

## Prerequisites

| Domain | Tools |
| ------ | ----- |
| Webots projects | Webots R2023b+ and, for C/C++ controllers, a compiler toolchain plus `make`. |
| Arduino demos | Arduino IDE or PlatformIO with the `Servo` library available. |
| CoppeliaSim scenes | CoppeliaSim Edu 4.6+ with Lua scripting enabled. |
| Industrial IoT demos | Python 3.10+ and `pip install opcua`, plus access to an OPC UA server. |
| Embedded ESP32 sketch | Arduino IDE or PlatformIO with ESP32 board support. |
| Circuit simulation | SimulIDE 1.x or another tool that opens `.sim1` XML circuits. |
| CAD assets | FreeCAD 0.21+, Blender 3.x, and any viewer that can inspect OBJ/STL exports. |

## LivMach Walker

`livmach_walker/` is the newest Webots project in the repo and uses a single local keyboard controller.

- World: `worlds/livmach_walker.wbt`
- Controller: `controllers/livmach_walker/livmach_walker.py`
- Project notes: `livmach_walker/README.md`

Current behavior:

- Keyboard controls the crawl gait directly.
- IMU-based pitch and roll stabilization remains in the controller.
- No external process or TCP bridge is required.

Run it from the project directory:

```bash
webots worlds/livmach_walker.wbt
```

Inside Webots, make sure the robot controller is `livmach_walker`, then start or reset the simulation.

## Turret Simulation

- Where: `turret_simulation/controllers/turret_manual/`, `worlds/Turret Control Simulation.wbt`, `protos/Turret.proto`
- Controls: `A/D` yaw, `W/S` pitch
- Build and run:

```bash
cd turret_simulation/controllers/turret_manual
make
webots ../../worlds/"Turret Control Simulation.wbt"
```

## Turret Targeting System

`turret_targeting_system/` contains an Arduino sketch for manually aiming a turret pan servo.

- Sketch: `turret_controller_manual.ino`
- Inputs: left button on pin `2`, right button on pin `3`
- Output: servo on pin `9`
- Behavior: button presses step the pan angle between `0` and `180` degrees, with `INPUT_PULLUP` on both buttons

Upload it with the Arduino IDE or PlatformIO after wiring the buttons and Servo library support.

## Shooter Mechanism

- Controller: `controllers/my_Shooter_controller/my_Shooter_controller.c`
- World: `worlds/Shooter_arena.wbt`
- Build:

```bash
cd shooter_mechanism/controllers/my_Shooter_controller
make
webots ../../worlds/Shooter_arena.wbt
```

## Conveyor Belt

- World: `conveyor_belt/worlds/conveyor_belt_test.wbt`
- Controller: `controllers/conveyor_controller/conveyor_controller.c`
- Behavior: supervisor compares desired belt speed against package velocity and applies corrective force along the belt.
- Run:

```bash
cd conveyor_belt/controllers/conveyor_controller
make
webots ../../worlds/conveyor_belt_test.wbt
```

## Sorting Machine

- Status: work in progress
- World: `sorting_machine/worlds/sorting_machine.wbt`
- Controller: `sorting_machine/controllers/sorting_machine_conveyer/sorting_machine_conveyer.c`
- Current state: roller conveyor motion is wired; box classification and routing are still to be added.

## CoppeliaSim Scenes

| File | Purpose |
| ---- | ------- |
| `Pioneer.ttt` + `pioneer_script.lua` | Pioneer P3-DX demo that drives forward indefinitely. |
| `robotnik_motion.ttt` + `robotnik_movement.lua` | Robotnik Summit XL routine with scripted forward and reverse phases. |
| `conveyer_belt.ttt` | Conveyor layout ready for further scripting. |

## Industrial IoT OPC UA Demos

Located in `industrial-iot/`:

- `ingest.py`: polls a Codesys PLC endpoint for button and conveyor-related values
- `opcua_ingest.py`: lightweight poller for a simulation-server-style OPC UA endpoint

Setup:

```bash
cd industrial-iot
python -m venv venv
source venv/bin/activate
pip install opcua
python ingest.py
```

## Embedded 4WD Robot Car

`4wd_robot_car/4wd_robot_control.ino` starts an ESP32 access point named `ESP32_Robot`, serves a simple browser UI, and maps HTTP routes such as `/forward`, `/left`, `/right`, and `/stop` to motor pin outputs.

## CAD And Circuit Assets

- `part_design_cad/` contains FreeCAD, Blender, and exported mesh assets reused by simulator projects.
- `circuit_simulations/` contains SimulIDE circuit files such as `series_voltage_regulator.sim1`.
- `Skeleton_male/` contains a Blender skeleton asset and related script tooling.

## Development Notes

- Keep generated artifacts such as `build/`, `.wbproj`, local `venv/`, and Python cache files out of commits.
- Re-export CAD meshes when geometry changes so simulator assets stay aligned.
- Add a short note to this README when introducing a new top-level project.

## License

This repository is licensed under the MIT License. See [LICENSE](/home/shreyak/programming/robotics/LICENSE).
