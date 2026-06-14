# LivMach Walker

Webots walker project with a local TCP bridge for external balance or gait control.

## Files

- `worlds/livmach_walker.wbt`: main Webots world
- `controllers/livmach_walker/livmach_walker.py`: simulation controller
- `external_controller.py`: external Python controller backed by Ollama
- `bridge/protocol.py`: shared binary message format
- `bridge/tcp_link.py`: TCP client and server helpers

## Recent Changes

- Removed camera follow from the world setup.
- Added an IMU stack at the MuJoCo IMU site at `(0.001, 0, -0.0195)`:
  - `imu` as `InertialUnit`
  - `accelerometer`
  - `gyro`
- Passed TCP port `5555` into the controller through `controllerArgs`.
- Added a non-blocking localhost TCP server in the Webots controller.
- Added an external Python controller that connects to Webots as a TCP client.
- Webots controller now focuses on two jobs only: stream sensor/state data and execute leg-angle commands received from the external controller.
- Webots prints IMU and leg telemetry periodically on its own console instead of streaming every packet to the external controller console.
- The external controller is optimized for interactive use with `qwen2.5:3b`: it asks for one natural-language instruction at a time, sends a compact sensor snapshot to Ollama, sends the returned action to Webots, then prompts for the next instruction.

## Runtime Model

Webots is the TCP server. The external Python controller is the TCP client.

- Webots streams sensor and state data every step.
- External logic consumes those packets and sends desired left and right leg target angles back.

## Protocol

Two binary message types are shared by Webots and the external app.

- `MSG_IMU` from Webots to the app
  - time
  - roll, pitch, yaw
  - accel x, y, z
  - gyro x, y, z
  - left leg angle
  - right leg angle
- `MSG_CMD` from the app to Webots
  - left leg target angle in radians
  - right leg target angle in radians

`bridge/protocol.py` is the single source of truth for packet sizes and packing/unpacking.

## Running

Start Webots first:

```bash
webots worlds/livmach_walker.wbt
```

Then start the external controller from the repository root:

```bash
python3 livmach_walker/external_controller.py
```

Once connected, enter a natural-language control objective such as:

```text
Keep the walker balanced upright with small safe corrections.
```

You can prefill the first instruction from the command line:

```bash
python3 livmach_walker/external_controller.py --instruction "Keep the walker balanced upright with small safe corrections."
```

## Extending Control Logic

`external_controller.py` sends the model:

- your natural-language control objective
- actuator limits and execution constraints
- the latest IMU, accelerometer, gyro, and leg-position snapshot

It then expects JSON actuator targets back from local Ollama model `qwen2.5:3b`.

Before running it, make sure Ollama is installed, `ollama serve` is running, and the model is available locally.

If you want to change the policy logic, edit `LivMachExternalController.on_step()` or the prompt built in `OllamaPolicy._build_prompt()`.

Send commands with:

```python
self.client.send_cmd(left, right)
```
