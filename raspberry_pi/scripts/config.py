from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
print("Loaded api key: " + API_KEY)

BASE_URL = "http://34.88.154.35/api"

USE_SENSORS = True