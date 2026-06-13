# Robotics Project Portfolio

A collection of robotics experiments spanning Webots, CoppeliaSim, embedded control, industrial IoT, CAD, and circuit simulation. Most directories are independent projects, so you can work inside one subsystem without pulling in the rest of the repository.

## Repository Layout

| Path | Contents |
| ---- | -------- |
| `livmach_walker/` | Webots walker with IMU instrumentation and a localhost TCP bridge for external balance or gait control. |
| `turret_simulation/` | Webots project for a manually driven turret with custom PROTO and shared tripod assets. |
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
| CoppeliaSim scenes | CoppeliaSim Edu 4.6+ with Lua scripting enabled. |
| Industrial IoT demos | Python 3.10+ and `pip install opcua`, plus access to an OPC UA server. |
| Embedded ESP32 sketch | Arduino IDE or PlatformIO with ESP32 board support. |
| Circuit simulation | SimulIDE 1.x or another tool that opens `.sim1` XML circuits. |
| CAD assets | FreeCAD 0.21+, Blender 3.x, and any viewer that can inspect OBJ/STL exports. |

## LivMach Walker

`livmach_walker/` is the newest Webots project in the repo and now includes an external control bridge.

- World: `worlds/livmach_walker.wbt`
- Controller: `controllers/livmach_walker/livmach_walker.py`
- External client: `external_app.py`
- Shared bridge code: `bridge/protocol.py`, `bridge/tcp_link.py`

Recent additions:

- Removed camera follow from the world.
- Added an IMU stack at the MuJoCo IMU site:
  - `InertialUnit` for roll, pitch, yaw
  - `Accelerometer`
  - `Gyro`
- Passed TCP port `5555` via `controllerArgs`.
- Added a binary localhost TCP protocol between Webots and an external Python app.
- Controller now streams IMU plus left/right leg positions every simulation step and accepts remote leg-angle commands.
- Keyboard control remains available as a local fallback.

Protocol summary:

- `MSG_IMU`: time, roll/pitch/yaw, accel xyz, gyro xyz, left leg angle, right leg angle
- `MSG_CMD`: left leg target angle, right leg target angle

Run it in two terminals:

```bash
# Terminal 1
webots livmach_walker/worlds/livmach_walker.wbt

# Terminal 2
python livmach_walker/external_app.py
```

For project-specific details, see `livmach_walker/README.md`.

## Turret Simulation

- Where: `turret_simulation/controllers/turret_manual/`, `worlds/Turret Control Simulation.wbt`, `protos/Turret.proto`
- Controls: `A/D` yaw, `W/S` pitch
- Build and run:

```bash
cd turret_simulation/controllers/turret_manual
make
webots ../../worlds/"Turret Control Simulation.wbt"
```

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

No explicit license file exists yet. Add one if the repository is going to be shared broadly.
