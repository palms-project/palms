"""TCP server"""

__all__ = ["serve"]

import json
import logging
import socketserver

import data

SERVER_ADDRESS = ("raspberrypi.local", 35007)


def serve() -> None:
    """Run TCP server."""
    with LoggingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


class RequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.debug(f"Received new request")

    def handle(self) -> None:
        """
        Load JSON from received string and update global data.
        If JSON can't be loaded, then it must be a zero command
        """
        data_str = self.request.recv(1024)
        try:
            logging.info(f"Current targets: {data.targets}")
            data.targets = json.loads(data_str)
            logging.info(f"New targets: {data.targets}")
        except json.decoder.JSONDecodeError:
            # Following EAFP ;)
            data.zero_cmd = True
            data.targets = {"x": 0.0, "y": 0.0, "z": 0.0, "a": 0.0, "b": 0.0}
            logging.debug("Targets dict set to zero")

    def finish(self) -> None:
        logging.debug(f"Handled new request")


class LoggingTCPServer(socketserver.TCPServer):
    def server_activate(self) -> None:
        """Same as overridden method just with logging"""
        self.socket.listen()
        logging.info("Server activated. Ready to receive positioning data.")
