from agent.sentinel.runtime.session import Session
from agent.sentinel.tools.registry import ToolRegistry


class ToolExecutor:
    """
    ToolExecutor executes registered tools for planned decision steps
    and returns the updated Session.
    """

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute(self, session: Session, decisions: list[str]) -> Session:
        executed_tools: list[str] = list(session.selected_tools)

        for decision in decisions:
            tool = self.registry.get(decision)

            if tool is None:
                session = session.with_decision(f"missing_tool:{decision}")
                continue

            executed_tools.append(decision)
            session = session.with_selected_tools(executed_tools)

            try:
                session = tool(session)
            except Exception as e:
                session = (
                    session
                    .with_status("failed")
                    .with_output(f"Error executing '{decision}': {e}")
                    .merge_metadata({"error": str(e), "failed_decision": decision})
                )
                return session

        return session