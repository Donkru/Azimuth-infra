"""
Sentinel persistence layer.

Public surface:
    SentinelStore       - the class used by the runtime
    initialize_database - module-level helper for schema bootstrap

Implementation modules (schema, migrations) are intentionally not re-exported.
Callers should always go through SentinelStore.
"""
from .store import SentinelStore, initialize_database

__all__ = ["SentinelStore", "initialize_database"]