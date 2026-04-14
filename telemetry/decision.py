from __future__ import annotations


def decide_system_state(
    cpu_percent: float,
    memory: dict,
    service_assessment: dict,
) -> dict:
    mem_percent = memory.get("percent_used", 0)

    missing_services = service_assessment.get("missing", [])
    important_unknown = service_assessment.get("important_unknown", [])

    state = "HEALTHY"
    attention = "LOW"
    recommended_action = "No immediate action needed."
    reasons = []

    if cpu_percent >= 85:
        state = "CRITICAL"
        attention = "HIGH"
        recommended_action = "Investigate CPU-intensive processes immediately."
        reasons.append(f"CPU usage is critically high at {cpu_percent}%.")

    elif cpu_percent >= 60:
        state = "WARNING"
        attention = "MEDIUM"
        recommended_action = "Review active processes and confirm load is expected."
        reasons.append(f"CPU usage is elevated at {cpu_percent}%.")

    if mem_percent >= 90:
        state = "CRITICAL"
        attention = "HIGH"
        recommended_action = "Investigate memory-heavy processes immediately."
        reasons.append(f"Memory usage is critically high at {mem_percent}%.")

    elif mem_percent >= 75 and state != "CRITICAL":
        state = "WARNING"
        attention = "MEDIUM"
        recommended_action = "Review memory consumers before pressure worsens."
        reasons.append(f"Memory usage is high at {mem_percent}%.")

    if missing_services and state != "CRITICAL":
        state = "WARNING"
        attention = "MEDIUM"
        recommended_action = "Verify whether expected infrastructure services should be running."
        reasons.append(
            "Expected services missing from current snapshot: " + ", ".join(missing_services) + "."
        )

    if important_unknown and state != "CRITICAL":
        state = "WARNING"
        attention = "MEDIUM"
        recommended_action = "Inspect unknown non-trivial processes."
        names = ", ".join(proc["name"] for proc in important_unknown)
        reasons.append(f"Unknown significant processes detected: {names}.")

    if not reasons:
        reasons.append("CPU, memory, and expected service visibility all appear normal.")

    return {
        "state": state,
        "attention": attention,
        "recommended_action": recommended_action,
        "reasons": reasons,
    }


def summarize_decision(decision: dict) -> str:
    reasons_text = " ".join(decision.get("reasons", []))

    return (
        f"System State: {decision.get('state', 'UNKNOWN')}\n"
        f"Attention Level: {decision.get('attention', 'UNKNOWN')}\n"
        f"Recommended Action: {decision.get('recommended_action', 'None')}\n"
        f"Decision Basis: {reasons_text}"
    )
