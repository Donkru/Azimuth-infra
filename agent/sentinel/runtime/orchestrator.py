from typing import Protocol

from agent.sentinel.runtime.session import Session
from agent.sentinel.cognition.interpreter import SentinelInterpreter
from agent.sentinel.cognition.planner import SentinelPlanner
from agent.sentinel.tools.executor import ToolExecutor
from agent.sentinel.tools.registry import bootstrap_tools


class Orchestrator(Protocol):
    def run(self, session: Session) -> Session:
        ...


class BasicOrchestrator:
    """
    BasicOrchestrator is the default coordination layer for Sentinel.

    Responsibilities:
    - interpret session input
    - plan actions
    - delegate execution to tools
    - return an updated Session

    It does not perform infrastructure actions directly.
    It coordinates subsystems and evolves session state step-by-step.
    """

    def __init__(
        self,
        interpreter: SentinelInterpreter | None = None,
        planner: SentinelPlanner | None = None,
        executor: ToolExecutor | None = None,
    ) -> None:
        self.interpreter = interpreter or SentinelInterpreter()
        self.planner = planner or SentinelPlanner()
        self.executor = executor or ToolExecutor(bootstrap_tools())

    def run(self, session: Session) -> Session:
        session = self.interpreter.interpret(session)

        decisions = self.planner.plan(session)
        for decision in decisions:
            session = session.with_decision(decision)

        session = self.executor.execute(session, decisions)

        if not session.output:
            session = session.with_output(f"Received input: {session.input_text}")

        return session