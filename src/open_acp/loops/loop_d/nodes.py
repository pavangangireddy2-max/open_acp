"""Loop D nodes — evaluate content, classify insights, route fixes.

Nodes:
1. collect_feedback — gather signals from mock channels
2. classify_insights — classify feedback into fix types using Claude
3. route_fixes — deterministic routing via BackpropRouter
4. health_monitor — wiki lint + content health check
"""
import json
from datetime import datetime, UTC

from open_acp.channels.mock_ingestor import MockChannelIngestor
from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.utils.claude import ClaudeClient
from open_acp.models.feedback import FixType, Severity


def collect_feedback(state: dict) -> dict:
    """Collect feedback signals from channels."""
    domain = state.get("domain", "ml-engineering")
    cycle_id = state.get("cycle_id", "cycle_1")
    content_modules = state.get("content_modules", [])

    # Use mock ingestor for now
    ingestor = MockChannelIngestor()
    batch = ingestor.generate_feedback_batch(
        domain=domain,
        content_modules=content_modules if content_modules else ["m1"],
        cycle_id=cycle_id,
    )

    feedback = [
        {
            "signal_id": s.signal_id,
            "channel": s.channel_name,
            "content": s.content,
            "category": s.channel_category.value,
        }
        for s in batch.signals
    ]
    print(f"  Collected {len(feedback)} feedback signals")
    return {"raw_feedback": feedback}


def classify_insights(state: dict) -> dict:
    """Classify feedback into insight types using Claude."""
    raw_feedback = state.get("raw_feedback", [])
    if not raw_feedback:
        return {"insights": []}

    claude = ClaudeClient()
    feedback_text = "\n".join(
        [f"- [{f['channel']}] {f['content']}" for f in raw_feedback]
    )

    # Build the valid fix type / severity values from the enums
    fix_type_values = [ft.value for ft in FixType]
    severity_values = [sv.value for sv in Severity]

    prompt = f"""Classify these feedback signals into actionable insights.

## Feedback Signals
{feedback_text}

For each distinct issue, classify it as ONE of these fix types:
{', '.join(fix_type_values)}

And one of these severities:
{', '.join(severity_values)}

Return JSON array:
[
  {{
    "insight_id": "ins_1",
    "fix_type": "content_fix",
    "severity": "high",
    "description": "Brief description",
    "evidence": "Which feedback signals support this",
    "source_channels": ["channel_name"]
  }}
]

Return ONLY the JSON array."""

    response = claude.generate(
        prompt=prompt,
        system="You are a feedback analyst classifying educational content feedback.",
        model_tier="strong",
        max_tokens=4096,
    )

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n") + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        insights_raw = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        insights_raw = []

    insights = []
    for ins in insights_raw:
        # Normalise to lowercase to match enum values
        raw_fix = ins.get("fix_type", "content_fix").lower()
        raw_sev = ins.get("severity", "medium").lower()

        try:
            fix_type = FixType(raw_fix)
        except ValueError:
            fix_type = FixType.CONTENT_FIX
        try:
            severity = Severity(raw_sev)
        except ValueError:
            severity = Severity.MEDIUM

        insights.append({
            "insight_id": ins.get("insight_id", f"ins_{len(insights)}"),
            "fix_type": fix_type.value,
            "severity": severity.value,
            "description": ins.get("description", ""),
            "evidence": ins.get("evidence", ""),
            "source_channels": ins.get("source_channels", []),
        })

    print(f"  Classified {len(insights)} insights")
    for ins in insights:
        print(f"    {ins['fix_type']} ({ins['severity']}): {ins['description'][:60]}")
    return {"insights": insights}


def route_fixes(state: dict) -> dict:
    """Route insights to target loops using deterministic routing table."""
    insights = state.get("insights", [])
    if not insights:
        return {"fix_routes": []}

    # Deterministic routing table (from architecture spec)
    # Keys use FixType enum values (lowercase)
    ROUTING_TABLE = {
        FixType.CONTENT_FIX.value: {
            "target_loop": "C",
            "target_nodes": ["core_content", "activities"],
            "gate": "G3",
        },
        FixType.BRAND_FIX.value: {
            "target_loop": "C",
            "target_nodes": ["brand_polish"],
            "gate": "G3",
        },
        FixType.DESIGN_FIX.value: {
            "target_loop": "B",
            "target_nodes": ["generate_curriculum"],
            "gate": "G2",
        },
        FixType.CURRICULUM_FIX.value: {
            "target_loop": "A->B",
            "target_nodes": ["update_skill_graph", "generate_curriculum"],
            "gate": "G4",
        },
        FixType.PEDAGOGY_FIX.value: {
            "target_loop": "B+C",
            "target_nodes": ["resolve_pedagogy_profile", "activities"],
            "gate": "G4",
        },
    }

    default_routing = ROUTING_TABLE[FixType.CONTENT_FIX.value]

    routes = []
    for ins in insights:
        fix_type = ins.get("fix_type", FixType.CONTENT_FIX.value)
        severity = ins.get("severity", Severity.MEDIUM.value)
        routing = ROUTING_TABLE.get(fix_type, default_routing)

        # High/critical severity or structural fixes require gate approval
        auto_approved = (
            severity not in (Severity.HIGH.value, Severity.CRITICAL.value)
            and fix_type not in (FixType.CURRICULUM_FIX.value, FixType.PEDAGOGY_FIX.value)
        )

        route = {
            "route_id": f"route_{ins['insight_id']}",
            "fix_type": fix_type,
            "severity": severity,
            "target_loop": routing["target_loop"],
            "target_nodes": routing["target_nodes"],
            "gate": routing["gate"],
            "auto_approved": auto_approved,
            "description": ins.get("description", ""),
        }
        routes.append(route)

    print(f"  Routed {len(routes)} fixes:")
    for r in routes:
        auto = "auto" if r["auto_approved"] else "GATE"
        print(f"    -> {r['target_loop']} / {r['target_nodes']} ({auto})")
    return {"fix_routes": routes}


def health_monitor(state: dict) -> dict:
    """Run wiki lint and produce health report."""
    wiki = WikiEngine()

    # Wiki health
    lint_issues = wiki.lint()

    # Summarize
    insights = state.get("insights", [])
    fix_routes = state.get("fix_routes", [])

    health_report = {
        "cycle_id": state.get("cycle_id", "unknown"),
        "timestamp": datetime.now(UTC).isoformat(),
        "feedback_count": len(state.get("raw_feedback", [])),
        "insights_count": len(insights),
        "fix_routes_count": len(fix_routes),
        "wiki_lint_issues": len(lint_issues),
        "fix_type_distribution": {},
        "severity_distribution": {},
    }

    for ins in insights:
        ft = ins.get("fix_type", "unknown")
        health_report["fix_type_distribution"][ft] = (
            health_report["fix_type_distribution"].get(ft, 0) + 1
        )
        sev = ins.get("severity", "unknown")
        health_report["severity_distribution"][sev] = (
            health_report["severity_distribution"].get(sev, 0) + 1
        )

    print(
        f"  Health: {health_report['insights_count']} insights, "
        f"{health_report['fix_routes_count']} routes, "
        f"{health_report['wiki_lint_issues']} wiki issues"
    )
    return {"health_report": health_report}
