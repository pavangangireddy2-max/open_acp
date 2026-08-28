"""Reward regression against the verified gold set.

Runs the environment's reward logic over the 340 human-authored, verified CODING
questions (data/gold_coding.json). A well-calibrated reward should ACCEPT the
vast majority: verified questions are self-consistent and non-trivial by
construction, so `solvable` should be ~1.0 and `non_trivial` should reject only
the degenerate warmup problems.

Usage: python scripts/gold_regression.py [limit]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from coding_question_craft import (  # noqa: E402
    _distinct_expected, _edge_inputs, run_reference,
)

GOLD = Path(__file__).resolve().parents[1] / "data" / "gold_coding.json"


def main() -> None:
    gold = json.loads(GOLD.read_text())
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(gold)
    gold = gold[:limit]

    solvable = non_trivial = has_edge = 0
    trivial_hits = 0
    partial = []
    for g in gold:
        r = run_reference(g)
        ok = r["total"] > 0 and r["passed"] == r["total"] and r["error"] is None
        solvable += ok
        de = _distinct_expected(g["tests"])
        if ok and r["trivial_solved"] == 0 and de >= 2:
            non_trivial += 1
        if r["trivial_solved"]:
            trivial_hits += 1
        if _edge_inputs(g["tests"]) >= 1:
            has_edge += 1
        if not ok:
            partial.append((g["question_id"], g["topic"], r["passed"], r["total"], r["error"]))

    n = len(gold)
    print(f"gold questions evaluated: {n}\n")
    print(f"solvable (ref passes all its own tests): {solvable}/{n} = {solvable/n:.0%}")
    print(f"accepted by non_trivial guard:           {non_trivial}/{n} = {non_trivial/n:.0%}")
    print(f"flagged trivial (const/echo/empty):      {trivial_hits}/{n} = {trivial_hits/n:.0%}")
    print(f"has >=1 edge input:                      {has_edge}/{n} = {has_edge/n:.0%}")
    if partial:
        print(f"\nnot fully self-consistent under our runner ({len(partial)}), first 10:")
        for qid, topic, p, t, err in partial[:10]:
            print(f"  {qid[:8]} {topic[:28]:28} {p}/{t}  {str(err)[:60]}")


if __name__ == "__main__":
    main()
