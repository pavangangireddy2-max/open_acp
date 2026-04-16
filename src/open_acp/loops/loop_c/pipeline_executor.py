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
from typing import Any, Optional
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
        runtime_context = self._build_runtime_context(
            content_type=content_type,
            module_context=module_context,
            domain=domain,
        )

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

    def execute_review_stage(
        self,
        content_type: str,
        module_context: dict,
        domain: str = "ml-engineering",
        stage_id: Optional[str] = None,
        review_notes: str = "",
    ) -> dict[str, Any]:
        """Execute exactly one stage, save a review packet, and stop.

        If ``stage_id`` is omitted, the next incomplete stage is executed.
        If ``stage_id`` is provided, that stage is re-generated using all saved
        artifacts from prior stages as context.
        """
        pipeline_def = self.pipeline_loader.load(content_type)
        runtime_context = self._build_runtime_context(
            content_type=content_type,
            module_context=module_context,
            domain=domain,
            review_notes=review_notes,
        )
        module_id = runtime_context.get("module_id", "unknown")

        existing_artifacts = self._load_saved_artifacts(
            content_type=content_type,
            module_id=module_id,
            pipeline_def=pipeline_def,
        )
        stage = self._select_review_stage(
            pipeline_def=pipeline_def,
            existing_artifacts=existing_artifacts,
            requested_stage_id=stage_id,
        )

        if stage is None:
            self._assemble_output(existing_artifacts, content_type, runtime_context)
            return {
                "status": "complete",
                "pipeline_id": pipeline_def.pipeline_id,
                "module_id": module_id,
                "artifacts": existing_artifacts,
                "final_document_path": str(
                    self.output_dir / content_type / module_id / "final_document.md"
                ),
            }

        prior_artifacts = self._collect_prior_artifacts(
            pipeline_def=pipeline_def,
            existing_artifacts=existing_artifacts,
            stage_id=stage.id,
        )

        artifact = self._execute_stage(
            stage=stage,
            pipeline_def=pipeline_def,
            previous_artifacts=prior_artifacts,
            module_context=runtime_context,
            domain=domain,
        )

        self._save_artifact(artifact, content_type, module_id)
        next_stage_id = self._next_stage_id(pipeline_def, stage.id)
        review_packet = self._build_review_packet(
            stage=stage,
            pipeline_def=pipeline_def,
            artifact=artifact,
            module_context=runtime_context,
            next_stage_id=next_stage_id,
        )
        review_packet_paths = self._save_review_packet(
            packet=review_packet,
            content_type=content_type,
            module_id=module_id,
            stage_id=stage.id,
        )

        artifacts_with_current = prior_artifacts.copy()
        artifacts_with_current[stage.id] = artifact

        if next_stage_id is None:
            self._assemble_output(artifacts_with_current, content_type, runtime_context)

        return {
            "status": "awaiting_review",
            "pipeline_id": pipeline_def.pipeline_id,
            "module_id": module_id,
            "stage_id": stage.id,
            "artifact": artifact,
            "review_packet": review_packet,
            "review_packet_paths": review_packet_paths,
            "next_stage_id": next_stage_id,
            "final_document_path": (
                str(self.output_dir / content_type / module_id / "final_document.md")
                if next_stage_id is None
                else None
            ),
        }

    def _build_runtime_context(
        self,
        content_type: str,
        module_context: dict,
        domain: str,
        review_notes: str = "",
    ) -> dict:
        """Build the runtime context shared by full and review-mode execution."""
        resolved_profile = module_context.get("pedagogy_profile") or self.pedagogy_resolver.resolve(
            content_type=content_type,
            domain=domain,
        )

        runtime_context = module_context.copy()
        runtime_context.setdefault("domain", domain)
        runtime_context["pedagogy_profile"] = resolved_profile
        runtime_context.setdefault("execution_scope", "module")
        runtime_context.setdefault("execution_id", runtime_context.get("module_id", "unknown"))
        runtime_context.setdefault("execution_title", runtime_context.get("title", "Untitled"))
        runtime_context.setdefault("module_id", runtime_context["execution_id"])
        runtime_context.setdefault("title", runtime_context["execution_title"])
        if review_notes:
            runtime_context["manual_review_notes"] = review_notes
        return runtime_context

    @staticmethod
    def _context_id(module_context: dict) -> str:
        return module_context.get("execution_id", module_context.get("module_id", "unknown"))

    @staticmethod
    def _context_title(module_context: dict) -> str:
        return module_context.get("execution_title", module_context.get("title", "Untitled"))

    def _load_saved_artifacts(
        self,
        content_type: str,
        module_id: str,
        pipeline_def: PipelineDefinition,
    ) -> dict[str, StageArtifact]:
        """Load previously saved stage artifacts for a module."""
        output_path = self.output_dir / content_type / module_id
        loaded: dict[str, StageArtifact] = {}
        if not output_path.exists():
            return loaded

        for stage in pipeline_def.stages:
            artifact_file = output_path / f"{stage.id}.json"
            if not artifact_file.exists():
                continue
            with open(artifact_file, encoding="utf-8") as f:
                loaded[stage.id] = StageArtifact.model_validate(json.load(f))
        return loaded

    @staticmethod
    def _select_review_stage(
        pipeline_def: PipelineDefinition,
        existing_artifacts: dict[str, StageArtifact],
        requested_stage_id: Optional[str],
    ) -> Optional[StageDefinition]:
        """Choose which stage to execute in review mode."""
        if requested_stage_id:
            for stage in pipeline_def.stages:
                if stage.id == requested_stage_id:
                    return stage
            raise ValueError(f"Unknown stage_id='{requested_stage_id}' for pipeline '{pipeline_def.pipeline_id}'.")

        for stage in pipeline_def.stages:
            if stage.id not in existing_artifacts:
                return stage
        return None

    @staticmethod
    def _collect_prior_artifacts(
        pipeline_def: PipelineDefinition,
        existing_artifacts: dict[str, StageArtifact],
        stage_id: str,
    ) -> dict[str, StageArtifact]:
        """Collect artifacts from stages before ``stage_id`` in pipeline order."""
        prior: dict[str, StageArtifact] = {}
        for stage in pipeline_def.stages:
            if stage.id == stage_id:
                return prior
            if stage.id not in existing_artifacts:
                raise RuntimeError(
                    f"Cannot execute stage '{stage_id}' because prior stage '{stage.id}' has no saved artifact."
                )
            prior[stage.id] = existing_artifacts[stage.id]
        raise ValueError(f"Stage '{stage_id}' not found in pipeline '{pipeline_def.pipeline_id}'.")

    @staticmethod
    def _next_stage_id(pipeline_def: PipelineDefinition, stage_id: str) -> Optional[str]:
        """Return the stage that follows ``stage_id`` in the pipeline."""
        for index, stage in enumerate(pipeline_def.stages):
            if stage.id != stage_id:
                continue
            if index + 1 < len(pipeline_def.stages):
                return pipeline_def.stages[index + 1].id
            return None
        raise ValueError(f"Stage '{stage_id}' not found in pipeline '{pipeline_def.pipeline_id}'.")

    def _build_review_packet(
        self,
        stage: StageDefinition,
        pipeline_def: PipelineDefinition,
        artifact: StageArtifact,
        module_context: dict,
        next_stage_id: Optional[str],
    ) -> dict[str, Any]:
        """Create a concise human review packet for a completed stage."""
        return {
            "pipeline_id": pipeline_def.pipeline_id,
            "content_type": pipeline_def.content_type,
            "display_name": pipeline_def.display_name,
            "stage_id": stage.id,
            "execution_scope": module_context.get("execution_scope", "module"),
            "execution_id": self._context_id(module_context),
            "execution_title": self._context_title(module_context),
            "module_id": module_context.get("module_id", "unknown"),
            "module_title": module_context.get("title", "Untitled"),
            "instructional_pattern": module_context.get("instructional_pattern"),
            "course_title": module_context.get("course_title"),
            "curriculum_module_title": module_context.get("curriculum_module_title"),
            "module_topic_count": module_context.get("module_topic_count"),
            "module_learning_unit_count": module_context.get("module_learning_unit_count"),
            "module_learning_unit_types": module_context.get("module_learning_unit_types"),
            "module_practice_types": module_context.get("module_practice_types"),
            "module_assessment_question_types": module_context.get("module_assessment_question_types"),
            "checkpoint_required": stage.checkpoint_required,
            "human_approval_default": stage.human_approval_default,
            "validated": artifact.validated,
            "review_decision": artifact.review_decision,
            "review_summary": artifact.review_summary,
            "review_findings": artifact.review_findings,
            "attempts": artifact.attempts,
            "schema_path": artifact.schema_path,
            "key_decisions": self._extract_key_decisions(stage.id, artifact.data),
            "next_stage_id": next_stage_id,
            "generated_at": artifact.created_at,
        }

    def _extract_key_decisions(self, stage_id: str, data: dict) -> list[str]:
        """Summarize the most important human-review decisions for a stage."""
        if stage_id == "objectives":
            objectives = data.get("objectives", [])
            bloom_levels = sorted({obj.get("bloom_level", "?") for obj in objectives})
            assessment_methods = sorted({obj.get("assessment_method", "?") for obj in objectives})
            return [
                f"{len(objectives)} learning objectives were generated.",
                f"Bloom coverage: {', '.join(bloom_levels) if bloom_levels else 'none'}.",
                f"Assessment methods proposed: {', '.join(assessment_methods) if assessment_methods else 'none'}.",
            ]

        if stage_id == "outline":
            sections = data.get("sections", [])
            teaching_modes = [section.get("teaching_mode", "?") for section in sections]
            headings = [section.get("heading", "Untitled") for section in sections[:6]]
            return [
                f"{len(sections)} sections were sequenced for roughly {data.get('total_estimated_minutes', '?')} minutes.",
                f"Teaching modes used: {', '.join(teaching_modes) if teaching_modes else 'none'}.",
                f"Section flow: {' | '.join(headings) if headings else 'none'}.",
            ]

        if stage_id == "core_content":
            sections = data.get("sections", [])
            examples = sum(len(section.get("examples", [])) for section in sections)
            citations = sum(len(section.get("citations", [])) for section in sections)
            return [
                f"{len(sections)} content sections were generated with reported word count {data.get('word_count', '?')}.",
                f"Total examples included: {examples}.",
                f"Total citation entries included: {citations}.",
            ]

        if stage_id == "activities":
            activities = data.get("activities", [])
            activity_types = sorted({activity.get("type", "?") for activity in activities})
            total_minutes = sum(int(activity.get("time_minutes", 0)) for activity in activities)
            return [
                f"{len(activities)} activities were generated.",
                f"Activity types: {', '.join(activity_types) if activity_types else 'none'}.",
                f"Estimated practice time: {total_minutes} minutes.",
            ]

        if stage_id == "brand_polish":
            change_log = data.get("change_log", [])
            score = data.get("style_compliance_score")
            score_text = f"{score:.0%}" if isinstance(score, (int, float)) else "not reported"
            return [
                f"Style compliance score: {score_text}.",
                f"Change log entries: {len(change_log)}.",
                "Polished content is ready for final presentation packaging.",
            ]

        if stage_id == "slide_deck":
            slides = data.get("slides", [])
            notes_count = sum(1 for slide in slides if slide.get("speaker_notes"))
            visuals_count = sum(1 for slide in slides if slide.get("visual_description"))
            return [
                f"{len(slides)} slides were generated.",
                f"Slides with speaker notes: {notes_count}.",
                f"Slides with visual directions: {visuals_count}.",
            ]

        return [f"Artifact keys: {', '.join(sorted(data.keys()))}."]

    def _save_review_packet(
        self,
        packet: dict[str, Any],
        content_type: str,
        module_id: str,
        stage_id: str,
    ) -> dict[str, str]:
        """Persist review packet as JSON and Markdown."""
        review_dir = self.output_dir / content_type / module_id / "review_packets"
        review_dir.mkdir(parents=True, exist_ok=True)

        json_path = review_dir / f"{stage_id}.json"
        md_path = review_dir / f"{stage_id}.md"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=2)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(self._render_review_packet_markdown(packet))

        return {"json": str(json_path), "markdown": str(md_path)}

    @staticmethod
    def _render_review_packet_markdown(packet: dict[str, Any]) -> str:
        """Render a review packet into a human-readable checkpoint note."""
        lines = [
            f"# Review Packet: {packet['stage_id']}",
            "",
            f"- Pipeline: `{packet['pipeline_id']}`",
            f"- Content Type: `{packet['content_type']}`",
            f"- Execution Scope: `{packet.get('execution_scope', 'module')}`",
            f"- Execution Target: `{packet.get('execution_id', packet['module_id'])}` — {packet.get('execution_title', packet['module_title'])}",
            f"- Checkpoint Required: `{packet['checkpoint_required']}`",
            f"- Human Approval Default: `{packet['human_approval_default']}`",
            f"- Validated: `{packet['validated']}`",
            f"- Review Decision: `{packet['review_decision']}`",
            f"- Attempts: `{packet['attempts']}`",
            f"- Next Stage: `{packet['next_stage_id'] or 'complete'}`",
            "",
            "## Context",
        ]

        if packet.get("course_title"):
            lines.append(f"- Course: {packet['course_title']}")
        if packet.get("curriculum_module_title"):
            lines.append(f"- Module: {packet['curriculum_module_title']}")
        if packet.get("instructional_pattern"):
            lines.append(f"- Instructional Pattern: `{packet['instructional_pattern']}`")
        if packet.get("module_topic_count") is not None:
            lines.append(f"- Topics Planned: {packet['module_topic_count']}")
        if packet.get("module_learning_unit_count") is not None:
            lines.append(f"- Learning Units Planned: {packet['module_learning_unit_count']}")
        if packet.get("module_learning_unit_types"):
            rendered = ", ".join(f"`{item}`" for item in packet["module_learning_unit_types"])
            lines.append(f"- Learning Unit Types: {rendered}")
        if packet.get("module_practice_types"):
            lines.append(f"- Practice Types: {', '.join(packet['module_practice_types'])}")
        if packet.get("module_assessment_question_types"):
            lines.append(
                f"- Assessment Question Types: {', '.join(packet['module_assessment_question_types'])}"
            )

        lines.extend(
            [
                "",
            "## Review Summary",
            packet.get("review_summary", "") or "No summary provided.",
            "",
            "## Key Decisions",
            ]
        )

        for item in packet.get("key_decisions", []):
            lines.append(f"- {item}")

        lines.extend(["", "## Findings"])
        findings = packet.get("review_findings", [])
        if not findings:
            lines.append("- No explicit findings.")
        else:
            for finding in findings:
                lines.append(
                    f"- [{finding.get('status', 'WARNING')}] {finding.get('criterion', 'criterion')}: "
                    f"{finding.get('detail', '')}"
                )

        return "\n".join(lines) + "\n"

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
            instructional_pattern=module_context.get("instructional_pattern"),
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

        parts.append("\n## Execution Scope")
        scope_keys = [
            ("Execution Scope", "execution_scope"),
            ("Execution ID", "execution_id"),
            ("Execution Title", "execution_title"),
            ("Instructional Pattern", "instructional_pattern"),
            ("Curriculum", "curriculum_title"),
            ("Course", "course_title"),
            ("Module", "curriculum_module_title"),
            ("Planned Topics", "module_topic_count"),
            ("Planned Learning Units", "module_learning_unit_count"),
            ("Learning Unit Types", "module_learning_unit_types"),
            ("Practice Types", "module_practice_types"),
            ("Assessment Question Types", "module_assessment_question_types"),
            ("Estimated Hours", "estimated_hours"),
            ("Packaging Profile", "packaging_profile_id"),
        ]
        for label, key in scope_keys:
            value = module_context.get(key)
            if value not in (None, "", [], {}):
                parts.append(f"- {label}: {value}")

        parts.append("\n## Runtime Context")
        skip_keys = {
            "execution_scope",
            "execution_id",
            "execution_title",
            "instructional_pattern",
            "curriculum_title",
            "course_title",
            "curriculum_module_title",
            "module_topic_count",
            "module_learning_unit_count",
            "module_learning_unit_types",
            "module_practice_types",
            "module_assessment_question_types",
            "estimated_hours",
            "packaging_profile_id",
        }
        for key, value in module_context.items():
            if key in skip_keys:
                continue
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
