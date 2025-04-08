import cv2
import pytesseract
import re
import time
import os
import numpy as np

while True:
    key = input("Press enter to take a picture, or type 'q' to stop: ")

    if key == 'q':
        break

    # When the user presses enter it will take a picture
    timestamp = int(time.time())
    filename = f"capture_{timestamp}.jpg"
    os.system(f'libcamera-jpeg -o {filename} --width 1280 --height 720 --nopreview')

    # Load the picture into OpenCV
    image = cv2.imread(filename)
    if image is None:
        print("Error: No image found  .")
        continue

    # Preprocessing the image
    # 1. put the picture into grayscale
    # 2. Better contract with CLAHE (Contrast limited adaptive histogram equalization)
    # 3. Gaussian blur to reduce noise
    # 4. Thresholding (we want to focus on the text) 130 is the threshold everything above 130 becomes white, everything under 130 becomes black
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
    _, processed = cv2.threshold(blurred, 130, 255, cv2.THRESH_BINARY)

    # Save the prepocessed image (just for debugging and tweaking)
    processed_filename = f"preprocessed_{timestamp}.png"
    cv2.imwrite(processed_filename, processed)
    print(f"Preprocessed opgeslagen als: {processed_filename}")

    # Using the OCR model to extract the text and put it into a variable
    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(processed, config=custom_config)

    # Find all numbers in the image using regex
    numbers = re.findall(r'\d{6,7}', raw_text)

    # Initialise IDs
    student_id = None
    peppi_id = None

    # Check if the number is 6 or 7 digits, if it is 6 it is a peppi id, if it is 7 it is a student id (Temporary workaround)
    for num in numbers:
        if len(num) == 7:
            student_id = num
        elif len(num) == 6:
            peppi_id = num

    # Output logs
    print("\n📋 Scanned text:")
    print(raw_text.strip())

    print("\n Extracted IDs:")
    if student_id:
        print(f"Student ID: {student_id}")
    else:
        print("No Student ID found.")

    if peppi_id:
        print(f"Peppi ID: {peppi_id}")
    else:
        print("No Peppi ID found.")
