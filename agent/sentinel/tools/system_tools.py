from agent.sentinel.runtime.session import Session
import time
import psutil

from telemetry.interpreter import interpret_system_state


def gather_status(session: Session) -> Session:
    try:
        cpu_percent = psutil.cpu_percent(interval=0.2)
    except Exception:
        cpu_percent = 0.0

    try:
        mem = psutil.virtual_memory()
        memory_snapshot = {
            "percent_used": round(mem.percent, 2),
            "available_mb": round(mem.available / (1024 ** 2), 2),
            "used_mb": round(mem.used / (1024 ** 2), 2),
            "total_mb": round(mem.total / (1024 ** 2), 2),
        }
    except Exception:
        memory_snapshot = {
            "percent_used": 0.0,
            "available_mb": 0.0,
            "used_mb": 0.0,
            "total_mb": 0.0,
        }

    try:
        disk = psutil.disk_usage("/")
        disk_snapshot = {
            "used_percent": round(disk.percent, 2),
            "free_gb": round(disk.free / (1024 ** 3), 2),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "total_gb": round(disk.total / (1024 ** 3), 2),
        }
    except Exception:
        disk_snapshot = {
            "used_percent": 0.0,
            "free_gb": 0.0,
            "used_gb": 0.0,
            "total_gb": 0.0,
        }

    processes: list[dict] = []
    try:
        procs = list(psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_percent"]))

        for proc in procs:
            try:
                proc.cpu_percent(interval=None)
            except Exception:
                continue

        time.sleep(0.1)

        proc_list = []
        for proc in procs:
            try:
                proc_list.append({
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "cpu_percent": proc.cpu_percent(interval=None),
                    "memory_percent": proc.info["memory_percent"] or 0.0,
                })
            except Exception:
                continue

        processes = sorted(proc_list, key=lambda x: x["cpu_percent"], reverse=True)[:5]
    except Exception:
        processes = []

    try:
        boot_time = psutil.boot_time()
        uptime_hours = round((time.time() - boot_time) / 3600, 2)
    except Exception:
        uptime_hours = 0.0

    status_data = {
        "cpu_percent": cpu_percent,
        "memory": memory_snapshot,
        "disk": disk_snapshot,
        "processes": processes,
        "uptime_hours": uptime_hours,
    }

    return session.merge_context({"status_data": status_data})


def summarize_status(session: Session) -> Session:
    status_data = session.context.get("status_data", {})

    cpu_percent = status_data.get("cpu_percent", 0.0)
    memory = status_data.get("memory", {})
    disk = status_data.get("disk", {})
    processes = status_data.get("processes", [])
    uptime_hours = status_data.get("uptime_hours", 0.0)

    try:
        interpretation = interpret_system_state(cpu_percent, memory, processes)
    except Exception as e:
        interpretation = f"Failed to interpret system state: {e}"

    lines = [
        f"System status:",
        f"CPU: {cpu_percent}%",
        f"RAM: {memory.get('percent_used', '?')}% used ({memory.get('available_mb', '?')} MB available)",
        f"Disk: {disk.get('used_percent', '?')}% used ({disk.get('free_gb', '?')} GB free)",
        f"Uptime: {uptime_hours} hours",
        "",
        "Interpretation:",
        interpretation,
    ]

    if processes:
        lines.append("")
        lines.append("Top Processes:")
        for proc in processes:
            lines.append(
                f"- {proc['name']} (PID {proc['pid']}) CPU {proc['cpu_percent']}% MEM {round(proc['memory_percent'], 2)}%"
            )

    return session.with_output("\n".join(lines))