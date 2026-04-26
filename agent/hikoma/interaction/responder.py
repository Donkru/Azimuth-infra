"""HiKOMaResponder — the agent-layer fallback responder."""
from __future__ import annotations
import logging
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_HIKOMA_PERSONA: str = (
    "You are HiKOMa, the conversational layer of the Azimuth platform. "
    "You speak for Sentinel but you are not Sentinel. You are concise, "
    "technical, and never invent telemetry data."
)


class HiKOMaResponder:
    """Generates a reply when Sentinel's intent classifier returned 'unknown'."""

    def __init__(self, llm_client=None, *, persona: str = DEFAULT_HIKOMA_PERSONA):
        self._llm = llm_client
        self._persona = persona

    @property
    def has_llm(self) -> bool:
        return self._llm is not None

    def respond(self, session) -> tuple[str, bool]:
        user_text = (session.input_text or "").strip()
        history = session.context.get("history", [])

        if self._llm is None:
            return (
                "HiKOMa could not match this request to a known intent and no "
                "language model is configured. Try: 'status', 'report', "
                "'processes', or 'uptime'.",
                False,
            )
        try:
            answer = self._llm.generate(
                system_prompt=self._persona,
                user_message=user_text,
                history=history,
            )
            return (answer, True)
        except Exception as exc:
            logger.exception("HiKOMa LLM call failed")
            return (
                f"HiKOMa could not reach the language model. ({exc.__class__.__name__})",
                False,
            )
