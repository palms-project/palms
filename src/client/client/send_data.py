__all__ = ["send_positions", "send_commands", "ServerConnectionError"]

import json
import socket

HOSTNAME = "raspberrypi.local"


def send_positions(data: dict) -> None:
    send(data, 35007)


def send_commands(data: dict) -> None:
    send(data, 35008)


def send(data: dict, port: int) -> None:
    """Send data to server by serializing the provided dict and sending it."""
    serialized_data = json.dumps(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOSTNAME, port))
        except socket.gaierror as e:
            raise ServerConnectionError(
                f'Address-related error connecting to server.\nCheck server is on and running.\n\nLib says: "{e.__class__.__module__}.{e.__class__.__qualname__}: {e}"'
            )
        except socket.error as e:
            raise ServerConnectionError(
                f'General connection error.\nCheck server is on and running.\n\nLib says: "{e.__class__.__module__}.{e.__class__.__qualname__}: {e}"'
            )
        else:
            sock.sendall(bytes(serialized_data + "\n", "utf-8"))


class ServerConnectionError(Exception):
    def __init__(self, message: str):
        self.message = message
