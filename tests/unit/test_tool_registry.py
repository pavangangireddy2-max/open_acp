"""Unit tests for the tool registry and base tool contract."""
import pytest

from open_acp.tools.base_tool import BaseTool, ToolResult, ToolStatus, ToolTier
from open_acp.tools.tool_registry import ToolRegistry


class MockGenerateTool(BaseTool):
    name = "mock_generate"
    capability = "generation"
    provider = "mock"
    tier = ToolTier.LOCAL
    description = "A mock generation tool for testing"

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, data={"text": "mock output"})


class MockAssessmentTool(BaseTool):
    name = "mock_assessment"
    capability = "assessment"
    provider = "mock"
    tier = ToolTier.LOCAL
    description = "A mock assessment tool for testing"

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=True, data={"questions": []})


class UnavailableTool(BaseTool):
    name = "unavailable_tool"
    capability = "generation"
    provider = "missing"
    tier = ToolTier.STRONG

    def execute(self, **kwargs) -> ToolResult:
        return ToolResult(success=False, error="Not available")

    def get_status(self) -> ToolStatus:
        return ToolStatus.UNAVAILABLE


def test_tool_result():
    result = ToolResult(success=True, data={"key": "value"}, cost_usd=0.01)
    assert result.success is True
    assert result.cost_usd == 0.01


def test_base_tool_default_status():
    tool = MockGenerateTool()
    assert tool.get_status() == ToolStatus.AVAILABLE


def test_base_tool_estimate_cost():
    tool = MockGenerateTool()
    assert tool.estimate_cost() == 0.0


def test_base_tool_execute():
    tool = MockGenerateTool()
    result = tool.execute()
    assert result.success is True
    assert result.data["text"] == "mock output"


def test_base_tool_repr():
    tool = MockGenerateTool()
    assert "MockGenerateTool" in repr(tool)
    assert "mock_generate" in repr(tool)


def test_registry_starts_empty():
    reg = ToolRegistry()
    reg.reset()
    assert reg.list_all() == []


def test_registry_manual_registration():
    reg = ToolRegistry()
    reg.reset()
    reg._tools["mock_generate"] = MockGenerateTool()
    reg._tools["mock_assessment"] = MockAssessmentTool()

    assert len(reg.list_all()) == 2
    assert reg.get("mock_generate") is not None
    assert reg.get("nonexistent") is None


def test_registry_get_by_capability():
    reg = ToolRegistry()
    reg.reset()
    reg._tools["mock_generate"] = MockGenerateTool()
    reg._tools["mock_assessment"] = MockAssessmentTool()
    reg._tools["unavailable_tool"] = UnavailableTool()

    gen_tools = reg.get_by_capability("generation")
    assert len(gen_tools) == 2  # mock_generate + unavailable_tool

    assess_tools = reg.get_by_capability("assessment")
    assert len(assess_tools) == 1


def test_registry_get_available():
    reg = ToolRegistry()
    reg.reset()
    reg._tools["mock_generate"] = MockGenerateTool()
    reg._tools["unavailable_tool"] = UnavailableTool()

    available = reg.get_available()
    assert len(available) == 1
    assert available[0].name == "mock_generate"


def test_registry_capability_catalog():
    reg = ToolRegistry()
    reg.reset()
    reg._tools["mock_generate"] = MockGenerateTool()
    reg._tools["mock_assessment"] = MockAssessmentTool()

    catalog = reg.capability_catalog()
    assert "generation" in catalog
    assert "assessment" in catalog
    assert "mock_generate" in catalog["generation"]


def test_registry_reset():
    reg = ToolRegistry()
    reg._tools["test"] = MockGenerateTool()
    reg.reset()
    assert len(reg.list_all()) == 0


def test_registry_singleton():
    """Verify ToolRegistry is a singleton."""
    reg1 = ToolRegistry()
    reg2 = ToolRegistry()
    assert reg1 is reg2
