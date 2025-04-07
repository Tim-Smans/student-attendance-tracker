import cv2
import pytesseract

# Laad afbeelding
image = cv2.imread('image.png')

# Resize om OCR makkelijker te maken (optioneel, afhankelijk van resolutie)
scale_percent = 150  # 150% van origineel
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

# Grijswaarden
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian Blur - zachte smoothing tegen artefacten
blurred = cv2.GaussianBlur(gray, (5,5), 0)

# Adaptive Threshold - slim lokaler drempelen
thresh = cv2.adaptiveThreshold(
    blurred, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    11, 2
)

# OCR
text = pytesseract.image_to_string(thresh, config='--psm 6')

print("Gescande tekst:")
print(text.strip())

# Optioneel: beeld tonen
cv2.imshow('Voorbewerkt', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
