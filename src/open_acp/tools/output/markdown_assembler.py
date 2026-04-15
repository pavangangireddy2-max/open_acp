"""MarkdownAssembler tool — assembles stage artifacts into a final markdown document."""
import time
from typing import Optional

from open_acp.tools.base_tool import BaseTool, ToolResult, ToolTier


# Canonical stage ordering for document assembly.
_STAGE_ORDER = [
    "objectives",
    "outline",
    "core_content",
    "activities",
    "brand_polish",
    "slide_deck",
]


class MarkdownAssembler(BaseTool):
    """Assemble pipeline stage artifacts into a final markdown document."""

    name = "markdown_assembler"
    capability = "output"
    provider = "local"
    tier = ToolTier.LOCAL
    cost_per_call = 0.0
    description = "Assemble pipeline stage artifacts into a final markdown document"

    def execute(self, **kwargs) -> ToolResult:
        """Assemble stage artifacts into markdown.

        Args:
            stage_artifacts: dict[str, dict] mapping stage_id to artifact data.
            pipeline_id: Identifier for the pipeline run.
            module_title: Optional title for the assembled document.
        """
        stage_artifacts: dict[str, dict] = kwargs.get("stage_artifacts", {})
        pipeline_id: str = kwargs.get("pipeline_id", "unknown")
        module_title: Optional[str] = kwargs.get("module_title")

        if not stage_artifacts:
            return ToolResult(success=False, error="stage_artifacts is required and must not be empty")

        try:
            start = time.time()
            parts: list[str] = []

            # Document title
            title = module_title or f"Module: {pipeline_id}"
            parts.append(f"# {title}\n")
            parts.append(f"*Pipeline: `{pipeline_id}`*\n")

            # Sort stages by canonical order, with unknown stages appended at the end
            ordered_stages = sorted(
                stage_artifacts.keys(),
                key=lambda s: _STAGE_ORDER.index(s) if s in _STAGE_ORDER else len(_STAGE_ORDER),
            )

            for stage_id in ordered_stages:
                artifact = stage_artifacts[stage_id]
                parts.append(f"\n---\n\n## {_stage_heading(stage_id)}\n")
                parts.append(_render_artifact(stage_id, artifact))

            document = "\n".join(parts)
            word_count = len(document.split())
            duration = time.time() - start

            return ToolResult(
                success=True,
                data={"document": document, "word_count": word_count},
                duration_seconds=round(duration, 4),
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


def _stage_heading(stage_id: str) -> str:
    """Convert a stage_id like 'core_content' to a readable heading."""
    return stage_id.replace("_", " ").title()


def _render_artifact(stage_id: str, artifact: dict) -> str:
    """Render a single stage artifact to markdown."""
    if stage_id == "objectives":
        return _render_objectives(artifact)
    elif stage_id == "outline":
        return _render_outline(artifact)
    elif stage_id == "core_content":
        return _render_core_content(artifact)
    elif stage_id == "activities":
        return _render_activities(artifact)
    elif stage_id == "brand_polish":
        return _render_brand_polish(artifact)
    elif stage_id == "slide_deck":
        return _render_slide_deck(artifact)
    else:
        return _render_generic(artifact)


def _render_objectives(artifact: dict) -> str:
    lines: list[str] = []
    for obj in artifact.get("objectives", []):
        bloom = obj.get("bloom_level", "")
        lines.append(f"- **{obj.get('id', '?')}** [{bloom}]: {obj.get('statement', '')}")
    return "\n".join(lines)


def _render_outline(artifact: dict) -> str:
    lines: list[str] = []
    for section in artifact.get("sections", []):
        minutes = section.get("estimated_minutes", "?")
        lines.append(f"### {section.get('heading', 'Untitled')} (~{minutes} min)")
        lines.append(f"{section.get('purpose', '')}")
        for sub in section.get("subsections", []):
            lines.append(f"  - {sub}")
        lines.append("")
    if artifact.get("teaching_flow"):
        lines.append(f"**Teaching flow:** {artifact['teaching_flow']}")
    return "\n".join(lines)


def _render_core_content(artifact: dict) -> str:
    lines: list[str] = []
    for section in artifact.get("sections", []):
        lines.append(f"### {section.get('heading', 'Untitled')}\n")
        lines.append(section.get("content_markdown", ""))
        if section.get("key_terms"):
            lines.append(f"\n**Key terms:** {', '.join(section['key_terms'])}")
        lines.append("")
    return "\n".join(lines)


def _render_activities(artifact: dict) -> str:
    lines: list[str] = []
    for i, act in enumerate(artifact.get("activities", []), 1):
        act_type = act.get("type", "exercise")
        lines.append(f"### Activity {i}: {act.get('title', act_type.title())} ({act_type})\n")
        lines.append(f"**Time:** {act.get('time_minutes', '?')} minutes\n")
        lines.append(act.get("instructions", ""))
        if act.get("expected_output"):
            lines.append(f"\n**Expected output:** {act['expected_output']}")
        lines.append("")
    return "\n".join(lines)


def _render_brand_polish(artifact: dict) -> str:
    lines: list[str] = []
    lines.append(artifact.get("polished_content", ""))
    score = artifact.get("style_compliance_score")
    if score is not None:
        lines.append(f"\n*Style compliance: {score:.0%}*")
    return "\n".join(lines)


def _render_slide_deck(artifact: dict) -> str:
    lines: list[str] = []
    for slide in artifact.get("slides", []):
        num = slide.get("slide_number", "?")
        lines.append(f"### Slide {num}: {slide.get('title', 'Untitled')}\n")
        for point in slide.get("content_points", []):
            lines.append(f"- {point}")
        lines.append(f"\n> **Speaker notes:** {slide.get('speaker_notes', '')}")
        if slide.get("visual_description"):
            lines.append(f"\n*Visual: {slide['visual_description']}*")
        lines.append("")
    return "\n".join(lines)


def _render_generic(artifact: dict) -> str:
    """Fallback renderer for unknown stage types."""
    lines: list[str] = []
    for key, value in artifact.items():
        if isinstance(value, str):
            lines.append(f"**{key}:** {value}\n")
        elif isinstance(value, list):
            lines.append(f"**{key}:**\n")
            for item in value:
                lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append(f"**{key}:** `{value}`\n")
    return "\n".join(lines)
