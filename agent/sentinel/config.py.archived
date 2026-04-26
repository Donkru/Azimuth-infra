from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
DB_PATH = DATA_DIR / "chatbot.db"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

HOST = "0.0.0.0"
PORT = 8000

SYSTEM_PROMPT = (
    "You are a local server-side assistant. "
    "Be concise, factual, and useful."
)
