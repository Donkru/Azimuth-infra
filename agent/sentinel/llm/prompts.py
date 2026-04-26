"""
Centralised prompt templates for the Sentinel LLM layer.

Keep prompts here so they can be versioned, tested, and audited
without touching the client or the decision engine.
"""
from __future__ import annotations

# Default system prompt used when no override is provided.
# Mirrors agent.sentinel.config.settings.SYSTEM_PROMPT but lives here
# so the LLM layer can be packaged independently.
DEFAULT_SYSTEM_PROMPT: str = (
    "You are Sentinel, the local server-side intelligence layer of the "
    "Azimuth platform. You are technical, concise, and accurate. "
    "Never invent telemetry data — if you do not have a number, say so. "
    "Prefer short paragraphs over long ones. Use plain text, no markdown."
)


# Few-shot or persona suffixes can be appended here as the project grows.
FALLBACK_NUDGE: str = (
    "If the user is asking about live system state (CPU, RAM, disk, "
    "processes, uptime), tell them to use the matching keyword: "
    "'status', 'report', 'processes', or 'uptime'."
)
