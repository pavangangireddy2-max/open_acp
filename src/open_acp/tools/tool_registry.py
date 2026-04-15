"""Auto-discovery tool registry — singleton that discovers all BaseTool subclasses."""
import importlib
import pkgutil
from typing import Optional

from .base_tool import BaseTool, ToolStatus


class ToolRegistry:
    """Singleton registry that auto-discovers tools under the tools/ package."""

    _instance: Optional["ToolRegistry"] = None
    _tools: dict[str, BaseTool]

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def discover(self, package_name: str = "open_acp.tools") -> None:
        """Walk the tools/ package tree and register all concrete BaseTool subclasses."""
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            return

        if not hasattr(package, "__path__"):
            return

        for importer, modname, ispkg in pkgutil.walk_packages(
            package.__path__, prefix=package.__name__ + "."
        ):
            try:
                module = importlib.import_module(modname)
            except ImportError:
                continue

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseTool)
                    and attr is not BaseTool
                    and hasattr(attr, "name")
                    and attr.name  # skip abstract or unnamed
                ):
                    instance = attr()
                    self._tools[instance.name] = instance

    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def get_by_capability(self, capability: str) -> list[BaseTool]:
        """Get all tools with a given capability."""
        return [t for t in self._tools.values() if t.capability == capability]

    def get_available(self) -> list[BaseTool]:
        """Get all tools that are currently available."""
        return [t for t in self._tools.values() if t.get_status() == ToolStatus.AVAILABLE]

    def list_all(self) -> list[BaseTool]:
        """List all registered tools."""
        return list(self._tools.values())

    def capability_catalog(self) -> dict[str, list[str]]:
        """Return tools grouped by capability."""
        catalog: dict[str, list[str]] = {}
        for tool in self._tools.values():
            catalog.setdefault(tool.capability, []).append(tool.name)
        return catalog

    def reset(self) -> None:
        """Clear all registered tools. Useful for testing."""
        self._tools.clear()


# Global singleton
registry = ToolRegistry()
