#!/usr/bin/env python3
"""Diagnostic residual analysis for the frozen V2 endface-hybrid retrospective result.

This script does NOT modify or tune any estimator. It only analyzes preserved
V2 PCA observations and the already-recorded frozen endface-hybrid retrospective
observations to determine where the remaining repositioning tail originates.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
import math
from pathlib import Path
import statistics
from typing import Any

from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data/oal_validation"

V2_CSV = DATA_ROOT / "v2_cv_observations.csv"
HYBRID_CSV = (
    DATA_ROOT
    / "derived_v2/endface_hybrid_retrospective/v2_endface_hybrid_observations.csv"
)
SPECIMEN_CSV = DATA_ROOT / "formal_validation_specimens.csv"

OUTPUT_DIR = DATA_ROOT / "derived_v2/endface_hybrid_residual_diagnostics"

EXPECTED_OBSERVATIONS = 180
EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_yes(value: str) -> bool:
    return value.strip().upper() in {"YES", "TRUE", "1"}


def nearest_rank(values: list[float], p: float) -> float:
    if not values:
        fail("Cannot compute percentile on empty input.")
    ordered = sorted(values)
    rank = math.ceil(p * len(ordered))
    return ordered[rank - 1]


def pairwise(values_by_round: dict[int, float]) -> list[tuple[str, float, float]]:
    if set(values_by_round) != EXPECTED_ROUNDS:
        fail(f"Expected rounds 1,2,3; got {sorted(values_by_round)}")
    out = []
    for a, b in ((1, 2), (1, 3), (2, 3)):
        signed = values_by_round[a] - values_by_round[b]
        out.append((f"{a}-{b}", signed, abs(signed)))
    return out


def safe_corr(x: list[float], y: list[float]) -> tuple[float, float]:
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return float("nan"), float("nan")
    return stats.pearsonr(x, y).statistic, stats.spearmanr(x, y).statistic


def main() -> int:
    v2_all = read_csv(V2_CSV)
    hybrid_all = read_csv(HYBRID_CSV)
    specimen_rows = read_csv(SPECIMEN_CSV)

    v2 = [
        r for r in v2_all
        if r["measurement_status"].strip().upper() == "VALID"
        and not is_yes(r["protocol_invalid"])
    ]
    hybrid = [r for r in hybrid_all if str(r["passed"]).strip().lower() in {"true", "1", "yes"}]

    if len(v2) != EXPECTED_OBSERVATIONS:
        fail(f"Expected 180 V2 observations, found {len(v2)}")
    if len(hybrid) != EXPECTED_OBSERVATIONS:
        fail(f"Expected 180 passing hybrid observations, found {len(hybrid)}")
    if len(specimen_rows) != EXPECTED_SPECIMENS:
        fail(f"Expected 60 specimen rows, found {len(specimen_rows)}")

    v2_by_run = {r["cv_run_id"]: r for r in v2}
    hybrid_by_run = {r["cv_run_id"]: r for r in hybrid}
    if set(v2_by_run) != set(hybrid_by_run):
        fail("V2 and hybrid cv_run_id sets do not match.")

    specimen_meta = {r["part_id"]: r for r in specimen_rows}
    if len(specimen_meta) != EXPECTED_SPECIMENS:
        fail("Specimen IDs are not unique.")

    per_part_pca: dict[str, dict[int, float]] = defaultdict(dict)
    per_part_hybrid: dict[str, dict[int, float]] = defaultdict(dict)

    joined_rows: list[dict[str, Any]] = []
    for run_id in sorted(v2_by_run):
        vr = v2_by_run[run_id]
        hr = hybrid_by_run[run_id]
        pid = vr["part_id"]
        rnd = int(vr["cv_round"])

        if pid != hr["part_id"] or rnd != int(hr["cv_round"]):
            fail(f"Join mismatch for {run_id}")

        pca = float(vr["oal_in"])
        hyb = float(hr["hybrid_oal_in"])
        per_part_pca[pid][rnd] = pca
        per_part_hybrid[pid][rnd] = hyb

        joined_rows.append(
            {
                "cv_run_id": run_id,
                "part_id": pid,
                "cv_round": rnd,
                "selection_stratum": specimen_meta[pid]["selection_stratum"],
                "pca_oal_in": pca,
                "hybrid_oal_in": hyb,
            }
        )

    if len(per_part_pca) != EXPECTED_SPECIMENS:
        fail(f"Expected 60 PCA specimens, found {len(per_part_pca)}")

    specimen_summary: list[dict[str, Any]] = []
    pca_pairwise_records: list[dict[str, Any]] = []
    hybrid_pairwise_records: list[dict[str, Any]] = []

    pca_centered: list[float] = []
    hybrid_centered: list[float] = []

    for pid in sorted(specimen_meta, key=int):
        pca_rounds = per_part_pca[pid]
        hyb_rounds = per_part_hybrid[pid]
        if set(pca_rounds) != EXPECTED_ROUNDS or set(hyb_rounds) != EXPECTED_ROUNDS:
            fail(f"Incomplete round coverage for specimen {pid}")

        pca_vals = [pca_rounds[r] for r in (1, 2, 3)]
        hyb_vals = [hyb_rounds[r] for r in (1, 2, 3)]
        pca_mean = statistics.fmean(pca_vals)
        hyb_mean = statistics.fmean(hyb_vals)

        for r in (1, 2, 3):
            pca_centered.append(pca_rounds[r] - pca_mean)
            hybrid_centered.append(hyb_rounds[r] - hyb_mean)

        pca_pairs = pairwise(pca_rounds)
        hyb_pairs = pairwise(hyb_rounds)

        for pair_name, signed, absolute in pca_pairs:
            pca_pairwise_records.append(
                {
                    "part_id": pid,
                    "selection_stratum": specimen_meta[pid]["selection_stratum"],
                    "round_pair": pair_name,
                    "signed_difference_in": signed,
                    "absolute_difference_in": absolute,
                }
            )
        for pair_name, signed, absolute in hyb_pairs:
            hybrid_pairwise_records.append(
                {
                    "part_id": pid,
                    "selection_stratum": specimen_meta[pid]["selection_stratum"],
                    "round_pair": pair_name,
                    "signed_difference_in": signed,
                    "absolute_difference_in": absolute,
                }
            )

        pca_range = max(pca_vals) - min(pca_vals)
        hyb_range = max(hyb_vals) - min(hyb_vals)
        improvement = pca_range - hyb_range
        pct = (100.0 * improvement / pca_range) if pca_range > 0 else float("nan")

        specimen_summary.append(
            {
                "part_id": pid,
                "selection_stratum": specimen_meta[pid]["selection_stratum"],
                "pca_range_in": pca_range,
                "hybrid_range_in": hyb_range,
                "range_improvement_in": improvement,
                "range_improvement_pct": pct,
                "pca_max_pairwise_in": max(x[2] for x in pca_pairs),
                "hybrid_max_pairwise_in": max(x[2] for x in hyb_pairs),
                "hybrid_over_0p002": hyb_range > 0.002,
                "hybrid_over_0p003": hyb_range > 0.003,
            }
        )

    pca_ranges = [float(r["pca_range_in"]) for r in specimen_summary]
    hyb_ranges = [float(r["hybrid_range_in"]) for r in specimen_summary]
    range_pearson, range_spearman = safe_corr(pca_ranges, hyb_ranges)
    centered_pearson, centered_spearman = safe_corr(pca_centered, hybrid_centered)

    pca_abs = [float(r["absolute_difference_in"]) for r in pca_pairwise_records]
    hyb_abs = [float(r["absolute_difference_in"]) for r in hybrid_pairwise_records]

    pca_p95 = nearest_rank(pca_abs, 0.95)
    hyb_p95 = nearest_rank(hyb_abs, 0.95)

    # Nearest-rank P95 of 180 is the 171st ascending observation, leaving
    # 10 observations from rank 171 through rank 180 in the upper tail.
    top_n = len(hyb_abs) - math.ceil(0.95 * len(hyb_abs)) + 1
    pca_top = sorted(
        pca_pairwise_records,
        key=lambda r: float(r["absolute_difference_in"]),
        reverse=True,
    )[:top_n]
    hyb_top = sorted(
        hybrid_pairwise_records,
        key=lambda r: float(r["absolute_difference_in"]),
        reverse=True,
    )[:top_n]

    pca_top_parts = Counter(r["part_id"] for r in pca_top)
    hyb_top_parts = Counter(r["part_id"] for r in hyb_top)
    overlap_parts = set(pca_top_parts) & set(hyb_top_parts)

    threshold_counts = {
        "pairwise_le_0p001": sum(v <= 0.001 for v in hyb_abs),
        "pairwise_le_0p002": sum(v <= 0.002 for v in hyb_abs),
        "pairwise_gt_0p002": sum(v > 0.002 for v in hyb_abs),
        "pairwise_gt_0p003": sum(v > 0.003 for v in hyb_abs),
        "specimen_range_le_0p002": sum(v <= 0.002 for v in hyb_ranges),
        "specimen_range_gt_0p002": sum(v > 0.002 for v in hyb_ranges),
        "specimen_range_gt_0p003": sum(v > 0.003 for v in hyb_ranges),
        "specimen_range_gt_0p004": sum(v > 0.004 for v in hyb_ranges),
    }

    round_pair_rows: list[dict[str, Any]] = []
    for pair_name in ("1-2", "1-3", "2-3"):
        pca_rows = [r for r in pca_pairwise_records if r["round_pair"] == pair_name]
        hyb_rows = [r for r in hybrid_pairwise_records if r["round_pair"] == pair_name]

        pca_signed = [float(r["signed_difference_in"]) for r in pca_rows]
        hyb_signed = [float(r["signed_difference_in"]) for r in hyb_rows]
        pca_a = [abs(v) for v in pca_signed]
        hyb_a = [abs(v) for v in hyb_signed]

        round_pair_rows.append(
            {
                "round_pair": pair_name,
                "pca_mean_signed_in": statistics.fmean(pca_signed),
                "hybrid_mean_signed_in": statistics.fmean(hyb_signed),
                "pca_median_abs_in": statistics.median(pca_a),
                "hybrid_median_abs_in": statistics.median(hyb_a),
                "pca_p95_abs_in": nearest_rank(pca_a, 0.95),
                "hybrid_p95_abs_in": nearest_rank(hyb_a, 0.95),
                "pca_max_abs_in": max(pca_a),
                "hybrid_max_abs_in": max(hyb_a),
            }
        )

    stratum_rows: list[dict[str, Any]] = []
    strata = sorted({r["selection_stratum"] for r in specimen_summary})
    for stratum in strata:
        part_ids = {
            r["part_id"] for r in specimen_summary
            if r["selection_stratum"] == stratum
        }
        pair_vals = [
            float(r["absolute_difference_in"])
            for r in hybrid_pairwise_records
            if r["part_id"] in part_ids
        ]
        ranges = [
            float(r["hybrid_range_in"])
            for r in specimen_summary
            if r["part_id"] in part_ids
        ]
        stratum_rows.append(
            {
                "selection_stratum": stratum,
                "n_specimens": len(part_ids),
                "n_pairwise": len(pair_vals),
                "median_pairwise_in": statistics.median(pair_vals),
                "p95_pairwise_in": nearest_rank(pair_vals, 0.95),
                "max_pairwise_in": max(pair_vals),
                "median_specimen_range_in": statistics.median(ranges),
                "max_specimen_range_in": max(ranges),
            }
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def write_rows(name: str, rows: list[dict[str, Any]]) -> None:
        path = OUTPUT_DIR / name
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    write_rows("specimen_residual_summary.csv", specimen_summary)
    write_rows("pca_pairwise_differences.csv", pca_pairwise_records)
    write_rows("hybrid_pairwise_differences.csv", hybrid_pairwise_records)
    write_rows("round_pair_summary.csv", round_pair_rows)
    write_rows("stratum_summary.csv", stratum_rows)

    worst_hybrid = sorted(
        specimen_summary,
        key=lambda r: float(r["hybrid_range_in"]),
        reverse=True,
    )[:15]
    most_improved = sorted(
        specimen_summary,
        key=lambda r: float(r["range_improvement_in"]),
        reverse=True,
    )[:10]
    worsened = sorted(
        [r for r in specimen_summary if float(r["range_improvement_in"]) < 0],
        key=lambda r: float(r["range_improvement_in"]),
    )

    lines = [
        "# Endface-Hybrid V2 Residual Diagnostics",
        "",
        "**Diagnostic only. No estimator parameters are changed by this analysis.**",
        "",
        "## Population-level tail",
        "",
        f"- PCA pooled P95 pairwise repositioning: {pca_p95:.6f} in",
        f"- Hybrid pooled P95 pairwise repositioning: {hyb_p95:.6f} in",
        f"- Hybrid pairwise differences <= 0.001 in: {threshold_counts['pairwise_le_0p001']}/180",
        f"- Hybrid pairwise differences <= 0.002 in: {threshold_counts['pairwise_le_0p002']}/180",
        f"- Hybrid pairwise differences > 0.002 in: {threshold_counts['pairwise_gt_0p002']}/180",
        f"- Hybrid pairwise differences > 0.003 in: {threshold_counts['pairwise_gt_0p003']}/180",
        f"- Specimens with hybrid range <= 0.002 in: {threshold_counts['specimen_range_le_0p002']}/60",
        f"- Specimens with hybrid range > 0.002 in: {threshold_counts['specimen_range_gt_0p002']}/60",
        f"- Specimens with hybrid range > 0.003 in: {threshold_counts['specimen_range_gt_0p003']}/60",
        f"- Specimens with hybrid range > 0.004 in: {threshold_counts['specimen_range_gt_0p004']}/60",
        "",
        "## PCA-versus-hybrid association",
        "",
        f"- Specimen range Pearson correlation: {range_pearson:.4f}",
        f"- Specimen range Spearman correlation: {range_spearman:.4f}",
        f"- Within-specimen centered observation Pearson correlation: {centered_pearson:.4f}",
        f"- Within-specimen centered observation Spearman correlation: {centered_spearman:.4f}",
        "",
        "High centered-observation correlation means the two different estimators tend to move in the same direction on the same physical placement, which is evidence for a shared placement/pose component rather than independent endpoint noise.",
        "",
        "## Upper-tail concentration",
        "",
        f"- Nearest-rank P95 upper-tail observations considered: {top_n}",
        f"- Unique specimens contributing to PCA upper tail: {len(pca_top_parts)}",
        f"- Unique specimens contributing to hybrid upper tail: {len(hyb_top_parts)}",
        f"- Specimens present in both estimator upper tails: {len(overlap_parts)}",
        f"- Overlap specimen IDs: {', '.join(sorted(overlap_parts, key=int)) if overlap_parts else 'none'}",
        "",
        "### Hybrid upper-tail observations",
        "",
    ]

    for r in hyb_top:
        lines.append(
            f'- Part {r["part_id"]}, rounds {r["round_pair"]}: '
            f'{float(r["absolute_difference_in"]):.6f} in'
        )

    lines.extend(["", "## Fifteen largest hybrid specimen ranges", ""])
    for r in worst_hybrid:
        lines.append(
            f'- Part {r["part_id"]} ({r["selection_stratum"]}): '
            f'hybrid {float(r["hybrid_range_in"]):.6f} in; '
            f'PCA {float(r["pca_range_in"]):.6f} in; '
            f'change {float(r["range_improvement_in"]):+.6f} in'
        )

    lines.extend(["", "## Ten largest specimen-level improvements", ""])
    for r in most_improved:
        lines.append(
            f'- Part {r["part_id"]}: PCA {float(r["pca_range_in"]):.6f} in '
            f'-> hybrid {float(r["hybrid_range_in"]):.6f} in '
            f'({float(r["range_improvement_in"]):+.6f} in)'
        )

    lines.extend(["", "## Specimens worsened by the hybrid", ""])
    if worsened:
        for r in worsened:
            lines.append(
                f'- Part {r["part_id"]}: PCA {float(r["pca_range_in"]):.6f} in '
                f'-> hybrid {float(r["hybrid_range_in"]):.6f} in '
                f'({float(r["range_improvement_in"]):+.6f} in)'
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Round-pair comparison", ""])
    for r in round_pair_rows:
        lines.append(
            f'- Rounds {r["round_pair"]}: '
            f'hybrid mean signed {float(r["hybrid_mean_signed_in"]):+.6f} in; '
            f'P95 abs {float(r["hybrid_p95_abs_in"]):.6f} in; '
            f'max abs {float(r["hybrid_max_abs_in"]):.6f} in'
        )

    lines.extend(["", "## Stratum comparison", ""])
    for r in stratum_rows:
        lines.append(
            f'- {r["selection_stratum"]}: n={r["n_specimens"]}; '
            f'P95 pairwise {float(r["p95_pairwise_in"]):.6f} in; '
            f'max pairwise {float(r["max_pairwise_in"]):.6f} in'
        )

    lines.extend(
        [
            "",
            "## Interpretation guardrail",
            "",
            "This analysis is intended only to localize the residual error mechanism. It must not be used to change the already-frozen endface-hybrid estimator parameters. Any new software hypothesis should be physically motivated and developed on non-formal development data before prospective validation.",
            "",
        ]
    )

    summary_path = OUTPUT_DIR / "SUMMARY.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 90)
    print("ENDFACE-HYBRID V2 RESIDUAL DIAGNOSTICS")
    print("=" * 90)
    print(f"PCA P95 pairwise:      {pca_p95:.6f} in")
    print(f"Hybrid P95 pairwise:   {hyb_p95:.6f} in")
    print(
        f"Hybrid <=0.002 in:     "
        f"{threshold_counts['pairwise_le_0p002']}/180 pairwise observations"
    )
    print(
        f"Specimen range <=.002: "
        f"{threshold_counts['specimen_range_le_0p002']}/60 specimens"
    )
    print(
        f"Specimen range >.003:  "
        f"{threshold_counts['specimen_range_gt_0p003']}/60 specimens"
    )
    print()
    print(f"Range correlation (Pearson):     {range_pearson:.4f}")
    print(f"Range correlation (Spearman):    {range_spearman:.4f}")
    print(f"Centered placement corr Pearson: {centered_pearson:.4f}")
    print(f"Centered placement corr Spearman:{centered_spearman:.4f}")
    print()
    print(
        "Hybrid upper-tail unique specimens: "
        f"{len(hyb_top_parts)} / {EXPECTED_SPECIMENS}"
    )
    print(
        "PCA/hybrid upper-tail overlap: "
        f"{len(overlap_parts)} specimens"
    )
    print(
        "Overlap IDs: "
        + (", ".join(sorted(overlap_parts, key=int)) if overlap_parts else "none")
    )
    print()
    print("Worst hybrid specimen ranges:")
    for r in worst_hybrid[:10]:
        print(
            f'  Part {r["part_id"]:>3}: hybrid={float(r["hybrid_range_in"]):.6f} in; '
            f'PCA={float(r["pca_range_in"]):.6f} in'
        )
    print()
    print(f"Wrote: {summary_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
