from agent.sentinel.runtime.session import Session


class SentinelInterpreter:
    """
    SentinelInterpreter classifies operator intent from session input
    and stores the resulting intent in session context.

    Example intents:
    - status_request
    - report_request
    - process_request
    - unknown
    """

    def interpret(self, session: Session) -> Session:
        input_text = (session.input_text or "").strip().lower()

        if not input_text:
            intent = "unknown"
        elif any(phrase in input_text for phrase in ["what is happening", "what's happening", "what is going on"]):
            intent = "status_request"
        elif any(word in input_text for word in ["status", "health", "state", "uptime"]):
            intent = "status_request"
        elif any(word in input_text for word in ["report", "summary", "overview"]):
            intent = "report_request"
        elif any(word in input_text for word in ["process", "task", "job"]):
            intent = "process_request"
        else:
            intent = "unknown"

        return session.merge_context({"intent": intent})