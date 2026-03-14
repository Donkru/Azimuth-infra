OWNER_PROFILE = {
    "identity": {
        "name": "Zawinley Joseph",
        "preferred_name": "Zawinley",
        "role": "Creator and primary operator of Sentinel",
        "organization": "Azimuth",
    },

    "education": {
        "university": "Butler University",
        "location": "Indianapolis, Indiana",
        "degrees": [
            "Computer Science",
            "Theatre"
        ],
        "minor": "Creative Writing",
    },

    "projects": {
        "sentinel": {
            "description": (
                "Sentinel is an owner-centered infrastructure intelligence agent "
                "being developed as part of Azimuth infrastructure."
            ),
            "purpose": (
                "To build a machine-aware agent that understands its creator, "
                "monitors infrastructure, and evolves into a server operator AI."
            ),
        },
        "azimuth_infra": {
            "description": (
                "Infrastructure repository used to build the Sentinel agent "
                "and supporting telemetry and automation systems."
            )
        },
        "nali_lab": {
            "description": (
                "Research and experimentation environment used for networking, "
                "security exploration, and technical experimentation."
            )
        },
    },

    "machines": {
        "mac": "Primary development machine",
        "thinkstation_server": "Ubuntu ThinkStation server used for infrastructure and agent runtime",
        "nali_environment": "Research and security experimentation environment",
    },

    "goals": {
        "short_term": (
            "Develop Sentinel into a machine-aware agent capable of monitoring "
            "system telemetry, understanding its operator, and learning system structure."
        ),
        "long_term": (
            "Build Sentinel into a full infrastructure operator agent that can "
            "monitor, reason about, and eventually manage servers and services."
        ),
    },

    "preferences": {
        "interaction_style": "direct, structured, realistic",
        "learning_priority": (
            "Sentinel should understand its creator first, then the systems it runs on, "
            "before expanding to broader external knowledge."
        ),
    }
}


def get_owner_profile() -> dict:
    return OWNER_PROFILE


def summarize_owner_profile() -> str:
    p = OWNER_PROFILE

    return (
        f"Creator: {p['identity']['name']} ({p['identity']['preferred_name']}). "
        f"Role: {p['identity']['role']} at {p['identity']['organization']}. "
        f"Education: {p['education']['university']} studying "
        f"{', '.join(p['education']['degrees'])}. "
        f"Current project: Sentinel, an infrastructure intelligence agent. "
        f"Primary goal: {p['goals']['long_term']} "
        f"Development machines include a Mac development system and a ThinkStation server."
    )
