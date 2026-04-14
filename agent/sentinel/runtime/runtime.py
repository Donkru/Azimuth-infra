from typing import Any

from agent.sentinel.runtime.session import Session
from agent.sentinel.runtime.orchestrator import Orchestrator


class SentinelRuntime:
    """
    SentinelRuntime is the execution entry point for the agent.

    Responsibilities:
    - receive external input
    - create a new session
    - manage execution lifecycle
    - delegate execution to the orchestrator
    - return the final Session
    """

    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator

    def run(
        self,
        input_text: str,
        metadata: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> Session:
        session = Session.initialize(input_text=input_text)

        if metadata:
            session = session.merge_metadata(metadata)

        if context:
            session = session.merge_context(context)

        session = session.with_status("running")

        try:
            session = self.orchestrator.run(session)

            if session.status == "running":
                session = session.with_status("completed")

            return session

        except Exception as e:
            error_str = str(e)

            failed_session = (
                session
                .with_status("failed")
                .with_output(error_str)
                .merge_metadata({"error": error_str})
            )

            return failed_session