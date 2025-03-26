import requests

BASE_URL = "https://student-attendance-tracker-ungw.onrender.com"  # Verander dit naar je Render URL als nodig
API_KEY = "4ee1fc3d3a9aa6d1ffec21c094c93fa9"       # Als je API beveiligd is met een key

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY  # Verwijder deze regel als je geen key gebruikt
}

attendance = {
    "student_id": "12345",
    "room": "Lokaal B101"
}

print("\n🕒 Attendance registreren...")
res = requests.post(f"{BASE_URL}/attendance", json=attendance, headers=headers)
print("Status:", res.status_code)
print("Response:", res.json())