"""Loop B nodes — curriculum design using wiki intelligence.

Nodes:
1. load_wiki_context — read skill graph + learner model from wiki
2. select_pedagogy — choose pedagogy framework (Bloom's/ADDIE/Merrill's/4C-ID)
3. generate_curriculum — backward design curriculum map
4. generate_differentiation — competitor coverage analysis
5. align_assessments — map objectives to assessment methods
"""
import json
from open_acp.knowledge.wiki_engine import WikiEngine
from open_acp.utils.claude import ClaudeClient


def load_wiki_context(state: dict) -> dict:
    """Load skill graph and learner model from wiki entities."""
    wiki = WikiEngine()
    domain = state.get("domain", "ml-engineering")

    # Gather skill entities
    skills = wiki.list_entities(entity_type="skill")
    skill_context = "## Skills in Wiki\n"
    for s in skills:
        entity = wiki.get_entity("skill", s["entity_id"])
        if entity:
            skill_context += f"- **{s['title']}** (confidence={s['confidence']:.2f}, durability={s.get('durability', '?')})\n"

    # Gather learner entities
    learners = wiki.list_entities(entity_type="audience_segment")
    learner_context = "## Learner Segments\n"
    for l in learners:
        entity = wiki.get_entity("audience_segment", l["entity_id"])
        if entity:
            learner_context += f"- **{l['title']}**: {entity['content'][:300]}\n"

    # Gather competitor entities
    competitors = wiki.list_entities(entity_type="competitor")
    competitor_context = "## Competitors\n"
    for c in competitors:
        entity = wiki.get_entity("competitor", c["entity_id"])
        if entity:
            competitor_context += f"- **{c['title']}**: {entity['content'][:300]}\n"

    print(f"  Wiki context loaded: {len(skills)} skills, {len(learners)} learner segments, {len(competitors)} competitors")
    return {
        "skill_graph_context": skill_context + "\n" + competitor_context,
        "learner_context": learner_context,
    }


def select_pedagogy(state: dict) -> dict:
    """Select and justify a pedagogy framework."""
    domain = state.get("domain", "ml-engineering")
    skill_context = state.get("skill_graph_context", "")
    learner_context = state.get("learner_context", "")

    claude = ClaudeClient()
    prompt = f"""For a {domain} curriculum, select the most appropriate pedagogy framework.

Options:
1. **Bloom's Taxonomy Mastery** — progressive cognitive levels (remember -> create)
2. **ADDIE** — structured phases (Analyze, Design, Develop, Implement, Evaluate)
3. **Merrill's First Principles** — real-world task-centered instruction
4. **4C/ID** — complex skill integration with whole-task practice

{skill_context}

{learner_context}

Select ONE framework and justify why it's the best fit for this domain and these learners.

Return JSON:
{{
  "framework": "blooms_taxonomy_mastery",
  "justification": "2-3 sentence justification for why this framework fits",
  "key_principles": ["principle 1", "principle 2", "principle 3"]
}}

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are an instructional design expert selecting pedagogy frameworks.",
        model_tier="strong",
        max_tokens=2048,
    )

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n") + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
        framework = data.get("framework", "blooms_taxonomy_mastery")
        justification = data.get("justification", "Default selection")
    except (json.JSONDecodeError, ValueError):
        framework = "blooms_taxonomy_mastery"
        justification = "Default: Bloom's provides clear cognitive progression"

    print(f"  Pedagogy: {framework}")
    return {"selected_pedagogy": framework, "pedagogy_justification": justification}


def generate_curriculum(state: dict) -> dict:
    """Generate a curriculum map using backward design."""
    domain = state.get("domain", "ml-engineering")
    pedagogy = state.get("selected_pedagogy", "blooms_taxonomy_mastery")
    skill_context = state.get("skill_graph_context", "")
    learner_context = state.get("learner_context", "")
    content_type = state.get("content_type", "concept_explainer")

    claude = ClaudeClient()
    prompt = f"""Design a curriculum for "{domain}" using {pedagogy} framework.

{skill_context}

{learner_context}

Use backward design:
1. Start with terminal outcomes (what can learners DO after?)
2. Map prerequisites per outcome
3. Sequence modules respecting prerequisite chains
4. Estimate duration per module

Return JSON:
{{
  "curriculum_id": "cur_{domain}",
  "program_name": "ML Engineering Fundamentals",
  "domain": "{domain}",
  "pedagogy_framework": "{pedagogy}",
  "modules": [
    {{
      "module_id": "m1",
      "title": "Module Title",
      "sequence": 1,
      "objectives": [
        {{"id": "obj_1", "statement": "...", "bloom_level": "understand", "skill_ids": ["skill_id"]}}
      ],
      "estimated_hours": 1.5,
      "prerequisite_modules": [],
      "content_types": ["{content_type}"]
    }}
  ],
  "total_hours": 20.0
}}

Design 4-6 modules. Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are a curriculum architect using backward design.",
        model_tier="strong",
        max_tokens=8192,
    )

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n") + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        data = {"curriculum_id": f"cur_{domain}", "modules": [], "total_hours": 0}

    modules = data.get("modules", [])
    print(f"  Curriculum: {len(modules)} modules, {data.get('total_hours', 0)} hours")
    return {"curriculum_map": data}


def generate_differentiation(state: dict) -> dict:
    """Generate differentiation matrix (our approach vs competitors)."""
    domain = state.get("domain", "ml-engineering")
    curriculum = state.get("curriculum_map", {})
    skill_context = state.get("skill_graph_context", "")

    claude = ClaudeClient()
    modules_summary = json.dumps(
        [
            {
                "title": m.get("title", "?"),
                "skills": [o.get("skill_ids", []) for o in m.get("objectives", [])],
            }
            for m in curriculum.get("modules", [])
        ],
        indent=2,
    )

    prompt = f"""Analyze how our curriculum differentiates from competitors.

## Our Curriculum Modules
{modules_summary}

{skill_context}

For each key skill area, indicate: our coverage level, competitor coverage, and our unique advantage.

Return JSON:
{{
  "differentiators": [
    {{
      "skill_area": "MLOps",
      "our_coverage": "deep",
      "competitor_coverage": "shallow",
      "our_advantage": "Hands-on pipeline building with real tools"
    }}
  ],
  "summary": "One paragraph positioning statement"
}}

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are a competitive analyst.",
        model_tier="cheap",
        max_tokens=4096,
    )

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n") + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        data = {"differentiators": [], "summary": "N/A"}

    print(f"  Differentiation: {len(data.get('differentiators', []))} areas analyzed")
    return {"differentiation_matrix": data}


def align_assessments(state: dict) -> dict:
    """Align assessments to objectives across the curriculum."""
    curriculum = state.get("curriculum_map", {})

    claude = ClaudeClient()
    prompt = f"""For this curriculum, align assessment methods to each learning objective.

## Curriculum
{json.dumps(curriculum, indent=2)[:6000]}

For each objective across all modules, specify the assessment type and method.

Return JSON:
{{
  "alignments": [
    {{
      "module_id": "m1",
      "objective_id": "obj_1",
      "assessment_type": "mcq",
      "bloom_level": "understand",
      "when": "module_quiz"
    }}
  ],
  "assessment_schedule": {{
    "classroom_quizzes": "Every 15-20 min during sessions",
    "module_quizzes": "After every 4 sessions",
    "fortnight_quizzes": "Biweekly skill checks",
    "final_quiz": "End of course comprehensive",
    "final_project": "Capstone project"
  }}
}}

Return ONLY the JSON object."""

    response = claude.generate(
        prompt=prompt,
        system="You are an assessment alignment specialist.",
        model_tier="cheap",
        max_tokens=4096,
    )

    try:
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned[cleaned.index("\n") + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        data = json.loads(cleaned.strip())
    except (json.JSONDecodeError, ValueError):
        data = {"alignments": [], "assessment_schedule": {}}

    print(f"  Assessment alignment: {len(data.get('alignments', []))} objective-assessment pairs")
    return {"assessment_alignment": data}
