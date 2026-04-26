"""
Database schema for Sentinel persistence.

Tables defined here are owned by the persistence layer.
Callers must not query these models directly — go through SentinelStore.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Index, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Message(Base):
    """A single message in a conversation session."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(128), nullable=False)
    role = Column(String(32), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_messages_session_created", "session_id", "created_at"),
    )

    def __repr__(self) -> str:
        return (
            f"Message(id={self.id}, session={self.session_id!r}, "
            f"role={self.role!r}, len={len(self.content or '')})"
        )
