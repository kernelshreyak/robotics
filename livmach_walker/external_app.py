#!/usr/bin/env python3
"""
External LivMach bridge client.

Connects to the Webots controller over TCP, receives IMU packets, and can
send leg commands back. Extend `on_imu()` with your balance / gait logic.

Usage:
  1. Start Webots simulation (livmach_walker.wbt)
  2. python livmach_walker/external_app.py
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from bridge.tcp_link import ExternalTcpClient

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5555


class LivMachExternalApp:
    def __init__(self, host: str, port: int) -> None:
        self.client = ExternalTcpClient(host=host, port=port)
        self.start_time = time.monotonic()
        self.packet_count = 0

    def connect(self, timeout_s: float) -> None:
        print(f"Connecting to Webots bridge at {self.client.host}:{self.client.port} ...")
        self.client.connect(timeout_s=timeout_s)
        print("Connected.")

    def run(self) -> None:
        latest_imu: dict[str, float] | None = None

        while True:
            packets = self.client.poll_imu()
            for imu in packets:
                latest_imu = imu
                self.packet_count += 1
                self.on_imu(imu)

            if latest_imu is not None:
                self.on_step(latest_imu)

            time.sleep(0.001)

    def on_imu(self, imu: dict[str, float]) -> None:
        if self.packet_count % 125 == 0:
            print(
                "IMU "
                f"t={imu['time_s']:.3f}s "
                f"pitch={imu['pitch']:+.3f} "
                f"roll={imu['roll']:+.3f} "
                f"legs=({imu['left_leg']:+.3f}, {imu['right_leg']:+.3f})"
            )

    def on_step(self, imu: dict[str, float]) -> None:
        # Example command: small sinusoidal leg motion for wiring verification.
        phase = imu["time_s"] * 1.5
        left = 0.15 * math.sin(phase)
        right = 0.15 * math.sin(phase + math.pi)
        self.client.send_cmd(left, right)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LivMach external TCP bridge client")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--connect-timeout", type=float, default=60.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    app = LivMachExternalApp(host=args.host, port=args.port)

    try:
        app.connect(timeout_s=args.connect_timeout)
        app.run()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        app.client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
