"""Quick check that the Sentinel persistence layer works end-to-end."""
from __future__ import annotations
import logging, sys, uuid
from agent.sentinel.memory import SentinelStore, initialize_database

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("check_memory_store")


def main() -> int:
    log.info("Initialising database...")
    initialize_database()
    store = SentinelStore()
    sid = f"diag-{uuid.uuid4().hex[:8]}"
    log.info("Using diagnostic session: %s", sid)

    store.save_message(sid, "user", "ping")
    store.save_message(sid, "assistant", "pong")
    store.save_message(sid, "user", "status?")

    if store.message_count(sid) != 3:
        log.error("Expected 3 messages, got %d", store.message_count(sid))
        return 1

    for msg in store.get_recent_messages(sid, limit=10):
        log.info("  [%s] %s: %s", msg["created_at"], msg["role"], msg["content"])

    log.info("Store healthy. Sessions: %d  Messages: %d",
             len(store.list_sessions()), store.message_count())
    return 0


if __name__ == "__main__":
    sys.exit(main())
