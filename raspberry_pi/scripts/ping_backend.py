

import os
from dotenv import load_dotenv
import requests

from utils.device_utils import get_device_identifier

load_dotenv()
API_KEY = os.getenv("API_KEY")

PI_ID = get_device_identifier()  # unieke naam of UUID
API_URL = "http://34.88.154.35/api/status/ping"

try:
    resp = requests.post(API_URL, json={"id": PI_ID}, headers={"x-api-key": API_KEY})
    print(resp.text)
    print(resp.status_code)
except Exception:
    pass