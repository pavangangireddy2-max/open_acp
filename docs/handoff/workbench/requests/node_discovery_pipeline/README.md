# Node-discovery pipeline — process validation package (for DE)

> The runnable, end-to-end version of the analysis behind the node proposals and the SME
> validation instrument. Purpose: let the DE re-derive every number independently and
> challenge the method, not just the outputs. One script, four stages, all constants
> visible at the top of `node_discovery.py`. 2026-07-15.

## What produced what

```
pilot_extract.csv  (542,021 first-attempt rows — you produced this)
   │  stage: pairs        co-failure stats per item pair (phi, lift, cells)
   ▼
pairs.csv.gz       144,171 pairs (n_both ≥ 50)
   │  stage: communities  robust filter → average-linkage clustering per session
   ▼
communities.json   42 communities / 174 items across s11–s15
   │  [JUDGMENT LAYER — not algorithmic]  content adjudication: community → node,
   │  item-level moves where a community mixed skills (recorded, flagged, SME-validated)
   ▼
node_sme_validation_s11_s15.csv   (workbench/reviews/ — the instrument the SME reviews)
```

The pipeline validates the two algorithmic stages and *derives* the judgment layer from
the committed instrument so you can see exactly where human calls were made
(`community_node_map.csv`: baseline node per community + item overrides).

## Run it

```bash
cd docs/handoff/workbench/requests/node_discovery_pipeline
python3 node_discovery.py --stage all --extract /path/to/pilot_extract.csv --outdir ./out
```

Deps: `pandas numpy scipy`. Runtime ≈ 1 min. `--stage pairs|communities|verify-de|verify-instrument`
run individually (later stages read the earlier stage's output from `--outdir`).
`pilot_extract.csv` is deliberately not committed — use your copy (also at
`workbench/requests/pilot_extract.csv` on this machine).

## Expected checkpoints (actual output, 2026-07-15 run)

```
[pairs] extract rows=542,021 users=4,812 items=584
[pairs] CHECK n_both>=150 (all pairs): 71,891   (= your co_failure_pairs.csv row count)
[pairs] CHECK robust within-session: 670
[pairs] CHECK robust cross-session:  163
[communities] Conditional Statements: 351 robust / 105 items -> 17 communities (75 items)
[communities] Nested Conditional Statements: 44 / 52 -> 7 (24)
[communities] Loops: 133 / 64 -> 11 (38)
[communities] For Loop: 135 / 42 -> 5 (31)
[communities] Understanding Coding Question Formats: 7 / 11 -> 2 (6)
[communities] CHECK total: 42 communities / 174 items
[verify-de] CHECK max |Δphi| = 9.97e-17 · |Δlift| = 1.78e-15 · |Δn_both| = 0
[verify-instrument] CHECK community membership vs CSV (42 communities): MATCH
```

## Method constants (decided in review_cofailure_pilot.md, addendum 2)

| constant | value | why |
|---|---|---|
| fail | `first_attempt_result != "CORRECT"` | PARTIALLY_CORRECT (3 rows) counts as fail |
| within-session pair floor | n_both ≥ 150 | phi unstable below |
| cross-session pair floor | n_both ≥ 300 | stricter: cross pairs carry ability confound |
| association floor | phi ≥ 0.2 | rank by phi, never lift (lift explodes on rare items) |
| both-fail cell | ≥ 10 | kills 2-learner "lift 16" artifacts |
| distance | 1 − phi; non-robust pairs = 1.0 | conservative: unproven ≠ close |
| clustering | average linkage, cut t = 0.92 | communities = groups ≥ 3 items |

## Known nuances (read before challenging)

1. **C-numbers are identifiers, not ordering claims.** They were assigned at the first run
   (insertion order among equal-size communities) and are preserved in the committed CSV.
   The re-run reproduces identical membership; `verify-instrument` prints the label
   crosswalk for same-size permutations. Membership is the claim under validation.
2. **Fragmentation is intentional.** The strict pair filter makes average distances between
   same-skill communities land just above the 0.92 cut (e.g. s11 C3×C7 = 0.936). The
   judgment layer repairs this by reading content — that's why node ≠ community.
3. **`time_spent` is 100% null in the extract** — unused everywhere.
4. **No CODING items exist in the extract** (types: CA_MCQ, CA_TEXTUAL, MCQ, REARRANGE,
   FIB_CODING) — coding items are a separate lane in the full-scale spec.

## What we'd like you to challenge (the actual ask)

- Re-run all four stages; confirm every CHECK line.
- Sensitivity: sweep the cut `t ∈ {0.88, 0.90, 0.92, 0.94}` and report how community
  membership churns (we claim the big communities are stable; the 3-item tail is not).
- Alternative clustering (e.g. Leiden/graph modularity on the robust-pair graph) —
  do the same cores emerge?
- Anything about the phi/cell arithmetic in `stage_pairs` (matrix identities:
  `n_both = AᵀA`, `both_fail = FᵀF`, `fx = FᵀA`).
- Full-scale readiness: this exact pipeline is the one we intend to run on all sessions
  once the content-hash export lands (method spec v2 in the review addendum).
