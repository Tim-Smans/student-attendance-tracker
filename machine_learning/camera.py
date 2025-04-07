import cv2
import pytesseract
import re
import numpy as np
import time

# Camera openen
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not camera.isOpened():
    print("FOUT: Kan camera niet openen.")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("FOUT: Frame niet gelezen.")
        break

    # Toon live preview
    cv2.imshow('Live Preview', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    if key == ord(' '):
        # Capture frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        kernel = np.ones((2,2), np.uint8)
        processed = cv2.erode(thresh, kernel, iterations=1)

        # ➡️ Save preprocessed frame
        timestamp = int(time.time())
        filename = f"preprocessed_{timestamp}.png"
        cv2.imwrite(filename, processed)
        print(f"Preprocessed afbeelding opgeslagen als: {filename}")

        # ➡️ OCR uitvoeren
        custom_config = r'--oem 3 --psm 6'
        raw_text = pytesseract.image_to_string(processed, config=custom_config)

        match = re.search(r'Student ID\s*:?[\s\n]*([0-9]{5,})', raw_text, re.IGNORECASE)
        if match:
            student_id = match.group(1)
            print(f"Gevonden student ID: {student_id}")
        else:
            print("Geen student ID gevonden.")

camera.release()
cv2.destroyAllWindows()
