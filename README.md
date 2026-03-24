# Azimuth-Infra

## Overview

Azimuth-Infra is a system-level infrastructure project focused on building an intelligent local operator agent.

The system is composed of:

- **Sentinel** → Core infrastructure intelligence agent
- **HiKOMa** → Identity/personality layer built on top of Sentinel

---

## Current Capabilities (Phase 4)

Sentinel can:

- Observe system telemetry
  - CPU usage
  - Memory usage
  - Disk usage
  - Processes
  - Uptime

- Interpret system state
  - Detect load conditions
  - Analyze memory pressure
  - Identify active processes

- Perform cause analysis
  - Explain why the system is in its current state

- Provide service awareness
  - Detect expected infrastructure services
  - Identify missing services
  - Flag unknown high-impact processes

- Make decisions
  - HEALTHY / WARNING / CRITICAL states
  - Attention level
  - Recommended actions

- Maintain continuity (state memory)
  - Persist system state over time
  - Track previous system conditions
  - Enable future trend analysis

---

## API Endpoints

- `/health` → service status
- `/identity` → Sentinel / HiKOMa identity
- `/status` → summarized system state
- `/full-report` → full operator report
- `/observe` → natural language system query

---

## Architecture

agent/
sentinel/
app.py
model.py
config.py

telemetry/
cpu.py
memory.py
summary.py
interpreter.py
service_awareness.py
decision.py
system_stats.py

memory/
state_store.py

owner/
owner_profile.py

core/
(shared utilities)


---

## Philosophy

- Build from real system data, not abstractions
- Prioritize clarity over complexity
- Develop a true infrastructure operator agent
- Separate core intelligence (Sentinel) from identity (HiKOMa)

---

## Next Phase

- Expand memory into historical analysis
- Add anomaly detection
- Introduce autonomous response capability
- Integrate container and multi-node awareness
- Prepare CI/CD pipelines (GitLab)

---

## Repository Strategy

- **GitHub** → primary codebase and public visibility
- **GitLab** → CI/CD, automation, and infrastructure control
