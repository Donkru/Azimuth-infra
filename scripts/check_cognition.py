"""End-to-end check of the Sentinel cognition loop with HiKOMa fallback."""
from __future__ import annotations
import logging, sys

from agent.hikoma.interaction.responder import HiKOMaResponder
from agent.sentinel.cognition.decision_engine import SentinelDecisionEngine
from agent.sentinel.cognition.interpreter import SentinelInterpreter
from agent.sentinel.cognition.planner import SentinelPlanner
from agent.sentinel.llm.client import LocalLLMClient
from agent.sentinel.runtime.session import Session

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("check_cognition")

CASES = [
    ("status",                         "status_request"),
    ("what is happening on my system", "status_request"),
    ("give me a full report",          "report_request"),
    ("show me the top processes",      "process_request"),
    ("write me a haiku about CPUs",    "unknown"),
]


def run_one(query, expected, interp, plan, engine):
    log.info("─" * 60)
    log.info("Q: %s", query)
    session = interp.interpret(Session(input_text=query))
    intent = session.context.get("intent")
    log.info("intent  → %s", intent)
    if intent != expected:
        log.error("expected %r, got %r", expected, intent)
        return False
    steps = plan.plan(session)
    log.info("plan    → %s", steps)
    result = engine.execute(session, steps)
    log.info("steps   → %s", result.steps_run)
    log.info("llm     → %s", result.used_llm)
    if result.errors:
        log.warning("errors  → %s", result.errors)
    log.info("output  →\n%s", result.output)
    return True


def main() -> int:
    interpreter = SentinelInterpreter()
    planner = SentinelPlanner()
    responder = HiKOMaResponder(llm_client=LocalLLMClient())
    engine = SentinelDecisionEngine(responder=responder)

    failures = sum(1 for q, e in CASES if not run_one(q, e, interpreter, planner, engine))
    log.info("─" * 60)
    if failures:
        log.error("%d / %d cases failed", failures, len(CASES))
        return 1
    log.info("all %d cases passed", len(CASES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
