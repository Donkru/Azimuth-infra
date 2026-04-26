# Azimuth-infra

Self-hosted infrastructure platform with an intelligent agent system.

[![Wiki](https://img.shields.io/badge/wiki-DokuWiki-2D9CDB?style=for-the-badge&logo=readthedocs&logoColor=white)](http://wiki.azimuth-labs.local)
[![Issues](https://img.shields.io/github/issues/Donkru/Azimuth-infra?style=for-the-badge&color=EF4444)](https://github.com/Donkru/Azimuth-infra/issues)
[![PRs](https://img.shields.io/badge/PRs-welcome-22C55E?style=for-the-badge)](CONTRIBUTING.md)
[![License](https://img.shields.io/badge/license-MIT-3B82F6?style=for-the-badge)](LICENSE)

---

## Overview

Azimuth runs on your own hardware and is structured as three layers:

| Layer | Name | Role |
|---|---|---|
| Infrastructure | **Azimuth** | Docker, Traefik, networking, deployment |
| Intelligence | **Sentinel** | Telemetry, observability, decision engine |
| Agent | **HiKOMa** | AI operator: reads telemetry, helps with code and admin |

## Stack

| Layer | Language | Purpose |
|---|---|---|
| Agent | Python 3.12 | HiKOMa, Sentinel runtime, FastAPI |
| Network | Go | gRPC server, API gateway *(planned)* |
| Algorithms | Java | Decision engine, analytics *(planned)* |
| System | C++ | Native telemetry collector *(planned)* |
| UI | JavaScript | Dashboard, CLI *(planned)* |

## Quick start

```bash
git clone https://github.com/Donkru/Azimuth-infra.git
cd Azimuth-infra

python3 -m venv .venv && source .venv/bin/activate
pip install -r agent/sentinel/requirements.txt

cp .env.example .env       # add your API keys

docker compose -f infra/traefik/docker-compose.yml up -d
python3 -m agent.sentinel.app
```

## Documentation

Full documentation lives in the project DokuWiki:

- [Architecture](http://wiki.azimuth-labs.local/doku.php?id=architecture)
- [Sentinel](http://wiki.azimuth-labs.local/doku.php?id=sentinel)
- [HiKOMa](http://wiki.azimuth-labs.local/doku.php?id=hikoma)
- [Algorithms](http://wiki.azimuth-labs.local/doku.php?id=algorithms)
- [Roadmap](http://wiki.azimuth-labs.local/doku.php?id=roadmap)
- [Contributing](http://wiki.azimuth-labs.local/doku.php?id=contributing)

The wiki is internal to the lab network. A public mirror is on the roadmap.

## Project structure
<img width="2472" height="1312" alt="image" src="https://github.com/user-attachments/assets/099a8b5d-eec9-4313-aa5b-41a225b8477d" />

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow, branch naming, and coding standards.

## License

MIT — see [LICENSE](LICENSE).
