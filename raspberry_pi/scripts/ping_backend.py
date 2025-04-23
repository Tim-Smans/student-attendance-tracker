

import requests

from scripts.utils.device_utils import get_device_identifier

PI_ID = get_device_identifier()  # unieke naam of UUID
API_URL = "https://student-attendance-tracker-ungw.onrender.com/api/ping"

try:
    requests.post(API_URL, json={"id": PI_ID})
except Exception:
    pass