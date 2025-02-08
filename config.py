import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
INSTITUTE_CHAT_ID = os.getenv("INSTITUTE_CHAT_ID")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
