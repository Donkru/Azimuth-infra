"""
LLM client interface and a local fallback implementation.

Two classes:

  LLMClient   — protocol every concrete client must implement.
  LocalLLMClient — no-network implementation that wraps the existing
                   keyword-matching LocalModel. Useful for development and
                   for environments without an Anthropic API key.

When you wire up Anthropic later, write an ``AnthropicClient`` that also
implements the LLMClient interface and inject it into SentinelDecisionEngine
in place of LocalLLMClient. No other module needs to change.
"""
from __future__ import annotations

import logging
from typing import Iterable, Protocol

from .message_builder import build_messages
from .prompts import DEFAULT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------

class LLMClient(Protocol):
    """Every concrete LLM client must implement this single method."""

    def generate(
            self,
            system_prompt: str,
            user_message: str,
            history: Iterable[dict] | None = None,
    ) -> str: ...


# ---------------------------------------------------------------------------
# Local implementation (no network)
# ---------------------------------------------------------------------------

class LocalLLMClient:
    """
    Local-only LLM client backed by the existing LocalModel keyword router.

    This is NOT a real language model. It exists so the cognition loop can be
    exercised end-to-end (interpret → plan → execute → fallback) without
    requiring an external API. Swap in a real client when you're ready.
    """

    def __init__(self) -> None:
        # Import here to avoid a hard dependency at module load
        from agent.sentinel.model import LocalModel
        self._model = LocalModel()

    def generate(
            self,
            system_prompt: str,
            user_message: str,
            history: Iterable[dict] | None = None,
    ) -> str:
        # build_messages validates inputs and trims history
        messages = build_messages(user_message, history)

        # The LocalModel signature predates this layer, so adapt:
        # it expects (user_message, history_list) and ignores system_prompt.
        recent = [m for m in messages[:-1] if m["role"] != "system"]
        new_msg = messages[-1]["content"]

        if system_prompt and system_prompt != DEFAULT_SYSTEM_PROMPT:
            logger.debug("LocalLLMClient ignoring custom system prompt: %r",
                         system_prompt[:60])

        return self._model.generate(new_msg, recent)
