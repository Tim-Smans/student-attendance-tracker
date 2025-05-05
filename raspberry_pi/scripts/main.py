import cv2
import pytesseract
import re
import numpy as np
import time
import os
import yaml

from scripts.api.student import get_student_by_id
from scripts.utils.scanning_utils import extract_ids, preprocess, warn_message
from scripts.api.attendance import add_attendance
from scripts.api.session import get_active_session, is_active_session
from scripts.sensors.helpers.lcd_helpers import LCDScreen
from scripts.sensors.helpers.led_helpers import RGBLED
from scripts.sensors.helpers.pir_motion_helpers import PirMotionDetector
from scripts.sensors.helpers.ranger_helpers import UltrasonicRanger
from config import USE_SENSORS

with open("./config.yaml", "r") as f:
    config = yaml.safe_load(f)

student_id_length = config["student_id_length"]

if student_id_length == None:
    student_id_length = 7

# Defining peripherals, sensors and pin layout
if USE_SENSORS:
    lcd_screen = LCDScreen()
    rgb_led = RGBLED(red_pin=23, green_pin=24, blue_pin=25)
    pir_motion_detector = PirMotionDetector(pir_pin=17)
    ultrasonic_ranger = UltrasonicRanger(trig_echo=26)

    if lcd_screen.safe_write_byte_data(0x3e, 0x40, ord('c')) is False:
        warn_message("!!! LCD is currently not connected or broken.")

    if ultrasonic_ranger.measure_distance() is None:
        warn_message("!!! Ultrasonic Ranger is currently not connected or broken.")

print("Started scanning...")





# Main loop
while True:
    if not is_active_session():
        print("No active session. Waiting 10 seconds...")
        lcd_screen.set_text_norefresh("No session...")
        time.sleep(10)
        continue
    
    lcd_screen.clear()
    rgb_led.white()

    if USE_SENSORS:
        motion_detected = pir_motion_detector.detected_movement()
    
        if not motion_detected:
            lcd_screen.set_text_norefresh("No motion\ndetected.")
            time.sleep(0.5)
            continue

    print('passed pir check')
    phone_range = ultrasonic_ranger.measure_distance()
    print(f"Phone range: {phone_range} cm")

    if phone_range != None and phone_range > 15:
        print("Phone too far away. Waiting 5 seconds...")
        lcd_screen.set_text("Please hold your\nphone closer")
        time.sleep(5)
        continue

    lcd_screen.set_text("Scanning...\nPlease hold still")
    timestamp = int(time.time())
    filename = f"snapshot.jpg"
    
    # Create snapshot
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

    # Load snapshot
    image = cv2.imread(filename)
    if image is None:
        print("Error: Could not load.")
        continue

    # Highten speed: resize picture
    small = cv2.resize(image, (320, 240))
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Preprocessing
    processed = preprocess(image)
    processed_filename = f"preprocessed.png"
    cv2.imwrite(processed_filename, processed)

    # OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    print("Scanned text:")
    print(raw_text.strip())

    # ID extraction
    student_id, peppi_id = extract_ids(raw_text, student_id_length)

    print("\nResult:")
    if student_id:
        print(f"Student ID: {student_id}")
        session = get_active_session()
        print("Active session:", f"{session}")
        response = add_attendance(student_id, session["id"])
        student = get_student_by_id(student_id=student_id)

        if(student is None):
            lcd_screen.set_text(f"Student not in\nthis session")
            rgb_led.red()
            time.sleep(3)
        else:
            lcd_screen.set_text(f"Scanned, Welcome\n{student['firstname']}")
            # Turn the LED green if the student is in the session
            rgb_led.green()

    else:
        # Turn the LED red if the student id is not found in the image.
        rgb_led.red()
        print("No Student ID found.")
        lcd_screen.set_text(f"Scanning failed\nTry again!")

    # Wait before scanning again
    time.sleep(3)


