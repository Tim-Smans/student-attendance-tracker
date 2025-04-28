import RPi.GPIO as GPIO
import time
                  

class PirMotionDetector:
  def __init__(self, pir_pin):
    self.pir_pin = pir_pin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.pir_pin, GPIO.IN)

  def detected_movement(self) -> bool:
      if GPIO.input(self.pir_pin):
        print("Detected movement")
        return True

      return False

  def is_plugged_in(self) -> bool:
    try: 
      if(GPIO.input(self.pir_pin)):
          print('Pir plugged in')
          return True
      print('Pir plugged in')
      return True 
    except (RuntimeError, OSError) as e:
      print('Pir not plugged in')
      return False 


