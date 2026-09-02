import os
from dotenv import load_dotenv

load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Redis
REDIS_URL = os.getenv("REDIS_URL")

# Google
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Redis Vector Store
REDIS_INDEX = "RAG_1"
REDIS_KEY_PREFIX = "Apple_doc"

# Gemini Models
GEMINI_CHAT_MODEL = "models/gemini-3.5-flash-lite"
GEMINI_SEARCH_MODEL = "models/gemini-flash-lite-latest"





