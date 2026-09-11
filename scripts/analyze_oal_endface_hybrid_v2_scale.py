#!/usr/bin/env python3
"""Decompose frozen endface-hybrid V2 repositioning into pixel-length and calibration-scale components.

Diagnostic only. This script does not reprocess images and does not modify or
tune any estimator. It reads the already-recorded frozen retrospective
observation table.

For each specimen:
- actual = hybrid_length_pixels / effective_ppi
- pixel_only = hybrid_length_pixels / specimen_mean_ppi
- scale_only = specimen_mean_length_pixels / effective_ppi

Pairwise repeatability of these counterfactual quantities indicates whether the
remaining placement variation is primarily in the observed pixel geometry or
in the spatial-calibration scale selected for each placement.
"""

from __future__ import annotations

import csv
from collections import defaultdict
import math
from pathlib import Path
import statistics

from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
INPUT = (
    REPO_ROOT
    / "data/oal_validation/derived_v2/endface_hybrid_retrospective/"
      "v2_endface_hybrid_observations.csv"
)
OUTPUT_DIR = (
    REPO_ROOT
    / "data/oal_validation/derived_v2/endface_hybrid_scale_diagnostics"
)

EXPECTED_OBSERVATIONS = 180
EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}


def fail(message: str) -> None:
    raise RuntimeError(message)


def nearest_rank(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        fail("Empty percentile input.")
    return ordered[math.ceil(p * len(ordered)) - 1]


def pairs(values: dict[int, float]) -> list[float]:
    if set(values) != EXPECTED_ROUNDS:
        fail(f"Expected rounds 1,2,3; found {sorted(values)}")
    return [
        abs(values[1] - values[2]),
        abs(values[1] - values[3]),
        abs(values[2] - values[3]),
    ]


def pearson(x: list[float], y: list[float]) -> float:
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return float("nan")
    return float(stats.pearsonr(x, y).statistic)


def spearman(x: list[float], y: list[float]) -> float:
    if len(x) < 3 or len(set(x)) < 2 or len(set(y)) < 2:
        return float("nan")
    return float(stats.spearmanr(x, y).statistic)


def main() -> int:
    if not INPUT.is_file():
        fail(f"Missing input: {INPUT}")

    with INPUT.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    passing = [
        r for r in rows
        if str(r["passed"]).strip().lower() in {"true", "1", "yes"}
    ]
    if len(passing) != EXPECTED_OBSERVATIONS:
        fail(
            f"Expected {EXPECTED_OBSERVATIONS} passing hybrid observations, "
            f"found {len(passing)}"
        )

    by_part: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in passing:
        by_part[r["part_id"]].append(r)

    if len(by_part) != EXPECTED_SPECIMENS:
        fail(f"Expected {EXPECTED_SPECIMENS} specimens, found {len(by_part)}")

    actual_pairwise: list[float] = []
    pixel_only_pairwise: list[float] = []
    scale_only_pairwise: list[float] = []

    centered_actual: list[float] = []
    centered_pixels: list[float] = []
    centered_ppi: list[float] = []
    centered_angle: list[float] = []

    specimen_rows = []

    for part_id in sorted(by_part, key=int):
        part_rows = sorted(by_part[part_id], key=lambda r: int(r["cv_round"]))
        rounds = {int(r["cv_round"]) for r in part_rows}
        if rounds != EXPECTED_ROUNDS:
            fail(f"Part {part_id}: incomplete rounds {sorted(rounds)}")

        px = {
            int(r["cv_round"]): float(r["hybrid_length_pixels"])
            for r in part_rows
        }
        ppi = {
            int(r["cv_round"]): float(r["hybrid_effective_ppi"])
            for r in part_rows
        }
        angle = {
            int(r["cv_round"]): float(r["hybrid_angle_degrees"])
            for r in part_rows
        }
        actual = {
            int(r["cv_round"]): float(r["hybrid_oal_in"])
            for r in part_rows
        }

        mean_px = statistics.fmean(px.values())
        mean_ppi = statistics.fmean(ppi.values())
        mean_actual = statistics.fmean(actual.values())
        mean_angle = statistics.fmean(angle.values())

        # Counterfactuals:
        # Pixel-only: placement-specific observed pixel length with calibration
        # scale held fixed at that specimen's three-round mean.
        pixel_only = {rnd: px[rnd] / mean_ppi for rnd in EXPECTED_ROUNDS}

        # Scale-only: observed pixel length held fixed while placement-specific
        # calibration scale varies.
        scale_only = {rnd: mean_px / ppi[rnd] for rnd in EXPECTED_ROUNDS}

        a_pairs = pairs(actual)
        p_pairs = pairs(pixel_only)
        s_pairs = pairs(scale_only)

        actual_pairwise.extend(a_pairs)
        pixel_only_pairwise.extend(p_pairs)
        scale_only_pairwise.extend(s_pairs)

        for rnd in (1, 2, 3):
            centered_actual.append(actual[rnd] - mean_actual)
            centered_pixels.append(px[rnd] - mean_px)
            centered_ppi.append(ppi[rnd] - mean_ppi)
            centered_angle.append(angle[rnd] - mean_angle)

        specimen_rows.append(
            {
                "part_id": part_id,
                "actual_range_in": max(actual.values()) - min(actual.values()),
                "pixel_only_range_in": max(pixel_only.values()) - min(pixel_only.values()),
                "scale_only_range_in": max(scale_only.values()) - min(scale_only.values()),
                "pixel_length_range_px": max(px.values()) - min(px.values()),
                "effective_ppi_range": max(ppi.values()) - min(ppi.values()),
                "angle_range_deg": max(angle.values()) - min(angle.values()),
            }
        )

    metrics = {
        "actual_p95": nearest_rank(actual_pairwise, 0.95),
        "pixel_only_p95": nearest_rank(pixel_only_pairwise, 0.95),
        "scale_only_p95": nearest_rank(scale_only_pairwise, 0.95),
        "actual_max": max(actual_pairwise),
        "pixel_only_max": max(pixel_only_pairwise),
        "scale_only_max": max(scale_only_pairwise),
        "corr_actual_pixels_pearson": pearson(centered_actual, centered_pixels),
        "corr_actual_pixels_spearman": spearman(centered_actual, centered_pixels),
        "corr_actual_ppi_pearson": pearson(centered_actual, centered_ppi),
        "corr_actual_ppi_spearman": spearman(centered_actual, centered_ppi),
        "corr_actual_angle_pearson": pearson(centered_actual, centered_angle),
        "corr_actual_angle_spearman": spearman(centered_actual, centered_angle),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "specimen_scale_decomposition.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(specimen_rows[0].keys()))
        writer.writeheader()
        writer.writerows(specimen_rows)

    lines = [
        "# Endface-Hybrid V2 Scale Decomposition",
        "",
        "**Diagnostic only. No estimator parameters are changed.**",
        "",
        "## Pairwise P95 repositioning",
        "",
        f"- Actual hybrid: {metrics['actual_p95']:.6f} in",
        f"- Pixel-length component with specimen calibration scale held fixed: {metrics['pixel_only_p95']:.6f} in",
        f"- Calibration-scale component with specimen pixel length held fixed: {metrics['scale_only_p95']:.6f} in",
        "",
        "## Maximum pairwise repositioning",
        "",
        f"- Actual hybrid: {metrics['actual_max']:.6f} in",
        f"- Pixel-length component: {metrics['pixel_only_max']:.6f} in",
        f"- Calibration-scale component: {metrics['scale_only_max']:.6f} in",
        "",
        "## Within-specimen centered correlations with actual hybrid OAL",
        "",
        f"- Pixel length Pearson: {metrics['corr_actual_pixels_pearson']:.4f}",
        f"- Pixel length Spearman: {metrics['corr_actual_pixels_spearman']:.4f}",
        f"- Effective PPI Pearson: {metrics['corr_actual_ppi_pearson']:.4f}",
        f"- Effective PPI Spearman: {metrics['corr_actual_ppi_spearman']:.4f}",
        f"- Geometry angle Pearson: {metrics['corr_actual_angle_pearson']:.4f}",
        f"- Geometry angle Spearman: {metrics['corr_actual_angle_spearman']:.4f}",
        "",
        "## Interpretation",
        "",
        "If the pixel-only P95 remains close to the actual hybrid P95 while the scale-only P95 is small, the remaining repositioning error is primarily present in the observed image geometry before inch conversion. If the scale-only component is substantial, spatial-calibration selection is materially contributing to placement sensitivity.",
        "",
    ]
    summary = OUTPUT_DIR / "SUMMARY.md"
    summary.write_text("\n".join(lines), encoding="utf-8")

    print("=" * 90)
    print("ENDFACE-HYBRID V2 SCALE / PIXEL DECOMPOSITION")
    print("=" * 90)
    print(f"Actual hybrid P95:       {metrics['actual_p95']:.6f} in")
    print(f"Pixel-only P95:          {metrics['pixel_only_p95']:.6f} in")
    print(f"Calibration-only P95:    {metrics['scale_only_p95']:.6f} in")
    print()
    print(f"Actual hybrid max:       {metrics['actual_max']:.6f} in")
    print(f"Pixel-only max:          {metrics['pixel_only_max']:.6f} in")
    print(f"Calibration-only max:    {metrics['scale_only_max']:.6f} in")
    print()
    print(
        "Centered actual vs pixel length: "
        f"Pearson {metrics['corr_actual_pixels_pearson']:.4f}; "
        f"Spearman {metrics['corr_actual_pixels_spearman']:.4f}"
    )
    print(
        "Centered actual vs effective PPI: "
        f"Pearson {metrics['corr_actual_ppi_pearson']:.4f}; "
        f"Spearman {metrics['corr_actual_ppi_spearman']:.4f}"
    )
    print(
        "Centered actual vs geometry angle: "
        f"Pearson {metrics['corr_actual_angle_pearson']:.4f}; "
        f"Spearman {metrics['corr_actual_angle_spearman']:.4f}"
    )
    print()
    print(f"Wrote: {summary.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
