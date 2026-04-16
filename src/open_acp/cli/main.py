"""open_acp CLI — Typer-based command-line interface."""
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="oacp",
    help="Agentic Content Production System",
    no_args_is_help=True,
)
console = Console()


def _build_module_context(
    content_type: str,
    module_id: str,
    module_title: str,
    domain: str,
    estimated_hours: float,
) -> dict:
    """Build the initial Loop C module context.

    First-wave pipelines generate objectives inside the pipeline, so they should
    not receive placeholder objectives up front.
    """
    context = {
        "module_id": module_id,
        "title": module_title,
        "domain": domain,
        "estimated_hours": estimated_hours,
        "prerequisites": [],
    }

    if content_type not in {"concept_explainer", "project_building"}:
        context["objectives"] = [
            {"id": "obj_1", "statement": f"Understand core concepts of {module_title}", "bloom_level": "understand"},
            {"id": "obj_2", "statement": f"Apply {module_title} concepts to solve problems", "bloom_level": "apply"},
            {"id": "obj_3", "statement": f"Analyze trade-offs in {module_title} approaches", "bloom_level": "analyze"},
        ]

    return context


def _outputs_root() -> Path:
    return Path(__file__).resolve().parents[3] / "outputs"


def _render_operator_guide() -> None:
    console.print(
        Panel(
            "[bold]Recommended Operating Mode[/bold]\n"
            "Use Open ACP in staged review mode for real curriculum and content work.\n"
            "Prefer [cyan]review-loop[/cyan], [cyan]review-domain[/cyan], and [cyan]review[/cyan]\n"
            "instead of jumping straight to [magenta]run[/magenta].",
            title="Operator Guide",
            border_style="blue",
        )
    )

    table = Table(title="Recommended Command Flow")
    table.add_column("Goal", style="cyan")
    table.add_column("Command", style="white")
    table.add_row(
        "Loop A one node at a time",
        "oacp review-loop loop_a --domain genai --cycle-id genai_niat_b3_v1 --product-family NIAT --product-version B3",
    )
    table.add_row(
        "Loop B one node at a time",
        "oacp review-loop loop_b --domain genai --content-type concept_explainer --cycle-id genai_niat_b3_v1 --product-family NIAT --product-version B3",
    )
    table.add_row(
        "Loop A + Loop B checkpoint",
        "oacp review-domain --domain genai --content-type concept_explainer --cycle-id genai_niat_b3_v1 --product-family NIAT --product-version B3",
    )
    table.add_row(
        "Loop C one stage at a time",
        "oacp review --content-type concept_explainer --domain genai --title \"How Retrieval-Augmented Generation Works\" --module-id rag_intro --hours 1.0",
    )
    table.add_row(
        "Batch/full execution only after approval",
        "oacp run --full --content-type concept_explainer --domain genai --title \"How Retrieval-Augmented Generation Works\" --module-id rag_intro --hours 1.0",
    )
    console.print(table)

    prompts = Table(title="Example Prompts To Ask Codex")
    prompts.add_column("#", style="cyan", width=4)
    prompts.add_column("Prompt", style="white")
    prompts.add_row("1", "Start a fresh genai + NIAT B3 run from Loop A in strict mode, one node at a time.")
    prompts.add_row("2", "Run only the next pending Loop B node for this cycle and stop for review.")
    prompts.add_row("3", "Start concept_explainer in review mode and stop after each stage.")
    prompts.add_row("4", "Wipe runtime wiki, restart the cycle, and show me the ingest_signals checkpoint first.")
    prompts.add_row("5", "Explain this review packet before moving to the next node.")
    console.print(prompts)

    console.print(
        "\n[dim]Operational rule of thumb: use staged review commands for real work, "
        "and use full run modes only after curriculum and product context are reviewed.[/dim]"
    )


def _build_domain_review_packet(
    domain: str,
    content_type: str,
    cycle_id: str,
    loop_a_result: dict,
    loop_b_result: dict,
) -> dict:
    curriculum = loop_b_result.get("curriculum_map", {})
    course_design = loop_b_result.get("course_design", {}) or {}
    courses = course_design.get("courses", []) or curriculum.get("modules", [])
    module_design = loop_b_result.get("module_design", {}) or {}
    topic_design = loop_b_result.get("topic_design", {}) or {}
    learning_unit_plan = loop_b_result.get("learning_unit_plan", {}) or {}
    packaging_profile = loop_b_result.get("packaging_profile", {}) or {}
    alignment_report = loop_b_result.get("assessment_alignment_report", {}) or {}
    return {
        "domain": domain,
        "content_type": content_type,
        "cycle_id": cycle_id,
        "product_context": {
            "product_label": (loop_b_result.get("product_context", {}) or {}).get("product_label", "Stack-only default"),
            "structure_profile_id": (loop_b_result.get("structure_profile", {}) or {}).get(
                "structure_profile_id",
                "standard_product_structure",
            ),
        },
        "loop_a": {
            "created_count": len(loop_a_result.get("wiki_entries_created", [])),
            "updated_count": len(loop_a_result.get("wiki_entries_updated", [])),
            "drift_score": loop_a_result.get("drift_score", 0.0),
        },
        "loop_b": {
            "pedagogy_profile": loop_b_result.get("pedagogy_profile", "unknown"),
            "pedagogy_rationale": loop_b_result.get("pedagogy_rationale", "unknown"),
            "curriculum_label": curriculum.get("program_name", f"{domain} Curriculum"),
            "total_hours": curriculum.get("total_hours", 0),
            "course_count": len(courses),
            "courses": [
                {
                    "course_id": course.get("course_id", course.get("module_id", f"course_{index+1}")),
                    "title": course.get("title", "Untitled"),
                    "sequence": course.get("sequence", index + 1),
                    "estimated_hours": course.get("estimated_hours", 0),
                    "content_types": course.get("content_types", []),
                    "objective_count": len(course.get("objective_ids", course.get("objectives", []))),
                }
                for index, course in enumerate(courses)
            ],
            "packaging_profile_id": packaging_profile.get("packaging_profile_id", "default"),
            "module_count": module_design.get("total_module_count", 0),
            "topic_count": topic_design.get("total_topic_count", 0),
            "learning_unit_count": learning_unit_plan.get("total_learning_unit_count", 0),
            "question_types_covered": loop_b_result.get("learning_assessment_plan", {}).get("question_types_covered", []),
            "alignment_status": alignment_report.get("overall_status", "unknown"),
            "assessment_schedule": loop_b_result.get("learning_assessment_plan", {}).get("assessment_schedule", {}),
        },
    }


def _render_domain_review_packet_markdown(packet: dict) -> str:
    product_context = packet["product_context"]
    loop_a = packet["loop_a"]
    loop_b = packet["loop_b"]
    lines = [
        f"# Domain Review Packet: {packet['domain']}",
        "",
        f"- Content Type Seed: `{packet['content_type']}`",
        f"- Cycle ID: `{packet['cycle_id']}`",
        f"- Product Context: `{product_context['product_label']}`",
        f"- Structure Profile: `{product_context['structure_profile_id']}`",
        "",
        "## Loop A Summary",
        f"- Wiki entries created: {loop_a['created_count']}",
        f"- Wiki entries updated: {loop_a['updated_count']}",
        f"- Drift score: {loop_a['drift_score']}",
        "",
        "## Loop B Summary",
        f"- Curriculum: {loop_b['curriculum_label']}",
        f"- Pedagogy Profile: `{loop_b['pedagogy_profile']}`",
        f"- Pedagogy Rationale: {loop_b['pedagogy_rationale']}",
        f"- Total Hours: {loop_b['total_hours']}",
        f"- Course Count: {loop_b['course_count']}",
        f"- Packaging Profile: `{loop_b['packaging_profile_id']}`",
        f"- Module Count: {loop_b['module_count']}",
        f"- Topic Count: {loop_b['topic_count']}",
        f"- Learning Unit Count: {loop_b['learning_unit_count']}",
        f"- Skill Assessment Alignment: `{loop_b['alignment_status']}`",
        "",
        "## Proposed Courses",
    ]

    for course in loop_b["courses"]:
        content_types = ", ".join(course.get("content_types", [])) or "not specified"
        lines.append(
            f"- C{course['sequence']}: `{course['course_id']}` — {course['title']} "
            f"({course['estimated_hours']}h, objectives={course['objective_count']}, content_types={content_types})"
        )

    if loop_b.get("question_types_covered"):
        lines.extend(
            [
                "",
                "## Learning Assessment Coverage",
                f"- Question Types Covered: {', '.join(loop_b['question_types_covered'])}",
            ]
        )

    schedule = loop_b.get("assessment_schedule", {})
    if schedule:
        lines.extend(["", "## Assessment Schedule"])
        for key, value in schedule.items():
            lines.append(f"- {key}: {value}")

    return "\n".join(lines) + "\n"


def _save_domain_review_packet(packet: dict) -> dict[str, str]:
    review_dir = _outputs_root() / "domain_reviews" / packet["domain"] / packet["cycle_id"]
    review_dir.mkdir(parents=True, exist_ok=True)

    json_path = review_dir / "curriculum_review.json"
    md_path = review_dir / "curriculum_review.md"

    json_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    md_path.write_text(_render_domain_review_packet_markdown(packet), encoding="utf-8")

    return {"json": str(json_path), "markdown": str(md_path)}


@app.command()
def run(
    content_type: str = typer.Option("concept_explainer", "--content-type", "-t", help="Content type to produce"),
    domain: str = typer.Option("ml-engineering", "--domain", "-d", help="Domain context"),
    module_title: str = typer.Option("Introduction to the Topic", "--title", help="Module title"),
    module_id: str = typer.Option("m1", "--module-id", help="Module identifier"),
    estimated_hours: float = typer.Option(1.0, "--hours", help="Estimated session hours"),
    auto_approve: bool = typer.Option(False, "--auto-approve", help="Auto-approve all gates"),
    cycle_id: str = typer.Option("cycle_1", "--cycle-id", help="Cycle identifier"),
    full_pipeline: bool = typer.Option(False, "--full", "-f", help="Run full A→B→C→D pipeline (not just Loop C)"),
):
    """Run a content production pipeline."""
    from open_acp.utils.logger import setup_logging
    setup_logging()

    console.print(Panel(
        f"[bold]Agentic Content Production[/bold]\n"
        f"Pipeline: [cyan]{content_type}[/cyan]\n"
        f"Domain: [green]{domain}[/green]\n"
        f"Module: [yellow]{module_title}[/yellow]\n"
        f"Mode: [magenta]{'Full A→B→C→D' if full_pipeline else 'Loop C only'}[/magenta]",
        title="open_acp",
        border_style="blue",
    ))

    if full_pipeline:
        # Run the complete 4-loop pipeline
        from open_acp.orchestrator.runner import PipelineRunner
        runner = PipelineRunner()

        try:
            result = runner.run_cycle(
                domain=domain,
                content_type=content_type,
                module_title=module_title,
                module_id=module_id,
                estimated_hours=estimated_hours,
                auto_approve=auto_approve,
                cycle_id=cycle_id,
            )

            console.print(f"\n[bold green]Pipeline complete![/bold green]")

            # Summary table
            table = Table(title="Cycle Summary")
            table.add_column("Loop", style="cyan")
            table.add_column("Result", style="green")

            loop_a = result.get("loop_a_result", {})
            table.add_row("A: Intelligence", f"{len(loop_a.get('wiki_entries_created', []))} created, {len(loop_a.get('wiki_entries_updated', []))} updated")

            loop_b = result.get("loop_b_result", {})
            curriculum = loop_b.get("curriculum_map", {})
            table.add_row("B: Curriculum", f"{len(curriculum.get('modules', []))} modules, pedagogy_profile={loop_b.get('pedagogy_profile', '?')}")

            loop_c = result.get("loop_c_result", {})
            table.add_row("C: Content", f"{loop_c.get('stages_completed', 0)} stages completed")

            loop_d = result.get("loop_d_result", {})
            health = loop_d.get("health_report", {})
            table.add_row("D: Evaluate", f"{health.get('insights_count', 0)} insights, {health.get('fix_routes_count', 0)} fixes")

            console.print(table)

        except Exception as e:
            console.print(f"\n[bold red]Pipeline failed: {e}[/bold red]")
            raise typer.Exit(code=1)
    else:
        # Run Loop C only (original behavior)
        from open_acp.tools.tool_registry import registry
        registry.discover()

        console.print(f"\n[dim]Tools: {len(registry.get_available())} available[/dim]")

        module_context = _build_module_context(
            content_type=content_type,
            module_id=module_id,
            module_title=module_title,
            domain=domain,
            estimated_hours=estimated_hours,
        )

        from open_acp.loops.loop_c.pipeline_executor import PipelineExecutor
        executor = PipelineExecutor()

        try:
            artifacts = executor.execute_pipeline(
                content_type=content_type,
                module_context=module_context,
                domain=domain,
            )
            console.print(f"\n[bold green]Pipeline complete! {len(artifacts)} stages[/bold green]")
        except Exception as e:
            console.print(f"\n[bold red]Pipeline failed: {e}[/bold red]")
            raise typer.Exit(code=1)


@app.command()
def guide():
    """Show the recommended agentic, stage-by-stage operating flow."""
    _render_operator_guide()


@app.command()
def review(
    content_type: str = typer.Option("concept_explainer", "--content-type", "-t", help="Content type to produce"),
    domain: str = typer.Option("ml-engineering", "--domain", "-d", help="Domain context"),
    module_title: str = typer.Option("Introduction to the Topic", "--title", help="Module title"),
    module_id: str = typer.Option("m1", "--module-id", help="Module identifier"),
    estimated_hours: float = typer.Option(1.0, "--hours", help="Estimated session hours"),
    stage_id: str = typer.Option("", "--stage", help="Optional stage to regenerate explicitly"),
    review_notes: str = typer.Option("", "--review-notes", help="Optional reviewer guidance to inject into this stage"),
):
    """Run exactly one Loop C stage, save a checkpoint packet, and stop for review."""
    from open_acp.utils.logger import setup_logging
    setup_logging()

    from open_acp.tools.tool_registry import registry
    registry.discover()

    module_context = _build_module_context(
        content_type=content_type,
        module_id=module_id,
        module_title=module_title,
        domain=domain,
        estimated_hours=estimated_hours,
    )

    from open_acp.loops.loop_c.pipeline_executor import PipelineExecutor
    executor = PipelineExecutor()

    try:
        result = executor.execute_review_stage(
            content_type=content_type,
            module_context=module_context,
            domain=domain,
            stage_id=stage_id or None,
            review_notes=review_notes,
        )
    except Exception as e:
        console.print(f"\n[bold red]Review-stage run failed: {e}[/bold red]")
        raise typer.Exit(code=1)

    if result["status"] == "complete":
        console.print(
            Panel(
                f"[bold green]Pipeline already complete[/bold green]\n"
                f"Final document: [cyan]{result['final_document_path']}[/cyan]",
                title="Review Mode",
                border_style="green",
            )
        )
        return

    packet = result["review_packet"]
    console.print(
        Panel(
            f"[bold]Stage[/bold]: [cyan]{result['stage_id']}[/cyan]\n"
            f"[bold]Decision[/bold]: [green]{packet['review_decision']}[/green]\n"
            f"[bold]Validated[/bold]: [yellow]{packet['validated']}[/yellow]\n"
            f"[bold]Next Stage[/bold]: [magenta]{result['next_stage_id'] or 'complete'}[/magenta]\n"
            f"[bold]Review Packet[/bold]: [blue]{result['review_packet_paths']['markdown']}[/blue]",
            title="Stage Complete — Awaiting Review",
            border_style="blue",
        )
    )

    table = Table(title="Key Decisions")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Decision", style="white")
    for idx, item in enumerate(packet.get("key_decisions", []), start=1):
        table.add_row(str(idx), item)
    console.print(table)

    findings = packet.get("review_findings", [])
    if findings:
        findings_table = Table(title="Reviewer Findings")
        findings_table.add_column("Status", style="magenta", width=10)
        findings_table.add_column("Criterion", style="cyan")
        findings_table.add_column("Detail", style="white")
        for finding in findings:
            findings_table.add_row(
                finding.get("status", "WARNING"),
                finding.get("criterion", "criterion"),
                finding.get("detail", ""),
            )
        console.print(findings_table)

    console.print(
        "\n[dim]To proceed, run the same command again without --stage to execute the next pending stage.[/dim]"
    )


@app.command("review-loop")
def review_loop(
    loop_id: str = typer.Argument(..., help="Loop to review: loop_a or loop_b"),
    domain: str = typer.Option("ml-engineering", "--domain", "-d", help="Domain or stack context"),
    content_type: str = typer.Option("concept_explainer", "--content-type", "-t", help="Content type seed used by Loop B"),
    cycle_id: str = typer.Option("cycle_1", "--cycle-id", help="Cycle identifier"),
    product_family: str = typer.Option("", "--product-family", help="Optional product family context"),
    product_version: str = typer.Option("", "--product-version", help="Optional product version or batch"),
    require_product_context: bool = typer.Option(True, "--require-product/--allow-stack-only", help="Require explicit product context for this run"),
    strict_domain_inputs: bool = typer.Option(True, "--strict-domain-inputs/--allow-domain-fallback", help="Require manifest-backed domain inputs for this run"),
    stage_id: str = typer.Option("", "--stage", help="Optional stage to run explicitly"),
):
    """Run exactly one Loop A or Loop B stage, save a checkpoint packet, and stop."""
    from open_acp.utils.logger import setup_logging
    setup_logging()

    from open_acp.orchestrator.loop_review import LoopReviewRunner

    base_state = {
        "domain": domain,
        "cycle_id": cycle_id,
    }
    if product_family:
        base_state["product_family"] = product_family
    if product_version:
        base_state["product_version"] = product_version
    base_state["require_product_context"] = require_product_context
    base_state["strict_domain_inputs"] = strict_domain_inputs
    if loop_id.strip().lower().replace("-", "_") in {"loop_b", "b", "loopb"}:
        base_state["content_type"] = content_type

    runner = LoopReviewRunner()

    try:
        result = runner.execute_review_stage(
            loop_id=loop_id,
            base_state=base_state,
            stage_id=stage_id or None,
        )
    except Exception as e:
        console.print(f"\n[bold red]Loop review failed: {e}[/bold red]")
        raise typer.Exit(code=1)

    if result["status"] == "complete":
        console.print(
            Panel(
                f"[bold green]Loop already complete[/bold green]\n"
                f"State file: [cyan]{result['state_path']}[/cyan]",
                title="Loop Review",
                border_style="green",
            )
        )
        return

    packet = result["review_packet"]
    console.print(
        Panel(
            f"[bold]Loop[/bold]: [cyan]{result['loop_id']}[/cyan]\n"
            f"[bold]Stage[/bold]: [cyan]{result['stage_id']}[/cyan]\n"
            f"[bold]Next Stage[/bold]: [magenta]{result['next_stage_id'] or 'complete'}[/magenta]\n"
            f"[bold]Review Packet[/bold]: [blue]{result['review_packet_paths']['markdown']}[/blue]",
            title="Loop Stage Complete — Awaiting Review",
            border_style="blue",
        )
    )

    console.print(packet.get("summary", "Stage complete."))

    table = Table(title="Key Decisions")
    table.add_column("#", style="cyan", width=4)
    table.add_column("Decision", style="white")
    for idx, item in enumerate(packet.get("key_decisions", []), start=1):
        table.add_row(str(idx), item)
    console.print(table)

    console.print(
        "\n[dim]To continue, rerun this command without --stage to execute the next pending stage in the same loop.[/dim]"
    )


@app.command("review-domain")
def review_domain(
    domain: str = typer.Option("ml-engineering", "--domain", "-d", help="Domain context"),
    content_type: str = typer.Option("concept_explainer", "--content-type", "-t", help="Content type seed used for curriculum shaping"),
    cycle_id: str = typer.Option("cycle_1", "--cycle-id", help="Cycle identifier"),
    product_family: str = typer.Option("", "--product-family", help="Optional product family context"),
    product_version: str = typer.Option("", "--product-version", help="Optional product version or batch"),
    require_product_context: bool = typer.Option(True, "--require-product/--allow-stack-only", help="Require explicit product context for this run"),
    strict_domain_inputs: bool = typer.Option(True, "--strict-domain-inputs/--allow-domain-fallback", help="Require manifest-backed domain inputs for this run"),
):
    """Run Loop A and Loop B, save a curriculum review packet, and stop."""
    from open_acp.utils.logger import setup_logging
    setup_logging()

    console.print(
        Panel(
            f"[bold]Curriculum Review[/bold]\n"
            f"Domain: [green]{domain}[/green]\n"
            f"Content Type Seed: [cyan]{content_type}[/cyan]\n"
            f"Product: [yellow]{product_family or 'stack-only default'}[/yellow]\n"
            f"Mode: [magenta]Loop A → Loop B only[/magenta]",
            title="open_acp",
            border_style="blue",
        )
    )

    from open_acp.loops.loop_a.graph import run_loop_a
    from open_acp.loops.loop_b.graph import run_loop_b

    try:
        loop_a_result = run_loop_a(
            domain=domain,
            cycle_id=cycle_id,
            product_family=product_family or None,
            product_version=product_version or None,
            require_product_context=require_product_context,
            strict_domain_inputs=strict_domain_inputs,
        )
        loop_b_result = run_loop_b(
            domain=domain,
            cycle_id=cycle_id,
            content_type=content_type,
            product_family=product_family or None,
            product_version=product_version or None,
            require_product_context=require_product_context,
            strict_domain_inputs=strict_domain_inputs,
        )
    except Exception as e:
        console.print(f"\n[bold red]Curriculum review failed: {e}[/bold red]")
        raise typer.Exit(code=1)

    packet = _build_domain_review_packet(
        domain=domain,
        content_type=content_type,
        cycle_id=cycle_id,
        loop_a_result=loop_a_result,
        loop_b_result=loop_b_result,
    )
    paths = _save_domain_review_packet(packet)

    loop_b = packet["loop_b"]
    console.print(
        Panel(
            f"[bold]Pedagogy Profile[/bold]: [cyan]{loop_b['pedagogy_profile']}[/cyan]\n"
            f"[bold]Rationale[/bold]: [white]{loop_b['pedagogy_rationale']}[/white]\n"
            f"[bold]Courses[/bold]: [yellow]{loop_b['course_count']}[/yellow]\n"
            f"[bold]Packaging[/bold]: [magenta]{loop_b['packaging_profile_id']}[/magenta]\n"
            f"[bold]Review Packet[/bold]: [blue]{paths['markdown']}[/blue]",
            title="Curriculum Checkpoint — Awaiting Review",
            border_style="blue",
        )
    )

    modules_table = Table(title="Proposed Curriculum Courses")
    modules_table.add_column("Seq", style="cyan", width=5)
    modules_table.add_column("Course", style="white")
    modules_table.add_column("Hours", style="green", width=8)
    modules_table.add_column("Content Types", style="magenta")
    for course in loop_b["courses"]:
        modules_table.add_row(
            str(course["sequence"]),
            course["title"],
            str(course["estimated_hours"]),
            ", ".join(course.get("content_types", [])) or "n/a",
        )
    console.print(modules_table)

    console.print(
        "\n[dim]Review the curriculum packet first. Once approved, pick a course seed or a downstream module/topic design stage before continuing into Loop C.[/dim]"
    )


@app.command()
def status():
    """Show system status — tools, pipelines, wiki."""
    from open_acp.tools.tool_registry import registry
    registry.discover()

    # Tools
    console.print("[bold]Tool Registry[/bold]")
    catalog = registry.capability_catalog()
    for capability, tools in sorted(catalog.items()):
        console.print(f"  {capability}: {', '.join(tools)}")

    # Pipelines
    from open_acp.pipeline_defs.pipeline_loader import PipelineLoader
    loader = PipelineLoader()
    available = loader.list_available()

    table = Table(title="Available Pipelines")
    table.add_column("Content Type")
    table.add_column("Family")
    table.add_column("Stages")

    for p in sorted(available):
        try:
            pd = loader.load(p)
            table.add_row(p, pd.family, str(len(pd.stages)))
        except Exception:
            table.add_row(p, "?", "error")

    console.print(table)

    # Wiki
    from open_acp.knowledge.wiki_engine import WikiEngine
    wiki = WikiEngine()
    entities = wiki.list_entities()
    console.print(f"\n[bold]Wiki[/bold]: {len(entities)} entities")
    for etype in ["skill", "competitor", "audience_segment", "concept"]:
        count = len([e for e in entities if e["entity_type"] == etype])
        if count > 0:
            console.print(f"  {etype}: {count}")


if __name__ == "__main__":
    app()
