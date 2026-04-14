from __future__ import annotations

from pathlib import Path
from typing import Dict


PROC_STAT = Path("/proc/stat")


def read_cpu_times() -> Dict[str, int]:
    if not PROC_STAT.exists():
        raise FileNotFoundError("/proc/stat not found")

    with PROC_STAT.open("r", encoding="utf-8") as f:
        first_line = f.readline().strip()

    parts = first_line.split()
    if not parts or parts[0] != "cpu":
        raise ValueError("Unexpected /proc/stat format")

    values = [int(x) for x in parts[1:9]]
    keys = ["user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal"]

    return dict(zip(keys, values))


def total_cpu_time(cpu_times: Dict[str, int]) -> int:
    return sum(cpu_times.values())


def idle_cpu_time(cpu_times: Dict[str, int]) -> int:
    return cpu_times["idle"] + cpu_times["iowait"]


def cpu_usage_percent(snapshot1: Dict[str, int], snapshot2: Dict[str, int]) -> float:
    total1 = total_cpu_time(snapshot1)
    total2 = total_cpu_time(snapshot2)

    idle1 = idle_cpu_time(snapshot1)
    idle2 = idle_cpu_time(snapshot2)

    total_delta = total2 - total1
    idle_delta = idle2 - idle1

    if total_delta <= 0:
        return 0.0

    usage = 100.0 * (1.0 - (idle_delta / total_delta))
    return round(usage, 2)
