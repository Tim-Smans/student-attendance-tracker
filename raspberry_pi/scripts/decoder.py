import cv2
import numpy as np
import json
import time
import json
import time
from .api import add_attendance



def decode_qr(qr_codes, frame, previous_data, last_scan_time=0, cooldown=30):

  for qr in qr_codes:
        qr_data = qr.data.decode('utf-8')
        current_time = time.time()

        if qr_data == previous_data and (current_time - last_scan_time < cooldown):
            break
        
        
        # Update state
        previous_data = qr_data
        last_scan_time = current_time

        print(f"QR Code detected: {qr_data}")

        # Writing data to csv file
        try:
          parsed = json.loads(qr_data)
          elem_u = parsed["elem"]["u"]
          elem_i = parsed["elem"]["i"]

          
          add_attendance(elem_u, "Room " + elem_i)

        except json.JSONDecodeError:
          print("Invalid JSON data")
        except KeyError:
          print("Invalid JSON data")

        # Draw rectangle around the QR code
        pts = qr.polygon
        pts = [(point.x, point.y) for point in pts]
        cv2.polylines(frame, [np.array(pts)], True, (0, 255, 0), 2)

  return previous_data, last_scan_time