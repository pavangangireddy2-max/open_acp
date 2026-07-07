# Coding Question Creation Intelligence — Python Course

> **Standalone handoff document (the HOW rail).** The v0 instruction set for Forge — the
> agent that generates fresh practice-question banks for NxtWave's **Computer Programming
> using Python** course (Programming & Algorithms stack; absolute beginners, first language;
> course outcome: "zero to writing correct, working Python programs … with fluency in
> Python's specific error patterns").
>
> **What this doc is NOT:** the node registry (the WHAT rail). Nodes, depths, and the
> dependency graph are authored separately from course content; this doc tells the
> generator HOW to write items well once a work-order cell (node × level × axis) exists.
>
> **Interpretation rule (verdict layer):** unlike the pedagogy doc's curated brand decks,
> this corpus is NOT curated — part of it is what the rebuild is escaping. Every mined
> pattern therefore carries a verdict: **KEEP** (proven, carry forward), **DROP** (observed
> failure mode, forbidden), or **ADOPT-NEW** (rule the corpus lacks but the new bank needs).
>
> Generated 2026-07-06. Version 1.

---

## 1. Corpus inventory & method

### 1.1 What was mined

The complete existing question corpus for the course: **4,963 questions across 188 units**,
100% joined to the course structure (32 sessions / 17 modules) via the session–unit map.

| module (session span) | CODING | FIB_CODING | CA_MCQ | CA_TEXTUAL | MC | MTO | REARR | total |
|---|---|---|---|---|---|---|---|---|
| Introduction to Python (s1–4) | 4 | 17 | 65 | 32 | 86 | 18 | 0 | 222 |
| Sequence of Instructions (s5–6) | 17 | 27 | 182 | 122 | 69 | 0 | 0 | 417 |
| Type Conversions (s7–8) | 18 | 26 | 109 | 68 | 16 | 0 | 0 | 237 |
| Operators (s9–10) | 25 | 60 | 227 | 0 | 27 | 0 | 0 | 339 |
| Conditional Statements (s11–12) | 25 | 37 | 237 | 64 | 30 | 0 | 0 | 393 |
| Loops (s13–15) | 50 | 27 | 212 | 56 | 28 | 0 | 13 | 386 |
| Strings Methods (s16) | 14 | 27 | 130 | 32 | 11 | 0 | 0 | 214 |
| Nested Loops & Loop control (s17–18) | 24 | 46 | 165 | 24 | 19 | 0 | 0 | 278 |
| Comparing Strings & Naming (s19) | 9 | 12 | 108 | 20 | 34 | 11 | 0 | 194 |
| Lists (s20–21) | 24 | 45 | 238 | 48 | 27 | 0 | 0 | 382 |
| Lists and Strings (s22) | 18 | 35 | 123 | 0 | 4 | 0 | 0 | 180 |
| Functions (s23–24) | 32 | 31 | 247 | 64 | 29 | 0 | 0 | 403 |
| Built-in Functions (s25) | 12 | 11 | 105 | 24 | 13 | 0 | 0 | 165 |
| List Methods and Tuples (s26–27) | 24 | 42 | 196 | 36 | 33 | 0 | 0 | 331 |
| Sets and Set Operations (s28–29) | 19 | 76 | 262 | 0 | 59 | 0 | 0 | 416 |
| Dictionaries (s30–31) | 14 | 49 | 180 | 0 | 56 | 0 | 0 | 299 |
| Python Standard Library (s32) | 11 | 14 | 52 | 0 | 29 | 1 | 0 | 107 |
| **total** | **340** | **582** | **2,838** | **590** | **570** | **30** | **13** | **4,963** |

(CA = CODE_ANALYSIS predict-output items; MC/MTO = multiple choice / more-than-one; REARR = rearrange.
Unit kinds per session: Reading Material, Classroom Quiz A/B/C, MCQ Practice, Coding Practice.)

### 1.2 Method — and why the findings are trustworthy

Seven analysts mined the corpus in parallel (one per question-type/module chunk), each
**executing code rather than just reading it**:

- All 340 CODING reference solutions were run against their own test suites.
- All runnable CODE_ANALYSIS snippets (~1,700 across three chunks) were executed to verify
  answer keys; 652 in the data-structures chunk, every snippet in the loops and lists chunks.
- 172 FIB blanks were probed by substituting alternate tokens from category pools and
  executing every variant (the ambiguity audit).
- Every claim below is grounded in `question_id`s (8-char UUID prefixes, collision-checked).

### 1.3 Corpus-wide facts that shape everything downstream

1. **No tags, no difficulty labels exist anywhere.** The taxonomy was never applied at
   authoring time — confirming the WHAT rail must be authored fresh, and rungs must be
   defined mechanically (they are, in §2.2).
2. **Classroom Quiz A/B/C are parallel forms, not difficulty tiers** (verified three ways:
   FIB size/blank stats, objective clone clusters, CA duplicate analysis). Do not treat
   A/B/C as a difficulty signal.
3. **Duplication is heavy**: 19–34% of items per chunk are exact or template-level clones
   (91 exact FIB duplicates; 150 exact CA records in the foundations chunk; 206 objective
   items in near-clone clusters; 176 verbatim snippets reused across 399 loop/conditional
   items). Some cloning is deliberate design (see clone families, §2.1-Fix), most is drift.
4. **Answer keys are mostly — not fully — reliable.** Data-structures and lists chunks:
   0 wrong keys found. But execution caught: 1 CODING reference solution failing its own
   suite, 2 FIB stored answers provably wrong, 1 CA family keyed with the wrong error class,
   and 2 quote-wrapped "correct" outputs that contradict the course's own lesson. Full
   do-not-port list in §5.
5. **The platform grader's normalization is now CONFIRMED by the platform owner
   (2026-07-07)**: CODING grading is per-line trailing-whitespace + trailing-newline tolerant
   (internal whitespace strict); **FIB typed answers are EXACT STRING MATCH**; TEXTUAL
   (type-the-output) is NOT exact-match (normalization applied, details unspecified —
   generate TEXTUAL keys as if strict, which is safe under any normalization). Runtime:
   **emit everything as Python 3.10**.
6. **Answer-key pathologies invite test-wise gaming**: 67% of True/False items key True;
   correct answers sit at option D only 7% of the time; "None of the given options" appears
   36+ times across chunks and is **never correct**; every Code-A/B-equivalence item keys True.

---

## 2. UNIVERSAL ITEM-CRAFT LAYER

Everything in §2 transfers to any coding course (Java, JS, C++); only §3 is Python-specific.

### 2.1 Item anatomy per axis

The new bank's coding axes are **Read** (predict output), **Fix** (correct broken code),
**Fill** (complete a blank), **Tweaked** (modify reference code to a new requirement), plus
**Write** (write-from-scratch, the classic coding item). Corpus ancestors: Read ← CODE_ANALYSIS
(3,428 items), Fill ← FIB_CODING (582), Write ← CODING (340), Fix ← the corpus's error-identify/
error-fix stems (~130 items) and "bug biography" arcs. Tweaked has no direct ancestor (adopt-new).

#### Read (predict the output)

- **Stem:** one frozen sentence — "What will be the output of the given Python code?" —
  with code in a separate fenced field, never inline. Satellite stems reuse the same snippet:
  True/False claim ("The given code snippet will print **X** as output"), purpose,
  identify-error, count-iterations ("How many times is the print statement executed?"),
  reverse-engineer inputs, counterfactual ("What would be the output if the break were removed?").
- **Snippet norms:** complete runnable programs, never fragments; one concept + at most one
  interaction; ends with `print()` except pure-error items; no comments; concrete snake_case
  names. Beginner ceiling: ≤6 lines foundations, ≤11 lines loops, ≤14 anywhere.
- **Two response modes:** MCQ (recognition) and TEXTUAL (student types the exact output —
  production). TEXTUAL is the deliberate *retrieval twin* of an MCQ snippet — recognition →
  recall progression. **KEEP** the twinning. Two hard rules observed: TEXTUAL is reserved for
  runnable code (never error answers — error prediction stays MCQ where the taxonomy is
  controlled), and TEXTUAL keys must be exact-match friendly (see C24).
- **Option set:** 4 options standard; 2-option True/False for claims; 5–6 only when the trap
  space is genuinely rich. Option roles in a canonical 4-option item: 1 correct + 1
  computed-wrong-path + 1 format/echo lookalike + 1 error-option or second wrong path.
- **Mirror pairs — the corpus's best teaching device (KEEP, elevate to rule):** boundaries are
  taught by paired items with flipped facts: `print(name)` vs `print("name")`; `int(2.3)` valid
  vs `int("2.3")` ValueError; `s[8]` IndexError vs `s[:8]` fine; `pass` vs `continue` on the
  identical loop; `+` rebind vs `+=` in-place on an aliased list. Generate traps in pairs.

#### Fix (correct broken code)

- **The generation template is the "bug biography" arc** (observed as clone families): the same
  buggy snippet examined through an escalating stem sequence — predict output → count
  iterations → True/False claim → **diagnose the cause** → **choose the fix**. Diagnose items
  carry *wrong-diagnosis distractors* (a plausible different bug: "the counter is not
  incremented" when the real bug is a captured condition variable). Fix items carry repairs
  that run but miss the stated goal.
- **The bug must be a catalogued misconception, never a typo hunt.** Exception: misspelled
  API names (`ends_with`, `startsWith`, `stript`) are allowed because the resulting
  AttributeError/NameError is itself a catalogued error-pattern class with a stable 3-item
  arc (identify → verify claim → fix).
- **Premise checks (KEEP):** occasionally the correct answer is "There is no error" /
  "No change needed" — prevents "stem says error, so there's an error" gaming.

#### Fill (complete the blank)

- **Format contract (holds 582/582, machine-checkable):** blank rendered as exactly six
  underscores `______` in the code; the stored answer is the full completed code with each
  filled span wrapped in `<>…</>`; replacing every `<>…</>` span with `______` must reproduce
  the code field byte-for-byte (round-trip invariant). Marker count == blank count; no
  multiline answers.
- **Blanks per item:** 1 (87%), 2 (11%), 3 (max). Granularity ladder: single closed-vocabulary
  token → expression (≤ ~12 chars) → whole statement/line.
- **What a good blank is:** a *decision* whose correctness is observable in output —
  solve-for-operand (`print((4+4) / ______ - 1)` → `2` for output 3.0), discriminating
  operands (chosen so every alternate token diverges), range endpoints from a stated goal,
  whole-line blanks pinned by downstream code. Variable-name blanks only when the name occurs
  elsewhere in the snippet.
- **What a bad blank is (all observed):** answer stated verbatim in the stem (60+19 of 667
  blanks); comparison operators over constant operands (multiple operators satisfy the code);
  positive/negative index equivalents; blank boundaries that cut balanced syntax (unbalanced
  parens); snippets referencing undefined names. The measured cost: **~1 in 4 blanks admits a
  semantically valid alternate answer** — the uniqueness probe (C04) exists to kill this.

#### Write (write-from-scratch)

- **Canonical stem (≈90% of corpus):** one-sentence imperative task, then `---`-ruled markdown
  sections `#### Input` / `#### Output` / `#### Explanation`. Input names each stdin line's
  type; Output restates the full success condition including both branches of any conditional;
  Explanation walks ONE worked example with bold constants and shown arithmetic.
- **Constants in the stem (bold), variable data via stdin.** Scenario wrapping only from
  mid-course onward and only when it adds meaning.
- **ADOPT-NEW stem requirements the corpus lacks:** a Constraints block (present in only
  6/340 — hidden large-N cases are otherwise unfair); a second sample I/O pair (0/340 —
  one example invites overfitting); an explicit output-whitespace contract sentence.
- **Solution conventions:** descriptive snake_case; early sessions split casting into two
  statements before `int(input())` becomes standard; accumulator loops before builtins;
  exactly one reference solution.

#### Tweaked (modify reference code) — adopt-new axis

No corpus ancestor. Closest relatives to build from: counterfactual Read stems ("what if the
break were removed"), goal-referenced fix stems ("change the slice so the output is [1,2,3]"),
and same-output equivalence items. Contract: reference code + a new requirement + test suite
that the unmodified reference fails; the required delta should be one rung-sized decision
(easy: change a constant/operator; medium: add a branch/condition; hard: restructure a loop
or compose with a prior concept).

### 2.2 Mechanical rung definitions (easy / medium / hard)

The platform's difficulty vocabulary is easy/medium/hard. Rungs are defined **per axis**, by
statically checkable properties. (The observed fine-grained ladders R1–R7 are preserved below
as sub-structure; e/m/h is their rollup.)

**Read axis** (rollup of observed R1–R6 + adopt-new R7):
- **easy** = R1–R2: 1–3 lines, ≤1 variable, single construct; answer is a literal in the code
  or one transform away; traps are format-level (quotes, `.0`) plus ONE misconception boundary.
- **medium** = R3–R4: 2–6 lines; a reassignment/precedence interaction, a short loop trace
  (2–6 iterations), an accumulator, or an error-boundary decision (snippet one token from a
  real error, options mix named errors with near-variant outputs); ≥2 computed-wrong-path
  distractors including an off-by-one.
- **hard** = R5–R6 (+R7): multi-variable/moving-bound traces, aliasing/mutation chains
  (holding 3 names / 2 objects), nested or dependent loops, behavior-category answers
  (infinite loop / error class / no-output), exact multi-line TEXTUAL production. Adopt-new
  R7 (above the corpus ceiling): nested loops with break/continue, multi-function call
  chains, nested data structures.
- **Two invariants worth copying:** numbers never add load (single-digit arithmetic
  everywhere; difficulty scales by structure, not arithmetic), and **distractor quality — not
  snippet length — is the real difficulty dial**.

**Fill axis:**
- **easy:** 1 blank; single closed-vocabulary token (keyword, operator, method/builtin name,
  small literal); code ≤3 lines; instruction may name the construct family.
- **medium:** 1–2 blanks; answer derived from a stated goal or pinned exact output, never
  named in the stem (solve-for-operand, range endpoints, condition operand); 3–6 lines, one
  control structure.
- **hard:** 2–3 coordinated blanks (import+use; slice triple) or one whole-line blank inside
  nesting/a function; requires simulating the code. Cap at 3 blanks.

**Write axis:**
- **easy:** single new concept + mastered I/O; ≤1 stdin line; ≤1 branch or 1 non-nested loop;
  solution ≤6 lines; single-value output.
- **medium:** new concept composed with exactly one prior concept; ≤3 stdin lines; one
  accumulator or output-formatting requirement; solution 7–12 lines; ≥1 boundary the naive
  version fails.
- **hard:** two+ interacting priors or nested control; multi-record stdin (count-then-N-lines)
  or structured parse; tie/empty/degenerate hidden cases; solution 13–20 lines. **Ceiling
  rule:** nothing beyond ~20 solution lines / LeetCode-Hard territory (the corpus's one such
  item is a documented landmine).

**Fix axis:**
- **easy:** one bug, visible symptom, single-line fix; bug = one catalogued misconception.
- **medium:** diagnose-then-fix (cause item with wrong-diagnosis distractors); or a fix where
  a tempting repair runs but misses the goal.
- **hard:** two candidate bugs where only one fires (error-precedence reasoning); or fix under
  a counterfactual constraint ("make it print X without changing line 1").

### 2.3 Distractor design rules

**The prime directive (KEEP, strongest pattern in the corpus): every distractor = one
reachable wrong execution path, applied consistently.** Distractors are *simulated
misconceptions*: the exact output the code would produce if the wrong belief held. This is
what made the corpus mineable — and each distractor in the new bank must be **tagged with
its misconception_id at authoring time** (ADOPT-NEW; generation becomes "pick 3 misconceptions
reachable from this snippet").

KEEP:
- Off-by-one triads for loop items: {one-extra, shifted-start, one-fewer}.
- Trace-adjacent numeric distractors (one-iteration-early/late, boundary-included) — never
  arithmetic ±1 noise.
- Error-option economics: error options appear ~4× more often as bait than as the key
  (observed 18–27% of MCQs carry one; correct in 3–7% of items). Plant error options on valid
  code adjacent to genuinely-erroring variants, and "No error"/"There is no error" as the
  occasional key. This kills "error option = answer" and "error option = never" strategies alike.
- Verbatim interpreter messages as options for error-keyed items (builds the error fluency
  the course outcome names); error-class lineups (IndexError/KeyError/ValueError/TypeError)
  as discrimination sets; message-precision options ("missing 1" vs "missing 2 required
  positional arguments").
- Case-grid options for case transforms (all-upper / all-lower / unchanged / swapcase).
- "All the given options" reserved for genuinely order-nondeterministic prints (its presence
  itself teaches unorderedness).
- Contrast sets: one snippet, three slices; replace with vs without assignment.

DROP (all observed):
- Unreachable numeric filler (no mental path computes it) — dead weight lowering effective
  option count.
- Format-noise distractors with no belief behind them (`N a m e`, random case flips).
- "None of the above/given options" as a permanent never-correct filler — either retire it or
  key it ~20% of the time.
- Joke/echo options beyond one per easy item.
- 2-option content MCQs (coin flips) for non-claim stems.
- True/False gluts: 2-option items cap information at a 50% guess rate; keep claim stems but
  pair every T/F with a sibling output item, and **balance the key base rate** (corpus: 67% True).

### 2.4 Test-suite design rules (Write/Tweaked axes)

Observed modal suite: 2 visible + 3 hidden, 5–7 total; visible = the stem's worked example
(weight ~1, "free samples"); hidden carry the marks, heavier for harder cases.

KEEP: visible-equals-worked-example convention; hidden majority carrying weight; boundary
values hidden with elevated weight; ≥5 test cases for anything with a branch; input-shape
sweeps for grid/list problems; tie/all-equal hidden cases.

DROP: single-visible-TC items (hardcoding the sample scores 100% — 14 such items observed);
zero-hidden suites; zero-weight test cases; non-normalized weight sums (observed 5–50);
float-repr expected outputs (`4.666666666666667`); expected outputs that encode
solution-specific trailing whitespace; constant-print no-input items as *graded* exercises.

ADOPT-NEW (the corpus lacks all of these):
1. **Hidden-case minimum:** ≥3 hidden, and ≥1 hidden per branch/boundary class of the spec.
2. **Edge-class checklist per input type** — numeric: {0, 1, boundary, boundary±1, negative
   if domain allows, large-N}; string: {len 1, repeated chars, target-absent → 0-count};
   list: {singleton, all-equal, duplicates, values that break a naive string-sort}.
3. **Mutant-killing discrimination:** every test case must kill ≥1 plausible wrong program
   (off-by-one range, `>` vs `>=`, int-vs-string sort), verified by running mutant solutions.
   (The corpus's latent-bug exemplar: a solution that sorts numbers as strings survives only
   because no two-digit numbers were ever tested.)
4. **CI gate:** the reference solution must pass its own suite byte-exact under the stated
   normalization contract (would have caught the one broken reference item).
5. **Normalized weight sum** (100) with a documented visible/hidden split.
6. **Determinism ban** on random/time-dependent outputs unless an explicit checker harness
   exists and is declared.

### 2.5 Stem style & framing rules

KEEP: second-person imperative, zero fluff in early sessions; goal-stating stems always ("Fill
in the blank to <observable goal>" — the corpus has zero generic stems and it should stay
that way); bold constants + backticked identifiers; one fully-worked example with arithmetic
shown; explicit whitespace notes for pattern-printing; scaffold lines that remove memorization
as the tested skill (the Unicode table line on every ord/chr item — "recall is never the
tested skill" is a course norm); story→technical translation items that teach students to
decode the course's own story-framed problems.

DROP: raw-HTML stems and inline-styled `<pre>` blocks (99 legacy items — markdown only);
external images as the only spec of expected output; ambiguous "between X and Y" without
inclusivity; grammar/typo noise in stems; environment-dependent outputs (`help()` text);
mixed input encodings within one item.

ADOPT-NEW: output pinned in the stem for medium/hard Fill items ("…so the output is exactly
`X`" — only 57/582 corpus items pin output; invert that ratio); construct-family naming
allowed only at easy; every statistic-free claim in a stem must be checkable against the code.

### 2.6 Generation gates (the automated pipeline before human review)

Order matters; each gate is cheap and kills a measured failure mode:

1. **Execution gate** — the item's code compiles and runs; completed FIB code runs; the
   reference solution passes its suite; the stated output claim is reproduced. (Measured
   corpus cost of its absence: 1 broken CODING reference, 2 wrong FIB answers, 2 runtime-broken
   FIB snippets, 1 mis-keyed CA family.)
2. **Key-verification gate** — Read/MCQ keys re-derived by execution; error keys match the
   actual exception class AND message.
3. **Uniqueness probe (Fill)** — enumerate the blank's category pool (operators / logical
   keywords / ints −12..12 / method names / builtins) and execute every alternate; require
   every alternate to change output or violate the stated goal. (Kills the measured 33%
   token-blank ambiguity rate.)
4. **Nondeterminism scan** — no exact-print grading of unordered collections (wrap in
   `sorted()` or use order-safe options); no random/time without a checker; no float-repr
   equality.
5. **Answer-distribution balancer** — across a generated batch: True/False ≈ 50/50, correct
   options uniform across positions, error-correct rate inside the 5–25% band, "no error"
   keyed sometimes.
6. **Dedup budget** — literal-normalized template key per item; max 2 items per template per
   session; clone families (same snippet, different stems) capped at 3–4 stem types and
   linked by an item-family id.
7. **Rung conformance check** — the item's statically measurable properties (lines, blanks,
   concepts, iterations, names held) match its claimed rung per §2.2.
8. **Misconception-tag check** — every distractor carries a misconception_id from the bank
   (§3.2); every Fix bug maps to a catalogued misconception.

### 2.7 C-series eval set (machine-checkable review criteria)

Mirrors the pedagogy doc's E-series. Reviewers reject with rule IDs, not prose; gates C01–C08
run automatically (§2.6), the rest are review checklists.

```yaml
eval_set_c:
  version: 1
  items:
    - id: C01
      gate: execution
      check: "Code compiles & runs; reference passes own suite byte-exact under the declared normalization; FIB completed code runs clean; stated outputs reproduced."
    - id: C02
      gate: key_verification
      check: "MCQ/TEXTUAL key re-derived by execution; error keys match real exception class and message."
    - id: C03
      gate: fib_roundtrip
      check: "FIB: replacing every <>…</> span with ______ reproduces the code field byte-for-byte; marker count == blank count; ≤3 blanks; no multiline answers."
    - id: C04
      gate: fib_uniqueness
      check: "FIB: substitution probe over the blank's category pool leaves no alternate token that matches output AND satisfies the stem goal; expression blanks ship an accepted-answers list (spacing/quote/commutative canonicalization) or are restricted to closed-vocabulary tokens."
    - id: C05
      gate: fib_ast
      check: "Every blank is a complete AST node; granularity matches rung (token=easy, expression=medium, statement/line=hard)."
    - id: C06
      check: "The answer (or any blank's answer) does not appear verbatim in the stem; stems may name a construct FAMILY at easy only."
    - id: C07
      check: "Stem states an observable goal; medium/hard Fill and Tweaked stems pin the exact output; Write stems have Input/Output/Explanation sections + Constraints block + TWO sample I/O pairs + an output-whitespace sentence."
    - id: C08
      check: "Every distractor is a reachable wrong execution path tagged with a misconception_id; no unreachable numeric filler; no format-noise options; ≤1 echo option per easy item."
    - id: C09
      check: "Error-option economics: error options present as bait ~4x their key rate; batch error-correct rate 5–25%; 'No error' keyed occasionally; 'None of the above' either absent or keyed ~20%."
    - id: C10
      check: "Batch answer-key balance: T/F ≈ 50/50; correct-option position uniform (incl. D); equivalence items key both True and False."
    - id: C11
      check: "Write/Tweaked suites: ≥2 visible (first = the stem's worked example), ≥3 hidden, ≥1 hidden per branch/boundary class, weights normalized to a documented sum."
    - id: C12
      check: "Edge-class checklist satisfied for each input type (numeric: 0/1/boundary/boundary±1/negative-if-legal/large; string: len-1/repeats/absent-target; list: singleton/all-equal/duplicates/naive-sort killers)."
    - id: C13
      check: "Every test case kills ≥1 named mutant (off-by-one, >/>= swap, str-vs-int sort, missing-branch); no suite dodges its solution's own latent bug."
    - id: C14
      check: "Determinism: no unordered-collection exact prints (sorted() or order-safe options); no random/time without declared checker; no float-repr equality grading."
    - id: C15
      check: "No expected output depends on trailing whitespace; TEXTUAL keys are exact-match friendly (no leading-space lines, no count-the-dots answers, \\n only, trailing whitespace stripped per line)."
    - id: C16
      check: "Rung conformance: statically measured properties match the claimed easy/medium/hard definition for the axis (§2.2)."
    - id: C17
      check: "Fix-axis bug = a catalogued misconception (or catalogued misspelled-API error class); never an arbitrary typo hunt; diagnose items include ≥1 wrong-diagnosis distractor; ≥1 offered repair runs but misses the goal."
    - id: C18
      check: "Mirror-pair coverage: every boundary-type misconception ships as a pair (working twin + trap twin) within the same session's bank."
    - id: C19
      check: "Dedup: literal-normalized template appears ≤2x per session; clone families ≤4 stem types, linked by family id."
    - id: C20
      check: "Style: markdown only (no raw HTML/inline CSS); no load-bearing external images; beginner-safe vocabulary; idioms allowed at this course stage only (see §3.4); snake_case identifiers."
    - id: C21
      check: "Read TEXTUAL items: snippet runs clean (error answers are MCQ-only); output ≤ ~6 lines; format precision (quotes, .0, \\n) is itself the tested fact when demanded."
    - id: C22
      check: "Error text in options/keys uses verbatim CPython form 'ExceptionName: message' consistently (no bare-name/prose mixing within a bank)."
    - id: C23
      check: "Language/runtime = Python 3.10 for all emitted items (legacy PYTHON/PYTHON39 tags retired); function-mode items declare their harness contract explicitly."
    - id: C24
      check: "Every item carries node, level (rung), axis, and role tags — born tagged, cell-directed; distractors carry misconception ids."
    - id: C25
      check: "Scenario framing only where it adds meaning; story-framed items have a story→technical sibling available in the objective bank at early sessions."
```

---

## 3. PYTHON OVERLAY

### 3.1 Platform format contracts (as observed in the export)

**Record envelope (all types):** `question_id` (UUID) · `question_type` · `content` (stem,
markdown with legacy HTML leakage) · `multimedia` · plus type-specific fields below. Unit
kinds: Reading Material / Classroom Quiz A/B/C / MCQ Practice / Coding Practice.

| type | key fields & semantics |
|---|---|
| CODING | `codes[]`: exactly one `{code_content, language: PYTHON\|PYTHON39, default_code:true}` — the reference solution, which **doubles as the prefill** (scaffold+answer merged in one blob; flag for the new schema to separate them). `test_cases[]`: `{input (raw stdin, newline-joined), output (expected stdout), is_hidden, weightage}`. Function-mode items (11 observed): bare `def`s, harness args/returns in input/output fields, contract pinned by a MultiLineNote — the wrapper itself is NOT in the export. |
| FIB_CODING | `code` = snippet with `______` blanks (six underscores, may abut text); `correct` = full completed code with `<>…</>` around each answer; round-trip invariant holds; language always PYTHON39; graded as typed input (no options). |
| CODE_ANALYSIS_MULTIPLE_CHOICE | `default_code_details.code` = snippet; `options` (plain strings, may be fenced code blocks); `correct` = JSON array of one `{option_id, content}`. |
| CODE_ANALYSIS_TEXTUAL | same, no options; `correct` = exact-match string (1–40 chars, occasionally multiline); stdin items append `Input: …` to the stem. |
| MULTIPLE_CHOICE | `correct` = JSON array of one `{option_id, content}`; True/False is just a 2-option MC; `content` matches an options entry byte-exactly (join on content is safe). |
| MORE_THAN_ONE_MULTIPLE_CHOICE | `correct` = array of 2–3 `{option_id, content}`, arbitrary order; never exactly 1, never all. |
| REARRANGE | `correct` = array of plain strings = an exact permutation of `options`; options are prose pseudo-code steps (3–5), never code lines. |

**Grader normalization (CONFIRMED 2026-07-07):** CODING = per-line trailing-whitespace +
trailing-newline tolerant, internal whitespace strict. **FIB = exact string match** — this
makes gate C04 non-negotiable: a blank admitting any semantically-valid alternate string
(quote style, spacing, commutative form, pos/neg index) will mark correct students wrong;
new FIB blanks must be closed-vocabulary tokens or have a by-construction-unique answer
string. TEXTUAL = not exact-match (unspecified normalization) — still author keys strictly.
Forge emits outputs that pass under strict matching (safe under any contract) and targets
**Python 3.10** (legacy PYTHON/PYTHON39 tags retired).

**Markup:** markdown with custom tags `<MultiLineNote>`, `<MultiLineQuickTip>`,
`<Img imageSrc=… widthPercent=…/>`; 99 legacy items are raw HTML — do not imitate. Angle-
bracket outputs (`<class 'list'>`) get eaten by HTML renderers — escape or backtick them.

### 3.2 Python idiom norms by course stage (what solutions/snippets may use)

- **s1–6:** `print`, arithmetic, `input()`, two-step casting (`x = input()` then `x = int(x)`),
  string `+`/`*`, `len`, indexing. No f-strings anywhere in the course (corpus has zero) —
  output built with `+` and `str()`.
- **s7–12:** `int()/float()/str()/type()`, slicing, relational/logical operators, if/elif/else.
- **s13–19:** `while`, `for`+`range` (2-arg), `break/continue/pass` (s18), string methods
  (s16), `ord`/`chr` (s19, always with the Unicode scaffold line).
- **s20–27:** lists, aliasing/`id()`, `split`/`join`, negative indexing/steps, functions,
  `*args`, positional/keyword/default args, built-ins (`min/max/sum/sorted`), list methods,
  tuples.
- **s28–32:** sets & set ops, dicts & views, `**kwargs`, `math`/`random`, `map/filter/reduce`
  (with `list()` wrapping), imports/aliases.
- Comprehensions and `lambda` appear only incidentally in late CODING solutions — treat as
  out-of-band for generated items unless the registry says otherwise.

### 3.3 THE MISCONCEPTION BANK

The highest-value section: ~310 named wrong beliefs reverse-engineered from distractors,
error keys, and fix arcs, each with its trap and evidence. **Usage:** Read-axis items pick
2–3 reachable misconceptions per snippet and simulate them as distractors; Fix-axis bugs ARE
these beliefs put into code; Fill-axis discriminating operands are chosen so these beliefs
produce divergent outputs. IDs are unique within module; cite as `<module>/<id>`.
`Sev`: C = corrupts program logic broadly, H = high, M = API-specific, L = display/format.
Question-id evidence (≤3 per row) refers to the mined corpus.

#### Introduction to Python (s1, s4)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| quotes-appear-in-output | `print("Name")` prints the quotes | `print("Name")` | de31e77f, 4fb866ed | H |
| quoted-math-evaluates | `"17 + 5"` prints 22 | `print("17 + 5")` | 313654dd, 68b6dabb | H |
| bare-math-echoes | `print(22 + 87)` prints the expression text | `print(22 + 87)` | 4a4b5ad2, 9b68c709 | H |
| division-yields-int | `10/5` → `2` (no `.0`) | `print(10 / 5)` | 0bba3a69, 9c5b6012 | H |
| division-order-reversed | `5/25` computed as `25/5` | `print(5 / 25)` | c14fbf15, bbd0f290 | M |
| mixed-add-truncates | int+float drops the fraction | `print(14 + 7.7)` | a06666f1, 5ae134e8 | M |
| bare-word-is-string | `print(CCBP)` works without quotes | `print(CCBP)` → NameError | 4e26bdb5, ac3aba01 | H |
| typo-name-is-syntaxerror | `prnt(...)` is a SyntaxError (it's NameError) | `prnt("Hello")` | 4c487b53 | H |
| python-case-insensitive | `Print(...)` works | `Print("Hello World")` | 57f4c45a, 3dcc4930 | H |
| unclosed-paren-ok | missing `)` still runs | `print("CCBP"` | af09f3f4, c5ad0264 | M |
| digit-string-is-number | `"123"` is stored as an integer | `number = "123"` | 5b57cc5a, f1a1f096 | H |
| quoted-bool-is-bool | `"True"` is a Boolean | `is_active = "False"` | 2b97f4cb, 56e81138 | H |
| equals-compares | `=` checks equality | `age = 30` | f823f682, a8ffd2a3 | H |
| whole-float-is-int | `7.0` is an integer | `x = 7.0` | 45066090, 864d1bf1 | M |
| bool-prints-lowercase | `print(True)` shows `true`/`"True"` | `print(True)` | b4662901 | L |

#### Sequence of Instructions (s5–6)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| eval-strict-left-to-right | `10/2+3` groups as `10/(2+3)`; BODMAS ignored | `print(1 + 1 * 2)` | 5b1004bc, 40cb4fd2 | H |
| parens-are-decoration | `(2+2)` doesn't run first | `print(8/2*(2+2))` | 7471b9be, 2caf4773 | H |
| division-result-stays-int | `6/1` → `6`, propagates through later math | `x = 6/1; y = x + 4` | 92750b77, 8d9a6197 | H |
| varname-echo | `print(name)` prints the text `name` | `name="Rahul"; print(name)` | 506dce8b, 38c09bae | H |
| quoted-varname-dereferences | `print("score")` prints `10` | `score=10; print("score")` | 6b032a76, bedae17e | H |
| use-before-assign-works | Python hoists variables | `print(score)` before `score=100` | 13ffcac1, 0d59c5e0 | H |
| rhs-undefined-defaults | undefined RHS var is 0/skipped | `z = y - z` (z undefined) | bfe0546c, e963d1da | H |
| reassign-accumulates | second assignment adds to the first | `b=10; b=2` → 12 | 3426fedd, fedd6ab5 | H |
| copy-binds-live | `b = a` tracks a's future values | `a=4; b=a; a=8; print(a*b)` | 5946cf35, 19a3b640 | H |
| final-value-everywhere | print/reassign/print shows final value twice | `a=5; print(a); a=10; print(a)` | c77848dd, 159e37fa | H |
| assignment-prints | an assignment line produces output | `a=5; print(a); a=10` | f49b5965 | M |
| prints-share-line | two prints join on one line | `print("Hi"); print("Paul")` | 9c123e10, 2d85cdc5 | H |
| stray-indent-harmless | a leading space is cosmetic | ` print(year)` → IndentationError | 69d859d8, c1db0797 | H |
| concat-inserts-space | `"Good"+"Morning"` → `Good Morning` | string `+` | 4dad75bc, 9c88b195 | H |
| explicit-space-dropped | `"Hello" + " " + "World"` → `HelloWorld` | explicit `" "` operand | e29e16bb, 9daca8bf | M |
| digit-strings-add | `"69" + "90"` → `159` | numeric-string `+` | 6693ae43, 4d531bcb | H |
| str-plus-int-coerces | `"Hi" + 3` → `Hi3` | → TypeError (verbatim msg) | db0832ab, b24a8a11 | H |
| str-times-int-errors | `"Banana" * 3` raises (over-generalized from `+`) | valid `*` | 5c0fd3ed, 47ee00f2 | H |
| repeat-appends-number | `"Banana" * 3` → `Banana3` | string `*` | 4d6de27f, d5eeb64f | M |
| repeat-binds-whole-concat | in `"He"+"ll"*4+"o"`, `*` applies to everything | precedence of `*` over `+` | 647934a2, e1103a15 | H |
| repeat-off-by-one | `"y"*4` gives 3 or 5 copies | count trace | a7e18da0, a18b94d8 | M |
| len-skips-nonletters | `len()` ignores spaces/punctuation | `len("Hello World!")` → 12 | 36ddb683, af293d43 | H |
| len-not-scaled-by-repeat | `len(s*4)` = `len(s)` | `len("Adams" * 4)` | 8583ca0c, a31cd883 | M |
| index-one-based | `s[2]` is the 2nd character | `"Pigeon"[2]` | be6410dc, ba8c8afc | H |
| index-len-is-valid | `s[len(s)]` returns the last char | `"Football"[8]` → IndexError | 535cf4c4, 128917d0 | H |
| input-gives-number | typing 123 makes `input()` return int | `number = input()` | 214e073e, b2fe73f8 | H |
| input-echoes-name | `print(sport)` after input prints `sport` | echo trap | 272530fd, 618eda99 | L |
| two-inputs-tangle | two `input()` lines merge/error | sequential inputs | 6fac6a95, f42dda97 | M |
| unclosed-string-runs | `name = "Jay` still assigns | → SyntaxError EOL | a4bc0453, 3358541d | H |

#### Type Conversions (s7–8)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| slice-end-inclusive | `s[7:12]` includes index 12 | `"Hello, World!"[7:12]` | a9182d8a, 9e0657b0 | H |
| slice-shifted-window | slice start counted 1-based | window-shift distractors | 3de923ac, 21d88321 | H |
| slice-arg-is-count | `s[5:]` = first five chars | `"data_analysis"[5:]` | 47419338, 96e66507 | H |
| slice-beyond-len-errors | any slice touching len raises | `food[:7]` on len-7 is fine | c8373a25, 86721f1b | H |
| int-rounds | `int(99.99)` → 100 | truncation, not rounding | 03b879bc, 9243b0e2 | H |
| int-of-float-errors | `int(14.65)` raises ValueError | valid conversion | adf53b7a | H |
| decimal-string-converts | `int("2.3")` → 2 | → ValueError (verbatim msg) — the module's marquee asymmetry vs `int(2.3)` | b89ae3a3, 437a8ce3 | **C** |
| word-string-converts | `int("Five")` understands words | → ValueError | f6d44913 | M |
| conversion-keeps-quotes | `int("10")` prints `"10"` | format trap | 80390bd3, 2f4a85f4 | M |
| conversion-adds-decimal | `int("22")` → `22.0` | format trap | eaa5d583, 250c1e46 | M |
| input-type-is-content | `input()` of `-23.56` is a float | `type(count)` | dc14d5bb, b15dae3b | H |
| conversion-doesnt-stick | after `age=int(age)` type is still str | rebinding | a1703f21, 66c714ee | H |
| type-echoes-expression | `print(type(x))` prints `type(x)` | echo | ca73ba5e, 5d9a8715 | L |
| quoted-bool-types-as-bool | `type("False")` → bool | `True` vs `"True"` vs `true` triangle | 1c0c0b88, 4301e47e | H |
| repeat-appends-count | `"#" * int("8")` → `########8` | conversion + repeat | 5528dc66, ec4a759e | M |
| converted-still-string | `x + int(y)` raises anyway | valid after conversion | 26bfad0c, e16648e7 | H |
| splice-keeps-length | `len(s[:4]+s[5:])` = original len | slice+concat+len composition — the module's hard rung | 56604c32, ac744695 | H |
| copy-leaves-undefined | after `a = b`, a is None/undefined | simple copy | ab6661d1, 24ec706c | M |

#### Operators (s9–10)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| cross-type-equals-true | `10 == '10'` is True | cross-type equality → False, not error | 38e3ffaf, 287116e2 | **C** |
| cross-type-equals-raises | comparing different types raises | `10 == '10'` runs fine | a96dba89, 96d5455a | H |
| int-float-unequal | `7.0 <= 7` is False | numeric cross-type compare | 38024ffd, cd52631a | H |
| string-eq-case-insensitive | `"Hello" == "hello"` → True | case sensitivity | 9427019c, 0b4d8676 | H |
| single-equals-compares | `print(5 = 5)` compares | → SyntaxError with verbatim CPython hint "perhaps you meant '=='?" | 08c596bf, 24b4d6c2 | **C** |
| spaced-operator-ok | `< =`, `= =`, `=>` are valid | operator lexing | fcd53426, e1c45d66 | H |
| comparison-returns-operand | `print(10 == 10)` → `10` | comparisons return bools | c52cd511, 7fb5ad0f | M |
| bool-op-returns-none-or-error | `not(True)` → None / error | boolean ops | 986cc3f8, 2562758e | M |
| or-needs-both | `or` needs both True | truth tables | 9cec841d, 0a757d40 | H |
| not-doesnt-invert-comparison | double-`not` confusion | `not(not(True))` | d198d5e5, 40df0cc3 | M |
| len-vs-content-confusion | `len("30") != len("50")` → True | equal-length pairs | 0cffe77b, d41e0378 | M |
| near-identifier-resolves | `Flase` still means False | → NameError | bfd3570e | M |

#### Conditional Statements (s11–12)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| C-01 | body after `if cond:` needn't be indented | → IndentationError: expected an indented block | ea1bc777, 540d3fa7 | **C** |
| C-02 | extra/deeper indentation on a later line is harmless | → IndentationError: unexpected indent | 8073b62c, 5feb9c46 | H |
| C-03 | if the condition is False the body isn't parsed (no error) | `if False:` + bad indent still errors | f511e3fa, 21b57840 | H |
| C-04 | indentation must be exactly 4 spaces | legal 1-space indent runs fine | 18c884d9, ccdd6b54 | M |
| C-05 | unindented code after an if-block still belongs to it | trailing statement always runs | dac370a4, d503a280 | **C** |
| C-06 | a false `if` with no else must print/error | correct: No Output | 4bf6ad4a, ab7db230 | H |
| C-07 | sequential `if`s behave like elif ladder (only first true runs) | grade-ladder: all true branches fire | 102d40c4, abe9d567 | **C** |
| C-08 | `else` can take a condition | `else a < b:` → SyntaxError | 49715b19, cb901b95 | M |
| C-09 | `elif` may follow `else` / needs no condition | → SyntaxError | a1fc7198, 2db67e3f | M |
| C-10 | a statement may sit between `if` and its `else` | → SyntaxError | 77c91858 | M |
| C-11 | `12 == "12"` is True inside a condition | cross-type equality | a11e4ec9 | H |
| C-13 | `input()` returns a number in comparisons | `x=input(); x>y` compares strings — NOTE: corpus items never fire this trap (see §5); fix with inputs like 9 vs 10 | 40bbf033 | **C** |
| C-14 | a stored boolean can't drive `if` / boundary `<=` errors in the stored expr | `is_day = (t>=6) and (t<=18); if is_day:` | 03669b6d, f9424c22 | H |
| C-15 | truth-table errors (`True and False` → True) | boolean gating of nested ifs | 3e3ba06a, 6b75e91e | H |
| C-16 | nested inner `if` checked even when outer is False | 2-level nesting | e0217484, 2f832442 | H |
| C-17 | `/` gives int when it divides evenly | `.0` exactness in branch output | 50d4588a, 007a043d | H |
| C-18 | equal float literals compare unequal | `12.34 != 12.34` | 718d6b75 | L |

#### Loops (s13, s15)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| LP-01 | `while i < 3` includes 3; `range(3)` = 1,2,3; `range(5,7)` includes 7 | off-by-one family (biggest in module) | e70489bb, c075b579 | **C** |
| LP-02 | a condition variable re-evaluates itself each iteration | `condition = (counter < 3); while condition:` → infinite | ea4d69eb, 0b1dc640 | H |
| LP-03 | `while` runs at least once (do-while model) | entry-false loops → No Output | 4c85f075, b33840ce | H |
| LP-04 | `while x == N` never runs / runs forever | runs exactly once with increment | a0081625, 6325d263 | M |
| LP-05 | missing counter update stops/errors the loop | identity update `row = row` → infinite | 21ddb473, a00eedb8 | **C** |
| LP-06 | loop variables needn't be defined before the loop | → NameError | 895cdb82, 85b590e2 | H |
| LP-07 | the loop prints once at the end | per-iteration printing | a92b0e58, c171899e | M |
| LP-08 | print shows the loop variable itself (blind to offsets) | `print(a + 1)` inside loop | 3378c402 | M |
| LP-09 | after the loop the counter is bound−1 | post-loop counter value | 34bc5113, acbc88d3 | M |
| LP-10 | iteration miscount when both ends move | `a` decreasing while `c` increasing | 16d1417c, 6c4bb42f | M |
| LP-11 | `range[3]` is valid syntax | → runtime TypeError (corpus mislabels as SyntaxError — see §5) | 0a6d1ec2, abc15e29 | M |
| LP-12 | `for ch in word` iterates words / reverses | character iteration | 1661f878, 3c7423f1 | H |
| LP-13 | multiplying accumulator over `range(N)` gives N! | `range` starts at 0 → product is 0 | fcf28486, d3e7f786 | H |
| LP-14 | loop-body indentation optional | → IndentationError | 14897449, 33c8196a | H |
| LP-15 | `<=` behaves like `<` | boundary term dropped | f7b59138, 60cc1447 | H |
| LP-16 | char counting is case-insensitive | count "s" in "Solar System" → 1 not 3 | 41d8edba | M |

#### Strings Methods (s16)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| S-01 | string methods mutate in place | `s.replace(...)` without assignment → unchanged | c8a6bc83, dbb79e90 | **C** |
| S-02 | `replace(a, b)` replaces b with a | argument order | dff0087e, f0434562 | H |
| S-03 | `strip(ch)` removes ALL occurrences anywhere | ends-only semantics | 8159f7a2, dd790b65 | H |
| S-04 | `strip()` removes internal whitespace too | `"  Hello World  ".strip()` | 86ccf813, 4773339c | M |
| S-05 | `startswith`/`endswith` are case-insensitive | case sensitivity | 2af88791, 5ed62da0 | H |
| S-06 | method names tolerate case/underscore variants (`ends_with`, `startsWith`, `stript`) | → AttributeError; 3-item fix arcs — Fix-axis gold | 541775a0, f131f9a4 | H |
| S-07 | `isdigit()` checks letters / validates any number | digit-only semantics | 98533840, 569542e1 | M |
| S-08 | `upper()`/`lower()` affect digits/symbols or swapcase | case-grid options | c37309c9, 3b8016c1 | M |
| S-09 | chained transforms lose earlier steps | `word.upper().lower()` | 5a5f7c5a, 49da8e87 | M |
| S-10 | slice stop index included | `message[7:12]` → World not World! | 572a223e, 230757e3 | **C** |
| S-11 | slicing is 1-based (`[1:]` = whole string) | `"Jasmine"[1::1]` | 8950eeef, c3a9e481 | H |
| S-12 | `[::2]` starts at index 1 / picks wanted letters | `".D.E.C.O.D.E."[::2]` → all dots | 6b05ecd9, 8505e11c | H |
| S-13 | start/stop/step arithmetic errors | `[1:8:2]` families | 6df96450, 33d7c456 | H |
| S-14 | `[::1]` reverses | only `[::-1]` reverses (corpus has NO real `[::-1]` item — gap) | 101f8c6a, 4b0c8eaf | M |

#### Nested Loops & Loop Control (s17–18)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| NL-01 | `break` exits all enclosing loops | inner break, outer continues | 4e0d9579, 01490ab4 | **C** |
| NL-02 | `continue` terminates the loop | continue ≡ break | cafa64e4, f3e9cb6a | **C** |
| NL-03 | `continue` jumps to the next statement | next iteration, not next line | ffe02145 | H |
| NL-04 | `pass` skips the rest of the iteration | pass is a no-op | 44a81289, f8171347 | H |
| NL-05 | `range(a,b)` includes b (nested count off-by-one) | 2×3 nest miscounts | af8587d3, b34d5d8d | **C** |
| NL-06 | inner loop runs once total, not once per outer pass | full re-sweep per outer iteration | 9aa8bf93, f3918e3e | **C** |
| NL-07 | `range(i)` with i=0 still runs / dependent range uses final i | dependent inner ranges | d1e8d363, 38bee32d | H |
| NL-08 | parallel loop vars advance in lockstep | `if i == j` across disjoint ranges → 0 | d3128bc8 | M |
| NL-09 | break is checked before the statements above it | accumulate-then-break ordering | 45281e5e, 71dd8859 | H |
| NL-10 | while body executes once before the check | do-while model in nests | 17a2f706, f7920905 | M |
| NL-11 | `<=` boundary blindness in while nests | iteration count | 48a9e802, 3448c25c | M |
| NL-12 | indentation cosmetic / colon optional | wrong-depth break | 898a21cb, e5c6c186 | H |
| NL-13 | code after `continue` in the block still executes | skipped statements | f3e9cb6a | M |
| NL-14 | a loop that never runs is an error | `while False:` → clean, accumulator unchanged | f7920905 | L |

#### Comparing Strings & Naming Variables (s19)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| CS-01 | string comparison is case-insensitive alphabetical | `"Mango" > "apple"` → False ('M'=77 < 'a'=97) | 23a4c549, c3279361 | **C** |
| CS-02 | uppercase letters are "bigger" | ord zones | c3279361 | H |
| CS-03 | numeric strings compare numerically | `"984" <= "99"` → True | d7731d96, 456a4143 | **C** |
| CS-04 | longer string is greater | `"root" <= "beetroot"` → False | 6ed9644f | H |
| CS-05 | prefix/substring relation decides ordering | `"rain" > "rainy"` | 25ae666e | M |
| CS-06 | strings can't be ordered with < > | valid comparison | 59fbc0bf, fb943eaf | M |
| CS-07 | a comparison prints None/nothing | `print(a < b)` | 59fbc0bf | L |
| CS-08 | mixing quote styles is an error | `"hello" < 'world'` fine | 613edb14 | M |
| CS-10 | ord/chr case & zone confusion | `chr(109)`='m' not 'M'; `ord("B")`=66 | 77b2b9c4, addf2802 | M |
| CS-11 | `chr('122')` / `ord(65)` accepted | argument types | 18f99fca, b61c95ad | H |
| CS-12 | hyphens legal in identifiers | `my-variable` → fix: underscore | fe9d16ff, cfc2f058 | M |
| CS-13 | identifiers may start with a digit | `2nd_place` invalid; `word12word2` valid — position vs presence pair | 4eb9cea8, e82f2e02 | M |
| CS-14 | bare words are strings; keywords usable as values | `keyword = and` → SyntaxError | a02e3278, e008c893 | M |

#### Lists (s20–21) — the aliasing core

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| LI-01 | `b = a` copies the list | mutate through alias, both change | aef8aecc, 877242a0 | **C** |
| LI-02 | `a = a + [x]` ≡ `a += [x]` on an aliased list | rebind vs in-place minimal pair | 1f76a48c, 3a28fbb3 | **C** |
| LI-03 | mutating an element changes the object's id | `id()` stable under mutation | aba53ac7, e8d2afaa | H |
| LI-04 | equal contents ⇒ same object | `id([1,2,3]) == id([1,2,3])` → False | 5af4f627, 879a2b2f | H |
| LI-05 | rebinding a source var retroactively updates the list | `a=2; list_a=[1,a]; a=3` (spreadsheet model) | 07df0d33, 73e4b0ad | H |
| LI-06 | a sublist in two containers is copied, not shared | mutate via third name, both parents show it | 5217b0e3, cad92dc0 | **C** |
| LI-07 | rebinding an extracted sublist mutates the parent | inverse of LI-06 | f168bcd1, 26653b46 | H |
| LI-08 | indexing is 1-based | largest bucket in module | fbc4be8e, de35cc08 | **C** |
| LI-09 | out-of-range index assignment appends | → IndexError | bd9cd821, 4cb8e774 | H |
| LI-10 | strings support item assignment like lists | `word[0]='I'` → TypeError | ab73d188, 5e91dc48 | H |
| LI-11 | error-name confusion (Type/Index/Value/Key/Name) | error-class lineups | 5e91dc48, 822adade | M |
| LI-12 | assigning a list to an index splices it flat | `my_list[1] = [4,5]` nests | fe178253 | M |
| LI-13 | `+` nests its operand / literal `[a, b]` flattens | concat models | fe3a39b5, 3adb75de | H |
| LI-14 | mixed-type list ops raise | `[1,2]+['a']` fine | 3adb75de, a3bc8e00 | M |
| LI-15 | `list * n` repeats element-wise / nests | `[1,2]*3` | b11017a2, 0f03543c | M |
| LI-16 | `list += int` appends the int | → TypeError; `+= [i]` works | 6405359b, 3511e0af | H |
| LI-17 | `list(str)` wraps the whole string | `list("Red")` → chars | 50e662bb, 06ca1907 | M |
| LI-18 | slice end included (lists) | 8 mechanically confirmed items | 63d452a6, b9eeabec | **C** |
| LI-19 | slice step misread | `[0:5:2]` semantics | 8dee935c, 5f3c3c5b | H |
| LI-20 | `a[i][j]` second index applies to outer list | double indexing | 4876b56b, 68540257 | H |
| LI-21 | `len` miscounts / `len[...]` valid | syntax + semantics | f4126e49, 3bf20dc6 | M |
| LI-22 | `print(list)` strips brackets / loop-print shows the list | display models | db0d0c31, b1d68e0b | M |
| LI-23 | adjacent lists auto-concatenate (missing comma harmless) | `[[1,2] [3,4]]` → error | 4f897a19 | L |

#### Lists and Strings (s22)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| LS-01 | negative index counts from the front | `list_a[-1]` on [5,4,3,2,1] → 1 not 5 | 359bea8b, ac36ff30 | **C** |
| LS-02 | last = `-0`/`-len`; `-k` counts 1-based from front | negative off-by-one | 26ef1308, 130aa9b0 | H |
| LS-03 | `[-6]` on a 5-item sequence is fine / negatives illegal | index vs slice asymmetry | 8fbe9dcb, 0fd746d9 | H |
| LS-04 | slice end inclusive with negative bounds | `list_a[-4:-1]` | 02ca0484, 051901f5 | **C** |
| LS-05 | out-of-range slices raise | slices clamp | 0fd746d9, 78445faa | H |
| LS-06 | step sign ignored / wrong-direction slice errors | `list_a[2:4:-1]` → `[]` | 04325adf, 6a865205 | H |
| LS-07 | reverse-slice bounds off-by-one | `"world"[4:0:-1]` → `dlro` not `dlrow` | 80c03448, d2f5d40f | H |
| LS-08 | `[::-1]` doesn't reverse / scrambles | canonical reverse | b218addb, 8f9abe21 | M |
| LS-09 | `split(sep)` keeps the separator in tokens | `"step-by-step".split('step')` → ['', '-by-', …] | f44ff420, bf27a19a | H |
| LS-10 | `split(',')` drops empty strings | adjacent/trailing separators produce `''` | 18b0a735, 6398abee | H |
| LS-11 | default `split()` splits on every single space | collapses runs, handles \n\t | 083441bd, 4c9c2106 | H |
| LS-12 | `split` converts numeric tokens to ints | tokens stay strings | 94f19dd3 | M |
| LS-13 | `join` stringifies non-strings automatically | → TypeError (verbatim msg) | 47cf7bf3, 896b6e4b | H |
| LS-14 | join separator placement confusion | between, not around | a84f338c, 82203859 | M |
| LS-15 | `list(s)` ≡ `s.split()` | chars vs tokens | 221ed27c, 71dcafeb | M |
| LS-16 | misspelled method still works | `splt()` → AttributeError | 650153f8, e7640321 | L |

#### Functions (s23–24)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| FN-01 | a function without `return` still hands back its computed value | `num = f(num)` → None | e3de2a0d, 4048b5c8 | H |
| FN-02 | `return` prints / `print` returns | `total = print(...)` | 27dfab3f, 20b2f529 | H |
| FN-03 | function locals are readable after the call | `print(msg)` after call → NameError | 567e76d6, a05bd0ab | H |
| FN-04 | a same-named global feeds the function / overrides its default | red-herring globals | 02b773c1, 64436489 | H |
| FN-05 | code after `return` executes | unreachable print | eca57bdb, 56c7789e | M |
| FN-06 | missing required args auto-fill | → TypeError: missing N required positional arguments | b3756c0a, 04f9e582 | H |
| FN-07 | the TypeError message doesn't count missing params | "missing 1" vs "missing 2" precision | 04f9e582 | L |
| FN-08 | keyword args must appear in parameter order | any order works | 63dfadd7, 23a1ecd0 | H |
| FN-09 | one positional arg fills the matching-named/default params | positional binding | 64436489, 2cc0633d | H |
| FN-10 | a default param may precede a non-default one | → SyntaxError | cffda9eb, 3b078c3f | M |
| FN-11 | `def` is hoisted (call before definition works) | → NameError | 010a8c96 | M |
| FN-12 | misspelled/undefined names resolve to the "obvious" one | → NameError | 3c3b04be, 0aa6b986 | M |
| FN-13 | `+` concatenation inserts a space | `HelloAnjali` distractors, pervasive | 567e76d6, 3b078c3f | L |
| FN-14 | args bind to outer variable NAMES, not positions | shadowing + swapped calls | 6efe8b6f, 49c2fd52 | H |
| FN-15 | `pass` returns "pass"; `print(None)` shows quotes | `def f(): pass; print(f())` | bbdbce40, aff94a6c | M |
| FN-16 | structural slips raise the wrong error class | missing colon → SyntaxError not NameError | daf198a8 | M |
| FN-17 | swapped keyword args still print in written order | binding vs write order | 23a1ecd0, d75f8479 | M |

#### Built-in Functions (s25)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| BI-01 | `min`/`max` on strings compares by length | lexicographic order | dbba32a2, e097bba2 | M |
| BI-02 | printed strings keep their quotes | `print(min([...]))` | dbba32a2 | L |
| BI-03 | `sorted()` returns unchanged / sorts by absolute value | negatives | 81086ae2 | M |
| BI-04 | `sorted()` deduplicates | duplicates survive | c1d0938a | M |
| BI-05 | descending sort of negatives puts most-negative first | reverse=True on negatives | 8e49024c | M |
| BI-06 | `sum()` ignores negatives / flips signs | mixed-sign sums | 7fa39651, cd437167 | M |
| BI-07 | unfamiliar-but-valid calls are SyntaxError | multi-arg min, nested calls (dead filler — see DROP) | 32772b13 | L |
| BI-08 | `list + list` nests / follows definition order | call-order concat | 74169460, 3a9c1740 | M |
| BI-09 | in-place `+=` on a list param doesn't reach the caller | double-call growth | 86ad87d3, a4ba1c34 | H |

#### List Methods and Tuples (s26–27)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| LT-01 | `sort()` returns a new list / `sorted()` sorts in place | `l1.sort()` vs `sorted(l2)` | ad7faaef | H |
| LT-02 | sorting deduplicates or truncates | full list survives | f6093919, 99e44992 | M |
| LT-03 | sort is partial/stops early | prefix-sorted distractors | f6093919 | L |
| LT-04 | `remove(x)` removes all occurrences | first occurrence only | 1a512a3a, 31d5aede | H |
| LT-05 | remove takes an index; missing value is TypeError; pop out-of-range is TypeError | ValueError vs IndexError discrimination | 9afe7a5a, 7dd91210 | M |
| LT-06 | `pop()` removes the first element / clears | last by default | 81b91b06, 002a54ed | M |
| LT-07 | `insert(i, x)` replaces at i / appends | inserts before | a7159d13, af8e4f7c | H |
| LT-08 | `append(seq)` merges / `extend` nests | append nests, extend flattens | 7d62385d, 8338ba26 | H |
| LT-09 | extend/concat prepends | order preserved | 8338ba26, ebbb4a63 | L |
| LT-10 | `index()` is 1-based / returns the element | returns 0-based position | 44e4c304, f5a93eb7 | M |
| LT-11 | tuples support item assignment | → TypeError | e77cc3b0, 056af026 | H |
| LT-12 | `(1)` is a one-element tuple | `(1,)` needs the comma | 4df88a90, e1e84371 | M |
| LT-13 | unpacking pads/truncates to fit | → ValueError: not enough values | d619fe6e, c5adea3f | M |
| LT-14 | `return a, b` returns only the first | tuple return + unpack | 63fa995e | M |
| LT-15 | read ops fail on tuples like mutation does | `len(tuple)` fine | 127dc2fc | L |

#### Sets and Set Operations (s28–29)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| SE-01 | `{}` creates an empty set | it's a dict; `set()` prints `set()` | b26ff057, 1ba89ba0 | M |
| SE-02 | sets keep duplicates | dedup on creation/update | 612bb8ce, a4c65d88 | H |
| SE-03 | set print order is predictable | correct: "All the given options" / cannot be guaranteed | 1764b2cd, bb0de8ff | M |
| SE-04 | sets support indexing | `set_a[1]` → TypeError not subscriptable | 3663a907, d3ecff30 | M |
| SE-05 | sets are immutable (add errors) | `add()` works | e01a9f28 | M |
| SE-06 | `remove()` on missing is a no-op | → KeyError; discard is the no-op | 75c36c9e, fb079c14 | H |
| SE-07 | `discard()` raises like `remove()` | discard/remove minimal pair | 3557c9e6, 6d229962 | M |
| SE-08 | set methods require set operands | `union(list)` works | fff8b3ea, a85304d2 | M |
| SE-09 | `update()` takes scalars | needs an iterable | 2633a7b4, 4df66537 | M |
| SE-10 | lists can be set elements | → TypeError unhashable | 1519b729, 0b892bd8 | M |
| SE-11 | `set("apple")` gives `{'apple'}` | char dedup: {'a','p','l','e'} | 5b3dbaea, f7dcc9a6 | M |
| SE-12 | operator meanings scrambled (`|`=common, `^`=union…) | set-operator semantics | 54192b14, 1fc55342 | H |
| SE-13 | difference is symmetric | `a - b ≠ b - a` | af8e7fd0 | H |
| SE-14 | `issubset` direction confusion | receiver vs argument | 26676e15, c166257b | M |
| SE-15 | `clear()` copies / checks emptiness | empties the set | d04a3eef | L |
| SE-16 | iterating a set is membership-checking | plain iteration | bd5dece1, adf99d08 | L |

#### Dictionaries (s30–31)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| DI-01 | `dict[missing]` returns None/0/the key | → KeyError | df3f0e22, 8c09636a | H |
| DI-02 | `dict.get(missing)` raises like `[]` | returns None — the []/get minimal pair | 2f282b7f, d13d8c8b | H |
| DI-03 | assigning to a new key raises | it inserts | 2c8db1b4 | H |
| DI-04 | error position ignored in mixed []/get code | first failing line wins | 8c09636a | M |
| DI-05 | deleting keys while iterating works | → RuntimeError: changed size | 58ee0865, 422e7ba7 | M |
| DI-06 | `dict_b = dict_a` copies | aliasing (same for lists into functions) | 422e7ba7, 8c70040c | H |
| DI-07 | `keys()`/`values()` return static lists | dynamic view objects | d8e89e00, 36852b5d | M |
| DI-08 | `**kwargs` restricts/rejects keyword args | collects into a dict | 43be8780, a313b0da | H |
| DI-09 | `kwargs['absent']` returns None | → KeyError | e3337e77, 16b273f4 | H |
| DI-10 | iterating a dict yields (key, value) pairs | keys only; use .items() | be07f960 | M |
| DI-11 | `f(**data)` maps by position | keys must match param names → TypeError | 86d62b16 | M |
| DI-12 | `*args` prints as a tuple even when iterated | element-wise vs container | b3399bba | M |
| DI-13 | `*tuple` unpacking pads missing params | → TypeError | aa9f5bc9 | M |
| DI-14 | anything can be a dict key | unhashable → TypeError | 85574600, 7a547c39 | M |
| DI-15 | dicts don't preserve insertion order | they do (3.7+) | fdf3b054 | L |
| DI-16 | `in` on a dict searches values | keys only | 4b76d8f8 | M |
| DI-17 | `len(dict)` counts keys+values | pairs count | f369dea9 | L |

#### Python Standard Library (s32)

| id | wrong belief | trap | evidence | sev |
|---|---|---|---|---|
| SL-01 | module attributes are case-insensitive / near-spellings resolve | `math.Pi`, `factoral` → AttributeError | 7c344dec, e4b8f417 | M |
| SL-02 | `random.randint(10)` works with one arg | needs two | d9e0d013, bba37482 | M |
| SL-03 | `randint` picks from a list (choice conflation) | randint vs choice | ec7166bf, 7598b4a4 | M |
| SL-04 | `map`/`filter` return lists directly | need `list()` wrapping | f3f031c0, 413393c7 | M |
| SL-05 | `filter` returns the rejected items | predicate keeps | 413393c7, 9f1201a1 | M |
| SL-06 | `round()` defaults to 2 decimal places | rounds to int | 3c1045bf | M |
| SL-07 | `reduce` returns the running partials | single value | 796f7e2a, a1d7a41d | M |
| SL-08 | `from m import f` vs `import m` namespace confusion | alias kills the original name → NameError | e248cc4e, 4fde38cd | M |

#### Conceptual layer (objective-only; no coding artifact can test these)

28 additional misconceptions (OBJ-M01–M28) live in the objective corpus: identifier
case-sensitivity beliefs, other-language forms (`printf`, `charAt`), quotes-as-decoration,
`=` direction, naming rules & snake_case, keyword identity, indentation-as-cosmetic,
error-class vocabulary, `"True"`-vs-`True`-vs-`true`, string immutability, `range`/`randint`
interval beliefs, loop-keyword swaps, function hoisting, `*args`/`**kwargs` containers,
sort-in-place vs sorted-new, pass-by-reference, set orderedness/hashability, dict views &
key eligibility, tuple `(1,)`, import-alias namespaces, module/syntax/software definitions,
`split()` whitespace handling, and `min`/`max`-by-length. **These are the evidence-flag
candidates for the registry**: the areas only the objective bank can prove — definitional
layer, naming conventions, keyword identity, error-class vocabulary, API-form recall,
semantic-equivalence judgment, nondeterministic-API contracts, memory/aliasing beliefs
(direct probe), problem-statement literacy (story→technical), and plan-level sequencing
(REARRANGE pseudo-code).

### 3.4 Confirmed coverage gaps (zero corpus items — adopt-new content)

Highest-value first; each is a misconception the course outcome implies but the bank never tests:

1. **`str + int` TypeError inside a loop** (`print("Count: " + i)`) — the single most common
   real beginner runtime error; zero items across 4,963.
2. **A firing str-vs-int `input()` comparison trap** (`'9' > '10'` → True) and `int(input())`
   omission leading to TypeError — the existing input-comparison family never discriminates (§5).
3. **`while` + `continue` skipping the increment** (the classic infinite-loop trap) — zero items.
4. **Nested loops with `break`/`continue`; 3-arg `range()`** incl. `range(10, 2)` → zero
   iterations — the Read axis's R7 rung doesn't exist yet.
5. **`x = lst.sort(); print(x)` → None** — the canonical sort-returns-None trap, only indirect.
6. **`tuple.append(...)` → AttributeError**; `dict.get(key, default)` two-arg form;
   `setdefault`/`popitem`/`fromkeys`/`dict.pop`.
7. **Copy idioms as aliasing-defeaters** (`.copy()`, `list(a)`, `a[:]`) — rebind-vs-mutate is
   tested, the fix never is. Pairs with **`is` vs `==`** (zero items).
8. **`chr(ord(c) + k)` arithmetic** — the scaffold line makes this the natural next rung.
9. **Slice assignment / `del`** — absent entirely.
10. **Traceback-reading items** (given real error output, locate cause/line) — only
    name-the-exception exists today; natural Fix-axis rung.
11. **Mutable default arguments** (`def f(x=[])` *called without* the arg).
12. **`"12.34".isdigit()`/`"".isdigit()`**; negative indexing on nested lists; `[::-1]` as a
    tested fact (currently only a distractor); multi-error precedence ("which error fires
    first"); `//` and `%` semantics; comments; f-strings; infinite-loop *recognition* as a
    concept; `==` vs `is`; interpreter-vs-compiler (objective layer).

---

## 4. Known corpus defects — do-not-port list

Execution-verified defects. If any old item is used as a reference or coverage floor, exclude these:

| item(s) | defect |
|---|---|
| CODING `97c09aca` | reference solution fails its own test suite (`500:3` vs `500: 3`) |
| CODING `8abc00b5` | LeetCode-Hard text justification (50-line solution) — out of band for this course; quote chars load-bearing in I/O |
| CODING `250fd05b` | LCM defined as "smallest positive factor" in the stem; inconsistent trailing newlines in its own suite |
| CODING `bceb669e` | nondeterministic (`random.choice`) graded by literal match — implies an undisclosed checker |
| CODING `259699fc` | float-repr equality grading (`4.666666666666667`) |
| CODING `d546e58d` | solution sorts numeric tokens as strings; suite avoids the inputs that would expose it |
| CODING 15 items (incl. `4ef7f535`, `59b640d6`, `33a6c19f`) | expected outputs depend on trailing whitespace (pass only under grader rstrip) |
| CODING 14 items (incl. `78c994fd`, `fdca9d93`, `89a49c8f`) | single-visible-TC / zero-hidden — hardcoding the sample scores 100% |
| FIB `bfc23733`, `edfe78de` | stored answer provably wrong (executed) |
| FIB `7dc8ccfc`, `55254a23` | snippet references undefined names — broken even when filled correctly |
| FIB `4c37462d` | instruction/code mismatch + `strip`/`lstrip` both valid |
| CA `22657adf`, `cb12bc20`, `076ba87c`, `68661890` | keyed "SyntaxError" — real behavior is runtime TypeError (verified) |
| CA `0a6d1ec2` family | `range[3]` labeled "Syntax error" — actually TypeError at runtime |
| CA `40bbf033`, `559fc447`, `8397c6d2`, `ccdd6b54` | input-comparison trap never fires (str/int orders agree for all chosen inputs) |
| CA `9c88b195`, `b58d7a25` | correct option wrapped in quotes — contradicts the quotes-don't-print lesson |
| CA `fff8b3ea` vs `94060845` | identical set-print code keyed with two different orders (hash-randomization landmine); ~5 strictly nondeterministic set items |
| CA `9243b0e2`, `844f4234`, `c8e1b568` | unreachable numeric filler distractors |
| CA `6eba1009` | environment-dependent `help()` output |
| OBJ `dd9b85e3` | distractor "order of keys is guaranteed" is TRUE since 3.7 — double-keyable |
| OBJ `e13d23f9` | keys `Print` as a *syntax* error (it's a NameError) |
| OBJ `ff5fc295`, `997df8a2`, `f0a5f98a`, `738fb805`, `37fb19bc` | double-keyable options / broken grammar / coin-flip 2-option items |
| OBJ (9 items, s1/s4) | "Is this a valid statement?" double-negation Yes/No frame |

---

## 5. Connection to the WHAT rail (registry) and delivery

- **Cell-directed generation:** Forge's work order is a cell — (node × level × axis × role).
  Items are born tagged; no retro-classification ever happens. This doc governs HOW the item
  filling that cell is written; the registry (authored from the Course Outline's key
  takeaways and outcome statements, in the React exemplar's schema) governs WHAT cells exist.
- **Misconception→node mapping:** bank entries above are grouped by module/session — when the
  registry lands, each misconception maps to its node(s); hard-rung items compose a primary
  node with `Depends_On` ancestors (interleaving is a bank constraint, not just a teaching one).
- **Evidence flags:** the conceptual-layer list (§3.3 end) marks node areas needing
  objective-bank proof; error-class vocabulary and equivalence judgment cannot be proven by
  test-case-graded code.
- **Pool sizing per adaptive session unit:** with retry + step-up guarantees, ≥3 fresh items
  per node × rung × axis; ~40–60 reviewed coding items per session (not 12).
- **Packaging:** the adaptive unit ships as a `coding_practice_unit` with adaptive internals;
  difficulty vocabulary easy/medium/hard is the platform's own scale.
- **Coverage floor:** the old bank's surface (the inventory in §1.1) is the never-narrower
  floor; the registry blueprint defines full coverage. The do-not-port list (§4) excludes
  defective floor entries. Module Quiz units are repurposed classroom-quiz/coding items —
  not part of the floor.
- **Item contract additions (owner-confirmed 2026-07-07):** every coding item ships with a
  step-by-step **tutorial** (Understand → Write incrementally → Show result, the platform's
  Tutorial-tab format); every objective item ships with an **explanation** (commented code +
  bullet walkthrough, the platform's explanation-modal format). Both are Forge outputs, both
  pass through the same review gate.
- **Delivery constraints that shape generation:** (1) the player reveals the correct answer
  after a wrong attempt — items are single-use, so retry/step-down requires fresh variants
  (≥3 per cell); (2) **Public Submissions expose accepted solutions** — novelty/rebuild
  cadence is real; (3) the read-only code pane cannot disable lint markers — until the portal
  supports it, avoid statically-lintable bugs (undefined-name style) as the ANSWER of
  delivered error-prediction items; prefer runtime-only errors.

---

## Provenance

Derived 2026-07-06 from: `question_details_json_with_coding_question_content.json` (4,963
questions, 188 units), `Computer Programming using Python Course Contents - Course Outline.csv`
(32 sessions), `…Session-Practice Content Linked Unit Ids.csv` (session–unit map), `Central
Stack Catalogue - Stack.csv` (course outcome), and seven parallel mining analyses (CODING,
FIB_CODING, CODE_ANALYSIS ×4 module groups, objective) with execution verification.
Companion documents: "Open ACP — Pedagogy Intelligence" (E-series eval set, session flows)
and "Open ACP — Canonical Product Context (All Products)".
