"""
Sentinel persistence — the public store API.
"""
from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .schema import Base, Message

logger = logging.getLogger(__name__)

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _resolve_db_path() -> str:
    try:
        from agent.sentinel.config.settings import DB_PATH
    except ImportError as exc:
        raise RuntimeError(
            "Cannot resolve DB_PATH. Ensure agent/sentinel/config/settings.py "
            "defines DB_PATH (e.g. DB_PATH = 'agent/sentinel/data/chatbot.db')."
        ) from exc
    return str(DB_PATH)


def _get_engine() -> Engine:
    global _engine, _SessionLocal
    if _engine is None:
        db_path = _resolve_db_path()
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False,
            future=True,
            connect_args={"check_same_thread": False},
        )
        _SessionLocal = sessionmaker(
            bind=_engine, autoflush=False, autocommit=False, future=True
        )
        logger.info("Sentinel store engine bound to %s", db_path)
    return _engine


@contextmanager
def _session_scope() -> Iterator[Session]:
    _get_engine()
    assert _SessionLocal is not None
    db = _SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def initialize_database() -> None:
    """Create all tables if they do not already exist."""
    engine = _get_engine()
    Base.metadata.create_all(bind=engine)
    logger.info("Sentinel schema initialised")


class SentinelStore:
    """The only object the runtime should use to read or write Sentinel state."""

    def save_message(self, session_id: str, role: str, content: str) -> int:
        if not session_id:
            raise ValueError("session_id is required")
        if not role:
            raise ValueError("role is required")
        if content is None:
            raise ValueError("content is required (use '' for empty body)")

        with _session_scope() as db:
            msg = Message(session_id=session_id, role=role, content=content)
            db.add(msg)
            db.flush()
            return int(msg.id)

    def get_recent_messages(self, session_id: str, limit: int = 12) -> list[dict]:
        if limit < 1:
            raise ValueError("limit must be >= 1")

        with _session_scope() as db:
            rows = (
                db.query(Message)
                .filter(Message.session_id == session_id)
                .order_by(Message.id.desc())
                .limit(limit)
                .all()
            )
            rows.reverse()
            return [
                {
                    "role": r.role,
                    "content": r.content,
                    "created_at": r.created_at.isoformat(),
                }
                for r in rows
            ]

    def message_count(self, session_id: str | None = None) -> int:
        with _session_scope() as db:
            q = db.query(Message)
            if session_id is not None:
                q = q.filter(Message.session_id == session_id)
            return int(q.count())

    def list_sessions(self) -> list[str]:
        with _session_scope() as db:
            rows = db.query(Message.session_id).distinct().all()
            return sorted(r[0] for r in rows)
