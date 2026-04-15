import json
import re

from open_acp.tools.tool_registry import registry


class RoutingClaude:
    def __init__(self, stage_outputs):
        self.stage_outputs = stage_outputs
        self.calls = []

    def generate(self, prompt: str, system: str = "", **kwargs) -> str:
        self.calls.append({"prompt": prompt, "system": system, "kwargs": kwargs})

        if "Open ACP self-review protocol" in system:
            return json.dumps(
                {
                    "summary": "Pass.",
                    "findings": [
                        {"criterion": "configured review criteria", "status": "PASS", "detail": "All checks passed."}
                    ],
                }
            )

        match = re.search(r"executing the '([^']+)' stage", system)
        if not match:
            raise AssertionError(f"Could not determine stage from system prompt: {system}")
        stage_id = match.group(1)
        return json.dumps(self.stage_outputs[stage_id])


def _long_markdown(title: str) -> str:
    return f"## {title}\n\n" + ("This section teaches the concept carefully with examples and explicit transitions. " * 12)


def _concept_outputs():
    return {
        "objectives": {
            "objectives": [
                {
                    "id": "obj_1",
                    "statement": "Explain how retrieval-augmented generation improves answer grounding with one concrete example.",
                    "bloom_level": "understand",
                    "skill_ids": ["skill_rag"],
                    "assessment_method": "short_answer",
                },
                {
                    "id": "obj_2",
                    "statement": "Compare prompt-only and retrieval-augmented approaches using at least two trade-offs.",
                    "bloom_level": "analyze",
                    "skill_ids": ["skill_rag"],
                    "assessment_method": "case_study",
                },
                {
                    "id": "obj_3",
                    "statement": "Use a guided retrieval workflow to answer a grounded question correctly.",
                    "bloom_level": "apply",
                    "skill_ids": ["skill_rag"],
                    "assessment_method": "exercise",
                },
            ]
        },
        "outline": {
            "sections": [
                {
                    "heading": "Why grounded answers matter",
                    "purpose": "Motivate the learner with the risks of hallucinated answers.",
                    "estimated_minutes": 10,
                    "bloom_level": "understand",
                    "teaching_mode": "motivation",
                    "objective_ids": ["obj_1"],
                    "subsections": ["Hallucinations", "Trust in AI outputs"],
                },
                {
                    "heading": "Bridge from prompting to retrieval",
                    "purpose": "Connect prompt-only behavior to the need for retrieved context.",
                    "estimated_minutes": 12,
                    "bloom_level": "understand",
                    "teaching_mode": "prior_knowledge_bridge",
                    "objective_ids": ["obj_1", "obj_2"],
                    "subsections": ["Prompt-only limits", "Context injection"],
                },
                {
                    "heading": "How RAG works",
                    "purpose": "Explain the main conceptual flow of a retrieval-augmented system.",
                    "estimated_minutes": 18,
                    "bloom_level": "analyze",
                    "teaching_mode": "concept_explain",
                    "objective_ids": ["obj_1", "obj_2"],
                    "subsections": ["Index", "Retrieve", "Generate"],
                },
                {
                    "heading": "Worked retrieval walkthrough",
                    "purpose": "Walk through a concrete example from question to grounded answer.",
                    "estimated_minutes": 10,
                    "bloom_level": "apply",
                    "teaching_mode": "worked_example",
                    "objective_ids": ["obj_3"],
                    "subsections": ["Question", "Retrieved chunks", "Answer"],
                },
                {
                    "heading": "Guided practice and wrap-up",
                    "purpose": "Let the learner apply the idea and summarize the lesson.",
                    "estimated_minutes": 10,
                    "bloom_level": "apply",
                    "teaching_mode": "guided_practice",
                    "objective_ids": ["obj_3"],
                    "subsections": ["Practice prompt", "Reflection"],
                },
                {
                    "heading": "Key takeaways",
                    "purpose": "Summarize the concept and transfer guidance.",
                    "estimated_minutes": 5,
                    "bloom_level": "understand",
                    "teaching_mode": "reflection_summary",
                    "objective_ids": ["obj_1", "obj_2", "obj_3"],
                    "subsections": ["When to use RAG", "What to watch out for"],
                },
            ],
            "teaching_flow": "The session moves from motivation to a prompt-vs-retrieval bridge, then to concept explanation, a worked example, guided practice, and a reflective close.",
            "prerequisite_check": "Ask learners what happens when an LLM answers without any external context.",
            "total_estimated_minutes": 65,
        },
        "core_content": {
            "sections": [
                {
                    "heading": "Why grounded answers matter",
                    "teaching_mode": "motivation",
                    "objective_ids": ["obj_1"],
                    "content_markdown": _long_markdown("Why grounded answers matter"),
                    "key_terms": ["grounding", "hallucination"],
                    "examples": [{"title": "Support bot example", "content": "A support bot invents a refund policy when no source is available."}],
                    "misconceptions": ["A confident answer is not always a grounded answer."],
                    "bridge_to_next": "Once the risk is visible, the learner is ready to compare prompt-only answers with retrieved context.",
                    "citations": ["Internal curriculum notes"],
                },
                {
                    "heading": "Bridge from prompting to retrieval",
                    "teaching_mode": "prior_knowledge_bridge",
                    "objective_ids": ["obj_1", "obj_2"],
                    "content_markdown": _long_markdown("Bridge from prompting to retrieval"),
                    "key_terms": ["prompt-only", "context window"],
                    "examples": [{"title": "Known vs unknown facts", "content": "A model can answer known facts, but struggles when the answer lives in proprietary docs."}],
                    "misconceptions": ["More prompt text alone does not equal better grounding."],
                    "bridge_to_next": "Now the learner can see why a retrieval step exists before generation.",
                    "citations": ["Internal curriculum notes"],
                },
                {
                    "heading": "How RAG works",
                    "teaching_mode": "concept_explain",
                    "objective_ids": ["obj_1", "obj_2"],
                    "content_markdown": _long_markdown("How RAG works"),
                    "key_terms": ["embedding", "retrieval", "chunk"],
                    "examples": [{"title": "Policy handbook", "content": "The system retrieves the handbook section before generating the answer."}],
                    "misconceptions": ["Retrieval is not the same as model fine-tuning."],
                    "bridge_to_next": "With the conceptual model in place, the next section shows one full walkthrough.",
                    "citations": ["Internal curriculum notes"],
                },
                {
                    "heading": "Worked retrieval walkthrough",
                    "teaching_mode": "worked_example",
                    "objective_ids": ["obj_3"],
                    "content_markdown": _long_markdown("Worked retrieval walkthrough"),
                    "key_terms": ["query", "retrieved context"],
                    "examples": [{"title": "Employee handbook question", "content": "A question retrieves the relevant leave-policy chunk before answer generation."}],
                    "misconceptions": ["The highest-similarity chunk is not always sufficient on its own."],
                    "bridge_to_next": "After seeing a full example, the learner is ready to try a guided activity.",
                    "citations": ["Internal curriculum notes"],
                },
                {
                    "heading": "Guided practice and wrap-up",
                    "teaching_mode": "guided_practice",
                    "objective_ids": ["obj_3"],
                    "content_markdown": _long_markdown("Guided practice and wrap-up"),
                    "key_terms": ["practice prompt", "grounded answer"],
                    "examples": [{"title": "Practice worksheet", "content": "Learners inspect retrieved chunks and decide whether the final answer is grounded."}],
                    "misconceptions": ["If a chunk is retrieved, the final answer is not automatically correct."],
                    "bridge_to_next": "The final section consolidates the big ideas and transfer rules.",
                    "citations": ["Internal curriculum notes"],
                },
                {
                    "heading": "Key takeaways",
                    "teaching_mode": "reflection_summary",
                    "objective_ids": ["obj_1", "obj_2", "obj_3"],
                    "content_markdown": _long_markdown("Key takeaways"),
                    "key_terms": ["transfer", "workflow"],
                    "examples": [{"title": "Decision checklist", "content": "Use retrieval when the answer depends on external, changing, or proprietary information."}],
                    "misconceptions": ["RAG is not necessary for every chatbot use case."],
                    "bridge_to_next": "This closes the session.",
                    "citations": ["Internal curriculum notes"],
                }
            ],
            "word_count": 2400,
            "reading_time_minutes": 12
        },
        "activities": {
            "activities": [
                {
                    "type": "quiz",
                    "title": "Grounded or not?",
                    "instructions": "Review three answer examples and mark which ones are grounded, then justify your choice in one sentence.",
                    "expected_output": "A short classification with one reason for each example.",
                    "time_minutes": 8,
                    "bloom_level": "understand",
                    "objective_ids": ["obj_1"],
                    "source_section": "Why grounded answers matter",
                    "teaching_mode": "motivation"
                },
                {
                    "type": "case_study",
                    "title": "Compare two workflows",
                    "instructions": "Compare a prompt-only flow and a retrieval-augmented flow for the same enterprise handbook question.",
                    "expected_output": "A short trade-off table with at least two differences.",
                    "time_minutes": 12,
                    "bloom_level": "analyze",
                    "objective_ids": ["obj_2"],
                    "source_section": "How RAG works",
                    "teaching_mode": "concept_explain"
                },
                {
                    "type": "exercise",
                    "title": "Guided retrieval practice",
                    "instructions": "Given a question and three retrieved chunks, choose the best supporting chunk and draft a grounded answer.",
                    "expected_output": "A short grounded answer with the chosen evidence chunk.",
                    "time_minutes": 15,
                    "bloom_level": "apply",
                    "objective_ids": ["obj_3"],
                    "source_section": "Guided practice and wrap-up",
                    "teaching_mode": "guided_practice"
                }
            ],
            "total_activity_time_minutes": 35
        },
        "brand_polish": {
            "polished_content": "# Retrieval-Augmented Generation\n\n" + ("Refined branded instructional prose. " * 20),
            "changes_made": [{"section": "How RAG works", "change_type": "tone", "before": "The learner should", "after": "You can"}],
            "style_compliance_score": 0.92,
            "brand_voice_notes": "Applied a clear, encouraging, semi-formal voice."
        },
        "slide_deck": {
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "Grounded Answers with RAG", "section_heading": "Session Opening", "teaching_mode": "motivation", "content_points": ["What RAG is", "Why grounding matters"], "speaker_notes": "Welcome learners. Today we will explore how retrieval-augmented generation improves answer quality by grounding outputs in trusted sources. We will first look at why hallucinations matter, then compare prompt-only answers with retrieved context, and finally walk through a practical example before guided practice.", "visual_description": "Title slide with a document icon feeding into a chatbot interface.", "layout": "title"},
                {"slide_number": 2, "slide_type": "agenda", "title": "Session Roadmap", "section_heading": "Session Opening", "teaching_mode": "motivation", "content_points": ["Motivation", "Bridge", "How RAG works", "Worked example", "Practice"], "speaker_notes": "Use this slide to set expectations. Explain the journey from motivation to practice and remind learners that they will leave with a practical mental model for when and how to use retrieval.", "visual_description": "Agenda slide with five labeled icons connected in sequence.", "layout": "content"},
                {"slide_number": 3, "slide_type": "prerequisite_check", "title": "What happens without context?", "section_heading": "Why grounded answers matter", "teaching_mode": "motivation", "content_points": ["No external source", "Possible hallucination"], "speaker_notes": "Ask learners what happens when a model answers from its internal knowledge alone. Use this to surface prior beliefs and tee up the need for grounding in real systems where answers depend on changing or private information.", "visual_description": "A chatbot answer bubble with a warning marker and no supporting document.", "layout": "content"},
                {"slide_number": 4, "slide_type": "concept", "title": "Prompt-only vs Retrieval", "section_heading": "Bridge from prompting to retrieval", "teaching_mode": "prior_knowledge_bridge", "content_points": ["Known facts", "Private docs", "Need retrieved context"], "speaker_notes": "Bridge from what learners already know about prompting to the new idea of retrieval. Explain that prompting works well for known facts, but private or changing information requires explicit context retrieval before generation.", "visual_description": "Two-column comparison of prompt-only and retrieval-augmented flows.", "layout": "two_column"},
                {"slide_number": 5, "slide_type": "concept", "title": "The RAG Flow", "section_heading": "How RAG works", "teaching_mode": "concept_explain", "content_points": ["Index", "Retrieve", "Generate"], "speaker_notes": "Explain the end-to-end flow of indexing documents, retrieving relevant chunks, and generating an answer with that context. Keep the explanation visual and emphasize how each step reduces the chance of unsupported answers.", "visual_description": "Boxes and arrows showing index, retrieve, and generate steps.", "layout": "content"},
                {"slide_number": 6, "slide_type": "example", "title": "Worked Example", "section_heading": "Worked retrieval walkthrough", "teaching_mode": "worked_example", "content_points": ["Question", "Retrieved chunks", "Grounded answer"], "speaker_notes": "Walk through one full example slowly. Narrate the question, the retrieved evidence, and how the final answer is constrained by the evidence. Point out where learners should look for grounding signals in the answer.", "visual_description": "A three-step diagram with question, evidence snippets, and final answer.", "layout": "content"},
                {"slide_number": 7, "slide_type": "activity", "title": "Guided Practice", "section_heading": "Guided practice and wrap-up", "teaching_mode": "guided_practice", "content_points": ["Choose evidence", "Draft answer", "Check grounding"], "speaker_notes": "Ask learners to inspect retrieved chunks, choose the strongest evidence, and draft a grounded answer. Give them a short timer and then debrief how they decided whether the answer stayed close to the source material.", "visual_description": "Practice slide with a worksheet-style layout and evidence cards.", "layout": "two_column"},
                {"slide_number": 8, "slide_type": "summary", "title": "Key Takeaways", "section_heading": "Key takeaways", "teaching_mode": "reflection_summary", "content_points": ["RAG adds evidence", "Use it for external knowledge", "Check grounding"], "speaker_notes": "Close by summarizing when to use retrieval, what the core workflow looks like, and how to tell whether an answer is genuinely grounded. Invite learners to transfer this mental model to future agent or chatbot systems.", "visual_description": "Summary slide with three takeaway cards and a small workflow icon.", "layout": "content"}
            ],
            "total_slides": 8,
            "estimated_duration_minutes": 65
        }
    }


def _project_outputs():
    return {
        "project_brief": {
            "project_title": "Build a Mini GenAI Assistant",
            "problem_statement": "Learners need to understand how a small GenAI application is structured and how its pieces fit together in practice.",
            "target_deliverable": "A working assistant that accepts a prompt, retrieves supporting context, and returns a grounded answer.",
            "audience": "Intermediate Python learners who are new to GenAI application design.",
            "architecture_overview": "The app accepts a question, retrieves supporting context from a small document store, and sends both the question and context to the model for answer generation.",
            "success_criteria": [
                "The starter app runs locally",
                "The retrieval step returns relevant context",
                "The final demo explains the architecture and trade-offs"
            ],
            "milestones": [
                {"id": "M1", "title": "Frame the project", "goal": "Understand the problem and final deliverable", "deliverable": "A shared understanding of what will be built", "verification": "Learners can state the app goal and user flow", "primary_mode": "project_context"},
                {"id": "M2", "title": "Design the architecture", "goal": "Map the main components and data flow", "deliverable": "A simple architecture sketch", "verification": "Learners can explain the component flow", "primary_mode": "architecture_reasoning"},
                {"id": "M3", "title": "Build the retrieval flow", "goal": "Implement the core build path", "deliverable": "A runnable retrieval-enabled app", "verification": "The app returns a grounded response", "primary_mode": "guided_build"}
            ]
        },
        "objectives": {
            "objectives": [
                {"id": "obj_1", "statement": "Explain the purpose and user flow of the assistant project in one concise walkthrough.", "bloom_level": "understand", "skill_ids": ["skill_rag"], "assessment_method": "short_answer", "milestone_id": "M1"},
                {"id": "obj_2", "statement": "Justify the main architecture components and their trade-offs for a small GenAI assistant.", "bloom_level": "analyze", "skill_ids": ["skill_rag"], "assessment_method": "discussion", "milestone_id": "M2"},
                {"id": "obj_3", "statement": "Build and verify a working retrieval-enabled assistant that returns a grounded response.", "bloom_level": "create", "skill_ids": ["skill_rag"], "assessment_method": "integration_demo", "milestone_id": "M3"}
            ]
        },
        "outline": {
            "sections": [
                {"heading": "Project framing", "purpose": "Clarify the user problem and the final deliverable.", "estimated_minutes": 10, "bloom_level": "understand", "teaching_mode": "project_context", "milestone": "M1", "deliverable": "A clear problem framing", "dependencies": [], "objective_ids": ["obj_1"]},
                {"heading": "How the assistant works", "purpose": "Explain the core GenAI concepts the project depends on.", "estimated_minutes": 12, "bloom_level": "understand", "teaching_mode": "concept_explain", "milestone": "M1", "deliverable": "A mental model of the assistant flow", "dependencies": ["Project framing"], "objective_ids": ["obj_1", "obj_2"]},
                {"heading": "Architecture reasoning", "purpose": "Explain the components and trade-offs before implementation.", "estimated_minutes": 15, "bloom_level": "analyze", "teaching_mode": "architecture_reasoning", "milestone": "M2", "deliverable": "An architecture sketch", "dependencies": ["How the assistant works"], "objective_ids": ["obj_2"]},
                {"heading": "Build the retrieval flow", "purpose": "Implement the main build path incrementally.", "estimated_minutes": 25, "bloom_level": "create", "teaching_mode": "guided_build", "milestone": "M3", "deliverable": "A runnable assistant", "dependencies": ["Architecture reasoning"], "objective_ids": ["obj_3"]},
                {"heading": "Verify and integrate", "purpose": "Test the app and show the final flow end to end.", "estimated_minutes": 15, "bloom_level": "create", "teaching_mode": "integration_demo", "milestone": "M3", "deliverable": "A verified end-to-end demo", "dependencies": ["Build the retrieval flow"], "objective_ids": ["obj_3"]},
                {"heading": "Reflect and extend", "purpose": "Summarize what was built and identify next improvements.", "estimated_minutes": 8, "bloom_level": "evaluate", "teaching_mode": "reflection_summary", "milestone": "M3", "deliverable": "A short retrospective", "dependencies": ["Verify and integrate"], "objective_ids": ["obj_1", "obj_2", "obj_3"]}
            ],
            "teaching_flow": "The session frames the problem, teaches the key idea, reasons about the architecture, builds the core flow, verifies the result, and closes with reflection.",
            "project_specification": "Build a small retrieval-enabled GenAI assistant.",
            "architecture_overview": "Prompt -> retrieval -> grounded generation -> demo.",
            "total_estimated_minutes": 85
        },
        "core_content": {
            "sections": [
                {"heading": "Project framing", "teaching_mode": "project_context", "objective_ids": ["obj_1"], "content_markdown": _long_markdown("Project framing"), "architecture_context": "This section sets the user problem and success condition for the rest of the build.", "files_created": [], "setup_commands": [], "verification_step": "Learners can restate the project goal and user flow.", "integration_points": ["This framing anchors later architecture and build decisions."], "key_terms": ["project scope", "user flow"]},
                {"heading": "How the assistant works", "teaching_mode": "concept_explain", "objective_ids": ["obj_1", "obj_2"], "content_markdown": _long_markdown("How the assistant works"), "architecture_context": "This section explains why retrieval exists before generation and how that supports grounded answers.", "files_created": [], "setup_commands": [], "verification_step": "Learners can explain why the app needs retrieved context.", "integration_points": ["The concept model informs the architecture sketch."], "key_terms": ["grounding", "retrieval"]},
                {"heading": "Architecture reasoning", "teaching_mode": "architecture_reasoning", "objective_ids": ["obj_2"], "content_markdown": _long_markdown("Architecture reasoning"), "architecture_context": "This section maps the major components and their responsibilities.", "files_created": ["architecture.md"], "setup_commands": [], "verification_step": "Learners can justify the chosen components and their order.", "integration_points": ["The architecture becomes the blueprint for implementation."], "key_terms": ["component", "trade-off"]},
                {"heading": "Build the retrieval flow", "teaching_mode": "guided_build", "objective_ids": ["obj_3"], "content_markdown": _long_markdown("Build the retrieval flow"), "architecture_context": "This section implements the core path defined by the architecture sketch.", "files_created": ["app.py", "retrieval.py"], "setup_commands": ["pip install anthropic", "python -m venv .venv"], "verification_step": "Run the app and confirm a grounded response is returned.", "integration_points": ["The built retrieval flow is reused unchanged in the final demo."], "key_terms": ["retrieval flow", "prompt assembly"]},
                {"heading": "Verify and integrate", "teaching_mode": "integration_demo", "objective_ids": ["obj_3"], "content_markdown": _long_markdown("Verify and integrate"), "architecture_context": "This section connects the implemented path to the final user-facing demo flow.", "files_created": ["demo_script.md"], "setup_commands": [], "verification_step": "Walk through one end-to-end example successfully.", "integration_points": ["This section validates the whole system working together."], "key_terms": ["integration", "demo"]},
                {"heading": "Reflect and extend", "teaching_mode": "reflection_summary", "objective_ids": ["obj_1", "obj_2", "obj_3"], "content_markdown": _long_markdown("Reflect and extend"), "architecture_context": "This section consolidates the major choices and future improvement ideas.", "files_created": [], "setup_commands": [], "verification_step": "Learners can describe one improvement they would make next.", "integration_points": ["The retrospective reinforces why the architecture and build flow were sequenced this way."], "key_terms": ["retrospective", "next steps"]}
            ],
            "word_count": 2600,
            "reading_time_minutes": 13
        },
        "activities": {
            "activities": [
                {"type": "build", "title": "Frame the user problem", "instructions": "Work in pairs to describe the user problem, the target workflow, and what the assistant should do in one end-to-end example.", "time_minutes": 10, "bloom_level": "understand", "objective_ids": ["obj_1"], "depends_on": [], "verification_checklist": ["Problem statement is clear", "One end-to-end user flow is described"], "pair_programming": "Navigator explains the user flow first, then driver captures the final version.", "stretch_goal": "Add one realistic edge case for the user journey.", "teaching_mode": "project_context"},
                {"type": "checkpoint", "title": "Architecture checkpoint", "instructions": "Review the architecture sketch and explain why each component exists before implementation begins.", "time_minutes": 12, "bloom_level": "analyze", "objective_ids": ["obj_2"], "depends_on": ["Frame the user problem"], "verification_checklist": ["Components are labeled", "Data flow is clear"], "pair_programming": "Driver walks through the sketch while navigator challenges each trade-off.", "stretch_goal": "Suggest one alternative architecture and why it was not chosen.", "teaching_mode": "architecture_reasoning"},
                {"type": "integration", "title": "Build and demo the assistant", "instructions": "Implement the retrieval flow, run the app, and demonstrate one grounded answer from end to end.", "time_minutes": 20, "bloom_level": "create", "objective_ids": ["obj_3"], "depends_on": ["Architecture checkpoint"], "verification_checklist": ["The app runs", "Retrieved context appears", "The answer is grounded"], "pair_programming": "Driver writes code while navigator verifies outputs and notes issues to fix.", "stretch_goal": "Add a second prompt pattern for a different user question.", "teaching_mode": "integration_demo"}
            ],
            "total_activity_time_minutes": 42
        },
        "brand_polish": {
            "polished_content": "# Mini GenAI Assistant Project\n\n" + ("Refined branded build-along prose. " * 20),
            "changes_made": [{"section": "Build the retrieval flow", "change_type": "format", "before": "Long paragraph", "after": "Shorter, presenter-friendly blocks"}],
            "style_compliance_score": 0.9,
            "brand_voice_notes": "Kept the project tone direct, encouraging, and operational."
        },
        "slide_deck": {
            "slides": [
                {"slide_number": 1, "slide_type": "title", "title": "Build a Mini GenAI Assistant", "milestone_id": "M1", "teaching_mode": "project_context", "content_points": ["Project goal", "What learners will build"], "speaker_notes": "Open by showing the final target and the learner promise for the session. Explain that the session will move from framing to architecture to the core build and then to an integration demo so learners can see the whole system come together.", "visual_description": "Title slide with a simple assistant UI mockup and a document retrieval icon.", "layout": "title"},
                {"slide_number": 2, "slide_type": "project_overview", "title": "What We Are Building", "milestone_id": "M1", "teaching_mode": "project_context", "content_points": ["User question", "Retrieve context", "Generate grounded answer"], "speaker_notes": "Explain the user flow in plain language and show the end-to-end outcome before any code appears. This gives learners a reason to care about each later milestone and keeps the session anchored to the final deliverable.", "visual_description": "Simple three-step user workflow with icons for question, retrieval, and answer.", "layout": "content"},
                {"slide_number": 3, "slide_type": "architecture", "title": "Architecture at a Glance", "milestone_id": "M2", "teaching_mode": "architecture_reasoning", "content_points": ["Input", "Retriever", "LLM", "Output"], "speaker_notes": "Introduce the major components and the data flow. Emphasize why retrieval exists before generation and how this layout supports grounded outputs. This slide should become the recurring checkpoint visual across the session.", "visual_description": "Boxes and arrows showing input, retrieval, prompt assembly, model, and output.", "layout": "content"},
                {"slide_number": 4, "slide_type": "milestone_goal", "title": "Milestone 1 Goal", "milestone_id": "M1", "teaching_mode": "project_context", "content_points": ["Clarify user need", "Define success"], "speaker_notes": "Use this slide to restate what learners should understand before implementation begins: the user problem, what success looks like, and what the final demo should prove.", "visual_description": "Goal card with checklist icons.", "layout": "content"},
                {"slide_number": 5, "slide_type": "architecture", "title": "Reason About the System", "milestone_id": "M2", "teaching_mode": "architecture_reasoning", "content_points": ["Why retrieval", "Why chunking", "Why grounding"], "speaker_notes": "Slow down and explain the reasoning behind the architecture choices. Highlight trade-offs and call out the exact component that will become the focus of the build milestone.", "visual_description": "Annotated architecture diagram with the retrieval component highlighted.", "layout": "content"},
                {"slide_number": 6, "slide_type": "code_demo", "title": "Build the Retrieval Flow", "milestone_id": "M3", "teaching_mode": "guided_build", "content_points": ["Setup", "Retrieve", "Assemble prompt"], "speaker_notes": "Move into the build milestone. Narrate the file structure, the sequence of commands, and what learners should verify after each step. Include troubleshooting notes for common setup issues while live coding.", "visual_description": "Two-column slide with file tree on one side and a short code snippet on the other.", "layout": "two_column"},
                {"slide_number": 7, "slide_type": "checkpoint", "title": "Checkpoint: Does It Work?", "milestone_id": "M3", "teaching_mode": "verification_checkpoint", "content_points": ["App runs", "Context appears", "Answer is grounded"], "speaker_notes": "Pause and verify the system before the final demo. Ask learners to confirm each checklist item so the build does not move forward with hidden issues.", "visual_description": "Checklist slide with status markers beside each verification step.", "layout": "content"},
                {"slide_number": 8, "slide_type": "architecture", "title": "Architecture Revisited", "milestone_id": "M3", "teaching_mode": "integration_demo", "content_points": ["Same flow", "Now implemented"], "speaker_notes": "Return to the architecture diagram and show how the abstract boxes now correspond to real code and runtime behavior. This reinforces the connection between design and implementation.", "visual_description": "The same architecture diagram as before with implemented components highlighted in a stronger color.", "layout": "content"},
                {"slide_number": 9, "slide_type": "integration", "title": "Final Demo", "milestone_id": "M3", "teaching_mode": "integration_demo", "content_points": ["Ask question", "Retrieve evidence", "Show grounded answer"], "speaker_notes": "Run the end-to-end demo and narrate each step clearly. Explain what the learner should notice in the retrieved context and how the final answer stays grounded in that evidence.", "visual_description": "Terminal or app mockup showing a user question, retrieved evidence, and final answer.", "layout": "content"},
                {"slide_number": 10, "slide_type": "retrospective", "title": "What We Built", "milestone_id": "M3", "teaching_mode": "reflection_summary", "content_points": ["Problem", "Architecture", "Build", "Next improvements"], "speaker_notes": "Close the session by summarizing the problem, the architecture, the build, and one or two next improvements learners could explore. This retrospective reinforces transfer and helps the learner see the whole session as a coherent build story.", "visual_description": "Retrospective slide with four cards for problem, architecture, build, and next steps.", "layout": "content"}
            ],
            "total_slides": 10,
            "estimated_duration_minutes": 85
        }
    }


def _make_executor(monkeypatch, tmp_path, stage_outputs):
    import open_acp.loops.loop_c.pipeline_executor as pipeline_executor_module

    fake = RoutingClaude(stage_outputs)
    monkeypatch.setattr(pipeline_executor_module, "ClaudeClient", lambda: fake)
    registry.discover()
    executor = pipeline_executor_module.PipelineExecutor(output_dir=str(tmp_path))
    return executor


def test_concept_explainer_pipeline_runs_end_to_end(monkeypatch, tmp_path):
    executor = _make_executor(monkeypatch, tmp_path, _concept_outputs())
    artifacts = executor.execute_pipeline(
        content_type="concept_explainer",
        module_context={"module_id": "m1", "title": "RAG Fundamentals", "estimated_hours": 1.0},
        domain="genai",
    )

    assert list(artifacts.keys()) == ["objectives", "outline", "core_content", "activities", "brand_polish", "slide_deck"]
    assert artifacts["outline"].validated is True
    assert (tmp_path / "concept_explainer" / "m1" / "final_document.md").exists()


def test_project_building_pipeline_runs_end_to_end(monkeypatch, tmp_path):
    executor = _make_executor(monkeypatch, tmp_path, _project_outputs())
    artifacts = executor.execute_pipeline(
        content_type="project_building",
        module_context={"module_id": "m1", "title": "Mini GenAI Assistant", "estimated_hours": 1.5},
        domain="genai",
    )

    assert list(artifacts.keys()) == [
        "project_brief",
        "objectives",
        "outline",
        "core_content",
        "activities",
        "brand_polish",
        "slide_deck",
    ]
    assert artifacts["project_brief"].validated is True
    assert (tmp_path / "project_building" / "m1" / "final_document.md").exists()
