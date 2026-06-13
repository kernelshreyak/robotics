"""Compact binary protocol for LivMach Webots <-> external app TCP bridge."""

from __future__ import annotations

import struct
from typing import Iterable

MSG_IMU = 1
MSG_CMD = 2

IMU_SIZE = struct.calcsize("<Bd9f2f")
CMD_SIZE = struct.calcsize("<B2f")

_IMU_PACKER = struct.Struct("<Bd9f2f")
_CMD_PACKER = struct.Struct("<B2f")


def pack_imu(
    time_s: float,
    roll: float,
    pitch: float,
    yaw: float,
    ax: float,
    ay: float,
    az: float,
    gx: float,
    gy: float,
    gz: float,
    left_leg: float,
    right_leg: float,
) -> bytes:
    return _IMU_PACKER.pack(
        MSG_IMU,
        time_s,
        roll,
        pitch,
        yaw,
        ax,
        ay,
        az,
        gx,
        gy,
        gz,
        left_leg,
        right_leg,
    )


def unpack_imu(packet: bytes) -> dict[str, float]:
    msg_type, time_s, roll, pitch, yaw, ax, ay, az, gx, gy, gz, left_leg, right_leg = _IMU_PACKER.unpack(
        packet
    )
    if msg_type != MSG_IMU:
        raise ValueError(f"expected IMU message, got type {msg_type}")
    return {
        "time_s": time_s,
        "roll": roll,
        "pitch": pitch,
        "yaw": yaw,
        "ax": ax,
        "ay": ay,
        "az": az,
        "gx": gx,
        "gy": gy,
        "gz": gz,
        "left_leg": left_leg,
        "right_leg": right_leg,
    }


def pack_cmd(left_leg: float, right_leg: float) -> bytes:
    return _CMD_PACKER.pack(MSG_CMD, left_leg, right_leg)


def unpack_cmd(packet: bytes) -> tuple[float, float]:
    msg_type, left_leg, right_leg = _CMD_PACKER.unpack(packet)
    if msg_type != MSG_CMD:
        raise ValueError(f"expected CMD message, got type {msg_type}")
    return left_leg, right_leg


def iter_imu_packets(buffer: bytes) -> tuple[list[dict[str, float]], bytes]:
    packets: list[dict[str, float]] = []
    offset = 0
    total = len(buffer)

    while offset + IMU_SIZE <= total:
        if buffer[offset] != MSG_IMU:
            offset += 1
            continue
        packet = buffer[offset : offset + IMU_SIZE]
        packets.append(unpack_imu(packet))
        offset += IMU_SIZE

    return packets, buffer[offset:]


def iter_cmd_packets(buffer: bytes) -> tuple[list[tuple[float, float]], bytes]:
    packets: list[tuple[float, float]] = []
    offset = 0
    total = len(buffer)

    while offset + CMD_SIZE <= total:
        if buffer[offset] != MSG_CMD:
            offset += 1
            continue
        packet = buffer[offset : offset + CMD_SIZE]
        packets.append(unpack_cmd(packet))
        offset += CMD_SIZE

    return packets, buffer[offset:]


def latest_cmd(commands: Iterable[tuple[float, float]]) -> tuple[float, float] | None:
    latest: tuple[float, float] | None = None
    for command in commands:
        latest = command
    return latest
