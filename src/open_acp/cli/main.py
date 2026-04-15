"""open_acp CLI — Typer-based command-line interface."""
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
            table.add_row("B: Curriculum", f"{len(curriculum.get('modules', []))} modules, pedagogy={loop_b.get('selected_pedagogy', '?')}")

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

        module_context = {
            "module_id": module_id,
            "title": module_title,
            "domain": domain,
            "estimated_hours": estimated_hours,
            "objectives": [
                {"id": "obj_1", "statement": f"Understand core concepts of {module_title}", "bloom_level": "understand"},
                {"id": "obj_2", "statement": f"Apply {module_title} concepts to solve problems", "bloom_level": "apply"},
                {"id": "obj_3", "statement": f"Analyze trade-offs in {module_title} approaches", "bloom_level": "analyze"},
            ],
            "prerequisites": [],
        }

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
