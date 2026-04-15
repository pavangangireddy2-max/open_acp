"""ToolContract ABC — every tool in open_acp inherits from this."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel


class ToolTier(str, Enum):
    STRONG = "strong"    # claude-opus-4-6
    CHEAP = "cheap"      # claude-haiku-4-5-20251001
    LOCAL = "local"      # No API call needed


class ToolStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"


class ToolResult(BaseModel):
    success: bool
    data: dict = {}
    error: Optional[str] = None
    cost_usd: float = 0.0
    duration_seconds: float = 0.0


class BaseTool(ABC):
    """Abstract base for all open_acp tools."""

    name: str = ""
    capability: str = ""          # "generation", "assessment", "knowledge", "review", "output"
    provider: str = ""            # "claude", "local", "web"
    tier: ToolTier = ToolTier.LOCAL
    cost_per_call: float = 0.0
    agent_skills: list[str] = []  # Layer 3 skills this tool needs
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool and return a result."""
        ...

    def get_status(self) -> ToolStatus:
        """Check if the tool is available. Override for API-dependent tools."""
        return ToolStatus.AVAILABLE

    def estimate_cost(self, **kwargs) -> float:
        """Estimate cost for this invocation. Override for variable-cost tools."""
        return self.cost_per_call

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name} capability={self.capability}>"
