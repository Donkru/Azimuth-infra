import socket
import time
import psutil
from telemetry.snapshot import SystemSnapshot, ProcessInfo
from telemetry.report import SystemReport
from telemetry.thresholds import Thresholds, DEFAULT_THRESHOLDS
from telemetry.inspectors.cpu import CpuInspector
from telemetry.inspectors.memory import MemoryInspector
from telemetry.inspectors.disk import DiskInspector
from telemetry.inspectors.processes import ProcessInspector
from telemetry.inspectors.services import ServiceInspector
from telemetry.findings import Finding, FindingCode, Severity

_DEFAULT_INSPECTORS = [
    CpuInspector(),
    MemoryInspector(),
    DiskInspector(),
    ProcessInspector(),
    ServiceInspector(),
]

class InspectionEngine:
    def __init__(
            self,
            inspectors=None,
            thresholds: Thresholds = DEFAULT_THRESHOLDS,
            node_id: str | None = None,
    ):
        self.inspectors = inspectors or _DEFAULT_INSPECTORS
        self.thresholds = thresholds
        self.node_id = node_id or socket.gethostname()

    def collect(self) -> SystemSnapshot:
        # single collection path — system_tools.py calls this
        ...

    def run(self, snapshot: SystemSnapshot | None = None) -> SystemReport:
        snap = snapshot or self.collect()
        findings: list[Finding] = []
        for inspector in self.inspectors:
            findings.extend(inspector.inspect(snap, self.thresholds))
        if not findings:
            findings.append(Finding(
                code=FindingCode.SYSTEM_HEALTHY,
                severity=Severity.INFO,
                message="All observed metrics within normal bounds.",
                context={},
            ))
        return SystemReport(
            node_id=snap.node_id,
            collected_at=snap.collected_at,
            findings=tuple(findings),
        )
