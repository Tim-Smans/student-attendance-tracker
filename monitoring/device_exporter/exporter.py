from prometheus_client import start_http_server, Gauge
import requests
import time
from config import API_KEY, BASE_URL

device_up = Gauge('device_up', 'Device online status', ['device_id'])
devices = set() 

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def update_status():
    for device_id in devices:
        try:
            res = requests.get(f'{BASE_URL}/status/is_online/{device_id}', headers=headers)
            status = res.json().get('online', False)
            device_up.labels(device_id=device_id).set(1 if status else 0)
        except Exception as e:
            device_up.labels(device_id=device_id).set(0)
            print(f"[ERROR] Device {device_id} check failed: {e}")


def get_device_ids():
    try:
        res = requests.get(f"{BASE_URL}/roomdevices/", headers=headers)
        data = res.json()['items']

        for device in data:
            devices.add(device['device_identifier'])
    except Exception as e:
      print(f"[ERROR] Something failed: {e}")

if __name__ == "__main__":
    start_http_server(8000)
    get_device_ids()  
    while True:
        update_status()
        time.sleep(60)
