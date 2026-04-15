"""Pipeline executor — reads YAML manifest and executes stages sequentially.

V1 behavior:
1. Load the stage director skill and layered style context
2. Generate a candidate artifact
3. Parse and schema-validate it
4. Review it against review_focus and success criteria
5. Revise up to the configured limit for strict pipelines
6. Persist the accepted artifact
"""
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Optional
import uuid

from open_acp.models.artifacts import StageArtifact
from open_acp.pipeline_defs.pipeline_loader import PipelineDefinition, PipelineLoader, StageDefinition
from open_acp.skills.skill_loader import SkillLoader
from open_acp.styles.pedagogy_resolver import PedagogyResolver
from open_acp.styles.style_loader import StyleLoader
from open_acp.tools.tool_registry import registry
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
        self.style_loader = StyleLoader()
        self.pedagogy_resolver = PedagogyResolver()
        self.claude = ClaudeClient()

        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).resolve().parents[4] / "outputs"

    def execute_pipeline(
        self,
        content_type: str,
        module_context: dict,
        domain: str = "ml-engineering",
    ) -> dict[str, StageArtifact]:
        """Execute all stages of a pipeline and return artifacts."""
        pipeline_def = self.pipeline_loader.load(content_type)
        resolved_profile = module_context.get("pedagogy_profile") or self.pedagogy_resolver.resolve(
            content_type=content_type,
            domain=domain,
        )

        runtime_context = module_context.copy()
        runtime_context.setdefault("domain", domain)
        runtime_context["pedagogy_profile"] = resolved_profile

        artifacts: dict[str, StageArtifact] = {}

        for stage in pipeline_def.stages:
            print(f"\n{'='*60}")
            print(f"  Stage: {stage.id} ({pipeline_def.display_name})")
            print(f"{'='*60}")

            artifact = self._execute_stage(
                stage=stage,
                pipeline_def=pipeline_def,
                previous_artifacts=artifacts,
                module_context=runtime_context,
                domain=domain,
            )
            artifacts[stage.id] = artifact
            self._save_artifact(artifact, content_type, runtime_context.get("module_id", "unknown"))

            print(
                f"  [ok] Stage '{stage.id}' complete "
                f"(validated: {artifact.validated}, review: {artifact.review_decision}, attempts: {artifact.attempts})"
            )

        self._assemble_output(artifacts, content_type, runtime_context)
        return artifacts

    def _execute_stage(
        self,
        stage: StageDefinition,
        pipeline_def: PipelineDefinition,
        previous_artifacts: dict[str, StageArtifact],
        module_context: dict,
        domain: str,
    ) -> StageArtifact:
        """Execute a single pipeline stage, with review/revision loops when enabled."""
        skill_content = self.skill_loader.load(stage.skill)
        reviewer_skill = ""
        if stage.review_focus or stage.success_criteria:
            reviewer_skill = self.skill_loader.load("meta/reviewer")

        style_context = self.style_loader.load_for_pipeline_as_text(
            content_type=pipeline_def.content_type,
            domain=domain,
            pedagogy_profile=module_context.get("pedagogy_profile"),
        )

        max_attempts = 1 + pipeline_def.review_max_rounds if pipeline_def.strict_execution else 1
        revision_request = ""
        last_artifact: Optional[StageArtifact] = None

        for attempt in range(1, max_attempts + 1):
            prompt = self._build_stage_prompt(
                stage=stage,
                pipeline_def=pipeline_def,
                previous_artifacts=previous_artifacts,
                module_context=module_context,
                domain=domain,
                style_context=style_context,
                revision_request=revision_request,
            )

            system_msg = (
                f"You are a content production agent executing the '{stage.id}' stage "
                f"of the '{pipeline_def.display_name}' pipeline.\n\n"
                f"{skill_content}\n\n"
                "CRITICAL: Return ONLY a valid JSON object. "
                "Do not include markdown code fences or explanatory prose outside the JSON."
            )

            content_heavy = stage.id in (
                "project_brief",
                "core_content",
                "brand_polish",
                "slide_deck",
                "activities",
            )
            response_text = self.claude.generate(
                prompt=prompt,
                system=system_msg,
                model_tier=stage.model_tier,
                max_tokens=16384 if content_heavy else 8192,
                temperature=0.7,
            )

            data = self._parse_json_response(response_text)
            artifact = StageArtifact(
                artifact_id=f"art_{uuid.uuid4().hex[:8]}",
                stage_id=stage.id,
                pipeline_id=pipeline_def.pipeline_id,
                content_type=pipeline_def.content_type,
                data=data,
                schema_path=stage.artifact_schema,
                created_at=datetime.now(UTC).isoformat(),
                attempts=attempt,
            )

            validation_errors = self._validate_artifact(artifact)
            artifact.validation_errors = validation_errors

            if validation_errors:
                artifact.review_decision = "REVISE" if pipeline_def.strict_execution else "PASS_WITH_WARNINGS"
                artifact.review_summary = "Schema validation failed."
                artifact.review_findings = [
                    {
                        "criterion": "schema_validation",
                        "status": "FAIL",
                        "detail": error,
                    }
                    for error in validation_errors
                ]
            else:
                review_result = self._review_stage(
                    stage=stage,
                    pipeline_def=pipeline_def,
                    artifact=artifact,
                    reviewer_skill=reviewer_skill,
                )
                artifact.review_decision = review_result["decision"]
                artifact.review_summary = review_result["summary"]
                artifact.review_findings = review_result["findings"]

            last_artifact = artifact

            if not pipeline_def.strict_execution:
                return artifact

            has_review_failures = any(
                finding.get("status", "").upper() == "FAIL"
                for finding in artifact.review_findings
            )
            if not validation_errors and not has_review_failures:
                return artifact

            revision_request = self._build_revision_request(artifact)

        if last_artifact is not None:
            raise RuntimeError(
                f"Strict execution failed for stage '{stage.id}' after {last_artifact.attempts} attempts: "
                f"{last_artifact.review_summary or '; '.join(last_artifact.validation_errors)}"
            )
        raise RuntimeError(f"Stage '{stage.id}' failed before producing an artifact.")

    def _build_stage_prompt(
        self,
        stage: StageDefinition,
        pipeline_def: PipelineDefinition,
        previous_artifacts: dict[str, StageArtifact],
        module_context: dict,
        domain: str,
        style_context: str,
        revision_request: str = "",
    ) -> str:
        """Build the user prompt for a stage, injecting context."""
        parts = [
            "## Pipeline Context",
            f"- Pipeline ID: {pipeline_def.pipeline_id}",
            f"- Content Type: {pipeline_def.content_type}",
            f"- Stage ID: {stage.id}",
            f"- Strict Execution: {pipeline_def.strict_execution}",
            f"- Schema: {stage.artifact_schema or 'none'}",
            f"- Domain: {domain}",
            f"- Pedagogy Profile: {module_context.get('pedagogy_profile', 'unknown')}",
        ]

        parts.append("\n## Module Context")
        for key, value in module_context.items():
            if isinstance(value, (list, dict)):
                rendered = json.dumps(value, indent=2)
                parts.append(f"- {key}: {rendered}")
            else:
                parts.append(f"- {key}: {value}")

        if style_context:
            parts.append("\n## Layered Guidance")
            parts.append(style_context)

        if stage.review_focus or stage.success_criteria:
            parts.append("\n## Review Contract")
            if stage.review_focus:
                parts.append("Review Focus:")
                for item in stage.review_focus:
                    parts.append(f"- {item}")
            if stage.success_criteria:
                parts.append("Success Criteria:")
                for item in stage.success_criteria:
                    parts.append(f"- {item}")

        if previous_artifacts:
            parts.append("\n## Previous Stage Artifacts")
            for stage_id, artifact in previous_artifacts.items():
                artifact_json = json.dumps(artifact.data, indent=2)
                if len(artifact_json) > 6000:
                    artifact_json = artifact_json[:6000] + "\n... [truncated]"
                parts.append(f"\n### {stage_id}")
                parts.append(f"```json\n{artifact_json}\n```")

        if revision_request:
            parts.append("\n## Revision Request")
            parts.append(revision_request)

        parts.append("\n## Your Task")
        parts.append(f"Execute the '{stage.id}' stage and return a JSON object matching the required schema.")
        return "\n".join(parts)

    def _review_stage(
        self,
        stage: StageDefinition,
        pipeline_def: PipelineDefinition,
        artifact: StageArtifact,
        reviewer_skill: str,
    ) -> dict:
        """Review a stage artifact against configured focus points."""
        if not stage.review_focus and not stage.success_criteria:
            return {"decision": "PASS", "summary": "No review criteria configured.", "findings": []}

        artifact_json = json.dumps(artifact.data, indent=2)
        if len(artifact_json) > 10000:
            artifact_json = artifact_json[:10000] + "\n... [truncated]"

        review_prompt = "\n".join(
            [
                "Review this stage artifact using the self-review protocol below.",
                "",
                "## Stage Metadata",
                f"- Stage ID: {stage.id}",
                f"- Pipeline ID: {pipeline_def.pipeline_id}",
                f"- Strict Execution: {pipeline_def.strict_execution}",
                f"- Schema Path: {stage.artifact_schema or 'none'}",
                "",
                "## Review Focus",
                *[f"- {item}" for item in stage.review_focus],
                "",
                "## Success Criteria",
                *[f"- {item}" for item in stage.success_criteria],
                "",
                "## Artifact JSON",
                f"```json\n{artifact_json}\n```",
                "",
                "Return ONLY JSON in this shape:",
                "{",
                '  "summary": "1-3 sentence summary",',
                '  "findings": [',
                '    {"criterion": "criterion text", "status": "PASS|WARNING|FAIL", "detail": "specific evidence"}',
                "  ]",
                "}",
            ]
        )

        review_response = self.claude.generate(
            prompt=review_prompt,
            system=(
                "You are executing the Open ACP self-review protocol.\n\n"
                f"{reviewer_skill}\n\n"
                "CRITICAL: Return ONLY JSON."
            ),
            model_tier=stage.model_tier,
            max_tokens=4096,
            temperature=0.2,
        )
        parsed = self._parse_json_response(review_response)
        findings = parsed.get("findings", [])
        normalized_findings = []
        for finding in findings:
            status = str(finding.get("status", "WARNING")).upper()
            if status not in {"PASS", "WARNING", "FAIL"}:
                status = "WARNING"
            normalized_findings.append(
                {
                    "criterion": finding.get("criterion", "unspecified"),
                    "status": status,
                    "detail": finding.get("detail", ""),
                }
            )

        if parsed.get("_parse_error"):
            normalized_findings.append(
                {
                    "criterion": "review_protocol",
                    "status": "FAIL",
                    "detail": parsed["_parse_error"],
                }
            )

        decision = "PASS"
        if any(finding["status"] == "FAIL" for finding in normalized_findings):
            decision = "REVISE"
        elif any(finding["status"] == "WARNING" for finding in normalized_findings):
            decision = "PASS_WITH_WARNINGS"

        return {
            "decision": decision,
            "summary": parsed.get("summary", "Review complete."),
            "findings": normalized_findings,
        }

    def _validate_artifact(self, artifact: StageArtifact) -> list[str]:
        """Validate the artifact schema and return any errors."""
        if artifact.data.get("_parse_error"):
            return [artifact.data["_parse_error"]]

        if not artifact.schema_path:
            artifact.validated = True
            return []

        try:
            artifact.validate_against_schema()
            return []
        except Exception as exc:
            return [str(exc)]

    def _build_revision_request(self, artifact: StageArtifact) -> str:
        """Build revision notes for the next generation attempt."""
        lines = [
            "Revise the previous output to fix the issues below.",
            "",
            "Previous artifact:",
            f"```json\n{json.dumps(artifact.data, indent=2)[:6000]}\n```",
        ]

        if artifact.validation_errors:
            lines.append("\nValidation Errors:")
            for error in artifact.validation_errors:
                lines.append(f"- {error}")

        if artifact.review_findings:
            lines.append("\nReview Findings:")
            for finding in artifact.review_findings:
                lines.append(
                    f"- [{finding.get('status', 'WARNING')}] {finding.get('criterion', 'criterion')}: "
                    f"{finding.get('detail', '')}"
                )

        lines.append("\nReturn corrected JSON only.")
        return "\n".join(lines)

    def _parse_json_response(self, text: str) -> dict:
        """Parse JSON from Claude's response, handling common formatting issues."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            first_newline = cleaned.index("\n")
            cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass

        if start >= 0:
            fragment = cleaned[start:]
            repaired = self._repair_truncated_json(fragment)
            if repaired is not None:
                return repaired

        return {"_raw_response": text, "_parse_error": "Could not parse JSON from response"}

    @staticmethod
    def _repair_truncated_json(text: str) -> dict | None:
        """Attempt to repair truncated JSON by trimming to the last complete structure."""
        import re

        for trim_target in ["},", "],"]:
            idx = text.rfind(trim_target)
            if idx <= 0:
                continue
            base = text[:idx + 1]

            for closing in ["]}", "]}", "}}", "]}}", "]}]}", "]]}}"]:
                attempt = base + closing
                attempt = re.sub(r",\s*([}\]])", r"\1", attempt)
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
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(artifact.model_dump(), f, indent=2)

    def _assemble_output(
        self,
        artifacts: dict[str, StageArtifact],
        content_type: str,
        module_context: dict,
    ) -> None:
        """Assemble all artifacts into a final document."""
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
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.data.get("document", ""))
                print(f"\n  Final document: {output_path}")
