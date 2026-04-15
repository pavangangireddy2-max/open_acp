"""Load markdown skill files and inject as system prompts."""
from pathlib import Path
from typing import Optional


class SkillLoader:
    """Reads markdown skill files from the skills/ directory."""

    def __init__(self, skills_dir: Optional[str] = None):
        if skills_dir:
            self.base_dir = Path(skills_dir)
        else:
            self.base_dir = Path(__file__).parent

    def load(self, skill_ref: str) -> str:
        """Load a skill markdown file by reference path.

        Examples:
            load("pipelines/concept_explainer/01_outline")
            load("meta/reviewer")
        """
        # Try with .md extension
        path = self.base_dir / f"{skill_ref}.md"
        if not path.exists():
            # Try without extension
            path = self.base_dir / skill_ref
            if not path.exists():
                raise FileNotFoundError(f"Skill not found: {skill_ref} (searched {self.base_dir})")

        return path.read_text(encoding="utf-8")

    def exists(self, skill_ref: str) -> bool:
        """Check if a skill file exists."""
        path = self.base_dir / f"{skill_ref}.md"
        return path.exists() or (self.base_dir / skill_ref).exists()

    def list_pipeline_skills(self, pipeline_name: str) -> list[str]:
        """List all skill files for a given pipeline."""
        pipeline_dir = self.base_dir / "pipelines" / pipeline_name
        if not pipeline_dir.exists():
            return []
        return sorted(
            f.stem for f in pipeline_dir.glob("*.md")
        )
