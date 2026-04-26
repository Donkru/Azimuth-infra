from typing import Callable

from agent.sentinel.runtime.session import Session
from agent.sentinel.tools.system_tools import (
    gather_status,
    summarize_status,
)


class ToolRegistry:
    """
    ToolRegistry manages the mapping between decision names
    and their corresponding tool handler functions.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[[Session], Session]] = {}

    def register(self, name: str, handler: Callable[[Session], Session]) -> None:
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered.")
        self._tools[name] = handler

    def get(self, name: str) -> Callable[[Session], Session] | None:
        return self._tools.get(name)

    def has(self, name: str) -> bool:
        return name in self._tools

    def list(self) -> list[str]:
        return list(self._tools.keys())


def bootstrap_tools() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register("gather_status", gather_status)
    registry.register("summarize_status", summarize_status)

    return registry