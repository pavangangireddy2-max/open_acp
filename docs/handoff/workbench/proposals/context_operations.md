# Proposal — Context Operations: keeping the intelligence layer alive

> How the handoff docs (now ~10) stay correct, current by EOD, and consumable by every agent
> surface (Claude Code, Cowork, claude.ai threads, Echo) as new context streams arrive
> (student feedback, weekly university schedules, data extracts, corpora). Grounded in the
> "own the outer loop" framing: **you own goals and review; the loop owns ingestion, update,
> and drift-checking.** Proposal v1 — 2026-07-08.

---

## 1. The principle: four layers, never mixed

| layer | lives in | is | never |
|---|---|---|---|
| **Knowledge** | `docs/handoff/` + `knowledge/` (git) | the single source of truth, standalone docs | duplicated into agent prompts or skills |
| **Procedure** | `.claude/skills/` | HOW to update each doc: sources, sections touched, provenance/verdict discipline | a place to store facts |
| **Labor** | `.claude/agents/` | few, generic workers that read docs + follow skills | 39 job titles holding baked-in context |
| **Cadence** | scheduled automation (Cowork task / cron) | WHEN the loop runs + the EOD digest you review | something you trigger by memory |

**The tweet-pattern critique:** "8 departments, 39 agents" puts identity and knowledge in
agent files. Agent .md files are system prompts — they drift silently, can't be reviewed
like data, and every fact baked into one is a fact the other 38 don't see. Your existing
discipline (standalone docs + provenance stamps + verdict layers) is the durable half; agents
should be **few and parameterized** ("mine this corpus with the verdict discipline from doc
X"), not many and specialized. The product agent family (Canon/Crux/Forge/Lens/Radar/Panel/
Prism/Docket/Compass) is an **architecture you are building**, not the workforce that
maintains this repo — don't mirror those names into `.claude/agents/`.

## 2. What goes where (decision rules)

- A **fact** (product flag, grading contract, misconception, schedule) → a doc/manifest,
  with source + date. Nothing else.
- A **repeatable procedure** ("how to fold a new corpus in", "how to update product context")
  → a skill. Skills are thin: trigger conditions, the doc-contract table, steps, checklists.
- A **unit of work** (mine 800 questions, synthesize a week of feedback) → a subagent
  invocation, disposable, reading docs + skill.
- A **rhythm** (EOD refresh, weekly drift audit) → a scheduled automation that invokes the
  skill and ends in a human-reviewable digest + git commit.

## 3. Concrete layout

```
.claude/
  skills/
    context-bootstrap/SKILL.md     # router: "read docs/handoff/README.md first"; truth map;
                                   # forbids answering program questions from memory
    context-refresh/SKILL.md       # THE EOD PROCEDURE (see §4) — intake → route → update →
                                   # drift-check → changelog → commit → digest
    doc-contracts/SKILL.md         # per-doc ownership table: for each handoff doc — what
                                   # inputs update it, which sections, provenance format,
                                   # who consumes it (Echo, Forge, product threads)
  agents/
    intake-classifier.md           # reads the intake folder, identifies file types, routes
    corpus-miner.md                # evidence-grounded mining w/ verdict layer (the 7-analyst
                                   # pattern, generalized; used for decks, questions, feedback)
    doc-refresher.md               # applies routed updates; stamps version/date/source
    drift-auditor.md               # consistency: docs ↔ manifests ↔ registries ↔ catalog ids
knowledge/raw/intake/              # DROP ZONE: intake/YYYY-MM-DD/<files> (+ optional note.md)
docs/handoff/
  README.md                        # bootstrap (exists)
  CHANGELOG.md                     # one line per doc change: date · doc · what · source
  digests/YYYY-MM-DD.md            # EOD digest the automation writes for your review
```

Why a drop zone: deterministic ingestion beats clever discovery. You (or anyone) drops the
day's inputs — feedback exports, schedule sheets, DE extracts, new corpora — into
`knowledge/raw/intake/<today>/`; the EOD loop takes it from there. Files you hand me in chat
still work; the loop also sweeps `~/Downloads` names it recognizes, but intake/ is the contract.

## 4. The EOD loop (what runs at end of day)

1. **Sweep intake** — list new files since last digest; classify (feedback / schedule /
   extract / corpus / question re-export / unknown→flag).
2. **Route per doc-contracts** — each input type maps to target docs + procedure, e.g.:
   schedule sheet → `knowledge/catalogs/niat/schedules/` + platform/product docs;
   feedback export → feedback synthesis → delivery-quality doc + pedagogy signals;
   DE extract → learner-behaviour doc + question-doc calibration sections.
3. **Update docs** — apply changes with source+date stamps; big inputs fan out to
   corpus-miner subagents (parallel), small ones are inline edits.
4. **Drift audit** — cheap checks: manifests vs product doc tables; registry vs outline
   session ids; README index vs actual files; docs claiming "pending" for things that
   arrived; stale >7d docs with unprocessed intake.
5. **Record** — CHANGELOG lines, README "Current state" refresh, memory pointer update.
6. **Commit** — one dated commit (`context-refresh: 2026-07-08 — feedback wk28, schedule
   SGU-sec-A, +1 corpus`), never pushing without you.
7. **Digest** — `docs/handoff/digests/<date>.md`: what arrived, what changed (doc + section),
   what was flagged, what needs YOUR decision. **This digest is the outer-loop checkpoint** —
   the one thing you read daily.

HITL stays where it matters: anything that changes a *locked decision*, a manifest flag, or
a verdict-layer judgment is flagged in the digest as "needs review" instead of silently
applied. Everything mechanical (new evidence rows, catalogs, changelogs) just lands.

## 5. Onboarding the two announced streams

**Student feedback about instructors** → new stream doc `context_delivery_quality.md`
(per university × section × course: themes, instructor signals, trend vs prior weeks).
Feeds: NIAT product context (delivery reality per partner), pedagogy doc (which observed
patterns correlate with complaints), and later Crux/Compass. Weekly synthesis, EOD ingest.
PII rule: pseudonymize student identities at intake; instructor names are the subject here —
confirm policy before first ingest.

**Weekly subject-wise schedule (per section, one of 17 universities)** → canonical tabular
input at `knowledge/catalogs/niat/schedules/<univ>/<week>.csv` (catalog layer, not docs).
This is the *teaching calendar* the learner-behaviour work needs (class-to-practice lag) —
the same artifact requested from the DE, arriving from you instead. The platform doc gains a
small "delivery rhythm" section synthesized from it.

## 6. Where to run the cadence

| option | fit |
|---|---|
| **Cowork automation / scheduled task** (recommended start) | You already work here; the schedule skill can create it; runs with your session auth; digest lands in repo + optionally notifies you. |
| Claude Code cron/scheduled routine | Same effect from the CLI side; good once you're living in VS Code. |
| GitHub Action + API key | Most robust/headless, but needs API billing + repo secrets and can't reach `~/Downloads`; adopt later if the loop must survive your laptop being off. |

Start attended-ish: schedule the EOD run, but you review the digest each morning. After two
clean weeks, you'll know exactly which steps deserve full autonomy.

## 7. Rollout

- **Week 1 (minimal, high value):** create the 3 skills + intake folder + CHANGELOG; run
  "context-refresh" manually at EOD by invoking the skill. Proves the procedure.
- **Week 2:** schedule it (Cowork automation); add drift-auditor as a subagent the skill
  calls; digests accumulate.
- **As volume grows:** add corpus-miner fan-out for big drops (new stacks per the intake
  spec) and a weekly deeper audit (Echo corpus refresh rides the same loop — Echo answers
  from these docs, so EOD freshness = Echo freshness).

## 8. What this does NOT change

Docs remain standalone and git-versioned; claude.ai product threads (Forge/Canon/…) still
consume them by paste/upload; my session memory stays a pointer index, never the truth;
the locked non-negotiables in README §"Non-negotiables" require your explicit sign-off to
change — the automation may propose, never decide.
