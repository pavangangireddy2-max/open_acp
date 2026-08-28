"""coding_question_craft — train a model to *author* programming problems.

The contract matches the verified programming_algorithms corpus: a problem is a
statement plus a **full Python program** that reads stdin and prints to stdout,
plus `tests` of the form {input: <stdin>, expected: <stdout>}. Scoring is
deterministic: we execute the model's own reference program against its own
tests in a guarded subprocess. A question scores well only if it is:

  * self-consistent  — the reference passes every test it declared;
  * non-trivial      — no cheap baseline (constant / echo / empty) passes the
                       tests, so the author cannot game reward with a degenerate
                       problem.

Edge-case coverage is tracked as a metric (not rewarded): the gold-set
regression showed verified authors don't follow any cheap edge heuristic.

Specs are grounded in the real corpus taxonomy (data/taxonomy.json) and the
authoring prompt carries verified few-shot exemplars (data/exemplars.json).
Format validity and test-count are gates, not flat reward — they saturated in
the baseline and gave no gradient.
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

from pydantic import Field

import verifiers.v1 as vf

_DATA = Path(__file__).resolve().parent / "data"


def _load_json(name: str, default):
    try:
        return json.loads((_DATA / name).read_text())
    except Exception:
        return default


# --------------------------------------------------------------------------- #
# Synthetic dataset generation — grounded in the verified corpus taxonomy.
# --------------------------------------------------------------------------- #

_TAXONOMY = _load_json("taxonomy.json", {"topics": [
    {"topic": "arrays", "count": 1}, {"topic": "strings", "count": 1},
    {"topic": "loops", "count": 1}, {"topic": "conditionals", "count": 1},
]})
_EXEMPLARS = _load_json("exemplars.json", [])

DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]
# Corpus median is 5–7 tests per question; scale the floor with difficulty.
MIN_TESTS = {"EASY": 5, "MEDIUM": 6, "HARD": 7}


def build_specs(n: int, seed: int) -> list[dict]:
    """Sample (topic, difficulty) specs. Topics are drawn from the real corpus
    frequency distribution; difficulty is cycled for training coverage since the
    corpus difficulty labels are almost entirely EASY/absent."""
    import random

    rng = random.Random(seed)
    topics = [t["topic"] for t in _TAXONOMY["topics"]]
    weights = [max(1, t.get("count", 1)) for t in _TAXONOMY["topics"]]
    specs = []
    for i in range(n):
        topic = rng.choices(topics, weights=weights, k=1)[0]
        difficulty = DIFFICULTIES[i % len(DIFFICULTIES)]
        specs.append(
            {
                "idx": i,
                "topic": topic,
                "difficulty": difficulty,
                "min_tests": MIN_TESTS[difficulty],
            }
        )
    return specs


def _exemplar_block() -> str:
    if not _EXEMPLARS:
        return ""
    ex = _EXEMPLARS[0]
    demo = {
        "title": "Number in range",
        "difficulty": "EASY",
        "topics": [ex["topic"]],
        "statement": ex["statement"],
        "reference_solution": ex["reference_solution"],
        "tests": ex["tests"],
    }
    return "\n\nHere is a verified example in exactly the required format:\n```json\n" \
        + json.dumps(demo, indent=2) + "\n```"


INSTRUCTIONS = dedent(
    """\
    You are a programming-problem author for an introductory Python course.
    Create ONE original coding problem that meets the spec below.

    Spec:
    - Topic: {topic}
    - Difficulty: {difficulty}
    - Provide at least {min_tests} test cases (include edge cases).

    The problem uses standard input / standard output: the solution reads from
    stdin and prints the answer to stdout.

    Respond with a SINGLE fenced ```json block and nothing else. Schema:
    {{
      "title": "short title",
      "difficulty": "{difficulty}",
      "topics": ["{topic}"],
      "statement": "markdown statement with clear Input and Output sections",
      "reference_solution": "a complete Python program that reads stdin and prints stdout",
      "tests": [{{"input": "<stdin text>", "expected": "<exact stdout text>"}}]
    }}

    Rules:
    - `reference_solution` is a full program using only the standard library.
    - For each test, running the program on `input` must print exactly `expected`
      (trailing whitespace is ignored). VERIFY each `expected` by mentally
      executing your program on that input.
    - The problem must be non-trivial: `expected` values must NOT all be
      identical, and simply echoing the input or printing a constant must NOT
      pass your tests.
    - Include at least one edge case (empty input, zero, a negative, or a
      boundary value).{exemplar}
    """
)


# --------------------------------------------------------------------------- #
# Sandboxed stdin/stdout execution of the reference program against its tests.
# Trivial baselines (const/echo/empty) are computed in-process — no subprocess.
# --------------------------------------------------------------------------- #


def _limit_resources():  # pragma: no cover - posix only, runs in child
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
        # Generous address-space cap: tight enough to stop a fork bomb / giant
        # allocation, loose enough that the interpreter itself always starts.
        resource.setrlimit(resource.RLIMIT_AS, (2 * 1024 * 1024 * 1024,) * 2)
    except Exception:
        pass


def _norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in (s or "").strip().splitlines())


def _empty_run(n_tests: int, error: str) -> dict:
    return {"passed": 0, "total": n_tests, "error": error,
            "trivial_solved": 0, "trivial": {}}


def _exec_tests(prog: str, tests: list[dict], timeout: float = 6.0) -> tuple[int, int, str | None]:
    """Run one program against every test's stdin, comparing stdout. Returns
    (passed, total, error). Shared by the reference check and the solver."""
    total = len(tests)
    passed = 0
    error = None
    for t in tests:
        try:
            proc = subprocess.run(
                [sys.executable, "-I", "-c", prog],
                input=t.get("input", ""),
                capture_output=True, text=True, timeout=timeout,
                preexec_fn=_limit_resources if sys.platform != "win32" else None,
            )
        except subprocess.TimeoutExpired:
            error = error or "timeout"
            continue
        except Exception as e:  # pragma: no cover - defensive
            error = error or f"{type(e).__name__}: {e}"
            continue
        if _norm(proc.stdout) == _norm(t.get("expected", "")):
            passed += 1
        elif error is None and proc.stderr:
            error = f"stderr: {proc.stderr.strip()[-160:]}"
    return passed, total, error


def run_reference(question: dict, timeout: float = 6.0) -> dict:
    """Run reference_solution on each test's stdin; compare stdout. Also probe
    trivial baselines. Returns {passed, total, error, trivial_solved, trivial}."""
    prog = question.get("reference_solution", "")
    tests = question.get("tests", [])
    passed, total, error = _exec_tests(prog, tests, timeout)

    # Adversarial trivial baselines, computed without running code.
    trivial = {}
    if tests:
        first = _norm(tests[0].get("expected", ""))
        trivial["const"] = all(_norm(t.get("expected", "")) == first for t in tests)
        trivial["echo"] = all(_norm(t.get("input", "")) == _norm(t.get("expected", "")) for t in tests)
        trivial["empty"] = all(_norm(t.get("expected", "")) == "" for t in tests)
    trivial_solved = sum(1 for v in trivial.values() if v)
    return {"passed": passed, "total": total, "error": error,
            "trivial_solved": trivial_solved, "trivial": trivial}


# --------------------------------------------------------------------------- #
# Parsing + validation of the model's output.
# --------------------------------------------------------------------------- #

_REQUIRED = {"title", "difficulty", "topics", "statement", "reference_solution", "tests"}


def _extract_json_block(text: str) -> str | None:
    """Pull the first JSON object, tolerating braces AND nested ``` fences inside
    string values. We do NOT bound on the closing fence: a code block inside the
    `statement` would truncate the object. Instead we brace-match, string-aware."""
    text = text or ""
    # Locate the object start, skipping an optional opening ```json fence.
    search_from = 0
    fence = text.find("```")
    if fence != -1:
        search_from = fence + 3
        if text[search_from:search_from + 4].lower() == "json":
            search_from += 4
    start = text.find("{", search_from)
    if start == -1:
        start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
    return None


def parse_question(text: str) -> dict | None:
    """Extract the JSON question package, or None if it is malformed."""
    raw = _extract_json_block(text)
    if raw is None:
        return None
    try:
        obj = json.loads(raw)
    except Exception:
        return None
    if not isinstance(obj, dict) or not _REQUIRED.issubset(obj):
        return None
    if not isinstance(obj["reference_solution"], str) or not obj["reference_solution"].strip():
        return None
    if not isinstance(obj["tests"], list) or not obj["tests"]:
        return None
    for t in obj["tests"]:
        if not isinstance(t, dict) or "input" not in t or "expected" not in t:
            return None
        if not isinstance(t["input"], str) or not isinstance(t["expected"], str):
            return None
    return obj


def _extract_code_block(text: str) -> str | None:
    """Pull the contents of the first fenced code block (```lang ... ```). Falls
    back to the whole text when the model answers with a bare program."""
    text = text or ""
    fence = text.find("```")
    if fence == -1:
        return text.strip() or None
    nl = text.find("\n", fence + 3)
    if nl == -1:
        return None
    start = nl + 1
    end = text.find("```", start)
    body = text[start:] if end == -1 else text[start:end]
    return body.strip() or None


# --------------------------------------------------------------------------- #
# Solver: an auxiliary model that attempts the authored problem from the
# statement alone (never the reference / expected values). Its solve-rate over k
# samples is the *empirical* difficulty, replacing the tautological self-label.
# --------------------------------------------------------------------------- #

_SOLVER_PROMPT = dedent(
    """\
    Solve this programming problem. Your program must read from standard input and
    print the answer to standard output.

    {title}

    {statement}

    Respond with a SINGLE fenced ```python code block containing a complete program,
    and nothing else.
    """
)

# What fraction of solver attempts *should* succeed at each requested difficulty.
_DIFFICULTY_TARGET = {"EASY": 1.0, "MEDIUM": 0.5, "HARD": 0.0}


class SolverConfig(vf.JudgeConfig):
    # A capable, cheap solver; a HARD problem is one this model cannot solve.
    base_url: str = "https://openrouter.ai/api/v1"
    api_key_var: str = "OPENROUTER_API_KEY"
    model: str = "openai/gpt-4.1-mini"
    sampling: vf.SamplingConfig = Field(
        default_factory=lambda: vf.SamplingConfig(temperature=0.7, max_tokens=2000)
    )


class Solver(vf.Judge[str, SolverConfig]):
    """A `vf.Judge` that returns a program instead of a verdict."""

    prompt = _SOLVER_PROMPT

    def parse(self, response: vf.JudgeResponse[str]) -> str:
        return _extract_code_block(response.text) or ""


# --------------------------------------------------------------------------- #
# Deterministic static checks over the declared tests.
# --------------------------------------------------------------------------- #


def _distinct_expected(tests: list[dict]) -> int:
    return len({_norm(t["expected"]) for t in tests})


def _is_edge_input(stdin: str) -> bool:
    s = (stdin or "").strip()
    if s == "":
        return True
    for tok in s.split():
        if tok in ("0", "-0"):
            return True
        try:
            if int(tok) < 0:
                return True
        except ValueError:
            pass
    return False


def _edge_inputs(tests: list[dict]) -> int:
    return sum(1 for t in tests if _is_edge_input(t["input"]))


# --------------------------------------------------------------------------- #
# Environment definition.
# --------------------------------------------------------------------------- #


class QuestionSpec(vf.TaskData):
    topic: str
    difficulty: str
    min_tests: int


def _gate(info: dict) -> bool:
    return bool(info.get("parsed_ok")) and bool(info.get("enough_tests"))


def _solvable(info: dict) -> bool:
    r = info.get("run", {})
    return bool(r.get("total")) and r.get("passed") == r.get("total") and r.get("error") is None


class CraftTaskConfig(vf.TaskConfig):
    solver: SolverConfig = Field(default_factory=SolverConfig)
    solver_samples: int = 4  # k; targets {0,.25,.5,.75,1} are all exactly hittable
    calibrate_difficulty: bool = True  # set False to skip solver calls (cheap eval)


class CraftTask(vf.Task[QuestionSpec, vf.State, CraftTaskConfig]):
    async def finalize(self, trace: vf.Trace, runtime: vf.Runtime) -> None:
        """Parse + run the reference exactly once; cache everything scoring needs."""
        info = trace.info
        info["solver"] = None
        q = parse_question(trace.last_reply)
        info["parsed_ok"] = q is not None
        if q is None:
            info["enough_tests"] = False
            info["run"] = _empty_run(0, "unparseable")
            info["distinct_expected"] = 0
            info["edge_inputs"] = 0
            info["num_tests"] = 0
            info["difficulty"] = None
            return
        tests = q["tests"]
        info["enough_tests"] = len(tests) >= self.data.min_tests
        info["run"] = run_reference(q)
        info["distinct_expected"] = _distinct_expected(tests)
        info["edge_inputs"] = _edge_inputs(tests)
        info["num_tests"] = len(tests)
        info["difficulty"] = str(q.get("difficulty", "")).upper()

        # Empirical difficulty: only meaningful once the problem is self-consistent,
        # so gate the (paid) solver calls on the deterministic core passing first.
        if self.config.calibrate_difficulty and _gate(info) and _solvable(info):
            info["solver"] = await self._calibrate(trace, q, tests)

    async def _calibrate(self, trace: vf.Trace, q: dict, tests: list[dict]) -> dict:
        solver = Solver(self.config.solver)
        k = max(1, self.config.solver_samples)
        title, statement = q.get("title", ""), q.get("statement", "")
        attempts = await asyncio.gather(
            *(
                solver.evaluate(trace=trace, title=title, statement=statement)
                for _ in range(k)
            ),
            return_exceptions=True,
        )
        solved = 0
        for a in attempts:
            if isinstance(a, Exception):
                continue
            prog = a.parsed or ""
            if not prog.strip():
                continue
            passed, total, error = _exec_tests(prog, tests)
            if total > 0 and passed == total and error is None:
                solved += 1
        solve_rate = solved / k
        target = _DIFFICULTY_TARGET.get(self.data.difficulty, 0.5)
        return {
            "k": k,
            "solved": solved,
            "solve_rate": solve_rate,
            "target": target,
            "calibration": 1.0 - abs(target - solve_rate),
        }

    @vf.reward(weight=0.5)
    async def format_valid(self, trace: vf.Trace) -> float:
        return float(bool(trace.info.get("parsed_ok")))

    @vf.reward(weight=3.0)
    async def tests_pass(self, trace: vf.Trace) -> float:
        info = trace.info
        if not _gate(info):
            return 0.0
        r = info["run"]
        return r["passed"] / r["total"] if r["total"] else 0.0

    @vf.reward(weight=2.0)
    async def solvable(self, trace: vf.Trace) -> float:
        """1.0 only if the reference passes every one of its own tests."""
        info = trace.info
        return float(_gate(info) and _solvable(info))

    @vf.reward(weight=1.5)
    async def non_trivial(self, trace: vf.Trace) -> float:
        info = trace.info
        if not (_gate(info) and _solvable(info)):
            return 0.0
        r = info["run"]
        return float(r.get("trivial_solved", 0) == 0 and info["distinct_expected"] >= 2)

    @vf.reward(weight=1.5)
    async def difficulty_calibrated(self, trace: vf.Trace) -> float:
        """Reward = 1 - |target_solve_rate - observed_solve_rate|. An independent
        solver attempts the problem from the statement alone; a problem labeled
        HARD that the solver aces (or EASY the solver fails) is mis-calibrated and
        scores low. Zero unless the deterministic core already passed (solver
        gated on solvable in finalize)."""
        s = trace.info.get("solver")
        return float(s["calibration"]) if s else 0.0

    # NOTE: edge coverage is a METRIC, not a reward. The gold-set regression
    # showed only ~33% of *verified* questions satisfy any cheap stdin edge
    # heuristic (real edges are domain-specific), so rewarding it would penalize
    # good questions. We observe it instead of paying for it.

    @vf.metric
    async def num_tests(self, trace: vf.Trace) -> float:
        return float(trace.info.get("num_tests", 0))

    @vf.metric
    async def difficulty_match(self, trace: vf.Trace) -> float:
        return float(trace.info.get("difficulty") == self.data.difficulty)

    @vf.metric
    async def trivial_solved(self, trace: vf.Trace) -> float:
        return float(trace.info.get("run", {}).get("trivial_solved", 0))

    @vf.metric
    async def distinct_expected(self, trace: vf.Trace) -> float:
        return float(trace.info.get("distinct_expected", 0))

    @vf.metric
    async def edge_inputs(self, trace: vf.Trace) -> float:
        return float(trace.info.get("edge_inputs", 0))

    @vf.metric
    async def solver_solve_rate(self, trace: vf.Trace) -> float:
        s = trace.info.get("solver")
        return float(s["solve_rate"]) if s else 0.0

    @vf.metric
    async def solver_ran(self, trace: vf.Trace) -> float:
        return float(trace.info.get("solver") is not None)


class CraftConfig(vf.TasksetConfig):
    num_tasks: int = 12
    seed: int = 0
    task: CraftTaskConfig = Field(default_factory=CraftTaskConfig)


class CodingQuestionCraftTaskset(vf.Taskset[CraftTask, CraftConfig]):
    def load(self) -> list[CraftTask]:
        specs = build_specs(self.config.num_tasks, self.config.seed)
        exemplar = _exemplar_block()
        return [
            CraftTask(
                QuestionSpec(
                    idx=s["idx"],
                    prompt=INSTRUCTIONS.format(exemplar=exemplar, **s),
                    topic=s["topic"],
                    difficulty=s["difficulty"],
                    min_tests=s["min_tests"],
                ),
                self.config.task,
            )
            for s in specs
        ]


__all__ = ["CodingQuestionCraftTaskset"]
