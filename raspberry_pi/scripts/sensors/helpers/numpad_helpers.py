from pad4pi import rpi_gpio
import RPi.GPIO as GPIO

KEYPAD = [
    ["1","2","3","F"],
    ["4","5","6","E"],
    ["7","8","9","D"],
    ["A","0","B","C"]
]

ROW_PINS = [2, 3, 4, 17]
COL_PINS = [14, 15, 18, 23]

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

def key_pressed(key):
    print(key)

keypad.registerKeyPressHandler(key_pressed)

try:
    while True:
        pass
except KeyboardInterrupt:
    GPIO.cleanup()
