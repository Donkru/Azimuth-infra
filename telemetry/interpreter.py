"""
interpreter.py
--------------
Translates raw system telemetry into a human-readable diagnostic narrative.

Public API
----------
    interpret_system_state(cpu_percent, memory, processes, *, config) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class InterpreterConfig:
    """
    All tunable thresholds and policy knobs in one place.
    Pass a custom instance to override defaults without touching the logic.
    """

    # Overall CPU % thresholds
    cpu_critical: float = 85.0
    cpu_elevated: float = 60.0

    # Per-process CPU % considered "notable" when system is otherwise calm
    cpu_process_notable: float = 5.0

    # Memory % thresholds
    mem_critical: float = 90.0
    mem_high: float = 75.0

    # How many processes to report in detail
    top_n_processes: int = 3

    # Known infrastructure service names (matched case-insensitively)
    infrastructure_services: frozenset[str] = field(
        default_factory=lambda: frozenset({
            "traefik", "dockerd", "portainer", "tailscaled",
            "nginx", "caddy", "consul", "vault", "prometheus",
        })
    )


_DEFAULT_CONFIG = InterpreterConfig()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _safe_float(value: Any, default: float = 0.0) -> float:
    """Return a non-negative float from an arbitrary value, or *default*."""
    try:
        result = float(value)
        return result if result >= 0 else default
    except (TypeError, ValueError):
        return default


def _validate_inputs(
        cpu_percent: float,
        memory: dict[str, Any],
        processes: list[dict[str, Any]],
) -> None:
    if not isinstance(cpu_percent, (int, float)):
        raise TypeError(f"cpu_percent must be numeric, got {type(cpu_percent).__name__!r}")
    if not (0.0 <= cpu_percent <= 100.0):
        raise ValueError(f"cpu_percent must be 0–100, got {cpu_percent}")
    if not isinstance(memory, dict):
        raise TypeError(f"memory must be a dict, got {type(memory).__name__!r}")
    if not isinstance(processes, list):
        raise TypeError(f"processes must be a list, got {type(processes).__name__!r}")


def _process_name(proc: dict[str, Any]) -> str:
    return str(proc.get("name") or "unknown")


def _process_pid(proc: dict[str, Any]) -> str:
    pid = proc.get("pid")
    return str(pid) if pid is not None else "?"


# ---------------------------------------------------------------------------
# Sub-interpreters
# ---------------------------------------------------------------------------

def _interpret_cpu(
        cpu_percent: float,
        processes: list[dict[str, Any]],
        cfg: InterpreterConfig,
) -> str:
    """Return a single sentence summarising CPU state."""

    sorted_procs = sorted(
        processes,
        key=lambda p: _safe_float(p.get("cpu_percent")),
        reverse=True,
    )

    # Strip zero-CPU entries when looking for an active leader
    active_procs = [
        p for p in sorted_procs
        if _safe_float(p.get("cpu_percent")) >= cfg.cpu_process_notable
    ]
    leader = active_procs[0] if active_procs else None

    def leader_tag() -> str:
        if not leader:
            return "no single process stands out"
        cpu = _safe_float(leader.get("cpu_percent"))
        # Per-process CPU > 100 % is normal on multi-core; surface it explicitly.
        note = " (multi-threaded, spanning multiple cores)" if cpu > 100 else ""
        return (
            f"{_process_name(leader)} (PID {_process_pid(leader)}) "
            f"at {cpu:.1f}% CPU{note}"
        )

    if cpu_percent >= cfg.cpu_critical:
        if leader:
            return (
                f"CPU pressure is critical at {cpu_percent:.1f}%. "
                f"The dominant process is {leader_tag()}."
            )
        return f"CPU pressure is critical at {cpu_percent:.1f}%, but no dominant process was identified."

    if cpu_percent >= cfg.cpu_elevated:
        if leader:
            return (
                f"CPU usage is elevated at {cpu_percent:.1f}%. "
                f"The main active process is {leader_tag()}."
            )
        return f"CPU usage is elevated at {cpu_percent:.1f}%, but no dominant process was identified."

    # Calm path
    if leader:
        return (
            f"CPU load is calm at {cpu_percent:.1f}%. "
            f"The most active visible process is {leader_tag()}."
        )
    return f"CPU load is calm at {cpu_percent:.1f}% with no process using notable CPU time."


def _interpret_memory(
        memory: dict[str, Any],
        processes: list[dict[str, Any]],
        cfg: InterpreterConfig,
) -> str:
    """Return a single sentence summarising memory state."""

    mem_percent = _safe_float(memory.get("percent_used"))
    available_mb = _safe_float(memory.get("available_mb"))

    sorted_procs = sorted(
        processes,
        key=lambda p: _safe_float(p.get("memory_percent")),
        reverse=True,
    )
    mem_leader = sorted_procs[0] if sorted_procs else None

    def mem_leader_tag() -> str:
        if not mem_leader:
            return ""
        pct = _safe_float(mem_leader.get("memory_percent"))
        return (
            f" The largest visible consumer is "
            f"{_process_name(mem_leader)} (PID {_process_pid(mem_leader)}) "
            f"at {pct:.2f}% of RAM."
        )

    if mem_percent >= cfg.mem_critical:
        return (
            f"Memory pressure is critical at {mem_percent:.1f}% used "
            f"({available_mb:,.0f} MB remaining).{mem_leader_tag()}"
        )

    if mem_percent >= cfg.mem_high:
        return (
            f"Memory usage is high at {mem_percent:.1f}% used "
            f"({available_mb:,.0f} MB remaining).{mem_leader_tag()}"
        )

    return (
        f"Memory state is stable at {mem_percent:.1f}% used "
        f"with {available_mb:,.0f} MB available."
    )


def _interpret_infrastructure(
        processes: list[dict[str, Any]],
        cfg: InterpreterConfig,
) -> str | None:
    """
    Return a sentence about detected infrastructure services, or None if none found.
    Matching is case-insensitive so 'Dockerd' and 'dockerd' both count.
    """
    found: set[str] = set()
    for proc in processes:
        name = (proc.get("name") or "").strip()
        if name.lower() in cfg.infrastructure_services:
            found.add(name)

    if not found:
        return None

    service_list = ", ".join(sorted(found))
    plural = "services" if len(found) > 1 else "service"
    return (
        f"Infrastructure {plural} detected: {service_list} "
        f"— all at low visible load."
    )


def _interpret_top_processes(
        processes: list[dict[str, Any]],
        cfg: InterpreterConfig,
) -> str | None:
    """
    Return a short ranked summary of the top-N CPU consumers if there are
    multiple noteworthy processes beyond the leader already mentioned.
    """
    active = sorted(
        (p for p in processes if _safe_float(p.get("cpu_percent")) >= cfg.cpu_process_notable),
        key=lambda p: _safe_float(p.get("cpu_percent")),
        reverse=True,
    )

    # Skip if there is only one — it was already mentioned in the CPU sentence.
    if len(active) <= 1:
        return None

    top = active[: cfg.top_n_processes]
    entries = [
        f"{_process_name(p)} ({_safe_float(p.get('cpu_percent')):.1f}% CPU, "
        f"{_safe_float(p.get('memory_percent')):.2f}% MEM)"
        for p in top
    ]
    return "Competing workloads: " + "; ".join(entries) + "."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def interpret_system_state(
        cpu_percent: float,
        memory: dict[str, Any],
        processes: list[dict[str, Any]],
        *,
        config: InterpreterConfig = _DEFAULT_CONFIG,
) -> str:
    """
    Produce a human-readable diagnostic narrative from raw system telemetry.

    Parameters
    ----------
    cpu_percent : float
        Aggregate CPU utilisation (0–100).
    memory : dict
        Must contain ``percent_used`` (float) and ``available_mb`` (float).
    processes : list[dict]
        Each entry should have ``name``, ``pid``, ``cpu_percent``,
        and ``memory_percent`` keys. Missing keys are handled gracefully.
    config : InterpreterConfig
        Thresholds and policy. Pass a custom instance to tune without
        changing this module.

    Returns
    -------
    str
        A multi-sentence diagnostic paragraph.

    Raises
    ------
    TypeError
        If ``cpu_percent`` is not numeric, or ``memory``/``processes``
        are the wrong container type.
    ValueError
        If ``cpu_percent`` is outside the 0–100 range.
    """
    _validate_inputs(cpu_percent, memory, processes)

    paragraphs: list[str] = [
        _interpret_cpu(cpu_percent, processes, config),
        _interpret_memory(memory, processes, config),
    ]

    competing = _interpret_top_processes(processes, config)
    if competing:
        paragraphs.append(competing)

    infra = _interpret_infrastructure(processes, config)
    if infra:
        paragraphs.append(infra)

    return "\n".join(paragraphs)