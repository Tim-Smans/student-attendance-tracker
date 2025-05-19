import sys
import requests


BASE_URL = "https://tracker.timsmans.be/api/"

if len(sys.argv) < 3:
    print("Usage: python setup.py <room_name> <device_identifier> <api_key>")
    exit(1)

room_name = sys.argv[1]
device_identifier = sys.argv[2]
API_KEY = sys.argv[3]


headers = {
    "x-api-key": f"{API_KEY}"
}


payload = {
  "room_name": room_name, "device_identifier": device_identifier
}
res = requests.post(BASE_URL + "roomdevices/", json=payload, headers=headers)

if res.status_code != 201:
  print(res.text)
  exit(1)


print("Room device created successfully!")