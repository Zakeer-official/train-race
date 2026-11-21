import time
from typing import Dict, Any, Optional

class CacheService:
    """
    High-performance caching service with TTL support.
    Supports in-memory dictionary caching with optional Redis extension.
    Prevents polling external providers independently for every connected viewer.
    """
    def __init__(self, default_ttl: int = 45):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            del self._cache[key]
            return None
        return entry["data"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        duration = ttl if ttl is not None else self.default_ttl
        self._cache[key] = {
            "data": value,
            "expires_at": time.time() + duration
        }

    def clear(self) -> None:
        self._cache.clear()

cache = CacheService()
