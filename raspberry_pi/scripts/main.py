from picamera2 import Picamera2
import cv2
from pyzbar.pyzbar import decode
from .decoder import decode_qr

# Initiasing the camera, configuring size, format and alignment.
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

picam2.set_controls({
    "ExposureTime": 8000,  # in microseconds (8ms)
    "AnalogueGain": 2.0,   # keep low to keep noise down
    "FrameDurationLimits": (10000, 10000),  # max ~100fps
    "Contrast": 1.5,
    "Sharpness": 2,
})

# Functie om te checken of een afbeelding te wazig is
def is_blurry(img, threshold=100.0):
    laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian_var < threshold

print("Scanning QR codes... Press 'q' to quit.")

previous_data = None
last_scan_time = 0


# Main loop, will keep running until it receives the 'q' key
while True:
    # Creates a snapshot of the camera
    frame = picam2.capture_array()
    
    # Check scherpte
    if is_blurry(frame):
        cv2.putText(frame, "Too Blurry - move the QR code", (40, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
    # QR decoding
    qr_codes = decode(frame)

    previous_data, last_scan_time = decode_qr(qr_codes, frame, previous_data, last_scan_time)    
    # Show frame to the user
    cv2.imshow("QR Scanner", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.close()
cv2.destroyAllWindows()
