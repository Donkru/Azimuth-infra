# Sentinel Algorithms

This package is the **design-stage seed for the Phase 5 Java algorithm engine**
(decision engine, analytics, scheduler).

The Python code here:
- demonstrates the architecture in pure Python first
- is a reference, not the active execution path
- will eventually be ported to Java with gRPC interfaces

## Layout

| Directory | Purpose | Status |
|---|---|---|
| `decision/` | Tool registry + executor pattern (Session-in/Session-out) | Reference, used by `BasicOrchestrator` |
| `analytics/` | Metric history, anomaly detection | Empty placeholder |
| `scheduler/` | Periodic jobs, automation triggers | Empty placeholder |

## Why it's separated from `tools/`

`tools/` holds active handlers used by `SentinelDecisionEngine`. That code is
the running execution path, with `(session, result) -> None` handlers that
mutate a `DecisionResult`.

`algorithms/decision/` holds the older `Session -> Session` pattern. It is
preserved as the conceptual blueprint for the Java port. Do not delete.
