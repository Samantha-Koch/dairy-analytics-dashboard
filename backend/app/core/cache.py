from __future__ import annotations


class Cache:
    """
    Placeholder cache interface.

    Swap to Redis or a proper caching layer when needed.
    """

    def get(self, key: str) -> str | None:
        return None

    def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        return None


cache = Cache()

