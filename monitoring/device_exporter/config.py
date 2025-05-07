from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://student-attendance-tracker-ungw.onrender.com"

if not API_KEY:
    raise ValueError("API_KEY is not set in .env or environment variables.")
