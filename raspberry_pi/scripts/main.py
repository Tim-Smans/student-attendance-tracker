import subprocess
import numpy as np
import cv2
import pytesseract
import time

from scripts.utils.scanning_utils import extract_ids, preprocess
from scripts.api.attendance import add_attendance
from scripts.api.session import get_active_session

def start_camera():
    # Start libcamera-still in stream mode
    return subprocess.Popen(
        [
            "libcamera-still",
            "--inline",
            "--timeout", "0",  # One shot
            "--nopreview",
            "--output", "-",   # Output to stdout
            "--width", "1280",
            "--height", "720"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )

def read_frame(proc):
    # Read JPEG image from stdout
    data = b''
    start = False
    while True:
        byte = proc.stdout.read(1)
        if not byte:
            break
        data += byte

        # JPEG start
        if data[-2:] == b'\xff\xd8':
            start = True
        # JPEG end
        if start and data[-2:] == b'\xff\xd9':
            image = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
            return image

    return None

def main_loop():
    print("Starting live scanning...")
    proc = start_camera()

    if proc.stdout is None:
        print("Error: Failed to start camera process.")
        return

    while True:
        frame = read_frame(proc)

        if frame is None:
            print("Error: Could not read frame.")
            continue

        # Blauw detectie
        small = cv2.resize(frame, (320, 240))
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([140, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        blue_pixels = cv2.countNonZero(mask)
        total_pixels = mask.shape[0] * mask.shape[1]
        blue_ratio = blue_pixels / total_pixels

        print(f"Blue detected: {blue_ratio:.2%}")

        if blue_ratio > 0.2:
            print("Enough blue, scanning...")

            processed = preprocess(frame)

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
                print("Active session:", f"{session}")
                response = add_attendance(student_id, session["id"])
            else:
                print("No Student ID found.")

            time.sleep(3)
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    main_loop()
