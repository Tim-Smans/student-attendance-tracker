import RPi.GPIO as GPIO
import time
                  

class PirMotionDetector:
  def __init__(self, pir_pin):
    self.pir_pin = pir_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

  def detected_movement(self) -> bool:
      if GPIO.input(self.pir_pin):
        print("Detected movement")
        return True

      return False

  def is_plugged_in(self) -> bool:
      timeout = time.time() + 2 
      while time.time() < timeout:
          if GPIO.input(self.pir_pin):
              return True
          time.sleep(0.05)
      return False


