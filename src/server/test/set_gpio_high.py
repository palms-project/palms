import RPi.GPIO as GPIO

from server import movement_controller as mc

if __name__ == "__main__":
    mc.set_up_gpio()

    GPIO.output(mc.STEP_X, GPIO.HIGH)
    GPIO.output(mc.STEP_Y, GPIO.HIGH)
    GPIO.output(mc.STEP_Z, GPIO.HIGH)
    GPIO.output(mc.STEP_A, GPIO.HIGH)
    GPIO.output(mc.STEP_B, GPIO.HIGH)

    input("Press enter to end execution")
    mc.clean_up()
