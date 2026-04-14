from __future__ import annotations


EXPECTED_SERVICES = {
    "traefik": "reverse proxy",
    "dockerd": "container engine",
    "portainer": "container management UI",
    "tailscaled": "mesh VPN / connectivity layer",
}


def assess_services(processes: list[dict]) -> dict:
    observed_names = set()
    important_unknown = []

    for proc in processes:
        name = (proc.get("name") or "").strip()
        lower_name = name.lower()

        if lower_name:
            observed_names.add(lower_name)

        cpu = proc.get("cpu_percent", 0) or 0
        mem = proc.get("memory_percent", 0) or 0

        if lower_name and lower_name not in EXPECTED_SERVICES:
            if cpu > 1 or mem > 1:
                important_unknown.append(
                    {
                        "name": name,
                        "pid": proc.get("pid", "?"),
                        "cpu_percent": cpu,
                        "memory_percent": round(mem, 2),
                    }
                )

    expected_names = set(EXPECTED_SERVICES.keys())
    present = sorted(expected_names & observed_names)
    missing = sorted(expected_names - observed_names)

    return {
        "present": present,
        "missing": missing,
        "important_unknown": important_unknown,
    }


def summarize_service_awareness(assessment: dict) -> str:
    lines = []

    present = assessment.get("present", [])
    missing = assessment.get("missing", [])
    important_unknown = assessment.get("important_unknown", [])

    if present:
        described = ", ".join(
            f"{name} ({EXPECTED_SERVICES[name]})" for name in present
        )
        lines.append(f"Expected services currently visible: {described}.")
    else:
        lines.append("None of the expected infrastructure services are visible in the current process snapshot.")

    if missing:
        missing_text = ", ".join(missing)
        lines.append(f"Expected services not visible in this snapshot: {missing_text}.")
    else:
        lines.append("All expected infrastructure services are visible in the current snapshot.")

    if important_unknown:
        unknown_lines = []
        for proc in important_unknown:
            unknown_lines.append(
                f"{proc['name']} (PID {proc['pid']}, CPU {proc['cpu_percent']}%, MEM {proc['memory_percent']}%)"
            )
        lines.append(
            "Unknown but non-trivial processes detected: " + "; ".join(unknown_lines) + "."
        )
    else:
        lines.append("No unknown high-impact processes were detected in the current snapshot.")

    return " ".join(lines)
