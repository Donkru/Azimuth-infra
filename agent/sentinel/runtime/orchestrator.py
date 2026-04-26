"""
Sentinel orchestrators — coordinate interpreter, planner, and execution.

Two implementations live here:

  BasicOrchestrator    (legacy)
    Uses the old Session-in/Session-out tool model from
    agent.sentinel.algorithms.decision. Kept as a reference for the
    future Java algorithm engine. Not the default.

  SentinelOrchestrator (active)
    Uses SentinelDecisionEngine + HiKOMaResponder. Honours the layer
    boundaries: tools/ for system actions, hikoma/ for LLM responses,
    cognition/ for orchestration.
"""
from __future__ import annotations

from typing import Any, Optional, Protocol

from agent.sentinel.cognition.decision_engine import SentinelDecisionEngine
from agent.sentinel.cognition.interpreter import SentinelInterpreter
from agent.sentinel.cognition.planner import SentinelPlanner
from agent.sentinel.runtime.session import Session


class Orchestrator(Protocol):
    def run(self, session: Session) -> Session: ...


# ───────────────────────────────────────────────────────────────────────────
# Active orchestrator
# ───────────────────────────────────────────────────────────────────────────

class SentinelOrchestrator:
    """
    The active coordination layer for Sentinel.

    Pipeline:
        interpret(session) → plan(session) → engine.execute(session, plan)
                                              ├── system handlers (tools/)
                                              └── fallback → HiKOMaResponder

    The result of engine.execute() is a DecisionResult; this class adapts
    that into the Session shape the rest of the runtime expects.
    """

    def __init__(
        self,
        interpreter: Optional[SentinelInterpreter] = None,
        planner: Optional[SentinelPlanner] = None,
        engine: Optional[SentinelDecisionEngine] = None,
        responder: Optional[Any] = None,
    ) -> None:
        self.interpreter = interpreter or SentinelInterpreter()
        self.planner = planner or SentinelPlanner()
        # If no engine passed, build one with optional responder
        self.engine = engine or SentinelDecisionEngine(responder=responder)

    def run(self, session: Session) -> Session:
        session = self.interpreter.interpret(session)

        plan = self.planner.plan(session)
        for step in plan:
            session = session.with_decision(step)

        result = self.engine.execute(session, plan)

        session = session.with_selected_tools(result.steps_run)
        if result.output:
            session = session.with_output(result.output)
        if result.errors:
            session = session.merge_metadata({"errors": result.errors})
        if result.used_llm:
            session = session.merge_metadata({"used_llm": True})

        return session


# ───────────────────────────────────────────────────────────────────────────
# Legacy orchestrator (kept as reference for the Java algorithm engine)
# ───────────────────────────────────────────────────────────────────────────

class BasicOrchestrator:
    """
    Legacy orchestrator using the old Session-in/Session-out tool model.

    Lives in agent.sentinel.algorithms.decision now. Preserved as the
    blueprint for the future Java port. Use SentinelOrchestrator for
    active runtime work.
    """

    def __init__(
        self,
        interpreter: Optional[SentinelInterpreter] = None,
        planner: Optional[SentinelPlanner] = None,
        executor: Optional[Any] = None,
    ) -> None:
        from agent.sentinel.algorithms.decision.executor import ToolExecutor
        from agent.sentinel.algorithms.decision.registry import bootstrap_tools

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
