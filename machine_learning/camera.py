import cv2
import pytesseract
import re
import time
import numpy as np
import os

while True:
    # Maak een nieuwe foto
    os.system('libcamera-jpeg -o capture.jpg --width 1280 --height 720 --nopreview')

    # Laad de foto
    image = cv2.imread('capture.jpg')
    if image is None:
        print("FOUT: Geen afbeelding geladen.")
        continue

    # Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2,2), np.uint8)
    processed = cv2.erode(thresh, kernel, iterations=1)

    # OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    # Extract Student ID
    match = re.search(r'Student ID\s*:?[\s\n]*([0-9]{5,})', raw_text, re.IGNORECASE)
    if match:
        student_id = match.group(1)
        print(f"Gevonden student ID: {student_id}")
    else:
        print("Geen student ID gevonden.")

    # Wacht even voor volgende scan
    time.sleep(2)  # elke 2 seconden nieuwe foto
