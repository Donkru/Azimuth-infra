from enum import Enum
from dataclasses import dataclass

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"

class FindingCode(Enum):
    CPU_ELEVATED = "cpu_elevated"
    CPU_CRITICAL = "cpu_critical"
    MEMORY_HIGH = "memory_high"
    MEMORY_CRITICAL = "memory_critical"
    DISK_HIGH = "disk_high"
    SERVICE_MISSING = "service_missing"
    PROCESS_UNKNOWN_HIGH = "process_unknown_high"
    SYSTEM_HEALTHY = "system_healthy"

@dataclass(frozen=True)
class Finding:
    code: FindingCode
    severity: Severity
    message: str
    context: dict  # e.g. {"process": "python3", "cpu_percent": 72.1}