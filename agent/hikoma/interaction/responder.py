"""HiKOMaResponder — the agent-layer fallback responder."""
from __future__ import annotations
import logging
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_HIKOMA_PERSONA: str = (
    "You are HiKOMa, the conversational layer of the Azimuth platform. "
    "You speak for Sentinel but you are not Sentinel. You are concise, "
    "technical, and never invent telemetry data. If the user asks about "
    "live system state, prefer to defer to Sentinel rather than guess. "
    "Plain text only, short paragraphs, no markdown."
)


class HiKOMaResponder:
    """Owns the LLM client. Sentinel must not bypass this."""

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
                "HiKOMa could not match this request to a known intent and "
                "no language model is configured. Try one of: 'status', "
                "'report', 'processes', or 'uptime'.",
                False,
            )

        try:
            answer = self._llm.generate(
                user_text,
                system_prompt=self._persona,
                history=history,
            )
            return (answer, True)
        except Exception as exc:
            logger.exception("HiKOMa LLM call failed")
            return (
                f"HiKOMa could not reach the language model. ({exc.__class__.__name__})",
                False,
            )
