import cv2
import pytesseract
import re
import time
import os
import numpy as np

while True:
    key = input("Druk ENTER om een foto te nemen, of typ 'q' om te stoppen: ")

    if key == 'q':
        break

    # Maak foto
    timestamp = int(time.time())
    filename = f"capture_{timestamp}.jpg"
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

    # Laad foto
    image = cv2.imread(filename)
    if image is None:
        print("FOUT: Geen afbeelding geladen.")
        continue

    # Preprocessing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    _, processed = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)

    # Preprocessed opslaan
    processed_filename = f"preprocessed_{timestamp}.png"
    cv2.imwrite(processed_filename, processed)
    print(f"Preprocessed opgeslagen als: {processed_filename}")

    # OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    # 🔥 ALLE NUMMERS zoeken
    numbers = re.findall(r'\d{6,7}', raw_text)

    # IDs initialiseren
    student_id = None
    peppi_id = None

    for num in numbers:
        if len(num) == 7:
            student_id = num
        elif len(num) == 6:
            peppi_id = num

    # Output
    print("\n📋 Gescande tekst:")
    print(raw_text.strip())

    print("\n🎯 Extracted IDs:")
    if student_id:
        print(f"Student ID gevonden: {student_id}")
    else:
        print("Geen Student ID gevonden.")

    if peppi_id:
        print(f"Peppi ID gevonden: {peppi_id}")
    else:
        print("Geen Peppi ID gevonden.")
