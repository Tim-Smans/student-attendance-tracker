import RPi.GPIO as GPIO
import time

class RGBLED:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)

    def warn_message(self, message):
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        print(f"{YELLOW}[Warn]: {message}{RESET}")

    def safe_output(self, pin, state):
        try:
            GPIO.output(pin, state)
        except (RuntimeError, OSError) as e:
            self.warn_message(f"Failed to set pin {pin} to {state}: {e}")


    def turn_off(self):     
        self.safe_output(self.red_pin, GPIO.HIGH)
        self.safe_output(self.green_pin, GPIO.HIGH)
        self.safe_output(self.blue_pin, GPIO.HIGH)

    def white(self):
        self.safe_output(self.red_pin, GPIO.LOW)
        self.safe_output(self.green_pin, GPIO.LOW)
        self.safe_output(self.blue_pin, GPIO.LOW)

    def red(self):
        self.safe_output(self.red_pin, GPIO.HIGH)
        self.safe_output(self.green_pin, GPIO.LOW)
        self.safe_output(self.blue_pin, GPIO.LOW)

    def green(self):
        self.safe_output(self.red_pin, GPIO.LOW)
        self.safe_output(self.green_pin, GPIO.HIGH)
        self.safe_output(self.blue_pin, GPIO.LOW)

    def blue(self):
        self.safe_output(self.red_pin, GPIO.HIGH)
        self.safe_output(self.green_pin, GPIO.HIGH)
        self.safe_output(self.blue_pin, GPIO.LOW)

    def yellow(self):
        self.safe_output(self.red_pin, GPIO.LOW)
        self.safe_output(self.green_pin, GPIO.LOW)
        self.safe_output(self.blue_pin, GPIO.HIGH)

    def purple(self):
        self.safe_output(self.red_pin, GPIO.LOW)
        self.safe_output(self.green_pin, GPIO.HIGH)
        self.safe_output(self.blue_pin, GPIO.LOW)

    def lightBlue(self):
        self.safe_output(self.red_pin, GPIO.HIGH)
        self.safe_output(self.green_pin, GPIO.LOW)
        self.safe_output(self.blue_pin, GPIO.LOW)
