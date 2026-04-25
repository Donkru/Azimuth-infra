from __future__ import annotations

from pathlib import Path
from typing import Dict


PROC_MEMINFO = Path("/proc/meminfo")


def read_meminfo() -> Dict[str, int]:
    if not PROC_MEMINFO.exists():
        raise FileNotFoundError("/proc/meminfo not found")

    result: Dict[str, int] = {}

    with PROC_MEMINFO.open("r", encoding="utf-8") as f:
        for line in f:
            key, value = line.split(":", 1)
            number = value.strip().split()[0]
            result[key] = int(number)

    return resultc


def memory_snapshot() -> Dict[str, float]:
    meminfo = read_meminfo()

    total_kb = meminfo.get("MemTotal", 0)
    free_kb = meminfo.get("MemFree", 0)
    available_kb = meminfo.get("MemAvailable", 0)
    buffers_kb = meminfo.get("Buffers", 0)
    cached_kb = meminfo.get("Cached", 0)

    used_kb = total_kb - available_kb if available_kb else total_kb - free_kb
    percent_used = (used_kb / total_kb * 100.0) if total_kb else 0.0

    return {
        "total_mb": round(total_kb / 1024, 2),
        "free_mb": round(free_kb / 1024, 2),
        "available_mb": round(available_kb / 1024, 2),
        "buffers_mb": round(buffers_kb / 1024, 2),
        "cached_mb": round(cached_kb / 1024, 2),
        "used_mb": round(used_kb / 1024, 2),
        "percent_used": round(percent_used, 2),
    }
