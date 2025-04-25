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

  def turn_off(self):
      GPIO.output(self.red_pin,GPIO.HIGH)
      GPIO.output(self.green_pin,GPIO.HIGH)
      GPIO.output(self.blue_pin,GPIO.HIGH)
      
  def white(self):
      GPIO.output(self.red_pin,GPIO.LOW)
      GPIO.output(self.green_pin,GPIO.LOW)
      GPIO.output(self.blue_pin,GPIO.LOW)
      
  def red(self):
      GPIO.output(self.red_pin,GPIO.LOW)
      GPIO.output(self.green_pin,GPIO.HIGH)
      GPIO.output(self.blue_pin,GPIO.HIGH)

  def green(self):
      GPIO.output(self.red_pin,GPIO.HIGH)
      GPIO.output(self.green_pin,GPIO.LOW)
      GPIO.output(self.blue_pin,GPIO.HIGH)
      
  def blue(self):
      GPIO.output(self.red_pin,GPIO.HIGH)
      GPIO.output(self.green_pin,GPIO.HIGH)
      GPIO.output(self.blue_pin,GPIO.LOW)
      
  def yellow(self):
      GPIO.output(self.red_pin,GPIO.LOW)
      GPIO.output(self.green_pin,GPIO.LOW)
      GPIO.output(self.blue_pin,GPIO.HIGH)
      
  def purple(self):
      GPIO.output(self.red_pin,GPIO.LOW)
      GPIO.output(self.green_pin,GPIO.HIGH)
      GPIO.output(self.blue_pin,GPIO.LOW)
      
  def lightBlue(self):
      GPIO.output(self.red_pin,GPIO.HIGH)
      GPIO.output(self.green_pin,GPIO.LOW)
      GPIO.output(self.blue_pin,GPIO.LOW)