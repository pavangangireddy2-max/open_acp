# Intake Spec — Per-Stack Question Intelligence

> **Purpose:** define exactly what data to supply for each stack so a fresh agent can mine it
> into a `context_question_intelligence_<stack>.md` doc at the same depth as the Python pilot
> ([context_question_intelligence_python.md](context_question_intelligence_python.md)). Read
> that doc to see the target output; read this one to gather the inputs.
>
> **Decision locked (2026-07-07):** user supplies the full input bundle for *all* stacks
> first; then batch-mine (parallel analysts per stack); **one doc per stack**, mirroring the
> Python doc's structure.
>
> Last updated: 2026-07-07.

---

## 1. What produced the Python doc (the bar to clear)

The Python doc was **not** written from description — it was mined by executing the corpus.
For each stack to reach the same trustworthiness, its bundle must let an analyst reproduce
that method:

- **Run reference solutions** against their own suites (caught a solution failing its own tests).
- **Execute predict-output snippets** to verify answer keys (~1,700 executed for Python).
- **Probe FIB blanks** by substituting alternate tokens and re-executing (the ambiguity audit).
- **Ground every claim in `question_id`s** (8-char UUID prefixes, collision-checked).

If the bundle can't support execution + join, the resulting doc drops from "mined intelligence"
to "described guesses" — which is exactly what the rebuild is escaping.

---

## 2. The per-stack input bundle (required)

For **each** stack, supply these four items. Items 1–3 are mandatory; 4 is a bonus overlay.

| # | Input | Format | Python equivalent | Why it's needed |
|---|---|---|---|---|
| 1 | **Full question corpus** — every question in the course, *including coding-question content* (reference solution, test cases w/ visible/hidden + weights, options, answer keys, explanations/tutorials if they exist) | JSON | `question_details_json_with_coding_question_content.json` | The mine: misconceptions, item anatomy, defects, format contracts |
| 2 | **Session–Unit linking table** — maps every `unit_id` to its `session_id`(s) and module | CSV | the session-unit CSV | The join spine; the *only* reliable way to attach questions to structure |
| 3 | **Course Outline** — sessions, modules, key takeaways, outcome statements; reading-material content + transcript links if available | CSV | `Computer Programming using Python Course Contents - Course Outline.csv` | Structure context + doubles as the WHAT-rail node source |
| 4 | **Curated brand decks** *(optional)* | PDF / Google Slides export | `sample_*` + session decks | Pedagogy overlay; several stacks already have these in `knowledge/raw/brand/` |

### What "corpus" must contain (field-level)

The Python export carried, per question type:
- **CODING:** `codes[]` (reference solution, language tag), `test_cases[]` with
  `{input, output, is_hidden, weightage}`. *If coding content lives in a separate export, include it* — the base `question_details` JSON alone was insufficient; the `_with_coding_question_content` variant was the one that mattered.
- **FIB_CODING:** stem, blank positions, stored answers.
- **CODE_ANALYSIS (predict-output):** snippet, answer key, error-class if applicable.
- **MC / MTO / REARR / TEXTUAL:** stem, options with `option_id`, answer key(s), and — if the
  platform stores them — misconception tags on distractors.
- Any **explanations / tutorials** attached to items (the Python re-export is adding these; if
  your stack export already has them, include them).

---

## 3. The non-negotiable join rules (carry over from Python — do not relitigate)

These are locked project-wide and apply to every stack's intake:

1. **Join by `session_id` / `unit_id` / `question_id` + content hash — never `course_id`.**
   Course ids have changed; they are not a stable key.
2. **`unit_id`s are reused across sessions** (proven: one Classroom-Quiz unit appeared under two
   different session titles). Always carry the **`(session_id, unit_id)` pair**, never `unit_id`
   alone.
3. **Identical question content exists under different `question_id`s** (clone families). Add a
   **content hash (stem + code + options)** so behaviour and stats aggregate across re-issued
   clones.
4. **Include exposure / served-denominator counts** for any per-item rate. The player samples
   ~15 of ~30 items per unit, so any "X% got this wrong" without a served denominator is biased.
   *(Relevant once learner-behaviour data is joined; note it now so the export carries it.)*
5. **Answer keys are not assumed correct** — they're verified by execution. The export must be
   runnable, not just readable.

---

## 4. Stack list — resolve these before mining

The manifest folder lists 15 stack files; some look redundant or are domain-level. **Confirm
which are live courses that need their own question-intelligence doc**, and give the canonical
name + its NxtWave course title(s):

| manifest stack | likely course(s) (from Central Stack Catalogue) | status — you confirm |
|---|---|---|
| `python` | Computer Programming using Python | ✅ done (pilot) |
| `reactjs` | Frontend Development Using React | 🟡 corpus exists (`react_question_details_json.json`) — **next easiest** |
| `cpp` / `dsa` / `ds_algo` | DSA using C++ / Advanced DSA / Problem Solving | ❓ **which of these three is the real one?** looks redundant |
| `fullstack` | Web App Dev / Backend (Node, Mongo) / Django / SpringBoot | ❓ one stack or several courses? |
| `genai` | (GenAI course) | ❓ |
| `cs_core` | Database Management Systems / Intro to Software Dev / Math for CSE | ❓ maps to multiple NIAT sem-1/2 courses |
| `aptitude` | (Aptitude) | ❓ has a question corpus? |
| `english` | (English/communication) | ❓ question-based? |
| `devops_testing` | (DevOps / Testing) | ❓ |
| `ds_ml` | (Data Science / ML) | ❓ |
| `system_design` | (System Design) | ❓ |
| `physical_ai` | (Physical AI) | ❓ |
| `programming` | (domain-level, groups python+cpp) | likely NOT its own doc |

> **Cross-check:** the NIAT B3 sem-1/2 course list you gave earlier — Python, DSA (C++), Web App
> Dev, React, Backend (Node/Mongo), DBMS, Intro to Software Dev, Math for CSE — is the priority
> subset. Several of these map to `cs_core` and `fullstack`, not a 1:1 stack file.

---

## 5. Delivery mechanics

- **Drop location:** put each stack's bundle in `~/Downloads/` (where the Python + React
  corpora already are) or tell me a folder. Name files so the stack is unambiguous
  (e.g. `react_session_unit_map.csv`, not `Sheet1.csv`).
- **Per-stack readiness = items 1+2+3 present.** As soon as a stack's three mandatory files are
  in place, it's mineable — you don't have to wait for all stacks if you'd rather I start the
  ready ones. (Current plan is to wait for the full set; this is the escape hatch.)
- **Output:** one `context_question_intelligence_<stack>.md` per stack + an index row added to
  [README.md](README.md). Batch mining uses parallel analysts (one per stack/chunk), same as
  the Python + deck-recovery runs.

---

## 6. Checklist you can copy per stack

```
Stack: __________  (canonical name + NxtWave course title)
[ ] 1. Question corpus JSON (WITH coding-question content: solutions, test cases, weights)
[ ] 2. Session–Unit linking CSV (unit_id → session_id + module)
[ ] 3. Course Outline CSV (sessions, modules, takeaways, outcomes; reading/transcripts if any)
[ ] 4. Brand decks (optional; check knowledge/raw/brand/ first — may already exist)
[ ] Confirmed: does the export carry explanations/tutorials? Y/N
[ ] Confirmed: does the export carry per-distractor misconception tags? Y/N
[ ] Confirmed: served/exposure counts available? Y/N (can follow later w/ learner data)
```
