import RPi.GPIO as GPIO
import time
from helpers.lcd_helpers import setText

class UltrasonicRanger:
    def __init__(self, trig_echo):
        self.trig_echo = trig_echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_echo, GPIO.OUT)
        GPIO.output(self.trig_echo, False)

    def measure_distance(self):
        # Trigger pulse: 10 microseconds HIGH this activates the sensor
        GPIO.output(self.trig_echo, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_echo, False)

        # Set our pin to input to get the returning echo
        GPIO.setup(self.trig_echo, GPIO.IN)

        # Waiting until the echo comes back
        timeout = time.time() + 0.04
        while GPIO.input(self.trig_echo) == 0:
            if time.time() > timeout:
                return None
        pulse_start = time.time()

        # Waiting for the end of the echo
        timeout = time.time() + 0.04
        while GPIO.input(self.trig_echo) == 1:
            if time.time() > timeout:
                return None
        pulse_end = time.time()
        
        # Calculating the distance based on the duration of the pulse.
        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 34300 / 2, 2)
        print(f"Distance: {distance} cm")

        setText(f"Distance: {distance} cm")

        # Put the
        GPIO.setup(self.trig_echo, GPIO.OUT)
        GPIO.output(self.trig_echo, False)
        time.sleep(0.002) 
        
        return distance