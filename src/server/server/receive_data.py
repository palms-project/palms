"""TCP server"""

__all__ = ["serve"]

import json
import logging
import socketserver

from . import data

SERVER_ADDRESS = ("raspberrypi.local", 35007)


def serve() -> None:
    """Run TCP server."""
    with LoggingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


class RequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.debug("Received new request")

    def handle(self) -> None:
        """
        Load JSON from received string and update global data.
        If JSON can't be loaded, then it must be a zero command
        """
        data_str = self.request.recv(1024)
        logging.info(f"Current targets: {data.data}")
        data.data = {**data.data, **json.loads(data_str)}
        logging.info(f"New target: {data.data}")

    def finish(self) -> None:
        logging.debug("Handled new request")


class LoggingTCPServer(socketserver.TCPServer):
    def server_activate(self) -> None:
        """Same as overridden method just with logging"""
        self.socket.listen()
        logging.info("Server activated. Ready to receive positioning data.")
