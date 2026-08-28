"""Baseline eval for coding_question_craft, in-process, local subprocess runtime,
against OpenRouter. Writes summary + generated questions to
outputs/eval/cqc_baseline.json.
"""
import asyncio, json, os
from pathlib import Path


def _load_dotenv(path=".env"):
    """Populate os.environ from a .env file (verifiers resolves keys from the
    process environment; nothing auto-loads .env)."""
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()

from verifiers.v1.cli.eval.runner import run_eval
from verifiers.v1.cli.resolve import narrow_config, with_positional_taskset
from verifiers.v1.configs.cli.eval import EvalConfig

N = int(os.environ.get("CQC_N", "3"))
MODEL = os.environ.get("CQC_MODEL", "openai/gpt-4.1-mini")
CLIENT = {"type": "eval",
          "base_url": "https://openrouter.ai/api/v1",
          "api_key_var": "OPENROUTER_API_KEY"}
SAMPLING = {"max_tokens": 4000, "temperature": 0.7}

# Narrow EvalConfig so the env.agent (harness/runtime) subtree exists.
CfgT = narrow_config(EvalConfig, with_positional_taskset(["coding_question_craft"]))
cfg = CfgT.model_validate({
    "env": {
        "taskset": {"id": "coding_question_craft", "num_tasks": N},
        "agent": {
            "runtime": {"type": "subprocess"},   # run harness locally, no cloud sandbox
            "model": MODEL, "client": CLIENT, "sampling": SAMPLING,
            "max_turns": 1,
        },
    },
    "model": MODEL, "client": CLIENT, "sampling": SAMPLING,
    "num_tasks": N, "num_rollouts": 1, "max_concurrent": min(N, 8),
    "rich": None, "serve": None,
})


def _num(v):
    return v.value if hasattr(v, "value") else v


def _flatten(m):
    return {k: _num(v) for k, v in dict(m or {}).items()}


async def main():
    episodes = await run_eval(cfg)
    rows = []
    for ep in episodes:
        for tr in ep.traces:
            data = tr.task.data if tr.task else None
            rows.append({
                "topic": getattr(data, "topic", None),
                "difficulty": getattr(data, "difficulty", None),
                "reward": _num(tr.reward),
                "metrics": _flatten(getattr(tr, "metrics", {})),
                "rewards": _flatten(getattr(tr, "rewards", {})),
                "has_error": tr.has_error,
                "last_error": str(tr.last_error)[:400] if tr.has_error else None,
                "reply": (tr.last_reply or "")[:12000],
            })
    out = Path("outputs/eval/cqc_baseline.json"); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"n": len(rows), "rows": rows}, indent=2))
    print(f"DONE episodes={len(episodes)} rows={len(rows)} -> {out}")


if __name__ == "__main__":
    asyncio.run(main())
