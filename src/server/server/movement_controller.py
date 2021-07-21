"""Movement controller"""

__all__ = ["run", "clean_up"]

import logging
import time
from functools import total_ordering

import RPi.GPIO as GPIO

from . import data

STEP_INCREMENT = 5.08 / 400  # Lead screw pitch / steps per rev

A_AXIS_STEP_INCREMENT = 4 / 170

CW = 1  # clockwise rotation
CCW = 0  # counterclockwise rotation

# Some axes are flipped
ALT_CW = 0
ALT_CCW = 1

STEP_X = 11  # x-axis step GPIO pin
DIR_X = 13  # x-axis direction GPIO pin

STEP_Y = 10  # y-axis step GPIO pin
DIR_Y = 12  # y-axis direction GPIO pin

STEP_Z = 38  # z-axis step GPIO pin
DIR_Z = 40  # z-axis direction GPIO pin

STEP_A = 21  # a-axis step GPIO pin
DIR_A = 22  # a-axis direction GPIO pin

STEP_B = 3  # b-axis step GPIO pin
DIR_B = 5  # b-axis direction GPIO pin

SLEEP = 15  # sleep GPIO pin


def run() -> None:
    """Receive movement instructions and execute until stopped."""
    set_up_gpio()

    x_axis = Axis(STEP_X, DIR_X, STEP_INCREMENT, CW, CCW, "x")
    y_axis = Axis(STEP_Y, DIR_Y, STEP_INCREMENT, CW, CCW, "y")
    z_axis = Axis(STEP_Z, DIR_Z, STEP_INCREMENT, ALT_CW, ALT_CCW, "z")
    a_axis = Axis(STEP_A, DIR_A, A_AXIS_STEP_INCREMENT, CW, CCW, "a")
    b_axis = Axis(STEP_B, DIR_B, STEP_INCREMENT, ALT_CW, ALT_CCW, "b")

    logging.info("Controller loop starting")
    while True:
        x_axis.target_position = data.data["x"]
        y_axis.target_position = data.data["y"]
        z_axis.target_position = data.data["z"]
        a_axis.target_position = data.data["a"]
        b_axis.target_position = data.data["b"]

        logging.debug(f"Targets: {data.data}")

        if not is_in_position(x_axis, y_axis, z_axis, a_axis, b_axis):
            logging.debug("Not in position")
            wake_up()

            x_axis.move()
            y_axis.move()
            z_axis.move()
            a_axis.move()
            b_axis.move()

            time.sleep(0.00075)

            x_axis.pulse_low()
            y_axis.pulse_low()
            z_axis.pulse_low()
            a_axis.pulse_low()
            b_axis.pulse_low()

            time.sleep(0.00075)
        else:
            logging.debug("In position")
            sleep()

        logging.debug("End of loop\n")


def wake_up() -> None:
    GPIO.output(SLEEP, GPIO.HIGH)
    logging.debug("Sleep pin set to low")


def sleep() -> None:
    GPIO.output(SLEEP, GPIO.LOW)
    logging.debug("Sleep pin set to high")


def is_in_position(*axes) -> bool:
    return all(axis.is_in_position() for axis in axes)


class Axis:
    def __init__(self, step_pin: int, dir_pin: int, step_increment: float, cw: int, ccw: int, name: str = "unnamed"):
        self._step_pin = step_pin
        self._dir_pin = dir_pin

        self._current_position = Position(step_increment)

        self._target_position = Position(step_increment)

        self._cw = cw
        self._ccw = ccw

        self.name = name

    def is_in_position(self) -> bool:
        return self._current_position == self._target_position

    def move(self) -> None:
        """Changes actual position to be closer to target position"""
        if self._current_position < self._target_position:
            self._step_increase()
            self._current_position.increment()
            logging.debug(f"Incremented {self.name}. Now {self._current_position.pos}.")
        elif self._current_position > self._target_position:
            self._step_decrease()
            self._current_position.decrement()
            logging.debug(f"Decremented {self.name}. Now {self._current_position.pos}.")
        else:
            logging.debug(f"{self.name}: No movement made")

    def _step_decrease(self) -> None:
        """Decreases axis position by stepping motor CLOCKWISE (CW)"""
        GPIO.output(self._dir_pin, self._cw)
        GPIO.output(self._step_pin, GPIO.HIGH)
        logging.debug(f"{self.name} moving to HIGH, CW (step decrease)")

    def _step_increase(self) -> None:
        """Increases axis position by stepping motor COUNTERCLOCKWISE (CCW)"""
        GPIO.output(self._dir_pin, self._ccw)
        GPIO.output(self._step_pin, GPIO.HIGH)
        logging.debug(f"{self.name}: moving to HIGH, CCW (step increase)")

    def pulse_low(self) -> None:
        GPIO.output(self._step_pin, GPIO.LOW)
        logging.debug(f"{self.name}: pulsing low")

    @property
    def current_position(self) -> float:
        return self._current_position.pos

    @current_position.setter
    def current_position(self, val: float) -> None:
        self._current_position.pos = val

    @property
    def target_position(self) -> float:
        return self._target_position.pos

    @target_position.setter
    def target_position(self, val: float) -> None:
        self._target_position.pos = val

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}({', '.join(repr(attr) for attr in self.__dict__.values())})"

    def __str__(self) -> str:
        return f"{self.name}. Current position: {self._current_position}. Target position {self._target_position}."


@total_ordering
class Position:
    def __init__(self, step_increment):
        self.pos = 0.0
        self._step_increment = step_increment

    def increment(self) -> None:
        self.pos += self._step_increment

    def decrement(self) -> None:
        self.pos -= self._step_increment

    def __eq__(self, other) -> bool:
        if type(self) is type(other):
            # Checks whether the positions are within the deadzone defined by half of the length of a single step.
            return abs(self.pos - other.pos) <= self._step_increment / 2
        raise TypeError("You can only compare a Position with another Position")

    def __lt__(self, other) -> bool:
        if type(self) is type(other):
            if self == other:
                return False
            return self.pos < other.pos
        raise TypeError("You can only compare a Position with another Position")

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}({', '.join(repr(attr) for attr in self.__dict__.values())})"

    def __str__(self) -> str:
        return str(self.pos)


def set_up_gpio() -> None:
    logging.info("Starting GPIO setup.")

    # Setting GPIO mode to BOARD. This uses straight up pin numbers as
    # opposed to actual GPIO channel numbers. For more info on this decision,
    # visit https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/#pin-numbering
    GPIO.setmode(GPIO.BOARD)

    # Set each axis's direction and step pins as outputs as well as the sleep pin.
    GPIO.setup(DIR_X, GPIO.OUT)
    GPIO.setup(STEP_X, GPIO.OUT)

    GPIO.setup(DIR_Y, GPIO.OUT)
    GPIO.setup(STEP_Y, GPIO.OUT)

    GPIO.setup(DIR_Z, GPIO.OUT)
    GPIO.setup(STEP_Z, GPIO.OUT)

    GPIO.setup(STEP_A, GPIO.OUT)
    GPIO.setup(DIR_A, GPIO.OUT)

    GPIO.setup(STEP_B, GPIO.OUT)
    GPIO.setup(DIR_B, GPIO.OUT)

    GPIO.setup(SLEEP, GPIO.OUT)
    logging.info("GPIO setup complete.")


def clean_up() -> None:
    """Run GPIO cleanup to return all channels to safe."""
    GPIO.cleanup()
    logging.info("GPIO cleanup complete")
    sleep()
    logging.info("Motors in sleep mode")
