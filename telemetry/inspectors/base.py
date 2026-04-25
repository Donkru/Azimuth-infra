from typing import Protocol
from telemetry.snapshot import SystemSnapshot
from telemetry.findings import Finding
from telemetry.thresholds import Thresholds

class Inspector(Protocol):
    def inspect(self, snapshot: SystemSnapshot, thresholds: Thresholds) -> tuple[Finding, ...]:
        ...
