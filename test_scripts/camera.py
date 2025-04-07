import cv2
import pytesseract
import re
import numpy as np
import time
import os

def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    _, processed = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)
    return processed

def extract_ids(text):
    numbers = re.findall(r'\d{6,7}', text)
    student_id = None
    peppi_id = None

    for num in numbers:
        if len(num) == 7 and not student_id:
            student_id = num
        elif len(num) == 6 and not peppi_id:
            peppi_id = num
    return student_id, peppi_id

print("✅ Scanner gestart. Zoekt automatisch naar blauw...")

# Main loop
while True:
    timestamp = int(time.time())
    filename = f"snapshot_{timestamp}.jpg"
    
    # Maak snapshot
    os.system(f'libcamera-jpeg -o {filename} --width 640 --height 480 --nopreview')

    # Laad snapshot
    image = cv2.imread(filename)
    if image is None:
        print("FOUT: snapshot niet geladen.")
        continue

    # Snelheid verhogen: verklein foto voor blauw detectie
    small = cv2.resize(image, (320, 240))
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    blue_ratio = blue_pixels / total_pixels

    print(f"🔵 Blue detected: {blue_ratio:.2%}")

    if blue_ratio > 0.2:
        print(f"📸 Genoeg blauw! OCR wordt uitgevoerd...")

        # Preprocessing
        processed = preprocess(image)
        processed_filename = f"preprocessed_{timestamp}.png"
        cv2.imwrite(processed_filename, processed)
        print(f"✅ Preprocessed opgeslagen als: {processed_filename}")

        # OCR
        custom_config = r'--oem 3 --psm 6'
        raw_text = pytesseract.image_to_string(processed, config=custom_config)

        print("\n📋 Gescande tekst:")
        print(raw_text.strip())

        # IDs extracten
        student_id, peppi_id = extract_ids(raw_text)

        print("\n🎯 Resultaat:")
        if student_id:
            print(f"✅ Student ID: {student_id}")
        else:
            print("❌ Geen Student ID gevonden.")

        if peppi_id:
            print(f"✅ Peppi ID: {peppi_id}")
        else:
            print("❌ Geen Peppi ID gevonden.")

        # Wachten om niet direct opnieuw te scannen
        time.sleep(3)

    else:
        # Wachten een korte tijd voor volgende foto
        time.sleep(0.5)

