# Python Node Registry — Module 1 Exemplar (for your review)

> **The WHAT rail, source-grounded.** First module of the Python course node registry, now
> authored **directly from the authoritative Course Outline** (Key Takeaways + Outline
> columns), not inferred. It's an exemplar for you to edit — agree the schema, granularity,
> and depth conventions before I do Modules 2–17. Give me **promote / fold / flatten /
> split** verbs per node and I'll apply them, then continue.
>
> Source: `knowledge/raw/corpora/python_course_outline.csv` (32 sessions / 17 modules,
> exported from the catalogue's Course Contents sheet). Companion: `module_01_introduction.csv`.
> Focus is **coding** nodes per your instruction. Authored 2026-07-08.

## Schema (how to read a row)

| Column | Meaning |
|---|---|
| `Node_ID` | Stable id `py_m<module>_<slug>` — the coordinate Forge generates against. |
| `Node` / `Module` / `Session` | The takeaway and where it's taught. |
| `Prereq` | In-course node needed first (the walk-down target on failure). |
| `L1–L5` | Mastery ladder — behavioural descriptors, ragged (stops at real depth). |
| `Depends_On` / `Dependency_Reason` | Graph edge + why. |
| `Node_Reason` | Editorial verdict — cites the Key Takeaway it came from. **Your decisions live here.** |
| `Evidence_Flag` | `coding` / `objective` / `coding+objective`. |
| `Confidence` | Now **`sourced`** (from the real outline), not `inferred`. |

## What changed from the first (inferred) draft — this is the point

Grounding against the real outline **materially changed Module 1**. The inferred draft had 9
nodes including `comments`, `naming rules`, `type()`, and `precedence`. The **actual**
Session 1 + Session 4 Key Takeaways contain none of those — they belong to later sessions:

| Inferred node | Reality |
|---|---|
| `comments` | **Not in Module 1** at all. Removed. |
| `naming rules & conventions` | **Not a Module-1 takeaway.** Removed. |
| `type()` inspection | Session **8** (Type Conversions), not here. Removed. |
| `operator precedence` | Session **5** (BODMAS), not here. Removed. |
| `programming_literacy` (software/code/syntax) | **Added** — it's Session-1's first Key Takeaway, which I'd missed. |

Net: **9 inferred nodes → 5 sourced nodes.** That correction is exactly why we ground against
the outline before authoring 17 modules.

## The 5 sourced nodes

| Node | Session | Depth | From Key Takeaway | Evidence |
|---|---|---|---|---|
| `py_m1_programming_literacy` | s1 | L1–L3 | "Introduction to Programming" | objective |
| `py_m1_print` | s1 | L1–L3 | "Displaying a Message / Hello World!" | coding+objective |
| `py_m1_arithmetic` | s1 | L1–L3 | "Calculations with Python / Arithmetic Operators" | coding+objective |
| `py_m1_variables` | s4 | L1–L3 | "Variables / Assigning Value" | coding+objective |
| `py_m1_datatypes` | s4 | L1–L3 | "Data types: Integer/Float/String/Boolean" | coding+objective |

Sessions **2** (Coding Practice Walkthrough) and **3** (Leveraging Gen AI) carry **no Key
Takeaways** — they're walkthrough/meta, not node-bearing. Confirmed against the source.

## Decisions I need from you

1. **Depth ceiling.** Every Module-1 node tops out at **L3**, because the outline's deeper
   behaviours (type conversion, precedence, reassignment-state) are taught in *later*
   sessions. **Question:** should a node's L4–L5 live in the module where the concept is
   *introduced* (so `arithmetic` gets L4–L5 rungs referencing later `//`/`%`), or should each
   session only own the rungs it actually teaches (my current choice — cleaner, but a node's
   full ladder is then split across modules)? This is the biggest convention decision.
2. **`programming_literacy`** is objective-only (no code to run). Keep as a real node, or treat
   it as non-assessable course-framing and drop from the registry?
3. **Granularity** otherwise looks 1:1 with Key Takeaways. OK as the rule (one node per
   takeaway bullet-group), or do you want finer/coarser?

## Coverage cross-check (the problem you flagged, confirmed)

Against `computer_programming_question_details.json` (340 CODING items, difficulty thin:
158 EASY / 3 MEDIUM / 179 untagged):

- Module 1's only real coding evidence is **arithmetic** (product/division items). `print`,
  `variables`, `datatypes` are coding-flagged but the bank has ~zero coding items for them.
- So Module 1's coding bank must be **built, not floored** — matches your "coverage would be a
  problem" note. And the all-EASY arithmetic drills are a plausible source of the "boring"
  feedback (no variety, no step-up).

## Next step

Mark up decisions 1–3. I apply them, lock the conventions (especially the L4–L5 placement
rule), then author Modules 2–17 straight from the same outline. The reading-material content
(in both the outline sheet and the question JSON) is available if you want node descriptors to
quote the exact taught wording.
