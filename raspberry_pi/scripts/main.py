from picamera2 import Picamera2
import cv2
from pyzbar.pyzbar import decode
from .utils.image_utils import is_blurry
from .utils.camera import init_camera
from .utils.decoder import decode_qr

# Initiasing the camera, configuring size, format and alignment.
picam2 = init_camera()

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
