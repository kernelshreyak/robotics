# LivMach Walker

Webots walker project with a local TCP bridge for external balance or gait control.

## Files

- `worlds/livmach_walker.wbt`: main Webots world
- `controllers/livmach_walker/livmach_walker.py`: simulation controller
- `external_app.py`: external Python client
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
- Added an external Python client that connects to Webots as a TCP client.
- Controller now streams IMU and leg position data every simulation step and applies leg-angle commands received from the external app.
- Keyboard control remains as a fallback when remote commands are absent.

## Runtime Model

Webots is the TCP server. The external Python process is the TCP client.

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

Then start the external app from the repository root:

```bash
python livmach_walker/external_app.py
```

## Extending Control Logic

Put balancing or gait logic in `LivMachExternalApp.on_step()` inside `external_app.py`.

Send commands with:

```python
self.client.send_cmd(left, right)
```

The current implementation sends a small sinusoidal leg motion as a wiring check.
