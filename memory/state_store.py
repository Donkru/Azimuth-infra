from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "system_state_history.json"


def _load_history() -> list[dict]:
    if not STATE_FILE.exists():
        return []

    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def _save_history(history: list[dict]) -> None:
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def save_system_state(snapshot: dict, max_entries: int = 100) -> None:
    history = _load_history()

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        **snapshot,
    }

    history.append(entry)
    history = history[-max_entries:]

    _save_history(history)


def get_recent_system_states(limit: int = 5) -> list[dict]:
    history = _load_history()
    return history[-limit:]


def get_last_system_state() -> dict | None:
    history = _load_history()
    if not history:
        return None
    return history[-1]
