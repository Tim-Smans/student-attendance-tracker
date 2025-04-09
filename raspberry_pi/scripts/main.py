import cv2
import pytesseract
import re
import numpy as np
import time
import os

from scripts.utils.scanning_utils import extract_ids, preprocess
from scripts.api.attendance import add_attendance
from scripts.api.session import get_active_session, is_active_session


print("Started scanning for blue...")

# Main loop
while True:

    if not is_active_session():
        print("No active session. Waiting 10 seconds...")
        time.sleep(10)
        continue

    timestamp = int(time.time())
    filename = f"snapshot.jpg"
    
    # Create snapshot
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

    # Load snapshot
    image = cv2.imread(filename)
    if image is None:
        print("Error: Could not load.")
        continue

    # Highten speed: resize picture for blue detection
    small = cv2.resize(image, (320, 240))
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    blue_ratio = blue_pixels / total_pixels

    print(f"Blue detected: {blue_ratio:.2%}")

    if blue_ratio > 0.2:
        print(f"Enough blue, scanning...")

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
        student_id, peppi_id = extract_ids(raw_text)

        print("\nResult:")
        if student_id:
            print(f"Student ID: {student_id}")
            session = get_active_session()
            print("Active session:", f"{session}")
            response = add_attendance(student_id, session["id"])
        else:
            print("No Student ID found.")

        # Wait before scanning again
        time.sleep(3)

    else:
        # Wait before scanning again
        time.sleep(0.5)

