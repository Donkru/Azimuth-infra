"""End-to-end check of SentinelRuntime with SentinelStore persistence."""
from __future__ import annotations
import logging, sys, uuid

from agent.hikoma.interaction.responder import HiKOMaResponder
from agent.sentinel.cognition.decision_engine import SentinelDecisionEngine
from agent.sentinel.llm.client import LocalLLMClient
from agent.sentinel.memory import SentinelStore, initialize_database
from agent.sentinel.runtime.orchestrator import SentinelOrchestrator
from agent.sentinel.runtime.runtime import SentinelRuntime

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("check_runtime")


def banner(text):
    log.info("─" * 60)
    log.info(text)


def main():
    initialize_database()
    store = SentinelStore()

    responder = HiKOMaResponder(llm_client=LocalLLMClient())
    engine = SentinelDecisionEngine(responder=responder)
    orch = SentinelOrchestrator(engine=engine)
    runtime = SentinelRuntime(orch, store=store)

    sid_before = store.message_count()
    log.info("messages in store at start: %d", sid_before)

    banner("Test 1 — one-off call (fresh session_id)")
    s1 = runtime.run("status")
    log.info("session_id : %s", s1.session_id)
    log.info("status     : %s", s1.status)
    log.info("output     :\n%s", s1.output)
    if s1.status != "completed":
        log.error("expected status 'completed', got %r", s1.status)
        return 1

    banner("Test 2 — continuation (same session_id)")
    conv = f"diag-conv-{uuid.uuid4().hex[:8]}"
    log.info("conversation id: %s", conv)
    runtime.run("status", session_id=conv)
    s3 = runtime.run("processes", session_id=conv)

    history = s3.context.get("history", [])
    log.info("history entries injected into 2nd call: %d", len(history))
    for h in history:
        snip = (h["content"][:60] + "…") if len(h["content"]) > 60 else h["content"]
        log.info("  [%s] %s", h["role"], snip)
    if len(history) < 2:
        log.error("expected at least 2 history entries, got %d", len(history))
        return 1

    banner("Test 3 — store grew after the runs")
    sid_after = store.message_count()
    log.info("messages in store at end: %d", sid_after)
    if sid_after - sid_before < 4:
        log.error("expected store to grow by at least 4, grew by %d",
                  sid_after - sid_before)
        return 1

    banner("Test 4 — replay conversation from the store")
    saved = store.get_recent_messages(conv, limit=20)
    for row in saved:
        snip = (row["content"][:80] + "…") if len(row["content"]) > 80 else row["content"]
        log.info("  [%s] %s: %s", row["created_at"], row["role"], snip)
    if len(saved) != 4:
        log.error("expected 4 saved messages, got %d", len(saved))
        return 1

    banner("all 4 tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
