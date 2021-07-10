import atexit
import logging
import os
from threading import Thread

from . import movement_controller, receive_data

log_levels = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}

log_level = log_levels[os.getenv("LOG_LEVEL", default="DEBUG")]

logging.basicConfig(
    format="{asctime} {levelname}: {message}", style="{", level=log_level, datefmt="%m/%d/%Y %I:%M:%S %p"
)

logging.info(f"Log level: {log_level}")
logging.info(f"Server version: {__import__('server').__version__}")

atexit.register(movement_controller.clean_up)

movement_system_thread = Thread(target=movement_controller.run, daemon=True)
movement_system_thread.start()
logging.info("Movement system thread started.")

receive_data.serve()
