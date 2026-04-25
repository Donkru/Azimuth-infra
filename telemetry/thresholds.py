from dataclasses import dataclass

@dataclass(frozen=True)
class Thresholds:
    cpu_warning: float = 60.0
    cpu_critical: float = 85.0
    memory_warning: float = 75.0
    memory_critical: float = 90.0
    disk_warning: float = 80.0
    disk_critical: float = 95.0
    process_cpu_unknown_threshold: float = 1.0
    process_mem_unknown_threshold: float = 1.0

DEFAULT_THRESHOLDS = Thresholds()
