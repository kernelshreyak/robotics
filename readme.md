# Robotics Project Portfolio

A grab bag of robotics experiments that span circuit-level simulations, full Webots and CoppeliaSim environments, OPC UA industrial IoT ingest scripts, and the CAD that ties them together. Each folder is self-contained so you can focus on the subsystem you care about.

## Repository Layout

| Path | Contents |
| ---- | -------- |
| `turret_simulation/` | Webots project for a manually driven turret (controllers, worlds, custom PROTO, shared assets). |
| `shooter_mechanism/` | Webots arena for a dual-wheel shooter plus its controller sources and binaries. |
| `copelliasim/` | Ready-to-run `.ttt` scenes and Lua scripts for Pioneer P3-DX and Robotnik mobile robots. |
| `industrial-iot/` | Python OPC UA ingestion examples and a `venv/` stub for Codesys/Kepware integrations. |
| `circuit_simulations/` | SimulIDE `.sim1` schematic of a series voltage regulator. |
| `part_design_cad/` | FreeCAD, OBJ/MTL, and Blender sources for the turret tripod mechanics. |

## Prerequisites

| Domain | Tools |
| ------ | ----- |
| Webots projects | Webots R2023b+, `gcc`/`make` (or MSVC on Windows). |
| CoppeliaSim scenes | CoppeliaSim Edu 4.6+ with Lua API enabled. |
| Industrial IoT demos | Python 3.10+, `pip install opcua`, access to an OPC UA server (Codesys, Kepware Simulation Server, etc.). |
| Circuit simulation | SimulIDE 1.x or another tool that opens `.sim1` XML circuits. |
| CAD assets | FreeCAD 0.21+, Blender 3.x for editing, any viewer for OBJ/MTL export. |

> Tip: keep Python dependencies inside `industrial-iot/venv` (already ignored) so simulator SDK files don’t leak into commits.

## Turret Simulation (Webots)

- **Where**: `turret_simulation/controllers/turret_manual/`, `worlds/Turret Control Simulation.wbt`, `protos/Turret.proto`, and OBJ tripod meshes in `assets/`.
- **Controls**: `A/D` yaw, `W/S` pitch with live angle readouts (`turret_manual.c`).
- **Build & run**:
  ```bash
  cd turret_simulation/controllers/turret_manual
  make
  webots ../../worlds/"Turret Control Simulation.wbt"
  ```
  Select the `turret_manual` controller when prompted (or set it in the world file).

## Shooter Mechanism (Webots)

- **Controller**: `controllers/my_Shooter_controller/my_Shooter_controller.c` spins two wheels in opposite directions at ~50% of their rated speed, reading the max velocity at runtime.
- **World**: `worlds/Shooter_arena.wbt` contains the shooter, targets, and arena walls.
- **Build**:
  ```bash
  cd shooter_mechanism/controllers/my_Shooter_controller
  make
  webots ../../worlds/Shooter_arena.wbt
  ```
  Tweak `shoot_speed` before compiling if you swap motors.

## CoppeliaSim Scenes

| File | Purpose |
| ---- | ------- |
| `Pioneer.ttt` + `pioneer_script.lua` | Pioneer P3-DX demo that drives forward indefinitely (`vel = 2`). |
| `robotnik_motion.ttt` + `robotnik_movement.lua` | Robotnik Summit XL routine with scripted forward/backward phases (`T1 = 26`, `T2 = 30`). |
| `conveyer_belt.ttt` | Conveyor layout (ready for scripting). |

**Usage**

1. Launch CoppeliaSim → `File > Open scene...` → select a `.ttt`.
2. Ensure the paired Lua script is attached as a child script.
3. Press *Play*; edit the Lua files for more advanced logic (sensor feedback, PID, etc.).

## Industrial IoT OPC UA Demos

Located in `industrial-iot/`:

- `ingest.py`: Connects to a Codesys PLC at `opc.tcp://192.168.29.10:4840`, reads button state plus set/actual conveyor speeds, and logs them every 0.5 s.
- `opcua_ingest.py`: Lightweight poller for Kepware/KIT Simulation Server (`SERVER_URL = "opc.tcp://shreyak-laptop:53530/OPCUA/SimulationServer"`, `NODE_ID = "ns=3;i=1003"`).

**Setup**

```bash
cd industrial-iot
python -m venv venv
source venv/bin/activate
pip install opcua
python ingest.py
```

Swap out the endpoint URL and node IDs for your PLC, and replace the `print()` calls with MQTT publishes, database writes, or cloud ingestion SDKs as needed.

## CAD: Turret Tripod

`part_design_cad/` contains the mechanical source of the turret base:

- Edit solids in `turret_tripod.FCStd` (FreeCAD) and meshes in `turret_tripod.blend`.
- Export updated OBJ/MTL pairs when you need to refresh the Webots assets (`turret_simulation/assets/`).
- Backup files (`*.FCBak`, `.blend1`) are kept alongside the masters for quick rollback.

## Circuit Simulation

`circuit_simulations/series_voltage_regulator.sim1` is an XML-based SimulIDE project for a MOSFET series regulator with oscilloscope probes, push-button, and measurement instrumentation.

1. Launch SimulIDE (or another `.sim1`-compatible simulator).
2. Open the file and run the transient analysis to inspect the scope traces.
3. Edit component values in the GUI or directly within the XML for version-controlled tweaks.

## Development Notes

- Keep generated artifacts (`build/`, controller binaries, `venv/`) out of commits or list them in `.gitignore`.
- Re-export shared meshes from CAD whenever you change geometry so CoppeliaSim and Webots stay aligned.
- Document new experiments in this README so others can discover and reuse them quickly.

## License

No explicit license file exists yet. Add one (e.g., MIT, Apache-2.0) if you plan to publish or distribute the assets.
