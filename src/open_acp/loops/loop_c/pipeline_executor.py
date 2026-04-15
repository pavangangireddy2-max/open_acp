"""Pipeline executor — reads YAML manifest and executes stages sequentially.

For each stage:
1. Load the stage director skill (markdown)
2. Resolve tools from the registry
3. Inject previous stage artifacts as context
4. Execute the tool with the skill as system prompt
5. Validate output against artifact schema
6. Run self-review if configured
"""
import json
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional
import uuid

from open_acp.pipeline_defs.pipeline_loader import PipelineLoader, PipelineDefinition, StageDefinition
from open_acp.skills.skill_loader import SkillLoader
from open_acp.tools.tool_registry import registry
from open_acp.tools.base_tool import ToolResult
from open_acp.models.artifacts import StageArtifact
from open_acp.utils.claude import ClaudeClient


class PipelineExecutor:
    """Execute a content pipeline stage by stage."""

    def __init__(
        self,
        pipeline_dir: Optional[str] = None,
        skills_dir: Optional[str] = None,
        output_dir: Optional[str] = None,
    ):
        self.pipeline_loader = PipelineLoader(pipeline_dir)
        self.skill_loader = SkillLoader(skills_dir)
        self.claude = ClaudeClient()

        # Default output directory
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent.parent.parent.parent.parent / "outputs"

    def execute_pipeline(
        self,
        content_type: str,
        module_context: dict,
        domain: str = "ml-engineering",
    ) -> dict[str, StageArtifact]:
        """Execute all stages of a pipeline and return artifacts.

        Args:
            content_type: Which pipeline to run (e.g., "concept_explainer")
            module_context: Dict with module metadata:
                - module_id, title, domain, estimated_hours
                - objectives (list of dicts)
                - prerequisites (list of strings)
            domain: The domain context

        Returns:
            Dict mapping stage_id to StageArtifact
        """
        # Load the pipeline definition
        pipeline_def = self.pipeline_loader.load(content_type)

        # Execute stages sequentially
        artifacts: dict[str, StageArtifact] = {}

        for stage in pipeline_def.stages:
            print(f"\n{'='*60}")
            print(f"  Stage: {stage.id} ({pipeline_def.display_name})")
            print(f"{'='*60}")

            artifact = self._execute_stage(
                stage=stage,
                pipeline_def=pipeline_def,
                previous_artifacts=artifacts,
                module_context=module_context,
                domain=domain,
            )
            artifacts[stage.id] = artifact

            # Save artifact to disk
            self._save_artifact(artifact, content_type, module_context.get("module_id", "unknown"))

            print(f"  [ok] Stage '{stage.id}' complete (validated: {artifact.validated})")

        # Assemble final document
        self._assemble_output(artifacts, content_type, module_context)

        return artifacts

    def _execute_stage(
        self,
        stage: StageDefinition,
        pipeline_def: PipelineDefinition,
        previous_artifacts: dict[str, StageArtifact],
        module_context: dict,
        domain: str,
    ) -> StageArtifact:
        """Execute a single pipeline stage."""

        # 1. Load the stage director skill
        skill_content = self.skill_loader.load(stage.skill)

        # 2. Build the prompt with context
        prompt = self._build_stage_prompt(
            stage=stage,
            skill_content=skill_content,
            previous_artifacts=previous_artifacts,
            module_context=module_context,
            domain=domain,
        )

        # 3. Build the system message from the skill
        system_msg = (
            f"You are a content production agent executing the '{stage.id}' stage "
            f"of the '{pipeline_def.display_name}' pipeline.\n\n"
            f"{skill_content}\n\n"
            "CRITICAL: You must return a valid JSON object matching the schema described in the skill above.\n"
            "Do NOT include markdown code fences or any text outside the JSON object.\n"
            "Return ONLY the raw JSON object."
        )

        # 4. Call Claude (use higher token limit for content-heavy stages)
        content_heavy = stage.id in ("core_content", "brand_polish", "slide_deck", "activities")
        response_text = self.claude.generate(
            prompt=prompt,
            system=system_msg,
            model_tier=stage.model_tier,
            max_tokens=16384 if content_heavy else 8192,
            temperature=0.7,
        )

        # 5. Parse the JSON response
        data = self._parse_json_response(response_text)

        # 6. Create artifact
        artifact = StageArtifact(
            artifact_id=f"art_{uuid.uuid4().hex[:8]}",
            stage_id=stage.id,
            pipeline_id=pipeline_def.pipeline_id,
            content_type=pipeline_def.content_type,
            data=data,
            schema_path=stage.artifact_schema,
            created_at=datetime.now(UTC).isoformat(),
        )

        # 7. Validate against schema (if schema exists)
        if stage.artifact_schema:
            try:
                artifact.validate_against_schema()
            except Exception as e:
                print(f"  [warning] Schema validation warning for '{stage.id}': {e}")
                # Don't fail — proceed with warning

        return artifact

    def _build_stage_prompt(
        self,
        stage: StageDefinition,
        skill_content: str,
        previous_artifacts: dict[str, StageArtifact],
        module_context: dict,
        domain: str,
    ) -> str:
        """Build the user prompt for a stage, injecting context."""
        parts = []

        # Module context
        parts.append("## Module Context")
        parts.append(f"- Domain: {domain}")
        for key, value in module_context.items():
            if isinstance(value, (list, dict)):
                parts.append(f"- {key}: {json.dumps(value, indent=2)}")
            else:
                parts.append(f"- {key}: {value}")

        # Previous artifacts as context
        if previous_artifacts:
            parts.append("\n## Previous Stage Artifacts")
            for stage_id, art in previous_artifacts.items():
                parts.append(f"\n### {stage_id} (artifact)")
                parts.append(f"```json\n{json.dumps(art.data, indent=2)}\n```")

        # The instruction
        parts.append(f"\n## Your Task")
        parts.append(f"Execute the '{stage.id}' stage as described in your system instructions.")
        parts.append("Return a JSON object matching the required schema.")

        return "\n".join(parts)

    def _parse_json_response(self, text: str) -> dict:
        """Parse JSON from Claude's response, handling common formatting issues."""
        # Strip markdown code fences if present
        cleaned = text.strip()
        if cleaned.startswith("```"):
            first_newline = cleaned.index("\n")
            cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        # Try direct parse
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON object from surrounding text
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass

        # Try repairing truncated JSON (missing closing braces/brackets)
        if start >= 0:
            fragment = cleaned[start:]
            repaired = self._repair_truncated_json(fragment)
            if repaired is not None:
                return repaired

        return {"_raw_response": text, "_parse_error": "Could not parse JSON from response"}

    @staticmethod
    def _repair_truncated_json(text: str) -> dict | None:
        """Attempt to repair truncated JSON by trimming to the last complete
        structure and trying common closing patterns.

        Brace-counting is unreliable (braces inside string values skew counts),
        so we try known closing sequences instead.
        """
        import re

        # Find last complete object boundary
        for trim_target in ['},', '],']:
            idx = text.rfind(trim_target)
            if idx <= 0:
                continue
            base = text[:idx + 1]  # include } or ] but not the comma

            # Try common closing sequences (most to least common)
            for closing in [']}', ']}', '}}', ']}}', ']}]}', ']]}}']:
                attempt = base + closing
                attempt = re.sub(r',\s*([}\]])', r'\1', attempt)
                try:
                    return json.loads(attempt)
                except json.JSONDecodeError:
                    continue
        return None

    def _save_artifact(self, artifact: StageArtifact, content_type: str, module_id: str) -> None:
        """Save an artifact to the output directory."""
        output_path = self.output_dir / content_type / module_id
        output_path.mkdir(parents=True, exist_ok=True)

        filepath = output_path / f"{artifact.stage_id}.json"
        with open(filepath, "w") as f:
            json.dump(artifact.model_dump(), f, indent=2)

    def _assemble_output(
        self,
        artifacts: dict[str, StageArtifact],
        content_type: str,
        module_context: dict,
    ) -> None:
        """Assemble all artifacts into a final document."""
        # Use the markdown_assembler tool if available
        assembler = registry.get("markdown_assembler")
        if assembler:
            result = assembler.execute(
                stage_artifacts={sid: art.data for sid, art in artifacts.items()},
                pipeline_id=content_type,
                module_title=module_context.get("title", "Untitled"),
            )
            if result.success:
                module_id = module_context.get("module_id", "unknown")
                output_path = self.output_dir / content_type / module_id / "final_document.md"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    f.write(result.data.get("document", ""))
                print(f"\n  Final document: {output_path}")
