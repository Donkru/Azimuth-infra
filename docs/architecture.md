# Azimuth / Sentinel Architecture

## Purpose
Sentinel is the infrastructure intelligence core of Azimuth. Its role is to observe system state, interpret what is happening, track continuity over time, and later support safe operator actions.

HiKOMa is the identity and interaction layer built on top of Sentinel. It is not the infrastructure brain. It is the expression, continuity, and relationship layer.

## Existing Top-Level Structure

- `agent/` → agent logic
- `apps/` → application services
- `core/` → infrastructure foundation
- `infra/` → service and routing configuration
- `memory/` → stored continuity/state data
- `owner/` → owner-aware context and priorities
- `telemetry/` → machine/system observation
- `docs/` → planning and architecture
- `deployment/` → deployment and automation scripts
- `server/` → host integration logic

## Sentinel Responsibilities

- observe machine and service state
- interpret telemetry into meaningful summaries
- track system continuity over time
- decide what matters
- prepare safe actions through tools
- expose API/CLI interfaces

## HiKOMa Responsibilities

- identity
- response style
- owner-aware framing
- continuity of interaction

## Runtime Flow

Input or system event
→ context gathering
→ telemetry read
→ interpretation
→ decision layer
→ tool selection or response generation
→ memory update
→ output

## Internal Sentinel Layers

### Runtime
Controls orchestration, sessions, and execution flow.

### Cognition
Interprets state, plans actions, and evaluates outcomes.

### Memory
Stores state, history, summaries, and recall.

### Tools
Defines callable actions and execution boundaries.

### Interface
API, CLI, and presentation output.

### LLM
Model interaction, prompt building, and response parsing.

### Config
Capabilities, settings, and feature flags.

### Security
Safety boundaries and authorization rules.

## Near-Term Goal

Build the Sentinel runtime spine:
- runtime controller
- telemetry ingestion
- memory state store
- interpretation layer
- tool registry

## Not Doing Yet

- autonomous destructive actions
- unrestricted shell execution
- secret management inside the agent
- full multi-agent orchestration
