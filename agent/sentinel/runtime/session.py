from dataclasses import dataclass, field, replace
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Session:
    session_id: str = field(default_factory=lambda: str(uuid4()))
    input_text: str = ""
    context: dict[str, Any] = field(default_factory=dict)
    decisions: list[str] = field(default_factory=list)
    selected_tools: list[str] = field(default_factory=list)
    output: str | None = None
    status: str = "initialized"
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def initialize(input_text: str = "") -> "Session":
        return Session(input_text=input_text)

    def merge_context(self, updates: dict[str, Any]) -> "Session":
        new_context = dict(self.context)
        new_context.update(updates)
        return replace(self, context=new_context)

    def with_decision(self, decision: str) -> "Session":
        return replace(self, decisions=[*self.decisions, decision])

    def with_selected_tools(self, tools: list[str]) -> "Session":
        return replace(self, selected_tools=tools)

    def with_output(self, output: str) -> "Session":
        return replace(self, output=output)

    def with_status(self, status: str) -> "Session":
        return replace(self, status=status)

    def merge_metadata(self, updates: dict[str, Any]) -> "Session":
        new_metadata = dict(self.metadata)
        new_metadata.update(updates)
        return replace(self, metadata=new_metadata)
        