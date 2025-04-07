import cv2
import pytesseract
import re
import time
import os
import numpy as np

while True:
    key = input("Druk op ENTER om een foto te nemen, of typ 'q' om te stoppen: ")

    if key == 'q':
        break

    # ➡️ Neem een nieuwe foto via libcamera-jpeg
    timestamp = int(time.time())
    filename = f"capture_{timestamp}.jpg"
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

    # ➡️ Laad de foto
    image = cv2.imread(filename)
    if image is None:
        print("FOUT: Geen afbeelding geladen.")
        continue

    # ➡️ Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2,2), np.uint8)
    processed = cv2.erode(thresh, kernel, iterations=1)

    # ➡️ Preprocessed foto saven
    processed_filename = f"preprocessed_{timestamp}.png"
    cv2.imwrite(processed_filename, processed)
    print(f"Preprocessed opgeslagen als: {processed_filename}")

    # ➡️ OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    match = re.search(r'Student ID\s*:?[\s\n]*([0-9]{5,})', raw_text, re.IGNORECASE)
    if match:
        student_id = match.group(1)
        print(f"Gevonden student ID: {student_id}")
    else:
        print("Geen student ID gevonden.")
