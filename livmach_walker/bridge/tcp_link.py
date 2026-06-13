"""Non-blocking TCP helpers for LivMach bridge."""

from __future__ import annotations

import socket

from bridge.protocol import iter_cmd_packets, iter_imu_packets, latest_cmd, pack_cmd, pack_imu


class SimulationTcpServer:
    """Webots controller side: accepts one client and streams IMU packets."""

    def __init__(self, host: str = "127.0.0.1", port: int = 5555) -> None:
        self.host = host
        self.port = port
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((host, port))
        self._server.listen(1)
        self._server.setblocking(False)
        self._client: socket.socket | None = None
        self._rx_buffer = b""
        self._connected_once = False

    def poll(self) -> tuple[float, float] | None:
        self._accept_client()
        if self._client is None:
            return None
        self._read_client()
        commands, self._rx_buffer = iter_cmd_packets(self._rx_buffer)
        return latest_cmd(commands)

    def send_imu(self, **fields: float) -> None:
        if self._client is None:
            return
        packet = pack_imu(**fields)
        try:
            self._client.sendall(packet)
        except OSError:
            self._close_client()

    def close(self) -> None:
        self._close_client()
        self._server.close()

    def status_message(self) -> str | None:
        if self._client is not None:
            return None
        if not self._connected_once:
            return f"TCP bridge listening on {self.host}:{self.port}"
        return "waiting for external app to reconnect"

    def _accept_client(self) -> None:
        if self._client is not None:
            return
        try:
            client, address = self._server.accept()
        except BlockingIOError:
            return
        client.setblocking(False)
        self._client = client
        self._rx_buffer = b""
        self._connected_once = True
        print(f"LivMach bridge: client connected from {address[0]}:{address[1]}")

    def _read_client(self) -> None:
        if self._client is None:
            return
        try:
            chunk = self._client.recv(4096)
        except BlockingIOError:
            return
        except OSError:
            self._close_client()
            return

        if not chunk:
            print("LivMach bridge: client disconnected")
            self._close_client()
            return

        self._rx_buffer += chunk

    def _close_client(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            except OSError:
                pass
        self._client = None
        self._rx_buffer = b""


class ExternalTcpClient:
    """External Python app side: receives IMU packets and sends leg commands."""

    def __init__(self, host: str = "127.0.0.1", port: int = 5555) -> None:
        self.host = host
        self.port = port
        self._socket: socket.socket | None = None
        self._rx_buffer = b""

    def connect(self, timeout_s: float = 30.0) -> None:
        deadline = socket.getdefaulttimeout()
        try:
            socket.setdefaulttimeout(timeout_s)
            sock = socket.create_connection((self.host, self.port))
        finally:
            socket.setdefaulttimeout(deadline)
        sock.setblocking(False)
        self._socket = sock

    def close(self) -> None:
        if self._socket is not None:
            try:
                self._socket.close()
            except OSError:
                pass
        self._socket = None
        self._rx_buffer = b""

    def poll_imu(self) -> list[dict[str, float]]:
        if self._socket is None:
            return []
        try:
            chunk = self._socket.recv(65536)
        except BlockingIOError:
            return []
        except OSError:
            self.close()
            return []

        if not chunk:
            self.close()
            return []

        self._rx_buffer += chunk
        packets, self._rx_buffer = iter_imu_packets(self._rx_buffer)
        return packets

    def send_cmd(self, left_leg: float, right_leg: float) -> None:
        if self._socket is None:
            raise RuntimeError("not connected to Webots bridge")

        try:
            self._socket.sendall(pack_cmd(left_leg, right_leg))
        except OSError as exc:
            self.close()
            raise RuntimeError("failed to send command to Webots bridge") from exc
