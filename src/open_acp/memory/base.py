"""MemoryStore ABC — all memory stores implement this interface."""
from abc import ABC, abstractmethod
from typing import Any, Optional


class MemoryStore(ABC):
    """Abstract base for memory stores (Episodic, Feedback)."""

    @abstractmethod
    def store(self, key: str, data: dict) -> None:
        """Store data under a key."""
        ...

    @abstractmethod
    def retrieve(self, key: str) -> Optional[dict]:
        """Retrieve data by key."""
        ...

    @abstractmethod
    def query(self, **filters) -> list[dict]:
        """Query stored data with filters."""
        ...

    @abstractmethod
    def append(self, collection: str, data: dict) -> None:
        """Append data to a collection (for append-only stores)."""
        ...
