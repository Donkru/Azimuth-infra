from __future__ import annotations

from typing import Dict


def summarize_cpu(cpu_percent: float) -> str:
    if cpu_percent >= 85:
        return f"CPU load is very high at {cpu_percent}%. The system may be under heavy computation or process pressure."
    if cpu_percent >= 60:
        return f"CPU load is elevated at {cpu_percent}%. The machine is active but not necessarily in distress."
    if cpu_percent >= 25:
        return f"CPU load is moderate at {cpu_percent}%. The system appears to be working normally."
    return f"CPU load is low at {cpu_percent}%. The system appears mostly idle."


def summarize_memory(memory: Dict[str, float]) -> str:
    percent_used = memory["percent_used"]
    available_mb = memory["available_mb"]

    if percent_used >= 90:
        return (
            f"Memory pressure is critical. About {percent_used}% of RAM is in use, "
            f"with only {available_mb} MB readily available."
        )
    if percent_used >= 75:
        return (
            f"Memory usage is high at {percent_used}%. "
            f"The system still has {available_mb} MB available, but pressure is rising."
        )
    if percent_used >= 50:
        return (
            f"Memory usage is moderate at {percent_used}%. "
            f"Available memory remains at {available_mb} MB."
        )
    return (
        f"Memory usage is comfortable at {percent_used}%. "
        f"Available memory is {available_mb} MB."
    )
