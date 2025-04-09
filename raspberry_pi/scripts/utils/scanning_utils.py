import re
import cv2

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

    numbers = re.findall(r'\b\d{6,7}\b', text)
    student_id = None
    peppi_id = None

    for num in numbers:
        if len(num) == 7 and not student_id:
            student_id = num
        elif len(num) == 6 and not peppi_id:
            peppi_id = num
    return student_id, peppi_id