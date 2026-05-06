import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
MEMORY_DB = DATA_DIR / "memory.json"
CONFIG_FILE = DATA_DIR / "config.json"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROK_API_KEY = os.getenv("GROK_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID", "")

MODEL_NAME = "gemini-2.0-flash"
FALLBACK_MODELS = ["grok-2", "deepseek-chat"]

VOICE_MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model")
TTS_VOICE_PATH = os.path.join(BASE_DIR, "models", "piper")

WAKE_WORD = "jarvis"
LANGUAGE = "en"

MAX_MEMORY_MESSAGES = 50
PROACTIVE_CHECK_INTERVAL = 30

LOG_FILE = DATA_DIR / "clawvis.log"

SAFETY_CONFIRM_ACTIONS = [
    "delete", "format", "uninstall", "remove",
    "execute_code", "send_message", "open_url"
]

TOOL_TIMEOUT = 30
TTS_ENGINE = "pyttsx3"

DEBUG = os.getenv("DEBUG", "false").lower() == "true"