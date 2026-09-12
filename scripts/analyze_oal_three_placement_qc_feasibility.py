#!/usr/bin/env python3
"""Retrospective feasibility test for a three-placement repeatability-QC rule.

Diagnostic/exploratory only.

This script asks whether the spread of three independent CV placements is
informative about specimen-level accuracy relative to the manual reference.

It does NOT:
- modify V1/V2,
- tune the frozen endface-hybrid estimator,
- select or optimize a QC threshold from V2,
- claim prospective validation of a retry/acceptance protocol.

The analysis reports continuous associations and several predeclared spread
cutoffs for both the recorded V2 PCA estimator and the frozen endface hybrid.

For each specimen:
- reported value = mean of the three CV placements
- internal QC signal = max(CV) - min(CV)
- accuracy error = reported value - manual-reference mean
"""

from __future__ import annotations

import csv
from collections import defaultdict
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
MANUAL_CSV = DATA_ROOT / "manual_reference_observations.csv"
SPECIMEN_CSV = DATA_ROOT / "formal_validation_specimens.csv"

OUTPUT_DIR = DATA_ROOT / "derived_v2/three_placement_qc_feasibility"

EXPECTED_OBSERVATIONS = 180
EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}

LSL_IN = 0.9900
USL_IN = 1.0100

# Predeclared diagnostic QC thresholds. These are descriptive only and are not
# "optimized" from V2.
SPREAD_THRESHOLDS_IN = (
    0.0010,
    0.0015,
    0.0020,
    0.0025,
    0.0030,
)

# Descriptive accuracy thresholds. These do not replace any formal thesis
# criterion; they simply show whether spread discriminates larger errors.
ABS_ERROR_THRESHOLDS_IN = (
    0.0010,
    0.0020,
    0.0030,
)

# Integrity anchors from preserved specimen-level mean results.
EXPECTED_PCA_MEAN_BIAS = 0.000277
EXPECTED_PCA_MEAN_RMSE = 0.001538
EXPECTED_HYBRID_MEAN_BIAS = -0.000505
EXPECTED_HYBRID_MEAN_RMSE = 0.001601
INTEGRITY_TOLERANCE = 0.000002


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_yes(value: str) -> bool:
    return value.strip().upper() in {"YES", "TRUE", "1"}


def classification(reference: float, measured: float) -> str:
    ref_ok = LSL_IN <= reference <= USL_IN
    meas_ok = LSL_IN <= measured <= USL_IN
    if ref_ok and meas_ok:
        return "TRUE_CONFORMING"
    if ref_ok and not meas_ok:
        return "FALSE_FAIL"
    if not ref_ok and meas_ok:
        return "FALSE_PASS"
    return "TRUE_NONCONFORMING"


def summarize_subset(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "n": 0,
            "mae_in": float("nan"),
            "rmse_in": float("nan"),
            "mean_abs_error_in": float("nan"),
            "median_abs_error_in": float("nan"),
            "p95_abs_error_in": float("nan"),
            "max_abs_error_in": float("nan"),
            "false_passes": 0,
            "false_fails": 0,
        }

    abs_errors = [float(r["abs_error_in"]) for r in rows]
    sq_errors = [float(r["error_in"]) ** 2 for r in rows]
    ordered = sorted(abs_errors)
    rank = math.ceil(0.95 * len(ordered))
    return {
        "n": len(rows),
        "mae_in": statistics.fmean(abs_errors),
        "rmse_in": math.sqrt(statistics.fmean(sq_errors)),
        "mean_abs_error_in": statistics.fmean(abs_errors),
        "median_abs_error_in": statistics.median(abs_errors),
        "p95_abs_error_in": ordered[rank - 1],
        "max_abs_error_in": max(abs_errors),
        "false_passes": sum(r["classification"] == "FALSE_PASS" for r in rows),
        "false_fails": sum(r["classification"] == "FALSE_FAIL" for r in rows),
    }


def correlation(x: list[float], y: list[float]) -> tuple[float, float]:
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return float("nan"), float("nan")
    return (
        float(stats.pearsonr(x, y).statistic),
        float(stats.spearmanr(x, y).statistic),
    )


def point_biserial(binary: list[int], continuous: list[float]) -> float:
    if len(set(binary)) < 2:
        return float("nan")
    return float(stats.pointbiserialr(binary, continuous).statistic)


def build_rows(
    grouped_cv: dict[str, dict[int, float]],
    manual_mean: dict[str, float],
    estimator_name: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pid in sorted(grouped_cv, key=int):
        values = [grouped_cv[pid][r] for r in (1, 2, 3)]
        reported = statistics.fmean(values)
        reference = manual_mean[pid]
        error = reported - reference
        rows.append(
            {
                "estimator": estimator_name,
                "part_id": pid,
                "cv_1_in": values[0],
                "cv_2_in": values[1],
                "cv_3_in": values[2],
                "spread_in": max(values) - min(values),
                "reported_mean3_in": reported,
                "manual_mean_in": reference,
                "error_in": error,
                "abs_error_in": abs(error),
                "classification": classification(reference, reported),
            }
        )
    return rows


def integrity_metrics(rows: list[dict[str, Any]]) -> tuple[float, float]:
    errors = [float(r["error_in"]) for r in rows]
    bias = statistics.fmean(errors)
    rmse = math.sqrt(statistics.fmean(e * e for e in errors))
    return bias, rmse


def analyze_estimator(
    rows: list[dict[str, Any]],
    estimator_label: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    spreads = [float(r["spread_in"]) for r in rows]
    abs_errors = [float(r["abs_error_in"]) for r in rows]
    pearson, spearman = correlation(spreads, abs_errors)

    continuous = {
        "estimator": estimator_label,
        "spread_abs_error_pearson": pearson,
        "spread_abs_error_spearman": spearman,
        "median_spread_in": statistics.median(spreads),
        "mean_spread_in": statistics.fmean(spreads),
        "max_spread_in": max(spreads),
        "median_abs_error_in": statistics.median(abs_errors),
        "mean_abs_error_in": statistics.fmean(abs_errors),
    }

    for error_threshold in ABS_ERROR_THRESHOLDS_IN:
        binary = [int(ae > error_threshold) for ae in abs_errors]
        continuous[
            f"point_biserial_spread_vs_abs_error_gt_{error_threshold:.4f}"
        ] = point_biserial(binary, spreads)

    threshold_rows: list[dict[str, Any]] = []
    for threshold in SPREAD_THRESHOLDS_IN:
        accepted = [r for r in rows if float(r["spread_in"]) <= threshold]
        rejected = [r for r in rows if float(r["spread_in"]) > threshold]

        a = summarize_subset(accepted)
        rj = summarize_subset(rejected)

        threshold_rows.append(
            {
                "estimator": estimator_label,
                "spread_threshold_in": threshold,
                "accepted_n": len(accepted),
                "accepted_pct": 100.0 * len(accepted) / len(rows),
                "rejected_n": len(rejected),
                "accepted_mae_in": a["mae_in"],
                "accepted_rmse_in": a["rmse_in"],
                "accepted_p95_abs_error_in": a["p95_abs_error_in"],
                "accepted_max_abs_error_in": a["max_abs_error_in"],
                "accepted_false_passes": a["false_passes"],
                "accepted_false_fails": a["false_fails"],
                "rejected_mae_in": rj["mae_in"],
                "rejected_rmse_in": rj["rmse_in"],
                "rejected_p95_abs_error_in": rj["p95_abs_error_in"],
                "rejected_max_abs_error_in": rj["max_abs_error_in"],
                "rejected_false_passes": rj["false_passes"],
                "rejected_false_fails": rj["false_fails"],
                "accepted_abs_error_gt_0p001": sum(
                    float(x["abs_error_in"]) > 0.001 for x in accepted
                ),
                "accepted_abs_error_gt_0p002": sum(
                    float(x["abs_error_in"]) > 0.002 for x in accepted
                ),
                "accepted_abs_error_gt_0p003": sum(
                    float(x["abs_error_in"]) > 0.003 for x in accepted
                ),
                "rejected_abs_error_gt_0p001": sum(
                    float(x["abs_error_in"]) > 0.001 for x in rejected
                ),
                "rejected_abs_error_gt_0p002": sum(
                    float(x["abs_error_in"]) > 0.002 for x in rejected
                ),
                "rejected_abs_error_gt_0p003": sum(
                    float(x["abs_error_in"]) > 0.003 for x in rejected
                ),
            }
        )

    return continuous, threshold_rows


def main() -> int:
    v2_all = read_csv(V2_CSV)
    hybrid_all = read_csv(HYBRID_CSV)
    manual_all = read_csv(MANUAL_CSV)
    specimen_rows = read_csv(SPECIMEN_CSV)

    v2 = [
        r for r in v2_all
        if r["measurement_status"].strip().upper() == "VALID"
        and not is_yes(r["protocol_invalid"])
    ]
    hybrid = [
        r for r in hybrid_all
        if str(r["passed"]).strip().lower() in {"true", "1", "yes"}
    ]
    manual = [
        r for r in manual_all
        if is_yes(r["measurement_valid"])
        and not is_yes(r["protocol_invalid"])
    ]

    if len(v2) != EXPECTED_OBSERVATIONS:
        fail(f"Expected 180 V2 PCA observations, found {len(v2)}")
    if len(hybrid) != EXPECTED_OBSERVATIONS:
        fail(f"Expected 180 hybrid observations, found {len(hybrid)}")
    if len(manual) != EXPECTED_OBSERVATIONS:
        fail(f"Expected 180 manual observations, found {len(manual)}")
    if len(specimen_rows) != EXPECTED_SPECIMENS:
        fail(f"Expected 60 specimen rows, found {len(specimen_rows)}")

    specimen_ids = {r["part_id"] for r in specimen_rows}

    pca_by_part: dict[str, dict[int, float]] = defaultdict(dict)
    hybrid_by_part: dict[str, dict[int, float]] = defaultdict(dict)
    manual_by_part: dict[str, dict[int, float]] = defaultdict(dict)

    for r in v2:
        pca_by_part[r["part_id"]][int(r["cv_round"])] = float(r["oal_in"])
    for r in hybrid:
        hybrid_by_part[r["part_id"]][int(r["cv_round"])] = float(
            r["hybrid_oal_in"]
        )
    for r in manual:
        manual_by_part[r["part_id"]][int(r["manual_round"])] = float(
            r["reading_in"]
        )

    for label, grouped in (
        ("PCA", pca_by_part),
        ("Hybrid", hybrid_by_part),
        ("Manual", manual_by_part),
    ):
        if set(grouped) != specimen_ids:
            fail(f"{label} specimen population mismatch.")
        for pid, rounds in grouped.items():
            if set(rounds) != EXPECTED_ROUNDS:
                fail(f"{label} part {pid}: incomplete rounds {sorted(rounds)}")

    manual_mean = {
        pid: statistics.fmean(values.values())
        for pid, values in manual_by_part.items()
    }

    pca_rows = build_rows(pca_by_part, manual_mean, "pca")
    hybrid_rows = build_rows(hybrid_by_part, manual_mean, "endface_hybrid")

    pca_bias, pca_rmse = integrity_metrics(pca_rows)
    hybrid_bias, hybrid_rmse = integrity_metrics(hybrid_rows)

    integrity_checks = [
        ("PCA bias", pca_bias, EXPECTED_PCA_MEAN_BIAS),
        ("PCA RMSE", pca_rmse, EXPECTED_PCA_MEAN_RMSE),
        ("Hybrid bias", hybrid_bias, EXPECTED_HYBRID_MEAN_BIAS),
        ("Hybrid RMSE", hybrid_rmse, EXPECTED_HYBRID_MEAN_RMSE),
    ]
    failures = [
        (label, actual, expected)
        for label, actual, expected in integrity_checks
        if abs(actual - expected) > INTEGRITY_TOLERANCE
    ]
    if failures:
        text = "\n".join(
            f"{label}: actual={actual:.9f}, expected≈{expected:.9f}"
            for label, actual, expected in failures
        )
        fail("Integrity baseline failed:\n" + text)

    pca_cont, pca_thresholds = analyze_estimator(pca_rows, "pca")
    hyb_cont, hyb_thresholds = analyze_estimator(
        hybrid_rows,
        "endface_hybrid",
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_specimen_rows = pca_rows + hybrid_rows
    with (OUTPUT_DIR / "qc_specimen_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(all_specimen_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(all_specimen_rows)

    threshold_rows = pca_thresholds + hyb_thresholds
    with (OUTPUT_DIR / "qc_threshold_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(threshold_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(threshold_rows)

    continuous_rows = [pca_cont, hyb_cont]
    with (OUTPUT_DIR / "qc_continuous_association.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        fieldnames = sorted(
            {key for row in continuous_rows for key in row.keys()}
        )
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(continuous_rows)

    def fmt(v: float) -> str:
        return "NA" if isinstance(v, float) and math.isnan(v) else f"{v:.6f}"

    lines = [
        "# Three-Placement Repeatability-QC Feasibility",
        "",
        "**Exploratory diagnostic only. No QC threshold is selected or validated by this analysis.**",
        "",
        "## Continuous association: spread versus absolute error",
        "",
        f"- PCA Pearson: {pca_cont['spread_abs_error_pearson']:+.4f}",
        f"- PCA Spearman: {pca_cont['spread_abs_error_spearman']:+.4f}",
        f"- Hybrid Pearson: {hyb_cont['spread_abs_error_pearson']:+.4f}",
        f"- Hybrid Spearman: {hyb_cont['spread_abs_error_spearman']:+.4f}",
        "",
        "A strong positive association would support using internal three-placement spread as an accuracy-risk signal. Weak association would indicate that good internal agreement does not reliably imply accuracy relative to the manual reference.",
        "",
        "## Predeclared spread thresholds — endface hybrid",
        "",
        "| Spread limit | Accept | Availability | Accepted MAE | Accepted RMSE | Accepted P95 abs | Accepted max abs | FP | FF |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in hyb_thresholds:
        lines.append(
            f"| {float(row['spread_threshold_in']):.4f} in "
            f"| {row['accepted_n']}/60 "
            f"| {float(row['accepted_pct']):.1f}% "
            f"| {fmt(float(row['accepted_mae_in']))} "
            f"| {fmt(float(row['accepted_rmse_in']))} "
            f"| {fmt(float(row['accepted_p95_abs_error_in']))} "
            f"| {fmt(float(row['accepted_max_abs_error_in']))} "
            f"| {row['accepted_false_passes']} "
            f"| {row['accepted_false_fails']} |"
        )

    lines.extend(
        [
            "",
            "## Predeclared spread thresholds — PCA",
            "",
            "| Spread limit | Accept | Availability | Accepted MAE | Accepted RMSE | Accepted P95 abs | Accepted max abs | FP | FF |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )

    for row in pca_thresholds:
        lines.append(
            f"| {float(row['spread_threshold_in']):.4f} in "
            f"| {row['accepted_n']}/60 "
            f"| {float(row['accepted_pct']):.1f}% "
            f"| {fmt(float(row['accepted_mae_in']))} "
            f"| {fmt(float(row['accepted_rmse_in']))} "
            f"| {fmt(float(row['accepted_p95_abs_error_in']))} "
            f"| {fmt(float(row['accepted_max_abs_error_in']))} "
            f"| {row['accepted_false_passes']} "
            f"| {row['accepted_false_fails']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation guardrail",
            "",
            "These cutoffs are descriptive feasibility checks only. V2 must not be used to select an optimized acceptance threshold and then claim that threshold as validated. A practical QC/retry protocol would need a threshold defined from independent development evidence and then prospectively validated, including availability, retry burden, accuracy, classification, and repeatability of the complete procedure.",
            "",
        ]
    )

    summary_path = OUTPUT_DIR / "SUMMARY.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 90)
    print("THREE-PLACEMENT REPEATABILITY-QC FEASIBILITY")
    print("=" * 90)
    print("Integrity baseline: PASS")
    print()
    print("SPREAD vs ABSOLUTE ERROR")
    print(
        f"PCA:             Pearson {pca_cont['spread_abs_error_pearson']:+.4f}  "
        f"Spearman {pca_cont['spread_abs_error_spearman']:+.4f}"
    )
    print(
        f"Endface hybrid:  Pearson {hyb_cont['spread_abs_error_pearson']:+.4f}  "
        f"Spearman {hyb_cont['spread_abs_error_spearman']:+.4f}"
    )
    print()
    print("ENDFACE HYBRID — PREDECLARED SPREAD CUTS")
    for row in hyb_thresholds:
        print(
            f"  <= {float(row['spread_threshold_in']):.4f} in: "
            f"accept {row['accepted_n']:2d}/60 "
            f"({float(row['accepted_pct']):5.1f}%); "
            f"MAE {fmt(float(row['accepted_mae_in']))}; "
            f"RMSE {fmt(float(row['accepted_rmse_in']))}; "
            f"P95abs {fmt(float(row['accepted_p95_abs_error_in']))}; "
            f"max {fmt(float(row['accepted_max_abs_error_in']))}; "
            f"FP {row['accepted_false_passes']}; "
            f"FF {row['accepted_false_fails']}"
        )
    print()
    print("PCA — PREDECLARED SPREAD CUTS")
    for row in pca_thresholds:
        print(
            f"  <= {float(row['spread_threshold_in']):.4f} in: "
            f"accept {row['accepted_n']:2d}/60 "
            f"({float(row['accepted_pct']):5.1f}%); "
            f"MAE {fmt(float(row['accepted_mae_in']))}; "
            f"RMSE {fmt(float(row['accepted_rmse_in']))}; "
            f"P95abs {fmt(float(row['accepted_p95_abs_error_in']))}; "
            f"max {fmt(float(row['accepted_max_abs_error_in']))}; "
            f"FP {row['accepted_false_passes']}; "
            f"FF {row['accepted_false_fails']}"
        )
    print()
    print("IMPORTANT: descriptive feasibility only; no QC threshold is selected here.")
    print(f"Wrote: {summary_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
