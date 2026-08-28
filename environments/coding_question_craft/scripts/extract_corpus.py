"""Extract the verified programming_algorithms corpus into bundled data assets.

Reads the human-authored, verified question bank and writes three files into the
package's data/ dir, which the environment loads at runtime:

  data/taxonomy.json   - topic frequencies + observed difficulties (spec grounding)
  data/gold_coding.json - 340 verified CODING questions, normalized to the
                          stdin/stdout authoring schema (reward regression set)
  data/exemplars.json  - a few verified questions, chosen ONLY from those that
                          are self-consistent + non-trivial (few-shot in prompt)

Run from anywhere:  python scripts/extract_corpus.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "knowledge/raw/corpora/programming_algorithms/python/question_details.json"
OUT = Path(__file__).resolve().parents[1] / "data"


def norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in (s or "").strip().splitlines())


def default_ref(q: dict) -> str | None:
    for c in q.get("codes") or []:
        if c.get("default_code") and c.get("code_content"):
            return c["code_content"]
    # fall back to any python code
    for c in q.get("codes") or []:
        if c.get("code_content"):
            return c["code_content"]
    return None


def normalize(q: dict) -> dict | None:
    ref = default_ref(q)
    tcs = q.get("test_cases") or []
    if not ref or not tcs:
        return None
    tests = [{"input": t.get("input", ""), "expected": t.get("output", "")} for t in tcs]
    return {
        "question_id": q.get("question_id"),
        "topic": q.get("topic_name"),
        "difficulty": (q.get("difficulty") or "").upper() or None,
        "statement": q.get("content", ""),
        "reference_solution": ref,
        "tests": tests,
    }


def run_ref(prog: str, tests: list[dict], timeout: float = 6.0) -> tuple[int, bool]:
    """Returns (passed, const_baseline_solves_all)."""
    passed = 0
    for t in tests:
        try:
            p = subprocess.run(
                [sys.executable, "-I", "-c", prog],
                input=t["input"], capture_output=True, text=True, timeout=timeout,
            )
            if norm(p.stdout) == norm(t["expected"]):
                passed += 1
        except Exception:
            pass
    first = tests[0]["expected"]
    const_solves = all(norm(t["expected"]) == norm(first) for t in tests)
    return passed, const_solves


def main() -> None:
    data = json.loads(SRC.read_text())
    coding = [
        q for unit in data
        for q in unit.get("content_data", {}).get("question_details", []) or []
        if q.get("question_type") == "CODING"
    ]
    gold = [g for g in (normalize(q) for q in coding) if g]

    # --- taxonomy: topic frequency + observed difficulties --------------------
    topic_counts = Counter(g["topic"] for g in gold if g["topic"])
    topic_diffs: dict[str, set] = {}
    for g in gold:
        if g["topic"] and g["difficulty"]:
            topic_diffs.setdefault(g["topic"], set()).add(g["difficulty"])
    taxonomy = {
        "topics": [
            {"topic": t, "count": c, "difficulties": sorted(topic_diffs.get(t, []))}
            for t, c in topic_counts.most_common()
        ]
    }

    # --- exemplars: verified self-consistent + non-trivial, compact -----------
    candidates = [
        g for g in gold
        if 3 <= len(g["tests"]) <= 6
        and len(g["reference_solution"]) <= 600
        and len(g["statement"]) <= 700
        and len({norm(t["expected"]) for t in g["tests"]}) >= 2  # not constant
    ]
    exemplars = []
    for g in candidates:
        passed, const_solves = run_ref(g["reference_solution"], g["tests"])
        if passed == len(g["tests"]) and not const_solves:
            exemplars.append(g)
        if len(exemplars) >= 2:
            break

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "taxonomy.json").write_text(json.dumps(taxonomy, indent=2))
    (OUT / "gold_coding.json").write_text(json.dumps(gold, indent=2))
    (OUT / "exemplars.json").write_text(json.dumps(exemplars, indent=2))
    print(f"gold questions: {len(gold)}")
    print(f"topics: {len(taxonomy['topics'])}  (top 5: "
          f"{[t['topic'] for t in taxonomy['topics'][:5]]})")
    print(f"exemplars chosen: {len(exemplars)} "
          f"({[e['question_id'][:8] for e in exemplars]})")
    print(f"wrote -> {OUT}")


if __name__ == "__main__":
    main()
