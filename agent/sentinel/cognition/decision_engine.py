"""SentinelDecisionEngine — orchestrates plan execution. No LLM, no telemetry."""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from agent.sentinel.runtime.session import Session

logger = logging.getLogger(__name__)


@dataclass
class DecisionResult:
    output: str = ""
    steps_run: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)
    used_llm: bool = False
    errors: list[str] = field(default_factory=list)

    def append_output(self, text: str) -> None:
        if not text:
            return
        self.output = self.output + "\n\n" + text if self.output else text


StepHandler = Callable[[Session, DecisionResult], None]
FALLBACK_STEP = "fallback_response"


class SentinelDecisionEngine:
    """Executes a plan. Owns no business logic — delegates to tools and HiKOMa."""

    def __init__(self, responder: Optional[Any] = None) -> None:
        self._responder = responder
        self._handlers: dict[str, StepHandler] = {}
        self._load_default_handlers()

    def execute(self, session: Session, plan: list[str]) -> DecisionResult:
        result = DecisionResult()
        for step in plan:
            if step == FALLBACK_STEP:
                self._run_fallback(session, result)
                result.steps_run.append(step)
                continue
            handler = self._handlers.get(step)
            if handler is None:
                result.errors.append(f"no handler for step: {step!r}")
                continue
            try:
                handler(session, result)
                result.steps_run.append(step)
            except Exception as exc:
                logger.exception("step %r failed", step)
                result.errors.append(f"step {step!r} failed: {exc}")
        if not result.output and not result.errors:
            result.output = "Sentinel completed the plan but produced no output."
        return result

    def register(self, step_name: str, handler: StepHandler) -> None:
        self._handlers[step_name] = handler

    def _load_default_handlers(self) -> None:
        from agent.sentinel.tools.system_tools import SYSTEM_HANDLERS
        self._handlers.update(SYSTEM_HANDLERS)

    def _run_fallback(self, session: Session, result: DecisionResult) -> None:
        if self._responder is None:
            result.append_output(
                "Sentinel could not match this request and no HiKOMa responder "
                "is configured. Try: 'status', 'report', 'processes', 'uptime'."
            )
            return
        try:
            text, used_llm = self._responder.respond(session)
            result.used_llm = used_llm
            result.append_output(text)
        except Exception as exc:
            logger.exception("HiKOMa responder failed")
            result.errors.append(f"responder failed: {exc}")
            result.append_output("Sentinel asked HiKOMa to respond but the call failed.")
