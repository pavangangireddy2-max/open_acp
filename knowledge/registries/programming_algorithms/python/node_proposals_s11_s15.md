# Node Proposals — Pilot Sessions (s11–s15) from Co-Failure Communities

> **The result of the filter→cluster method** (review addendum-2 spec) applied to the DE's
> raw pilot extract, interpreted at content level against the misconception bank and the
> course outline. Method: robust pairs only (N≥150 within-session / ≥300 cross, phi≥0.2,
> both-fail cell≥10) → average-linkage clustering on (1−phi) → communities ≥3 items → each
> community named by reading its actual questions. Confidence labels: **B+C** = behaviour
> community AND content family agree (strongest), **C** = content/bank only, **H** =
> hypothesis. For HOD review with the registry verbs (promote / fold / flatten / split).
> 2026-07-10.

## s11 — Conditional Statements → propose 4 nodes

| node | evidence | confidence |
|---|---|---|
| **N1 Indentation & block structure** (parse-time rules: expected block, unexpected indent, legal 1-space, if-False-still-parses) | C1+C17 (14 items; C1 = 11 items, 28 robust pairs, median phi 0.26) + legal-indent items in mixed C14/C16; bank C-01/02/03/04; outline "Indentation" | **B+C** |
| **N2 If/else execution scope** (what runs when; trailing unindented statements; else pairing) | C3+C7+C9+C15 (17 items) — `if a>b: print(a-b)` then unindented `print(a+b)`; 9 robust pairs run ACROSS these 4 communities (one family, fragmented by clustering); bank C-05/C-06 | **B+C** |
| **N3 Conditions as booleans** (comparison → bool driving the branch; stored booleans `is_day = (t>=8) and (t<=15)`) | C8+C11+C12 (+ stored-boolean items in mixed C2) — bank C-11/C-14/C-17; outline "Conditions" | **B+C** |
| **N4 Sequential ifs vs ladder** (independent ifs all fire; else binds to nearest if) | C4+C5+C13 (12 items; C5 = the 4 grade-ladder TEXTUALs, highest-fail cluster, 39–52%, phi 0.32) + ladder items inside mixed C2/C6; bank C-07 | **B+C** |

Mixed-community adjudication (step-4 record, item level): **C2** splits 6→N3 (stored
booleans `is_day`/`is_night`, ==/!= eval) + 3→N4 (`marks` sequential-if ladders 0a1d0356,
102d40c4, 48706095 — same demand as C5's TEXTUALs, easier rung). **C6** splits three ways:
1b9dd04a, ddbd17a4→N3 · 3bd498ec→N4 · 689112ed→N2 (case-sensitive compare + trailing
print; two-demand item — the kind born-tagging avoids). **C10**: 781ca854→N2; the two
FIB write-the-if-header items stay seam N3(condition construction)/N1(syntax) — registry
author's call. **C14**: 27961bab, e5036f1d→N3; 458400aa→N1 (legal 3-space indent, C-03).
**C16**: all → N3 (trailing-space `else:` is cosmetic; demand is eval). Merge arithmetic
(why same-skill communities stayed apart at t=0.92): C3×C7 avg cross-distance 0.936,
C9×C15 0.940, C1×C17 0.935, C4×C5 0.990 — non-robust cross-pairs (distance 1.0) dilute
the average above the cut; fragmentation is the deliberate price of the strict pair filter,
repaired by content reading. Single-pair noise exhibit: near-clones 0baf266e×8877aa15
phi 0.006 — never trust one pair, trust clumps + content.

Derivation audit (2026-07-10, all 17 communities content-read): funnel = 174 items /
142,617 attempts → 15,051 pairs → 351 robust (105 items) → 17 communities (75 items) →
4 themes. Separation test: within-theme median phi 0.149 (34% of pairs robust) vs
between-theme 0.085 (5%); closest theme pair N2×N4 at 0.105 — the fold candidate if a
3-node registry is preferred. 5 mixed/seam communities (C2, C6, C10 FIB if-header
writing, C14, C16) + the 69-item no-robust-pair tail are assigned by content during
registry authoring, not by behaviour.

Exemplar (N1, real items that co-fail): `21b57840` `if not(True):` + over-indented second
print vs `72e4a338` unindented `else` body vs `f511e3fa` `if False:` + bad indent (still a
parse error — C-03). Different bugs, one skill: *indentation defines structure before
anything runs.* The learners who miss one miss the others.

## s12 — Nested Conditional Statements → propose 3 nodes

| node | evidence | confidence |
|---|---|---|
| **N1 Boolean-gated nesting** (stored expression gates outer block; inner never checked when outer False) | C1 — 5 TEXTUALs, the session's hardest cluster (52–69% fail): `x=(True and False)… if x: … if y: … print("END")`; bank C-15/C-16 | **B+C** |
| **N2 Nested gating with comparisons/types** (expression building inside nests, accumulation across levels) | C3–C7 small communities (`expression1=(36<16)`, type() equality gates) | B+C (thin) |
| **N3 elif ladder semantics** (first-true-wins; elif-after-else illegal) | outline + bank C-08/C-09; no distinct robust community (items thin in pilot) | **C** |

## s13 — Loops (while) → propose 3 nodes  *(the session the 6-item candidate pointed at)*

| node | evidence | confidence |
|---|---|---|
| **N1 While trace & accumulation** (counter/accumulator simulation, both-ends-moving, factorial-style) | C3 (`count=(count+a)` countdown; both-ends LP-10; `fact*number`; the 42.7%-fail string-index trace `39ec96a0`) + C2/C6/C11 | **B+C** |
| **N2 Loop state & termination semantics** (missing update → infinite; captured condition never re-evaluated; entry-false never runs; runs-once) | C8 — `21ddb473` (no update), `4c85f075` (condition-capture, entry-false), `7f1940ee`; bank LP-02/03/04/05/06. **This is the seam the under-powered 6-item candidate pointed at — now backed by a robust community of well-failed items.** The leak-starved LP-06/LP-04 items (`dd4165ba`,`e4a74737`,`a0081625`,`7fe10957`) belong here by content | **B+C** |
| **N3 Boundary & filtered accumulation** (`<` vs `<=`, `%` filters inside loops, zero-iteration edges) | C5/C10 — `while i <= a` + `%2` squares pair (`8ce95b05`/`f7b59138`, near-identical templates — also a clone-family warning), `324bc659` (a=−1 → 0 iterations); bank LP-15 | **B+C** |

## s15 — For Loop → propose 2 nodes (session is ONE dominant skill + a satellite)

| node | evidence | confidence |
|---|---|---|
| **N1 range()/for trace & accumulation** — the session's core | C1 — **19 items, 80 robust pairs** (largest, most cohesive community in the pilot): `range(start,stop)` bounds (LP-01), `range(1,1)` zero iterations (`d6eed841`), factorial-times-zero (`fcf28486`/`e878f4c6`, LP-13), `%`-filtered sums (`af480cdd`), string-index scans (`2085e437`) | **B+C** |
| **N2 Iterating string slices** (`for ch in s[4:]` accumulation) | C2 — `0217e37b`/`b371b85c` (same template, different words — clone-family flag); bank LP-12 + slicing prereq | B+C (thin) |

Note: the writeup's lift-median method said For Loop had "no split." The phi-graph shows why:
it isn't two halves — it's one big node plus fringes. That is itself a registry decision:
**s15 ≈ one node**, don't force a split.

## s14 — Understanding Coding Question Formats → 2 meta-nodes (objective-only evidence flags)

| node | evidence | confidence |
|---|---|---|
| **N1 Problem-statement translation** (story → technical form) | C1 — `f01c350e`,`f43465d6` (story→technical MCQs) | **B+C** |
| **N2 Plan-level sequencing** (order the pseudo-code steps) | C2 — REARRANGE items (`5b83c111` Liam count-occurrences, `d49f74d6`) | **B+C** |

These are problem-literacy meta-skills, not Python concepts — registry should carry them
with `evidence: objective_only, meta` flags (they scaffold every coding session's stems).

## Cross-session — Depends_On candidates (not merges)

Robust cross-session edges (phi≥0.2, cell≥10, ability-tercile-stable) concentrate between
the *accumulation-trace* nodes: `4acf7edc`(s13 N1) ↔ `af480cdd`(s15 N1) phi .268;
`8ce95b05`(s13 N3) ↔ `d6eed841`(s15 N1) .258; For-Loop core ↔ Nested `6445782f` .280.
Reading: **one latent "accumulator tracing" skill spans while/for** — registry options:
(a) `Depends_On: s15.N1 → s13.N1` (for builds on while), or (b) a shared cross-session
node. Recommend (a) — matches teaching order. The Conditional↔Loops edges (e.g.
`3dc85a33`↔`7fe10957` phi .306) suggest `s13.N2 Depends_On s11.N3` (termination reasoning
builds on condition evaluation).

## Caveats & review verbs

- Communities are pilot-scale; clone families inflate two pockets (flagged above) — the
  content-hash rerun will clean these. Small communities (3 items, 2 pairs) are seeds, not
  proof.
- **HOD review:** promote each B+C node as drafted · fold N-candidates where you judge one
  skill (e.g. s11 N4 into N2 if preferred) · s12 N3 stays content-only until full scale.
- Next: extend module-01-style registry rows for s11–s15 with these nodes; map the ~60
  bank misconceptions for these sessions onto them (LP/C/NL families already named per node).

**Provenance:** raw `pilot_extract.csv` (542,021 attempts) → independent pair recompute
(matches DE to 1e-15) → robust filter → scipy average-linkage on (1−phi) → content
interpretation from `knowledge/raw/corpora/programming_algorithms/python/question_details.json`
+ misconception bank (question_intelligence.md §3.3). Full method: review_cofailure_pilot.md
addendum 2.
