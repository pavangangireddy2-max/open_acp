"""Item co-failure pilot pipeline.

Implements CLAUDE.md sections 3-9: build the base table, compute pairwise
co-failure statistics (lift, phi) over all item pairs, apply the confidence
floor N, and produce the session-pair roll-up.

Usage:
    python scripts/pipeline.py
Reads RAW_EXTRACT_PATH (default data/pilot_extract.csv) and writes outputs
under OUTPUT_DIR (default output/).
"""
import os

import numpy as np
import pandas as pd
from dotenv import load_dotenv

REQUIRED_COLUMNS = [
    "user_id",
    "question_id",
    "session_title",
    "first_attempt_result",
    "question_type",
    "time_spent_till_first_submission",
]

RESULT_MAP = {
    "CORRECT": 0,
    "INCORRECT": 1,
    "PARTIALLY_CORRECT": 1,
}


def load_base_table(path: str) -> pd.DataFrame:
    raw = pd.read_csv(path)
    df = raw[REQUIRED_COLUMNS].copy()

    df["failed"] = df["first_attempt_result"].str.upper().map(RESULT_MAP)
    unmapped = df[df["failed"].isna() & df["first_attempt_result"].notna()]
    assert unmapped.empty, (
        f"Unmapped first_attempt_result values found: "
        f"{unmapped['first_attempt_result'].unique()}"
    )
    return df


def check_rush_answer_field(df: pd.DataFrame) -> None:
    non_null_frac = df["time_spent_till_first_submission"].notna().mean()
    print(f"Fraction of rows with non-null time_spent: {non_null_frac:.2%}")

    observed = df.loc[
        df["time_spent_till_first_submission"].notna(),
        ["question_type", "time_spent_till_first_submission"],
    ]
    if not observed.empty:
        print(observed.groupby("question_type")["time_spent_till_first_submission"].describe())
    else:
        print("No non-null time_spent values present at all.")


def build_matrix(df: pd.DataFrame):
    fail_pivot = df.pivot_table(
        index="user_id", columns="question_id", values="failed", aggfunc="first"
    )
    F = fail_pivot
    A = ~F.isna()
    Fz = F.fillna(0).astype(int)

    print(f"Matrix shape: {F.shape}")
    print(f"Users with zero attempts after filtering: {(A.sum(axis=1) == 0).sum()}")
    print(f"Items with zero attempts after filtering: {(A.sum(axis=0) == 0).sum()}")

    return F, A, Fz


def phi_coefficient(a, b, c, d):
    n = a + b + c + d  # noqa: F841 (kept for readability/debugging parity with spec)
    num = (a * d) - (b * c)
    denom = np.sqrt((a + b) * (c + d) * (a + c) * (b + d))
    return np.divide(num, denom, out=np.zeros_like(num, dtype=float), where=denom > 0)


def compute_pairwise_stats(F: pd.DataFrame, A: pd.DataFrame, Fz: pd.DataFrame) -> pd.DataFrame:
    A_int = A.values.astype(np.int32)
    fail_masked = (Fz.values * A.values).astype(np.int32)  # fail=1 & attempted, else 0
    pass_masked = ((1 - Fz.values) * A.values).astype(np.int32)  # pass=1 & attempted, else 0

    n_both_attempted = A_int.T @ A_int
    both_fail_counts = fail_masked.T @ fail_masked
    both_pass_counts = pass_masked.T @ pass_masked
    # x fail & y pass (co-attempted), and x pass & y fail (co-attempted)
    x_fail_y_pass_counts = fail_masked.T @ pass_masked
    x_pass_y_fail_counts = pass_masked.T @ fail_masked

    items = F.columns.to_numpy()
    n_items = len(items)
    i_idx, j_idx = np.triu_indices(n_items, k=1)

    n_both = n_both_attempted[i_idx, j_idx]
    a = both_fail_counts[i_idx, j_idx].astype(float)      # both fail
    d = both_pass_counts[i_idx, j_idx].astype(float)      # both pass
    b = x_fail_y_pass_counts[i_idx, j_idx].astype(float)  # x fail, y pass
    c = x_pass_y_fail_counts[i_idx, j_idx].astype(float)  # x pass, y fail

    valid = n_both > 0

    p_fail_x = np.divide(a + b, n_both, out=np.zeros_like(a), where=valid)
    p_fail_y = np.divide(a + c, n_both, out=np.zeros_like(a), where=valid)
    p_fail_both = np.divide(a, n_both, out=np.zeros_like(a), where=valid)

    denom_lift = p_fail_x * p_fail_y
    lift = np.divide(p_fail_both, denom_lift, out=np.zeros_like(p_fail_both), where=denom_lift > 0)

    phi = phi_coefficient(a, b, c, d)

    co_failure_pairs = pd.DataFrame({
        "item_x": items[i_idx],
        "item_y": items[j_idx],
        "n_both_attempted": n_both,
        "p_fail_x": p_fail_x,
        "p_fail_y": p_fail_y,
        "p_fail_both": p_fail_both,
        "lift": lift,
        "phi": phi,
    })
    return co_failure_pairs


def attach_metadata(co_failure_pairs: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    item_meta = df.drop_duplicates("question_id").set_index("question_id")[
        ["session_title", "question_type"]
    ]
    co_failure_pairs["session_x"] = co_failure_pairs["item_x"].map(item_meta["session_title"])
    co_failure_pairs["session_y"] = co_failure_pairs["item_y"].map(item_meta["session_title"])
    co_failure_pairs["question_type_x"] = co_failure_pairs["item_x"].map(item_meta["question_type"])
    co_failure_pairs["question_type_y"] = co_failure_pairs["item_y"].map(item_meta["question_type"])
    return co_failure_pairs


def session_pair_rollup(co_failure_final: pd.DataFrame) -> pd.DataFrame:
    # item_x/item_y (and therefore session_x/session_y) are ordered by pivot
    # column index, not by session — so the same unordered session-pair can
    # appear as (A, B) for some item pairs and (B, A) for others. Canonicalize
    # to an unordered pair before grouping, or the same session-pair gets
    # split into two conflicting rows.
    session_a = np.minimum(co_failure_final["session_x"], co_failure_final["session_y"])
    session_b = np.maximum(co_failure_final["session_x"], co_failure_final["session_y"])
    co_failure_final = co_failure_final.assign(session_a=session_a, session_b=session_b)

    rollup = (
        co_failure_final
        .groupby(["session_a", "session_b"])
        .agg(
            n_item_pairs=("lift", "size"),
            median_lift=("lift", "median"),
            pct_lift_gt_1_5=("lift", lambda s: (s > 1.5).mean()),
            pct_lift_lt_0_7=("lift", lambda s: (s < 0.7).mean()),
        )
        .reset_index()
        .sort_values("median_lift", ascending=False)
    )
    return rollup


def main() -> None:
    load_dotenv()

    raw_path = os.environ.get("RAW_EXTRACT_PATH", "data/pilot_extract.csv")
    out_dir = os.environ.get("OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)

    df = load_base_table(raw_path)

    print("\n--- Rush-answer field check (informational only, not applied as a filter) ---")
    check_rush_answer_field(df)

    print("\n--- Building matrix ---")
    F, A, Fz = build_matrix(df)

    print("\n--- Computing pairwise statistics ---")
    co_failure_pairs = compute_pairwise_stats(F, A, Fz)
    co_failure_pairs = attach_metadata(co_failure_pairs, df)

    print("\n--- n_both_attempted distribution ---")
    print(co_failure_pairs["n_both_attempted"].describe())

    n_env = os.environ.get("CONFIDENCE_FLOOR_N", "").strip()
    if not n_env:
        print(
            "\nCONFIDENCE_FLOOR_N is not set in .env. Inspect the distribution above "
            "(and output/n_both_attempted_hist.csv) before deciding N. "
            "Writing the unfiltered pair table only."
        )
        co_failure_pairs.to_csv(os.path.join(out_dir, "co_failure_pairs_unfiltered.csv"), index=False)
        hist_counts, hist_edges = np.histogram(co_failure_pairs["n_both_attempted"], bins=50)
        pd.DataFrame({"bin_left": hist_edges[:-1], "bin_right": hist_edges[1:], "count": hist_counts}).to_csv(
            os.path.join(out_dir, "n_both_attempted_hist.csv"), index=False
        )
        return

    N = int(n_env)
    co_failure_final = co_failure_pairs[co_failure_pairs["n_both_attempted"] >= N].copy()
    print(f"\nApplied confidence floor N={N}: {len(co_failure_final):,} / {len(co_failure_pairs):,} pairs kept")

    co_failure_final.to_csv(os.path.join(out_dir, "co_failure_pairs.csv"), index=False)

    rollup = session_pair_rollup(co_failure_final)
    rollup.to_csv(os.path.join(out_dir, "session_pair_rollup.csv"), index=False)
    print("\n--- Session-pair roll-up ---")
    print(rollup)


if __name__ == "__main__":
    main()
