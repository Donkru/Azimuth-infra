import psutil


def top_processes(limit: int = 5) -> list[dict]:
    processes = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"] or "unknown",
                    "cpu_percent": info["cpu_percent"] or 0.0,
                    "memory_percent": round(info["memory_percent"] or 0.0, 2),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes.sort(key=lambda p: (p["cpu_percent"], p["memory_percent"]), reverse=True)
    return processes[:limit]


def summarize_top_processes(limit: int = 5) -> str:
    procs = top_processes(limit=limit)

    if not procs:
        return "No process data available."

    lines = ["Top processes:"]
    for i, proc in enumerate(procs, start=1):
        lines.append(
            f"{i}. {proc['name']} (PID {proc['pid']}) - "
            f"CPU: {proc['cpu_percent']}%, MEM: {proc['memory_percent']}%"
        )

    return "\n".join(lines)

