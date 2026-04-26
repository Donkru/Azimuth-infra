"""
Sentinel runtime settings.

Centralised configuration for the Sentinel runtime.
Reads sensitive values from environment variables (loaded from .env),
and computes safe defaults for paths.
"""
from __future__ import annotations

import os
from pathlib import Path

# ─── Project paths ──────────────────────────────────────────────────────────
# settings.py is at: <PROJECT>/agent/sentinel/config/settings.py
# parents[3]      → <PROJECT>/
PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]

# ─── Database ────────────────────────────────────────────────────────────────
DATA_DIR: Path = PROJECT_ROOT / "agent" / "sentinel" / "data"
DB_PATH: Path = Path(os.getenv("DB_PATH", DATA_DIR / "chatbot.db"))

# ─── LLM ─────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "claude-sonnet-4-6")
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))

# ─── Sentinel runtime ────────────────────────────────────────────────────────
SENTINEL_HOST: str = os.getenv("SENTINEL_HOST", "0.0.0.0")
SENTINEL_PORT: int = int(os.getenv("SENTINEL_PORT", "8000"))
LOG_LEVEL: str = os.getenv("SENTINEL_LOG_LEVEL", "INFO")

# ─── Telemetry ───────────────────────────────────────────────────────────────
TELEMETRY_INTERVAL_SECONDS: int = int(os.getenv("TELEMETRY_INTERVAL_SECONDS", "5"))
TELEMETRY_TOP_N_PROCESSES: int = int(os.getenv("TELEMETRY_TOP_N_PROCESSES", "10"))

# ─── Backwards-compatible aliases (kept for legacy imports) ─────────────────
HOST: str = SENTINEL_HOST
PORT: int = SENTINEL_PORT

# ─── LLM system prompt ──────────────────────────────────────────────────────
SYSTEM_PROMPT: str = (
    "You are a local server-side assistant. "
    "Be concise, factual, and useful."
)

# ─── Log directory (used by legacy code) ────────────────────────────────────
LOG_DIR = PROJECT_ROOT / "agent" / "sentinel" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ─── Backwards-compatible aliases ───────────────────────────────────────────
HOST: str = SENTINEL_HOST
PORT: int = SENTINEL_PORT

# ─── LLM system prompt ──────────────────────────────────────────────────────
SYSTEM_PROMPT: str = (
    "You are a local server-side assistant. "
    "Be concise, factual, and useful."
)

# ─── Log directory ──────────────────────────────────────────────────────────
LOG_DIR = PROJECT_ROOT / "agent" / "sentinel" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
