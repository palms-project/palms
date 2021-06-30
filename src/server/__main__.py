import atexit
import logging
from threading import Thread

from . import movement_controller, receive_data

logging.basicConfig(
    format="{asctime} {levelname}: {message}", style="{", level=logging.INFO, datefmt="%m/%d/%Y %I:%M:%S %p"
)

atexit.register(movement_controller.clean_up)

movement_system_thread = Thread(target=movement_controller.run, daemon=True)
movement_system_thread.start()
logging.info("Movement system thread started.")

receive_data.serve()
