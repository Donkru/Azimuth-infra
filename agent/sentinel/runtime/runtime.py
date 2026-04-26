"""SentinelRuntime - execution entry point with persistent memory."""
from __future__ import annotations

import logging
import uuid
from dataclasses import replace
from typing import Any, Optional

from agent.sentinel.runtime.orchestrator import Orchestrator
from agent.sentinel.runtime.session import Session

logger = logging.getLogger(__name__)
DEFAULT_HISTORY_LIMIT = 12


class SentinelRuntime:
    """Execution entry point. Owns persistence; orchestrator stays pure."""

    def __init__(self, orchestrator: Orchestrator, *, store=None,
                 history_limit: int = DEFAULT_HISTORY_LIMIT):
        self.orchestrator = orchestrator
        self.store = store
        self.history_limit = history_limit

    def run(self, input_text: str, session_id: Optional[str] = None,
            metadata: Optional[dict] = None,
            context: Optional[dict] = None) -> Session:
        sid = session_id or f"runtime-{uuid.uuid4().hex[:12]}"
        session = Session.initialize(input_text=input_text)
        session = replace(session, session_id=sid)

        if metadata:
            session = session.merge_metadata(metadata)
        if context:
            session = session.merge_context(context)

        history = self._load_history(sid)
        if history:
            session = session.merge_context({"history": history})

        session = session.with_status("running")

        try:
            session = self.orchestrator.run(session)
            if session.status == "running":
                session = session.with_status("completed")
            self._persist_turn(sid, "user", input_text)
            if session.output:
                self._persist_turn(sid, "assistant", session.output)
            return session
        except Exception as exc:
            err = str(exc)
            logger.exception("SentinelRuntime failed for session %s", sid)
            self._persist_turn(sid, "user", input_text)
            return (session.with_status("failed")
                    .with_output(err)
                    .merge_metadata({"error": err}))

    def _load_history(self, session_id: str) -> list[dict]:
        if self.store is None:
            return []
        try:
            rows = self.store.get_recent_messages(session_id, limit=self.history_limit)
        except Exception:
            logger.exception("history load failed for session %s", session_id)
            return []
        return [{"role": r["role"], "content": r["content"]}
                for r in rows
                if r.get("role") and r.get("content") is not None]

    def _persist_turn(self, session_id: str, role: str, content: str) -> None:
        if self.store is None or not content:
            return
        try:
            self.store.save_message(session_id, role, content)
        except Exception:
            logger.exception("save_message failed for session %s role %s",
                             session_id, role)
