# Sentinel Runtime Flow

## Primary Flow

Input
→ Session creation
→ Context gathering
→ Interpretation
→ Planning / decision
→ Optional tool execution
→ Memory update
→ Presentation
→ Output

## Module Order

1. `runtime/runtime.py`
2. `runtime/session.py`
3. `runtime/orchestrator.py`
4. `cognition/interpreter.py`
5. `cognition/planner.py`
6. `cognition/decision_engine.py`
7. `tools/registry.py`
8. `tools/validation.py`
9. `tools/executor.py`
10. `memory/state_store.py`
11. `memory/history.py`
12. `memory/recall.py`
13. `interface/presenter.py`

## Rules

- Runtime coordinates, it does not think.
- Cognition thinks, it does not execute tools directly.
- Tools execute, they do not decide policy.
- Memory stores and recalls, it does not orchestrate flow.
- Interface presents, it does not control logic.
- LLM layer is isolated from infrastructure logic.
