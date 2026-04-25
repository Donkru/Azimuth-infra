@dataclass(frozen=True)
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float

@dataclass(frozen=True)
class SystemSnapshot:
    node_id: str          # hostname — multi-node ready from day one
    collected_at: float   # time.time()
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    memory_total_mb: float
    disk_used_percent: float
    disk_free_gb: float
    uptime_hours: float
    processes: tuple[ProcessInfo, ...]