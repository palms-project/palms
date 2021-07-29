import atexit
import logging
import os
from threading import Thread

from . import movement_controller, receive_data


def main():
    log_level = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}[os.getenv("LOG_LEVEL", default="DEBUG")]

    logging.basicConfig(level=log_level, format="{levelname}: {message}", style="{")
    logging.info(f"Log level: {log_level}")
    logging.info(f"Server version: {__import__('server').__version__}")

    atexit.register(movement_controller.clean_up)

    movement_system_thread = Thread(target=movement_controller.run, daemon=True)
    movement_system_thread.start()
    logging.info("Movement system thread started.")

    commands_server_thread = Thread(target=receive_data.serve_commands, daemon=True)
    commands_server_thread.start()
    logging.info("Commands server thread started.")

    receive_data.serve_positions()


if __name__ == "__main__":
    main()
