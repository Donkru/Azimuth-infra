from agent.sentinel.config.settings import SYSTEM_PROMPT
from telemetry.system_stats import ( 
cpu_usage, 
memory_usage, 
disk_usage, 
uptime_hours, 
machine_identity, 
top_processes,
)
from owner.owner_profile import summarize_owner_profile
from telemetry.process_monitor import summarize_top_processes


class LocalModel:
    def __init__(self) -> None:
        self.system_prompt = SYSTEM_PROMPT

    def generate(self, user_message: str, history: list[dict]) -> str:
        msg = user_message.lower()

        if "who is your creator" in msg or "who made you" in msg or "owner profile" in msg:
            return summarize_owner_profile()
        
        if "top processes" in msg or "processes" in msg or "top cpu" in msg:
            return summarize_top_processes()
       
        if "system status" in msg or "status" in msg:
            cpu = cpu_usage()
            mem = memory_usage()
            disk = disk_usage()
            uptime = uptime_hours()

            return (
                f"System status:\n"
                f"CPU: {cpu}%\n"
                f"RAM: {mem['used_percent']}% used "
                f"({mem['available_gb']} GB free)\n"
                f"Disk: {disk['used_percent']}% used "
                f"({disk['free_gb']} GB free)\n"
                f"Uptime: {uptime} hours"
            )

        if "full report" in msg or "operator report" in msg:
            identity = machine_identity()
            cpu = cpu_usage()
            mem = memory_usage()
            disk = disk_usage()
            uptime = uptime_hours()
            processes = top_processes()

            proc_lines = []
            for i, p in enumerate(processes, 1):
                proc_lines.append(
                    f"{i}. {p['name']} (PID {p['pid']}) "
                    f"CPU {p['cpu_percent']}% MEM {round(p['memory_percent'], 2)}%"
                )

            proc_text = "\n".join(proc_lines)

            return (
                "Sentinel Operator Report\n\n"
                f"Machine:\n"
                f"Hostname: {identity['hostname']}\n"
                f"OS: {identity['os']}\n"
                f"Architecture: {identity['architecture']}\n"
                f"CPU cores: {identity['cpu_cores']}\n\n"
                f"System Status:\n"
                f"CPU usage: {cpu}%\n"
                f"RAM used: {mem['used_percent']}% ({mem['available_gb']} GB free)\n"
                f"Disk used: {disk['used_percent']}% ({disk['free_gb']} GB free)\n"
                f"Uptime: {uptime} hours\n\n"
                f"Top Processes:\n{proc_text}"
            )


        if "cpu" in msg:
            return f"Current CPU usage is {cpu_usage()}%."

        if "memory" in msg or "ram" in msg:
            mem = memory_usage()
            return (
                f"Memory total: {mem['total_gb']} GB, "
                f"used: {mem['used_percent']}%, "
                f"available: {mem['available_gb']} GB."
            )

        if "disk" in msg or "storage" in msg:
            disk = disk_usage()
            return (
                f"Disk total: {disk['total_gb']} GB, "
                f"used: {disk['used_percent']}%, "
                f"free: {disk['free_gb']} GB."
            )

        if "uptime" in msg:
            return f"System uptime is {uptime_hours()} hours."

        history_text = " | ".join(f"{m['role']}: {m['content']}" for m in history[-4:])

        return (
            f"[local-dev-reply]\n"
            f"system={self.system_prompt}\n"
            f"history={history_text}\n"
            f"user={user_message}\n\n"
            f"Sentinel received the message but no command matched."
        )
