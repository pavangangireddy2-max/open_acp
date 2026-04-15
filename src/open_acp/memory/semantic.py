"""Semantic memory — wiki-integrated knowledge layer."""
from typing import Optional
from open_acp.memory.base import MemoryStore
from open_acp.knowledge.wiki_engine import WikiEngine


class WikiSemanticStore(MemoryStore):
    """Semantic memory backed by the wiki engine."""

    def __init__(self, wiki_dir: Optional[str] = None):
        self.wiki = WikiEngine(wiki_dir)

    def store(self, key: str, data: dict) -> None:
        entity_type = data.get("entity_type", "concept")
        self.wiki.create_entity(
            entity_type=entity_type,
            entity_id=key,
            title=data.get("title", key),
            content=data.get("content", ""),
            confidence=data.get("confidence", 0.5),
        )

    def retrieve(self, key: str) -> Optional[dict]:
        # Try each entity type
        for etype in self.wiki.ENTITY_TYPES:
            entity = self.wiki.get_entity(etype, key)
            if entity:
                return entity
        return None

    def query(self, **filters) -> list[dict]:
        query_str = filters.get("query", "")
        entity_type = filters.get("entity_type")
        if query_str:
            return self.wiki.search(query_str, entity_type)
        return self.wiki.list_entities(entity_type)

    def append(self, collection: str, data: dict) -> None:
        # For semantic store, append = update entity
        entity_type = data.get("entity_type", "concept")
        entity_id = data.get("entity_id", collection)
        self.wiki.update_entity(
            entity_id=entity_id,
            entity_type=entity_type,
            content_delta=data.get("content", ""),
            reason=data.get("reason", "append"),
        )
