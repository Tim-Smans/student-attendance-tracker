import RPi.GPIO as GPIO
import time


class UltrasonicRanger:
    def __init__(self, trig_echo):
        self.trig_echo = trig_echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_echo, GPIO.OUT)
        GPIO.output(self.trig_echo, False)

def measure_distance(self):
    try:
        # Trigger pulse
        GPIO.output(self.trig_echo, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_echo, False)

        GPIO.setup(self.trig_echo, GPIO.IN)

        timeout = time.time() + 0.04
        while GPIO.input(self.trig_echo) == 0:
            if time.time() > timeout:
                return None
        pulse_start = time.time()

        timeout = time.time() + 0.04
        while GPIO.input(self.trig_echo) == 1:
            if time.time() > timeout:
                return None
        pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 34300 / 2, 2)

        GPIO.setup(self.trig_echo, GPIO.OUT)
        GPIO.output(self.trig_echo, False)
        time.sleep(0.002)

        return distance
    
    except (RuntimeError, OSError) as e:
        GPIO.setup(self.trig_echo, GPIO.OUT)
        GPIO.output(self.trig_echo, False)
        time.sleep(0.002)
        return None