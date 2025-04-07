import cv2
import pytesseract
import numpy as np

# 1. Laad afbeelding
image = cv2.imread('image.png')

# 2. Resize voor betere OCR (optioneel)
scale_percent = 200
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
image = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

# 3. Grijswaarden conversie
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 4. Threshold: alles boven een bepaalde lichtheid wit maken, rest zwart
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

# 5. Erosie toepassen om tekst net iets fijner te maken
kernel = np.ones((2,2), np.uint8)
processed = cv2.erode(thresh, kernel, iterations=1)

# 6. OCR uitvoeren
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(processed, config=custom_config)

# 7. Resultaat
print("Gescande tekst:")
print(text.strip())

# (optioneel beeld tonen)
cv2.imshow('Voorbewerkt', processed)
cv2.waitKey(0)
cv2.destroyAllWindows()
