"""BackpropRouter — deterministic routing table for fix tickets.

Routing table:
┌─────────────────┬────────────┬──────────────────────────────────────────┬──────┬──────┐
│ FixType         │ Severity   │ Target Loop / Nodes                      │ Gate │ Auto │
├─────────────────┼────────────┼──────────────────────────────────────────┼──────┼──────┤
│ CONTENT_FIX     │ < HIGH     │ C / core_content, activities             │ G3   │ Yes  │
│ CONTENT_FIX     │ HIGH/CRIT  │ C / core_content                         │ G3   │ No   │
│ BRAND_FIX       │ any        │ C / brand_polish                         │ G3   │ Yes  │
│ DESIGN_FIX      │ < HIGH     │ B / compose_product_specific_curriculum  │ G2   │ Yes  │
│ DESIGN_FIX      │ HIGH/CRIT  │ B / compose_product_specific_curriculum  │ G2   │ No   │
│ CURRICULUM_FIX  │ any        │ A→B / update_skill_graph, produce_stack_ │ G4   │ No   │
│                 │            │   curriculum_abstract → compose_product  │      │      │
│ PEDAGOGY_FIX    │ any        │ B+C / resolve_pedagogy_profile, acts     │ G4   │ No   │
│ CL_TAG_FIX      │ any        │ A / produce_stack_curriculum_abstract    │ G4   │ No   │
└─────────────────┴────────────┴──────────────────────────────────────────┴──────┴──────┘
"""


class BackpropRouter:
    """Deterministic router — no LLM calls."""

    HIGH_SEVERITY = {"HIGH", "CRITICAL"}

    def route(self, fix_type: str, severity: str) -> dict:
        """Return routing information for a fix type + severity."""
        if fix_type == "CONTENT_FIX":
            high = severity in self.HIGH_SEVERITY
            return {
                "target_loop": "C",
                "target_nodes": ["core_content"] if high else ["core_content", "activities"],
                "target_abstracts": [],
                "gate": "G3",
                "auto_approved": not high,
            }
        elif fix_type == "BRAND_FIX":
            return {
                "target_loop": "C",
                "target_nodes": ["brand_polish"],
                "target_abstracts": [],
                "gate": "G3",
                "auto_approved": True,
            }
        elif fix_type == "DESIGN_FIX":
            high = severity in self.HIGH_SEVERITY
            return {
                "target_loop": "B",
                "target_nodes": ["compose_product_specific_curriculum_container"],
                "target_abstracts": [],
                "gate": "G2",
                "auto_approved": not high,
            }
        elif fix_type == "CURRICULUM_FIX":
            return {
                "target_loop": "A→B",
                "target_nodes": [
                    "update_skill_graph",
                    "produce_stack_curriculum_abstract",
                    "compose_product_specific_curriculum_container",
                ],
                "target_abstracts": ["stack_curriculum_abstract", "stack_skill_graph"],
                "gate": "G4",
                "auto_approved": False,
            }
        elif fix_type == "PEDAGOGY_FIX":
            return {
                "target_loop": "B+C",
                "target_nodes": ["resolve_pedagogy_profile", "activities"],
                "target_abstracts": [],
                "gate": "G4",
                "auto_approved": False,
            }
        elif fix_type == "CL_TAG_FIX":
            return {
                "target_loop": "A",
                "target_nodes": ["produce_stack_curriculum_abstract"],
                "target_abstracts": ["stack_curriculum_abstract"],
                "gate": "G4",
                "auto_approved": False,
            }
        else:
            return {
                "target_loop": "C",
                "target_nodes": ["core_content"],
                "target_abstracts": [],
                "gate": "G3",
                "auto_approved": False,
            }
