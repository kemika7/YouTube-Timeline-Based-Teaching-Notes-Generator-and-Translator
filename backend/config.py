import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
CACHE_DIR = os.getenv("CACHE_DIR", ".cache")
HISTORY_FILE = os.getenv("HISTORY_FILE", ".cache/history.json")
PORT = int(os.getenv("PORT", "8000"))
