"""Wiki operations tool — wraps WikiEngine for the tool registry."""
from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier, ToolStatus


class WikiOps(BaseTool):
    """Wiki CRUD, search, and lint operations."""

    name = "wiki_ops"
    capability = "knowledge"
    provider = "local"
    tier = ToolTier.LOCAL
    description = "Create, update, search, and lint wiki entities"
    agent_skills = ["wiki_curator"]

    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from open_acp.knowledge.wiki_engine import WikiEngine
            self._engine = WikiEngine()
        return self._engine

    def execute(self, **kwargs) -> ToolResult:
        """Execute a wiki operation.

        Required kwargs:
            operation: str — "create", "update", "search", "list", "lint", "rebuild_index", "get", "supersede"

        Additional kwargs depend on operation (passed through to WikiEngine methods).
        """
        operation = kwargs.get("operation", "")
        engine = self._get_engine()

        try:
            if operation == "create":
                path = engine.create_entity(
                    entity_type=kwargs["entity_type"],
                    entity_id=kwargs["entity_id"],
                    title=kwargs["title"],
                    content=kwargs["content"],
                    confidence=kwargs.get("confidence", 0.5),
                    sources=kwargs.get("sources", []),
                    cross_references=kwargs.get("cross_references", []),
                    durability=kwargs.get("durability", "unknown"),
                )
                return ToolResult(success=True, data={"path": path, "operation": "create"})

            elif operation == "update":
                updated = engine.update_entity(
                    entity_id=kwargs["entity_id"],
                    entity_type=kwargs["entity_type"],
                    content_delta=kwargs["content_delta"],
                    reason=kwargs["reason"],
                    new_confidence=kwargs.get("new_confidence"),
                    new_sources=kwargs.get("new_sources"),
                )
                return ToolResult(success=updated, data={"operation": "update", "found": updated})

            elif operation == "search":
                results = engine.search(
                    query=kwargs["query"],
                    entity_type=kwargs.get("entity_type"),
                )
                return ToolResult(success=True, data={"results": results, "count": len(results)})

            elif operation == "list":
                entities = engine.list_entities(entity_type=kwargs.get("entity_type"))
                return ToolResult(success=True, data={"entities": entities, "count": len(entities)})

            elif operation == "get":
                entity = engine.get_entity(
                    entity_type=kwargs["entity_type"],
                    entity_id=kwargs["entity_id"],
                )
                if entity:
                    return ToolResult(success=True, data=entity)
                return ToolResult(success=False, error=f"Entity not found: {kwargs['entity_type']}/{kwargs['entity_id']}")

            elif operation == "lint":
                issues = engine.lint()
                return ToolResult(success=True, data={"issues": issues, "count": len(issues)})

            elif operation == "rebuild_index":
                index = engine.rebuild_index()
                return ToolResult(success=True, data={"index": index})

            elif operation == "supersede":
                result = engine.supersede(
                    old_entity_id=kwargs["old_entity_id"],
                    old_entity_type=kwargs["old_entity_type"],
                    new_entity_id=kwargs["new_entity_id"],
                    new_entity_type=kwargs["new_entity_type"],
                    reason=kwargs["reason"],
                )
                return ToolResult(success=result, data={"operation": "supersede"})

            else:
                return ToolResult(success=False, error=f"Unknown operation: {operation}")

        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def get_status(self) -> ToolStatus:
        engine = self._get_engine()
        return ToolStatus.AVAILABLE if engine.wiki_dir.exists() else ToolStatus.UNAVAILABLE
