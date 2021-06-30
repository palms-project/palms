__all__ = ["send"]

import json
import socket

SERVER_ADDRESS = ("raspberrypi.local", 35007)


def send(data: dict) -> None:
    """Send data to server by serializing the provided dict and sending it."""
    serialized_data = json.dumps(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(SERVER_ADDRESS)
        sock.sendall(bytes(serialized_data + "\n", "utf-8"))