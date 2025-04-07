import cv2
import pytesseract
import re
import json
import numpy as np

# Laad afbeelding
image = cv2.imread('image.png')

# Resize voor betere OCR
scale_percent = 200
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# Erosie om de tekst strakker te maken
kernel = np.ones((2,2), np.uint8)
processed = cv2.erode(thresh, kernel, iterations=1)

# OCR uitvoeren
custom_config = r'--oem 3 --psm 6'
raw_text = pytesseract.image_to_string(processed, config=custom_config)

# Regex om alleen de Student ID te vinden
match = re.search(r'Student ID\s*:?[\s\n]*([0-9]{5,})', raw_text, re.IGNORECASE)

# Resultaat verwerken
if match:
    student_id = match.group(1)
    result = {"student_id": student_id}
else:
    result = {"student_id": None}

# JSON printen
print(json.dumps(result, indent=2))

# (optioneel: processed beeld tonen)
cv2.imshow('Voorbewerkt', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
