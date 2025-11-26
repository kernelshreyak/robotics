# Agent Notes

## Repository Snapshot (2025-02)
- Top-level dirs: `circuit_simulations`, `copelliasim`, `conveyor_belt`, `industrial-iot`, `part_design_cad`, `shooter_mechanism`, `turret_simulation`, plus `readme.md` and this log (now uppercase `AGENTS.md` so it is easier to spot).
- Workspace was originally read-only; writes require explicit approval (already granted for README updates and this log).
- No license file yet; repo mixes simulation assets, CAD, and IoT scripts.

## Key Components
1. **turret_simulation**
   - Webots project with manual turret controller (`controllers/turret_manual/turret_manual.c`), world (`worlds/Turret Control Simulation.wbt`), PROTO (`protos/Turret.proto`), OBJ tripod assets.
   - Keyboard bindings: `A/D` yaw, `W/S` pitch. Motors run in velocity mode with optional force limits.

2. **shooter_mechanism**
   - Webots shooter arena; controller spins two motors opposite directions near max speed.
   - Build via `make` inside `controllers/my_Shooter_controller/`; world lives under `worlds/Shooter_arena.wbt`.

3. **copelliasim**
   - Scenes: `Pioneer.ttt`, `robotnik_motion.ttt`, `conveyer_belt.ttt` plus Lua scripts `pioneer_script.lua`, `robotnik_movement.lua`.
   - Pioneer script locks velocity to 2; Robotnik script toggles forward/back using simulation time thresholds (T1=26, T2=30).

4. **industrial-iot**
   - Python OPC UA ingestion examples `ingest.py` (Codesys endpoint) and `opcua_ingest.py` (Kepware Simulation Server).
   - Mentions `venv/` folder for dependencies (not populated here).

5. **part_design_cad**
   - FreeCAD (`.FCStd`, `.FCBak`), Blender (`.blend`, `.blend1`), and OBJ/MTL for turret tripod; assets reused in Webots.

6. **circuit_simulations**
   - SimulIDE `.sim1` file `series_voltage_regulator.sim1` describing MOSFET regulator with battery, ground, oscilloscope, push switch.
7. **conveyor_belt**
   - Webots world `worlds/conveyor_belt_test.wbt` builds a belt + packages scene; supervisor controller `controllers/conveyor_controller/conveyor_controller.c` scans for `PACKAGE1..PACKAGE10` nodes, compares desired belt speed vs. package velocity, and applies forces along X so parcels glide across low-friction contact surfaces.

## Outstanding Ideas / Follow-ups
- Consider adding screenshots or diagrams for each simulator project to README.
- Add `.gitignore` entries if build artifacts/venv become noisy.
- Introduce a license (MIT/Apache-2.0) if sharing widely.
- Potential future tasks: consolidate OPC UA logging into MQTT/cloud; add automated tests for controllers; document conveyor belt scene scripting.

## Environment Notes
- Shell command prefix: `bash -lc` with `workdir` set per command.
- `rg` preferred for searches (currently unused).
- Network access restricted; no external fetches performed.
