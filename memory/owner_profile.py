OWNER_PROFILE = {
    "name": "Zawinley Joseph",
    "preferred_name": "Zawinley",
    "role": "creator and operator of Sentinel",
    "organization": "Azimuth",
    "primary_goal": (
        "Build an owner-centered infrastructure intelligence agent "
        "that understands its creator, systems, and long-term projects."
    ),
    "machines": {
        "mac": "development machine",
        "server": "Ubuntu ThinkStation server for infrastructure and agent runtime",
        "nali": "research, networking, and security environment",
    },
    "repositories": {
        "azimuth_infra": "main infrastructure repository",
        "nali_lab": "research and experimentation repository",
    },
    "projects": {
        "sentinel": (
            "A machine-aware agent that will evolve into a server operator, "
            "telemetry reader, memory system, and owner-aware intelligence service."
        )
    },
    "preferences": {
        "style": "direct, serious, structured, realistic",
        "priority": "know the creator first, then the systems, then broader external knowledge",
    },
}


def get_owner_profile() -> dict:
    return OWNER_PROFILE


def summarize_owner_profile() -> str:
    p = OWNER_PROFILE
    return (
        f"Creator: {p['name']} ({p['preferred_name']}). "
        f"Role: {p['role']}. "
        f"Organization: {p['organization']}. "
        f"Primary goal: {p['primary_goal']} "
        f"Machines: Mac={p['machines']['mac']}, "
        f"Server={p['machines']['server']}, "
        f"Nali={p['machines']['nali']}. "
        f"Repositories: Azimuth-infra={p['repositories']['azimuth_infra']}, "
        f"Nali-lab={p['repositories']['nali_lab']}. "
        f"Preference: {p['preferences']['style']}."
    )
