"""Materialize the synthetic spec dataset to JSONL for inspection.

Usage: python scripts/gen_dataset.py [n] [seed] > data/specs.jsonl
The taskset generates the same specs at load() time; this is just for eyeballing.
"""

import json
import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))
from coding_question_craft import build_specs  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
for spec in build_specs(n, seed):
    print(json.dumps(spec))
