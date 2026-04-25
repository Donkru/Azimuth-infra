from dataclasses import dataclass, field
from telemetry.findings import Finding, Severity

@dataclass(frozen=True)
class SystemReport:
    node_id: str
    collected_at: float
    findings: tuple[Finding, ...]

    @property
    def severity(self) -> Severity:
        if any(f.severity == Severity.CRITICAL for f in self.findings):
            return Severity.CRITICAL
        if any(f.severity == Severity.WARNING for f in self.findings):
            return Severity.WARNING
        return Severity.INFO

    @property
    def is_healthy(self) -> bool:
        return self.severity == Severity.INFO

    def findings_by_severity(self, severity: Severity) -> tuple[Finding, ...]:
        return tuple(f for f in self.findings if f.severity == severity)