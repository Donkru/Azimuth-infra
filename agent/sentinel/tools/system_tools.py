"""System-level tool handlers used by the Sentinel decision engine."""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent.sentinel.cognition.decision_engine import DecisionResult
    from agent.sentinel.runtime.session import Session


def gather_status(session, result):
    from telemetry.system_stats import cpu_usage, memory_usage, disk_usage, uptime_hours
    result.artifacts["status"] = {
        "cpu": cpu_usage(), "memory": memory_usage(),
        "disk": disk_usage(), "uptime": uptime_hours(),
    }


def gather_processes(session, result):
    from telemetry.system_stats import top_processes
    result.artifacts["processes"] = top_processes(limit=5)


def gather_report(session, result):
    from telemetry.system_stats import (
        cpu_usage, memory_usage, disk_usage, uptime_hours,
        top_processes, machine_identity,
    )
    result.artifacts["report"] = {
        "identity": machine_identity(), "cpu": cpu_usage(),
        "memory": memory_usage(), "disk": disk_usage(),
        "uptime": uptime_hours(), "processes": top_processes(limit=5),
    }


def summarize_status(session, result):
    s = result.artifacts.get("status")
    if not s:
        result.append_output("No status data was gathered.")
        return
    result.append_output(
        f"System status:\n"
        f"CPU: {s['cpu']}%\n"
        f"RAM: {s['memory']['used_percent']}% used "
        f"({s['memory']['available_gb']} GB free)\n"
        f"Disk: {s['disk']['used_percent']}% used "
        f"({s['disk']['free_gb']} GB free)\n"
        f"Uptime: {s['uptime']} hours"
    )


def summarize_processes(session, result):
    procs = result.artifacts.get("processes", [])
    if not procs:
        result.append_output("No process data was gathered.")
        return
    lines = ["Top processes by memory:"]
    for i, p in enumerate(procs, 1):
        cpu = p.get("cpu_percent") or 0
        mem = p.get("memory_percent") or 0
        lines.append(f"{i}. {p.get('name', '?')} (PID {p.get('pid', '?')}) CPU {cpu}% MEM {round(mem, 2)}%")
    result.append_output("\n".join(lines))


def summarize_report(session, result):
    r = result.artifacts.get("report")
    if not r:
        result.append_output("No report data was gathered.")
        return
    idn = r["identity"]
    proc_lines = []
    for i, p in enumerate(r["processes"], 1):
        cpu = p.get("cpu_percent") or 0
        mem = p.get("memory_percent") or 0
        proc_lines.append(f"{i}. {p.get('name', '?')} (PID {p.get('pid', '?')}) CPU {cpu}% MEM {round(mem, 2)}%")
    result.append_output(
        "Sentinel Operator Report\n\n"
        f"Machine:\n  Hostname: {idn['hostname']}\n  OS: {idn['os']}\n"
        f"  Architecture: {idn['architecture']}\n  CPU cores: {idn['cpu_cores']}\n\n"
        f"System:\n  CPU: {r['cpu']}%\n"
        f"  RAM: {r['memory']['used_percent']}% used ({r['memory']['available_gb']} GB free)\n"
        f"  Disk: {r['disk']['used_percent']}% used ({r['disk']['free_gb']} GB free)\n"
        f"  Uptime: {r['uptime']} hours\n\n"
        f"Top processes:\n" + "\n".join(proc_lines)
    )


SYSTEM_HANDLERS = {
    "gather_status":       gather_status,
    "summarize_status":    summarize_status,
    "gather_processes":    gather_processes,
    "summarize_processes": summarize_processes,
    "gather_report":       gather_report,
    "summarize_report":    summarize_report,
}
