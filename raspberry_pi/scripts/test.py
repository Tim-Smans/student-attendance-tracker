

import requests

from config import API_KEY, BASE_URL

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}


response = requests.get(f"{BASE_URL}/student/", headers=headers)
print(response.json())