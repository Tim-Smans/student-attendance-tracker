import cv2
import pytesseract
import re
import numpy as np
import time
import os

from raspberry_pi.scripts.api.attendance import add_attendance
from raspberry_pi.scripts.api.session import get_active_session

def preprocess(image):
    """
    Preprocess an image before passing it to OCR.

    The preprocessing steps are as follows:

    1. Grayscale conversion
    2. Contrast limiting adaptive histogram equalization (CLAHE)
    3. Blurring
    4. Binary thresholding

    :param image: The image to preprocess
    :return: The preprocessed image
    """
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    _, processed = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)
    return processed

def extract_ids(text):
    """
    Extracts the student ID and Peppi ID from the given text.

    The function expects the text to contain two numbers: a 7-digit student ID and a 6-digit Peppi ID.
    The function returns a tuple containing the two IDs, or None if either ID could not be found.

    :param text: The text to extract the IDs from
    :return: A tuple containing the student ID and Peppi ID, or None if either ID could not be found
    """

    numbers = re.findall(r'\d{6,7}', text)
    student_id = None
    peppi_id = None

    for num in numbers:
        if len(num) == 7 and not student_id:
            student_id = num
        elif len(num) == 6 and not peppi_id:
            peppi_id = num
    return student_id, peppi_id

print("Started scanning for blue...")

# Main loop
while True:
    timestamp = int(time.time())
    filename = f"snapshot_{timestamp}.jpg"
    
    # Maak snapshot
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

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

    print(f"Blue detected: {blue_ratio:.2%}")

    if blue_ratio > 0.2:
        print(f"Enough blue, scanning...")

        # Preprocessing
        processed = preprocess(image)
        processed_filename = f"preprocessed_{timestamp}.png"
        cv2.imwrite(processed_filename, processed)

        # OCR
        custom_config = r'--oem 3 --psm 6'
        raw_text = pytesseract.image_to_string(processed, config=custom_config)

        print("Scanned text:")
        print(raw_text.strip())

        # IDs extracten
        student_id, peppi_id = extract_ids(raw_text)

        print("\nResult:")
        if student_id:
            print(f"Student ID: {student_id}")
            session = get_active_session()
            response = add_attendance(student_id, session.id)
        else:
            print("No Student ID found.")

        # Wait before scanning again
        time.sleep(3)

    else:
        # Wait before scanning again
        time.sleep(0.5)

