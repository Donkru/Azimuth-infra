from __future__ import annotations


def interpret_system_state(cpu_percent: float, memory: dict, processes: list[dict]) -> str:
    lines = []

    top_cpu = sorted(
        processes,
        key=lambda p: p.get("cpu_percent", 0) or 0,
        reverse=True
    )
    top_mem = sorted(
        processes,
        key=lambda p: p.get("memory_percent", 0) or 0,
        reverse=True
    )

    cpu_leader = top_cpu[0] if top_cpu else None
    mem_leader = top_mem[0] if top_mem else None

    if cpu_percent >= 85:
        if cpu_leader:
            lines.append(
                f"CPU pressure is critical. The leading process is "
                f"{cpu_leader.get('name', 'unknown')} (PID {cpu_leader.get('pid', '?')}) "
                f"at {cpu_leader.get('cpu_percent', 0)}% CPU."
            )
        else:
            lines.append("CPU pressure is critical, but no dominant process was identified.")

    elif cpu_percent >= 60:
        if cpu_leader:
            lines.append(
                f"CPU usage is elevated. The main active process appears to be "
                f"{cpu_leader.get('name', 'unknown')} (PID {cpu_leader.get('pid', '?')}) "
                f"at {cpu_leader.get('cpu_percent', 0)}% CPU."
            )
        else:
            lines.append("CPU usage is elevated, but no dominant process was identified.")

    else:
        if cpu_leader and (cpu_leader.get("cpu_percent", 0) or 0) > 0:
            lines.append(
                f"CPU load is currently calm. The most active visible process is "
                f"{cpu_leader.get('name', 'unknown')} (PID {cpu_leader.get('pid', '?')}) "
                f"at {cpu_leader.get('cpu_percent', 0)}% CPU."
            )
        else:
            lines.append("CPU load is calm. No process is currently using notable CPU time.")

    mem_percent = memory.get("percent_used", 0)
    available_mb = memory.get("available_mb", 0)

    if mem_percent >= 90:
        if mem_leader:
            lines.append(
                f"Memory pressure is critical at {mem_percent}%. The largest visible consumer is "
                f"{mem_leader.get('name', 'unknown')} (PID {mem_leader.get('pid', '?')}) "
                f"using {round(mem_leader.get('memory_percent', 0), 2)}% of RAM."
            )
        else:
            lines.append(
                f"Memory pressure is critical at {mem_percent}%, but no leading memory consumer was identified."
            )

    elif mem_percent >= 75:
        if mem_leader:
            lines.append(
                f"Memory usage is high at {mem_percent}%. The largest visible consumer is "
                f"{mem_leader.get('name', 'unknown')} (PID {mem_leader.get('pid', '?')}) "
                f"using {round(mem_leader.get('memory_percent', 0), 2)}% of RAM."
            )
        else:
            lines.append(f"Memory usage is high at {mem_percent}%.")

    else:
        lines.append(
            f"Memory state is stable at {mem_percent}% used, with {available_mb} MB available."
        )

    quiet_services = []
    for proc in processes:
        name = (proc.get("name") or "").lower()
        if name in {"traefik", "dockerd", "portainer", "tailscaled"}:
            quiet_services.append(proc.get("name"))

    if quiet_services:
        unique_services = ", ".join(sorted(set(quiet_services)))
        lines.append(
            f"Observed infrastructure services include {unique_services}, all currently at low visible load."
        )

    return " ".join(lines)
