#!/usr/bin/env python3
"""
Node-discovery pipeline — co-failure pairs -> robust filter -> communities -> node map.

This is the exact process behind:
  - workbench/reviews/review_cofailure_pilot.md (addendum 2: method spec v2)
  - knowledge/registries/programming_algorithms/python/node_proposals_s11_s15.md
  - workbench/reviews/node_sme_validation_s11_s15.{csv,md} (v2)

Stages (run all, or one at a time):
  pairs              raw attempt extract -> per-pair co-failure stats (phi, lift)
  communities        robust pairs -> average-linkage communities per session
  verify-de          compare stage-1 output against the DE's co_failure_pairs.csv
  verify-instrument  compare stage-2 communities against the committed SME CSV,
                     and derive the community->node judgment layer from it

Method constants (locked in review addendum 2 — change only with a new adjudication):
  FAIL            = first_attempt_result != "CORRECT"  (PARTIALLY_CORRECT counts as fail)
  N_MIN_WITHIN    = 150   co-attempters floor for within-session pairs
  N_MIN_CROSS     = 300   co-attempters floor for cross-session pairs
  PHI_MIN         = 0.2   association floor (rank by phi, never by lift)
  CELL_MIN        = 10    both-fail cell floor (kills rare-item lift artifacts)
  LINKAGE         = average linkage on distance 1-phi; non-robust pair distance = 1.0
  CUT             = 0.92  fcluster distance threshold
  COMMUNITY_MIN   = 3     min items per reported community
  C-numbering     = communities stable-sorted by size desc (ties keep fcluster
                    label order); members sorted lexicographically

Usage:
  python3 node_discovery.py --stage all \
      --extract pilot_extract.csv --outdir ./node_discovery_out
"""
import argparse, json, os, sys
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

N_MIN_WITHIN, N_MIN_CROSS, PHI_MIN, CELL_MIN = 150, 300, 0.2, 10
CUT, COMMUNITY_MIN = 0.92, 3
PAIR_EXPORT_FLOOR = 50  # keep the pair table small; all validation happens >= 150


# ---------------------------------------------------------------- stage: pairs
def stage_pairs(extract_path, outdir):
    raw = pd.read_csv(extract_path)
    print(f"[pairs] extract rows={len(raw):,} users={raw.user_id.nunique():,} "
          f"items={raw.question_id.nunique():,}")
    print(f"[pairs] first_attempt_result: {raw.first_attempt_result.value_counts().to_dict()}")

    raw = raw.assign(failed=raw.first_attempt_result.ne("CORRECT").astype(np.int32))
    # one row per user x question (extract is already first-attempt level; 'first' = no-op guard)
    piv = raw.pivot_table(index="user_id", columns="question_id", values="failed", aggfunc="first")
    A = (~piv.isna()).values.astype(np.int32)        # attempted
    F = piv.fillna(0).values.astype(np.int32)        # failed
    items = piv.columns.to_numpy()

    n_both = A.T @ A                                  # co-attempters
    both_fail = F.T @ F                               # a-cell: failed both
    fail_tot = F.sum(axis=0)                          # per-item fails among all attempters

    # per-pair contingency restricted to co-attempters:
    #   fx = failed x among co-attempters of (x,y) = F_x^T A_y
    FA = F.T @ A                                      # FA[i,j] = failed i among attempters of j
    iu, ju = np.triu_indices(len(items), k=1)
    n = n_both[iu, ju].astype(np.float64)
    a = both_fail[iu, ju].astype(np.float64)
    fx = FA[iu, ju].astype(np.float64)                # failed x among co-attempters
    fy = FA[ju, iu].astype(np.float64)
    b, c = fx - a, fy - a
    d = n - a - b - c
    with np.errstate(divide="ignore", invalid="ignore"):
        phi = (a * d - b * c) / np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
        p_x, p_y, p_both = fx / n, fy / n, a / n
        lift = p_both / (p_x * p_y)

    sess = raw.groupby("question_id").session_title.first()
    keep = n >= PAIR_EXPORT_FLOOR
    pairs = pd.DataFrame({
        "item_x": items[iu][keep], "item_y": items[ju][keep],
        "n_both": n[keep].astype(int), "both_fail": a[keep].astype(int),
        "p_fail_x": p_x[keep], "p_fail_y": p_y[keep], "p_fail_both": p_both[keep],
        "lift": lift[keep], "phi": phi[keep],
    })
    pairs["session_x"] = pairs.item_x.map(sess)
    pairs["session_y"] = pairs.item_y.map(sess)

    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "pairs.csv.gz")
    pairs.to_csv(out, index=False)

    w = pairs[(pairs.session_x == pairs.session_y) & (pairs.n_both >= N_MIN_WITHIN)]
    rob_w = w[(w.phi >= PHI_MIN) & (w.both_fail >= CELL_MIN)]
    x = pairs[(pairs.session_x != pairs.session_y) & (pairs.n_both >= N_MIN_CROSS)]
    rob_x = x[(x.phi >= PHI_MIN) & (x.both_fail >= CELL_MIN)]
    print(f"[pairs] exported {len(pairs):,} pairs (n_both>={PAIR_EXPORT_FLOOR}) -> {out}")
    print(f"[pairs] CHECK n_both>={N_MIN_WITHIN} (all pairs): "
          f"{(pairs.n_both >= N_MIN_WITHIN).sum():,}  (DE delivery: 71,891)")
    print(f"[pairs] CHECK robust within-session: {len(rob_w)}  (expected: 670)")
    print(f"[pairs] CHECK robust cross-session:  {len(rob_x)}  (expected: 163)")
    return pairs


# ---------------------------------------------------------- stage: communities
def stage_communities(pairs, outdir):
    out = {}
    for s in sorted(pairs.session_x.dropna().unique()):
        w = pairs[(pairs.session_x == s) & (pairs.session_y == s) & (pairs.n_both >= N_MIN_WITHIN)]
        rob = w[(w.phi >= PHI_MIN) & (w.both_fail >= CELL_MIN)]
        if rob.empty:
            out[s] = []
            continue
        items = pd.unique(rob[["item_x", "item_y"]].values.ravel())  # appearance order
        idx = {q: i for i, q in enumerate(items)}
        D = np.ones((len(items), len(items)))
        np.fill_diagonal(D, 0.0)
        for r in rob.itertuples():
            i, j = idx[r.item_x], idx[r.item_y]
            D[i, j] = D[j, i] = 1 - r.phi
        labels = fcluster(linkage(squareform(D), "average"), t=CUT, criterion="distance")
        groups = {}
        for q, l in zip(items, labels):
            groups.setdefault(l, []).append(q)
        comms = [sorted(g) for l, g in sorted(groups.items()) if len(g) >= COMMUNITY_MIN]
        comms.sort(key=len, reverse=True)             # stable: ties keep label order
        out[s] = comms
        print(f"[communities] {s}: {len(w)} pairs@N>={N_MIN_WITHIN} -> {len(rob)} robust "
              f"over {len(items)} items -> {len(comms)} communities "
              f"({sum(len(c) for c in comms)} items) sizes={[len(c) for c in comms]}")
    path = os.path.join(outdir, "communities.json")
    json.dump(out, open(path, "w"), indent=1)
    tot_c = sum(len(v) for v in out.values())
    tot_i = sum(len(c) for v in out.values() for c in v)
    print(f"[communities] CHECK total: {tot_c} communities / {tot_i} items "
          f"(expected: 42 / 174) -> {path}")
    return out


# ------------------------------------------------------------ stage: verify-de
def stage_verify_de(pairs, de_path):
    de = pd.read_csv(de_path)
    key = ["item_x", "item_y"]
    mine = pairs.rename(columns={"n_both": "n_both_attempted"})
    m = de.merge(mine, on=key, suffixes=("_de", "_mine"))
    # DE may have the opposite orientation for some pairs
    flipped = de.merge(
        mine.rename(columns={"item_x": "item_y", "item_y": "item_x",
                             "p_fail_x": "p_fail_y", "p_fail_y": "p_fail_x"}),
        on=key, suffixes=("_de", "_mine"))
    m = pd.concat([m, flipped]).drop_duplicates(subset=key)
    print(f"[verify-de] DE rows={len(de):,} matched={len(m):,}")
    for col in ["phi", "lift", "p_fail_both"]:
        diff = (m[f"{col}_de"] - m[f"{col}_mine"]).abs().max()
        print(f"[verify-de] CHECK max |Δ{col}| = {diff:.2e}  (expected < 1e-12)")
    nd = (m.n_both_attempted_de - m.n_both_attempted_mine).abs().max()
    print(f"[verify-de] CHECK max |Δn_both| = {nd}  (expected 0)")


# ---------------------------------------------------- stage: verify-instrument
def stage_verify_instrument(comms, instrument_path, outdir):
    """Membership (set of item-sets) is the claim under validation and must match
    exactly. C-numbers are identifiers assigned at the first run and preserved in
    the CSV; among equal-size communities their order is arbitrary, so labels are
    reconciled via a crosswalk, not required to coincide."""
    inst = pd.read_csv(instrument_path, dtype=str).fillna("")
    ok = True
    for s, clist in comms.items():
        sub = inst[inst.session_title == s]
        mine = {frozenset(c): f"C{i+1}" for i, c in enumerate(clist)}
        theirs = {frozenset(g.question_id): c for c, g in sub.groupby("community")}
        if set(mine) != set(theirs):
            ok = False
            for f in set(mine) ^ set(theirs):
                src = "computed-only" if f in mine else "csv-only"
                print(f"[verify-instrument] MEMBERSHIP MISMATCH {s} ({src}): "
                      f"{sorted(q[:8] for q in f)}")
            continue
        xwalk = [(mine[f], theirs[f]) for f in mine if mine[f] != theirs[f]]
        if xwalk:
            pretty = ", ".join(f"{a}->{b}" for a, b in sorted(xwalk))
            print(f"[verify-instrument] {s}: membership identical; "
                  f"label crosswalk (computed->csv): {pretty}")
    print(f"[verify-instrument] CHECK community membership vs CSV (42 communities): "
          f"{'MATCH' if ok else 'MISMATCH'}")

    # derive the judgment layer: baseline node per community + item overrides
    rows = []
    for (s, c), g in inst.groupby(["session_title", "community"]):
        base = g.proposed_node.mode()[0]
        ov = "; ".join(f"{r.question_id[:8]}→{r.proposed_node}"
                       for r in g.itertuples() if r.proposed_node != base)
        rows.append({"session_title": s, "community": c, "baseline_node": base,
                     "n_items": len(g), "item_overrides": ov})
    path = os.path.join(outdir, "community_node_map.csv")
    pd.DataFrame(rows).sort_values(["session_title", "community"]).to_csv(path, index=False)
    print(f"[verify-instrument] community->node judgment layer -> {path}")
    cov = inst.groupby(["session", "proposed_node"]).size()
    print(f"[verify-instrument] instrument coverage:\n{cov.to_string()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--stage", default="all",
                    choices=["all", "pairs", "communities", "verify-de", "verify-instrument"])
    ap.add_argument("--extract", default=os.path.join(here, "..", "pilot_extract.csv"))
    ap.add_argument("--de-pairs", default=os.path.join(here, "..", "cofailure check - share content",
                                                       "output", "co_failure_pairs.csv"))
    ap.add_argument("--instrument", default=os.path.join(here, "..", "..", "reviews",
                                                         "node_sme_validation_s11_s15.csv"))
    ap.add_argument("--outdir", default="./node_discovery_out")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    pairs = comms = None
    pairs_cache = os.path.join(args.outdir, "pairs.csv.gz")
    comms_cache = os.path.join(args.outdir, "communities.json")
    if args.stage in ("all", "pairs"):
        pairs = stage_pairs(args.extract, args.outdir)
    if args.stage in ("all", "communities", "verify-de", "verify-instrument") and pairs is None:
        if not os.path.exists(pairs_cache):
            sys.exit("run --stage pairs first (pairs.csv.gz missing)")
        pairs = pd.read_csv(pairs_cache)
    if args.stage in ("all", "communities"):
        comms = stage_communities(pairs, args.outdir)
    if args.stage == "verify-instrument" and comms is None:
        comms = json.load(open(comms_cache))
    if args.stage in ("all", "verify-de"):
        stage_verify_de(pairs, args.de_pairs)
    if args.stage in ("all", "verify-instrument"):
        stage_verify_instrument(comms, args.instrument, args.outdir)


if __name__ == "__main__":
    main()
