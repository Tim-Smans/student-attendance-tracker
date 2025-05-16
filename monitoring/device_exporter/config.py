from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://34.88.154.35/api"

if not API_KEY:
    raise ValueError("API_KEY is not set in .env or environment variables.")
