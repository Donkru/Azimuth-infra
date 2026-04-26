"""
Build the message list passed to an LLM client.

This module is provider-agnostic — it produces a generic list of
{role, content} dicts. Concrete clients (LocalLLMClient,
AnthropicClient, etc.) translate that into their own wire format.
"""
from __future__ import annotations

from typing import Iterable


def build_messages(
        user_message: str,
        history: Iterable[dict] | None = None,
        *,
        history_limit: int = 12,
) -> list[dict]:
    """
    Return a list of role/content dicts, oldest first, with the new
    user message appended at the end.

    History entries are filtered to known roles only, missing fields
    are tolerated (skipped silently), and the result is capped at
    ``history_limit`` past turns.
    """
    if not user_message or not user_message.strip():
        raise ValueError("user_message is required")

    valid_roles = {"user", "assistant", "system"}
    cleaned: list[dict] = []
    for turn in (history or []):
        role = (turn.get("role") or "").strip()
        content = turn.get("content")
        if role not in valid_roles or not content:
            continue
        cleaned.append({"role": role, "content": str(content)})

    if len(cleaned) > history_limit:
        cleaned = cleaned[-history_limit:]

    cleaned.append({"role": "user", "content": user_message.strip()})
    return cleaned
