import cv2
import pytesseract
import re
import numpy as np
import time
import os

def preprocess(image):
    # Preprocessing stap
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

# Open de camera
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not camera.isOpened():
    print("FOUT: Kan camera niet openen.")
    exit()

print("✅ Camera gestart. Zoek naar blauwe achtergrond...")

# Main loop
while True:
    ret, frame = camera.read()
    if not ret:
        print("FOUT: Frame niet gelezen.")
        break

    # Verklein voor snellere analyse
    small_frame = cv2.resize(frame, (320, 240))
    hsv = cv2.cvtColor(small_frame, cv2.COLOR_BGR2HSV)

    # Blauwe detectie
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    blue_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    blue_ratio = blue_pixels / total_pixels

    # Live preview
    cv2.imshow('Live Preview', small_frame)

    # Automatische capture bij veel blauw
    if blue_ratio > 0.2:  # Bijv. meer dan 20% blauw
        timestamp = int(time.time())
        filename = f"capture_{timestamp}.jpg"
        print(f"📸 Blauwe achtergrond gedetecteerd ({blue_ratio:.2%}). Foto nemen...")
        cv2.imwrite(filename, frame)

        # Preprocessing
        processed = preprocess(frame)
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

        # Wachten zodat je niet continu foto's maakt
        print("⏳ Even wachten om volgende scans te vermijden...")
        time.sleep(3)

    # Druk 'q' om te stoppen
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Gestopt.")
        break

camera.release()
cv2.destroyAllWindows()
