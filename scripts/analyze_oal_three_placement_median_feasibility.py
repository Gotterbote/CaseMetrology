#!/usr/bin/env python3
"""Retrospective feasibility test of a three-placement MEDIAN OAL protocol.

This is diagnostic/exploratory only. It does not alter V1/V2, does not tune the
frozen estimator, and does not constitute prospective validation of a
multi-placement protocol.

It compares four specimen-level estimands using the same 60 formal specimens:
1) Recorded V2 PCA mean of 3 placements (integrity baseline)
2) Recorded V2 PCA median of 3 placements
3) Frozen endface-hybrid mean of 3 placements (integrity baseline)
4) Frozen endface-hybrid median of 3 placements

Manual reference is the mean of the three valid manual-reference rounds.

Important limitation:
V2 contains only one set of three placements per specimen. Therefore this
script can assess accuracy/classification feasibility of a median-of-three
reported value, but it CANNOT estimate repeatability of the complete
median-of-three protocol. Prospective repeatability would require repeated
independent 3-placement groups.
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

OUTPUT_DIR = DATA_ROOT / "derived_v2/three_placement_median_feasibility"

EXPECTED_OBSERVATIONS = 180
EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}

LSL_IN = 0.9900
USL_IN = 1.0100

# Integrity anchors already established in the preserved analyses.
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


def empirical_nearest_rank(values: list[float], p: float) -> tuple[float, int]:
    if not values:
        fail("Cannot compute percentile on empty sequence.")
    ordered = sorted(values)
    rank = math.ceil(p * len(ordered))
    return ordered[rank - 1], rank


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


def summarize(
    reported_by_part: dict[str, float],
    manual_mean_by_part: dict[str, float],
) -> tuple[dict[str, Any], dict[str, str]]:
    if set(reported_by_part) != set(manual_mean_by_part):
        fail("Reported-value population does not match manual-reference population.")

    errors: list[float] = []
    abs_errors: list[float] = []
    classes: dict[str, str] = {}

    for pid in sorted(reported_by_part, key=int):
        error = reported_by_part[pid] - manual_mean_by_part[pid]
        errors.append(error)
        abs_errors.append(abs(error))
        classes[pid] = classification(
            manual_mean_by_part[pid],
            reported_by_part[pid],
        )

    n = len(errors)
    bias = statistics.fmean(errors)
    se = statistics.stdev(errors) / math.sqrt(n)
    tcrit = stats.t.ppf(0.975, df=n - 1)
    p95, p95_rank = empirical_nearest_rank(abs_errors, 0.95)

    counts = {
        label: sum(value == label for value in classes.values())
        for label in (
            "TRUE_CONFORMING",
            "TRUE_NONCONFORMING",
            "FALSE_PASS",
            "FALSE_FAIL",
        )
    }

    metrics = {
        "n_specimens": n,
        "bias_in": bias,
        "bias_95_ci_lower_in": bias - tcrit * se,
        "bias_95_ci_upper_in": bias + tcrit * se,
        "median_signed_error_in": statistics.median(errors),
        "mae_in": statistics.fmean(abs_errors),
        "rmse_in": math.sqrt(statistics.fmean(e * e for e in errors)),
        "p95_absolute_error_in": p95,
        "p95_absolute_error_rank": p95_rank,
        "maximum_absolute_error_in": max(abs_errors),
        "true_conforming": counts["TRUE_CONFORMING"],
        "true_nonconforming": counts["TRUE_NONCONFORMING"],
        "false_passes": counts["FALSE_PASS"],
        "false_fails": counts["FALSE_FAIL"],
    }
    return metrics, classes


def close_enough(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= INTEGRITY_TOLERANCE


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
        fail(f"Expected 60 formal specimens, found {len(specimen_rows)}")

    specimen_ids = {r["part_id"] for r in specimen_rows}
    if len(specimen_ids) != EXPECTED_SPECIMENS:
        fail("Formal specimen IDs are not unique.")

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
        bad = {
            pid: sorted(rounds)
            for pid, rounds in grouped.items()
            if set(rounds) != EXPECTED_ROUNDS
        }
        if bad:
            fail(f"{label} incomplete round coverage: {bad}")

    manual_mean = {
        pid: statistics.fmean(values.values())
        for pid, values in manual_by_part.items()
    }

    estimands = {
        "pca_mean3": {
            pid: statistics.fmean(values.values())
            for pid, values in pca_by_part.items()
        },
        "pca_median3": {
            pid: statistics.median(values.values())
            for pid, values in pca_by_part.items()
        },
        "hybrid_mean3": {
            pid: statistics.fmean(values.values())
            for pid, values in hybrid_by_part.items()
        },
        "hybrid_median3": {
            pid: statistics.median(values.values())
            for pid, values in hybrid_by_part.items()
        },
    }

    metrics: dict[str, dict[str, Any]] = {}
    classes: dict[str, dict[str, str]] = {}
    for name, reported in estimands.items():
        metrics[name], classes[name] = summarize(reported, manual_mean)

    # Verify that the two mean-of-three rows reproduce the already-preserved
    # V2 and hybrid specimen-level accuracy metrics closely.
    checks = [
        (
            "PCA mean bias",
            metrics["pca_mean3"]["bias_in"],
            EXPECTED_PCA_MEAN_BIAS,
        ),
        (
            "PCA mean RMSE",
            metrics["pca_mean3"]["rmse_in"],
            EXPECTED_PCA_MEAN_RMSE,
        ),
        (
            "Hybrid mean bias",
            metrics["hybrid_mean3"]["bias_in"],
            EXPECTED_HYBRID_MEAN_BIAS,
        ),
        (
            "Hybrid mean RMSE",
            metrics["hybrid_mean3"]["rmse_in"],
            EXPECTED_HYBRID_MEAN_RMSE,
        ),
    ]
    failed_checks = [
        (label, actual, expected)
        for label, actual, expected in checks
        if not close_enough(actual, expected)
    ]
    if failed_checks:
        details = "\n".join(
            f"{label}: actual={actual:.9f}, expected≈{expected:.9f}"
            for label, actual, expected in failed_checks
        )
        fail(
            "Integrity baseline did not reproduce expected preserved metrics:\n"
            + details
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    per_specimen_rows: list[dict[str, Any]] = []
    for pid in sorted(specimen_ids, key=int):
        pca_vals = [pca_by_part[pid][r] for r in (1, 2, 3)]
        hyb_vals = [hybrid_by_part[pid][r] for r in (1, 2, 3)]

        row = {
            "part_id": pid,
            "manual_mean_in": manual_mean[pid],
            "pca_1_in": pca_vals[0],
            "pca_2_in": pca_vals[1],
            "pca_3_in": pca_vals[2],
            "pca_range_in": max(pca_vals) - min(pca_vals),
            "pca_mean3_in": estimands["pca_mean3"][pid],
            "pca_median3_in": estimands["pca_median3"][pid],
            "pca_mean3_abs_error_in": abs(
                estimands["pca_mean3"][pid] - manual_mean[pid]
            ),
            "pca_median3_abs_error_in": abs(
                estimands["pca_median3"][pid] - manual_mean[pid]
            ),
            "hybrid_1_in": hyb_vals[0],
            "hybrid_2_in": hyb_vals[1],
            "hybrid_3_in": hyb_vals[2],
            "hybrid_range_in": max(hyb_vals) - min(hyb_vals),
            "hybrid_mean3_in": estimands["hybrid_mean3"][pid],
            "hybrid_median3_in": estimands["hybrid_median3"][pid],
            "hybrid_mean3_abs_error_in": abs(
                estimands["hybrid_mean3"][pid] - manual_mean[pid]
            ),
            "hybrid_median3_abs_error_in": abs(
                estimands["hybrid_median3"][pid] - manual_mean[pid]
            ),
            "hybrid_mean3_classification": classes["hybrid_mean3"][pid],
            "hybrid_median3_classification": classes["hybrid_median3"][pid],
        }
        per_specimen_rows.append(row)

    with (OUTPUT_DIR / "three_placement_median_specimen_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(per_specimen_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(per_specimen_rows)

    metric_rows: list[dict[str, Any]] = []
    for name in ("pca_mean3", "pca_median3", "hybrid_mean3", "hybrid_median3"):
        metric_rows.append({"estimand": name, **metrics[name]})

    with (OUTPUT_DIR / "three_placement_median_metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(metric_rows[0].keys()))
        writer.writeheader()
        writer.writerows(metric_rows)

    # Direct mean-vs-median comparisons.
    hybrid_median_better = sum(
        row["hybrid_median3_abs_error_in"] < row["hybrid_mean3_abs_error_in"]
        for row in per_specimen_rows
    )
    hybrid_mean_better = sum(
        row["hybrid_mean3_abs_error_in"] < row["hybrid_median3_abs_error_in"]
        for row in per_specimen_rows
    )
    hybrid_equal = EXPECTED_SPECIMENS - hybrid_median_better - hybrid_mean_better

    pca_median_better = sum(
        row["pca_median3_abs_error_in"] < row["pca_mean3_abs_error_in"]
        for row in per_specimen_rows
    )
    pca_mean_better = sum(
        row["pca_mean3_abs_error_in"] < row["pca_median3_abs_error_in"]
        for row in per_specimen_rows
    )
    pca_equal = EXPECTED_SPECIMENS - pca_median_better - pca_mean_better

    hmean = metrics["hybrid_mean3"]
    hmed = metrics["hybrid_median3"]
    pmean = metrics["pca_mean3"]
    pmed = metrics["pca_median3"]

    lines = [
        "# Three-Placement Median Protocol — Retrospective Feasibility",
        "",
        "**Exploratory feasibility analysis only. This does not revise formal V2 and does not prospectively validate a multi-placement protocol.**",
        "",
        "## Critical limitation",
        "",
        "The V2 dataset contains one three-placement group per specimen. It can therefore evaluate the accuracy and classification behavior of a median-of-three reported value, but it cannot estimate repeatability of the complete median-of-three protocol. Prospective repeatability requires multiple independent three-placement groups per specimen.",
        "",
        "## Integrity baseline",
        "",
        f"- PCA mean-of-three bias: {pmean['bias_in']:+.6f} in",
        f"- PCA mean-of-three RMSE: {pmean['rmse_in']:.6f} in",
        f"- Hybrid mean-of-three bias: {hmean['bias_in']:+.6f} in",
        f"- Hybrid mean-of-three RMSE: {hmean['rmse_in']:.6f} in",
        "",
        "These reproduce the previously preserved specimen-level mean results within the script's integrity tolerance.",
        "",
        "## PCA: mean-of-three versus median-of-three",
        "",
        "| Metric | Mean of 3 | Median of 3 |",
        "|---|---:|---:|",
        f"| Bias | {pmean['bias_in']:+.6f} in | {pmed['bias_in']:+.6f} in |",
        f"| MAE | {pmean['mae_in']:.6f} in | {pmed['mae_in']:.6f} in |",
        f"| RMSE | {pmean['rmse_in']:.6f} in | {pmed['rmse_in']:.6f} in |",
        f"| P95 absolute error | {pmean['p95_absolute_error_in']:.6f} in | {pmed['p95_absolute_error_in']:.6f} in |",
        f"| Maximum absolute error | {pmean['maximum_absolute_error_in']:.6f} in | {pmed['maximum_absolute_error_in']:.6f} in |",
        f"| False passes | {pmean['false_passes']} | {pmed['false_passes']} |",
        f"| False fails | {pmean['false_fails']} | {pmed['false_fails']} |",
        "",
        f"- PCA median had smaller absolute error on {pca_median_better}/60 specimens.",
        f"- PCA mean had smaller absolute error on {pca_mean_better}/60 specimens.",
        f"- Equal absolute error: {pca_equal}/60 specimens.",
        "",
        "## Endface hybrid: mean-of-three versus median-of-three",
        "",
        "| Metric | Mean of 3 | Median of 3 |",
        "|---|---:|---:|",
        f"| Bias | {hmean['bias_in']:+.6f} in | {hmed['bias_in']:+.6f} in |",
        f"| MAE | {hmean['mae_in']:.6f} in | {hmed['mae_in']:.6f} in |",
        f"| RMSE | {hmean['rmse_in']:.6f} in | {hmed['rmse_in']:.6f} in |",
        f"| P95 absolute error | {hmean['p95_absolute_error_in']:.6f} in | {hmed['p95_absolute_error_in']:.6f} in |",
        f"| Maximum absolute error | {hmean['maximum_absolute_error_in']:.6f} in | {hmed['maximum_absolute_error_in']:.6f} in |",
        f"| False passes | {hmean['false_passes']} | {hmed['false_passes']} |",
        f"| False fails | {hmean['false_fails']} | {hmed['false_fails']} |",
        "",
        f"- Hybrid median had smaller absolute error on {hybrid_median_better}/60 specimens.",
        f"- Hybrid mean had smaller absolute error on {hybrid_mean_better}/60 specimens.",
        f"- Equal absolute error: {hybrid_equal}/60 specimens.",
        "",
        "## Interpretation guardrail",
        "",
        "A favorable median-of-three accuracy result would justify considering a prospectively frozen multi-placement measurement protocol. It would not convert the original V2 single-placement repeatability criterion into a pass. A new protocol would require prospective validation, including repeatability of repeated independent three-placement groups.",
        "",
    ]

    summary = OUTPUT_DIR / "SUMMARY.md"
    summary.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 90)
    print("THREE-PLACEMENT MEDIAN FEASIBILITY")
    print("=" * 90)
    print("Integrity baseline: PASS")
    print()
    print("PCA")
    print(
        f"  Mean3   bias {pmean['bias_in']:+.6f}  "
        f"MAE {pmean['mae_in']:.6f}  RMSE {pmean['rmse_in']:.6f}  "
        f"P95 abs {pmean['p95_absolute_error_in']:.6f}  "
        f"max {pmean['maximum_absolute_error_in']:.6f}"
    )
    print(
        f"  Median3 bias {pmed['bias_in']:+.6f}  "
        f"MAE {pmed['mae_in']:.6f}  RMSE {pmed['rmse_in']:.6f}  "
        f"P95 abs {pmed['p95_absolute_error_in']:.6f}  "
        f"max {pmed['maximum_absolute_error_in']:.6f}"
    )
    print(
        f"  Classification Median3: false pass={pmed['false_passes']}, "
        f"false fail={pmed['false_fails']}"
    )
    print(
        f"  Median better / mean better / equal: "
        f"{pca_median_better} / {pca_mean_better} / {pca_equal}"
    )
    print()
    print("ENDFACE HYBRID")
    print(
        f"  Mean3   bias {hmean['bias_in']:+.6f}  "
        f"MAE {hmean['mae_in']:.6f}  RMSE {hmean['rmse_in']:.6f}  "
        f"P95 abs {hmean['p95_absolute_error_in']:.6f}  "
        f"max {hmean['maximum_absolute_error_in']:.6f}"
    )
    print(
        f"  Median3 bias {hmed['bias_in']:+.6f}  "
        f"MAE {hmed['mae_in']:.6f}  RMSE {hmed['rmse_in']:.6f}  "
        f"P95 abs {hmed['p95_absolute_error_in']:.6f}  "
        f"max {hmed['maximum_absolute_error_in']:.6f}"
    )
    print(
        f"  Classification Median3: false pass={hmed['false_passes']}, "
        f"false fail={hmed['false_fails']}"
    )
    print(
        f"  Median better / mean better / equal: "
        f"{hybrid_median_better} / {hybrid_mean_better} / {hybrid_equal}"
    )
    print()
    print("IMPORTANT: this tests accuracy feasibility only; it does not estimate")
    print("repeatability of a complete median-of-three protocol.")
    print()
    print(f"Wrote: {summary.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
