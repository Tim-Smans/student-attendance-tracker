import cv2
import pytesseract
import re
import numpy as np

# Open de camera
camera = cv2.VideoCapture(0)  # 0 is meestal je Pi Camera

# Controleer of camera opent
if not camera.isOpened():
    print("Error, cant open camera.")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("Error, cant read frame.")
        break

    # Preprocessing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2,2), np.uint8)
    processed = cv2.erode(thresh, kernel, iterations=1)

    # OCR
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    # Student ID zoeken
    match = re.search(r'Student ID\s*:?[\s\n]*([0-9]{5,})', raw_text, re.IGNORECASE)
    
    if match:
        student_id = match.group(1)
        print(f"Gevonden student ID: {student_id}")
    else:
        print("Geen student ID gevonden.")

    # Toon het beeld
    cv2.imshow('Live OCR', processed)

    # Stoppen op 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
