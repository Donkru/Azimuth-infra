from agent.sentinel.runtime.session import Session


class SentinelPlanner:
    """
    SentinelPlanner converts interpreted session intent into
    a simple ordered list of decision steps.

    It does not execute tools or produce output directly.
    It only defines what the agent should do next.
    """

    def plan(self, session: Session) -> list[str]:
        intent = session.context.get("intent", "unknown")

        plan_map: dict[str, list[str]] = {
            "status_request": ["gather_status", "summarize_status"],
            "report_request": ["gather_report", "summarize_report"],
            "process_request": ["gather_processes", "summarize_processes"],
            "unknown": ["fallback_response"],
        }

        return plan_map.get(intent, ["fallback_response"])