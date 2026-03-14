import psutil
import time


def cpu_usage():
    return psutil.cpu_percent(interval=1)


def memory_usage():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "used_percent": mem.percent,
        "available_gb": round(mem.available / (1024 ** 3), 2),
    }


def disk_usage():
    disk = psutil.disk_usage("/")
    return {
        "total_gb": round(disk.total / (1024 ** 3), 2),
        "used_percent": disk.percent,
        "free_gb": round(disk.free / (1024 ** 3), 2),
    }


def uptime_hours():
    boot = psutil.boot_time()
    return round((time.time() - boot) / 3600, 2)
