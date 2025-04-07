from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
print("Loaded api key: " + API_KEY)

BASE_URL = "https://student-attendance-tracker-ungw.onrender.com"