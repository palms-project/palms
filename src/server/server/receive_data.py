"""TCP server"""

__all__ = ["serve_positions", "serve_commands"]

import json
import logging
import socketserver

from . import data

HOSTNAME = "raspberrypi.local"


def serve_positions() -> None:
    """Run TCP server."""
    with LoggingTCPServer((HOSTNAME, 35007), PositionsRequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


def serve_commands() -> None:
    """Run TCP server for commands on different port"""
    with LoggingTCPServer((HOSTNAME, 35008), CommandsRequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


class MyRequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.debug("Received new request")

    def finish(self) -> None:
        logging.debug("Handled new request")


class PositionsRequestHandler(MyRequestHandler):
    def handle(self) -> None:
        """
        Load JSON from received string and update global data.
        If JSON can't be loaded, then it must be a zero command
        """
        data_str = self.request.recv(1024)
        logging.info(f"Current targets: {data.data}")
        data.data = {**data.data, **json.loads(data_str)}
        logging.info(f"New target: {data.data}")


class CommandsRequestHandler(MyRequestHandler):
    def handle(self) -> None:
        """
        Load JSON from received string and update global data.
        If JSON can't be loaded, then it must be a zero command
        """
        data_str = self.request.recv(1024)
        logging.info(f"Current commands: {data.commands}")
        data.commands = {**data.commands, **json.loads(data_str)}
        logging.info(f"New commands: {data.commands}")


class LoggingTCPServer(socketserver.TCPServer):
    def server_activate(self) -> None:
        """Same as overridden method just with logging"""
        self.socket.listen()
        logging.info("Server activated. Ready to receive positioning data.")
