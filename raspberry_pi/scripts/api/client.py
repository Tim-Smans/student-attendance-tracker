import requests
from config import API_KEY, BASE_URL

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

BASE_URL = BASE_URL


def post(path, payload):
    return requests.post(f"{BASE_URL}/{path}", json=payload, headers=headers)

def get(path):
    return requests.get(f"{BASE_URL}/{path}", headers=headers)