import sys
from api.client import post

BASE_URL = "https://student-attendance-tracker-ungw.onrender.com/"

if len(sys.argv) < 3:
    print("Usage: python setup.py <room_name> <device_identifier> <api_key>")
    exit(1)

room_name = sys.argv[1]
device_identifier = sys.argv[2]
API_KEY = sys.argv[3]


headers = {
    "x-api-key": f"{API_KEY}"
}

res = post("room_device", {"room_name": room_name, "device_identifier": device_identifier}, headers=headers)

if res.status_code != 201:
  print(res.text)
  exit(1)


print("Room device created successfully!")