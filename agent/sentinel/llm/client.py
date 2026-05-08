"""LLM client protocol and a local fallback implementation."""
from __future__ import annotations
import logging
from typing import Iterable, Optional, Protocol

logger = logging.getLogger(__name__)


class LLMClient(Protocol):
    def generate(self, prompt: str, *,
                 system_prompt: Optional[str] = None,
                 history: Optional[Iterable[dict]] = None) -> str: ...


class LocalLLMClient:
    """Local-only client backed by the keyword-matching LocalModel."""

    def __init__(self) -> None:
        from agent.sentinel.model import LocalModel
        self._model = LocalModel()

    def generate(self, prompt: str, *,
                 system_prompt: Optional[str] = None,
                 history: Optional[Iterable[dict]] = None) -> str:
        if system_prompt:
            logger.debug("LocalLLMClient ignoring system prompt: %r",
                         system_prompt[:60])
        recent = []
        for turn in (history or []):
            role = (turn.get("role") or "").strip()
            content = turn.get("content")
            if role in {"user", "assistant"} and content:
                recent.append({"role": role, "content": str(content)})
        return self._model.generate(prompt, recent)
