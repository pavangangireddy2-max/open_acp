"""
Investigates whether a single session's items split into two (or more)
sub-clusters, based on the within-session item-pair lift values already
computed by pipeline.py.

This does NOT decide the final node structure — that stays with the
curriculum team, per the original spec ("the clustering step is ours").
This script produces the evidence (cluster assignment + supporting stats)
so a candidate split can be reviewed and confirmed by them.

Usage:
    python scripts/investigate_split.py --session "For Loop"
    python scripts/investigate_split.py --session "Loops" --n-clusters 2
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform


def load_session_pairs(pairs_path: Path, session: str) -> pd.DataFrame:
    pairs = pd.read_csv(pairs_path)
    within = pairs[
        (pairs["session_x"] == session) & (pairs["session_y"] == session)
    ].copy()
    if within.empty:
        raise ValueError(
            f"No within-session pairs found for session '{session}'. "
            f"Check the exact session_title spelling against the source data, "
            f"or check whether every within-session pair for this session fell "
            f"below the confidence floor N."
        )
    print(f"{len(within):,} within-session item pairs found for '{session}' (after confidence floor)")
    return within


def full_session_item_count(unfiltered_path: Path, session: str) -> set:
    """All items ever seen for this session, from the UNFILTERED pairs table.

    Every item that co-occurred with at least one other item in the session
    appears in the unfiltered table regardless of the confidence floor, so
    this gives the true item universe to diagnose coverage against.
    """
    if not unfiltered_path.exists():
        return set()
    unfiltered = pd.read_csv(unfiltered_path)
    within = unfiltered[(unfiltered["session_x"] == session) & (unfiltered["session_y"] == session)]
    return set(within["item_x"]) | set(within["item_y"])


def build_item_lift_matrix(within: pd.DataFrame) -> tuple:
    """Builds a symmetric item x item lift matrix for one session's items only.

    Cells with no surviving (confidence-floor-passing) pair are left as NaN,
    not silently defaulted — see report_matrix_coverage() for how these are
    handled before clustering.
    """
    items = sorted(set(within["item_x"]) | set(within["item_y"]))
    idx = {item: i for i, item in enumerate(items)}
    n = len(items)

    lift_matrix = np.full((n, n), np.nan)
    np.fill_diagonal(lift_matrix, 1.0)  # self-lift, treated as max relation
    for _, row in within.iterrows():
        i, j = idx[row["item_x"]], idx[row["item_y"]]
        lift_matrix[i, j] = row["lift"]
        lift_matrix[j, i] = row["lift"]

    return pd.DataFrame(lift_matrix, index=items, columns=items), items


def report_matrix_coverage(lift_df: pd.DataFrame, session: str, full_items: set) -> pd.DataFrame:
    """Prints coverage diagnostics, then returns a matrix safe to cluster on
    (missing cells filled with the session's own median observed lift — a
    neutral fill relative to this session's actual scale, not a hardcoded 1.0).
    """
    n = len(lift_df)
    off_diag_mask = ~np.eye(n, dtype=bool)
    total_cells = off_diag_mask.sum()
    missing_cells = np.isnan(lift_df.values[off_diag_mask]).sum()

    dropped_items = full_items - set(lift_df.index) if full_items else set()

    print(f"\nMatrix coverage for '{session}':")
    print(f"  items included in clustering: {n}" + (f" (of {len(full_items)} total; {len(dropped_items)} dropped for zero surviving pairs)" if full_items else ""))
    if dropped_items:
        print(f"  dropped items (zero pairs cleared the confidence floor): {sorted(dropped_items)}")
    print(f"  matrix cells with real (confidence-floor-passing) lift: {total_cells - missing_cells} / {total_cells} ({(total_cells - missing_cells) / total_cells:.1%})")
    if missing_cells > 0:
        median_observed = np.nanmedian(lift_df.values[off_diag_mask])
        print(f"  {missing_cells} cells have no surviving pair — filled with this session's median observed lift ({median_observed:.3f}) as a neutral placeholder, NOT assumed independence (lift=1)")
        print(f"  CAUTION: treat any cluster boundary that relies heavily on filled cells as unconfirmed until re-checked with more data")
        filled = lift_df.fillna(median_observed)
    else:
        filled = lift_df

    return filled


def cluster_items(lift_df: pd.DataFrame, n_clusters: int = 2) -> pd.Series:
    """
    Converts lift (higher = more related) into a distance (higher = less related),
    then runs hierarchical clustering. Distance = 1 / lift, capped to avoid
    divide-by-zero blow-ups when lift is at or near zero.
    """
    lift_vals = lift_df.values.copy()
    lift_vals[lift_vals <= 0] = 0.01  # lift is a probability ratio, always >= 0; guard the zero case only
    distance = 1.0 / lift_vals
    np.fill_diagonal(distance, 0)

    # ensure symmetry (floating point safety) before squareform
    distance = (distance + distance.T) / 2
    condensed = squareform(distance, checks=False)

    Z = linkage(condensed, method="average")
    cluster_labels = fcluster(Z, t=n_clusters, criterion="maxclust")

    return pd.Series(cluster_labels, index=lift_df.index, name="cluster")


def summarize_clusters(lift_df: pd.DataFrame, clusters: pd.Series) -> None:
    print("\nCluster assignment:")
    for c in sorted(clusters.unique()):
        members = clusters[clusters == c].index.tolist()
        print(f"  Cluster {c} ({len(members)} items): {members}")

    print("\nWithin-cluster vs. between-cluster median lift:")
    cluster_ids = clusters.unique()
    for c1 in sorted(cluster_ids):
        for c2 in sorted(cluster_ids):
            if c2 < c1:
                continue
            items1 = clusters[clusters == c1].index
            items2 = clusters[clusters == c2].index
            sub = lift_df.loc[items1, items2].values
            if c1 == c2:
                # exclude diagonal (self-lift) for within-cluster median
                mask = ~np.eye(sub.shape[0], dtype=bool)
                vals = sub[mask] if sub.shape[0] > 1 else np.array([])
            else:
                vals = sub.flatten()
            if len(vals) > 0:
                print(f"  Cluster {c1} <-> Cluster {c2}: median lift = {np.median(vals):.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, help="Exact session_title to investigate")
    parser.add_argument("--n-clusters", type=int, default=2, help="Number of sub-clusters to test for")
    parser.add_argument(
        "--pairs-file", default="output/co_failure_pairs.csv",
        help="Path to the confidence-floor-filtered pairs CSV produced by pipeline.py"
    )
    parser.add_argument(
        "--unfiltered-file", default="output/co_failure_pairs_unfiltered.csv",
        help="Path to the unfiltered pairs CSV, used only to diagnose coverage/dropped items"
    )
    args = parser.parse_args()

    within = load_session_pairs(Path(args.pairs_file), args.session)
    lift_df, items = build_item_lift_matrix(within)

    full_items = full_session_item_count(Path(args.unfiltered_file), args.session)
    lift_df = report_matrix_coverage(lift_df, args.session, full_items)

    clusters = cluster_items(lift_df, n_clusters=args.n_clusters)
    summarize_clusters(lift_df, clusters)

    print(
        "\nInterpretation guide:\n"
        "  - If within-cluster median lift is clearly higher than between-cluster\n"
        "    median lift, this session likely hides a real split — the two clusters\n"
        "    are candidate sub-skills.\n"
        "  - If within- and between-cluster medians are similar, the split found\n"
        "    here is likely just noise from forcing n_clusters=2 on a genuinely\n"
        "    uniform session — do not report this as a split candidate.\n"
        "  - Check the matrix coverage % above before trusting the split — a low\n"
        "    percentage means much of the input was neutral-filled, not observed.\n"
        "  - Manually check the item content in each cluster to see if there's an\n"
        "    obvious shared theme (e.g. 'syntax basics' vs 'edge cases') before\n"
        "    handing this to the curriculum team."
    )


if __name__ == "__main__":
    main()
