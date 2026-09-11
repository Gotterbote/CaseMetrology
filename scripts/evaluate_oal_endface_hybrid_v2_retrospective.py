#!/usr/bin/env python3
"""Retrospective V2 evaluation of the pre-frozen endface-hybrid OAL estimator.

This is an exploratory retrospective analysis. It MUST NOT modify V1/V2 formal
records and MUST NOT be used to tune the estimator.

Guardrails:
- Verifies the frozen development script SHA-256 before use.
- Verifies 180 usable V2 observations and 60 specimens x 3 rounds.
- Reprocesses every V2 raw image with the recorded session blank.
- Requires exact/near-exact reproduction of the recorded V2 PCA OAL values
  before reporting hybrid results.
- Uses the already-frozen hybrid implementation by importing it from the
  frozen development script; no hybrid parameters are duplicated here.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import statistics
import subprocess
import sys
from typing import Any

from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]

FROZEN_HYBRID_SCRIPT = REPO_ROOT / "scripts/evaluate_oal_endface_hybrid_dev.py"
FROZEN_HYBRID_SHA256 = (
    "3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af"
)
FREEZE_COMMIT = "dbc4920"

DATA_ROOT = REPO_ROOT / "data/oal_validation"
V2_OBSERVATIONS = DATA_ROOT / "v2_cv_observations.csv"
MANUAL_OBSERVATIONS = DATA_ROOT / "manual_reference_observations.csv"
SPECIMENS = DATA_ROOT / "formal_validation_specimens.csv"
FORMAL_V2_ROOT = DATA_ROOT / "formal_cv_v2"

DEFAULT_OUTPUT_DIR = (
    DATA_ROOT / "derived_v2/endface_hybrid_retrospective"
)

EXPECTED_OBSERVATIONS = 180
EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}

LSL_IN = 0.9900
USL_IN = 1.0100

# Reproduction is expected to be exact on the authoritative Nano environment.
# This tiny tolerance is only to avoid false failure from text/float roundoff.
PCA_REPRODUCTION_TOLERANCE_IN = 1e-9


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"Required file is missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def is_yes(value: str) -> bool:
    return value.strip().upper() in {"YES", "TRUE", "1"}


def empirical_nearest_rank(
    values: list[float],
    probability: float,
) -> tuple[float, int]:
    if not values:
        fail("Cannot calculate percentile for an empty sequence.")
    ordered = sorted(values)
    rank = math.ceil(probability * len(ordered))
    return ordered[rank - 1], rank


def pairwise_three(values: list[float]) -> list[float]:
    if len(values) != 3:
        fail(f"Expected exactly 3 values, found {len(values)}")
    return [
        abs(values[0] - values[1]),
        abs(values[0] - values[2]),
        abs(values[1] - values[2]),
    ]


def git_head() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except Exception:
        return "UNKNOWN"


def load_frozen_hybrid_module():
    actual_hash = sha256_file(FROZEN_HYBRID_SCRIPT)
    if actual_hash != FROZEN_HYBRID_SHA256:
        fail(
            "Frozen hybrid implementation hash mismatch.\n"
            f"Expected: {FROZEN_HYBRID_SHA256}\n"
            f"Actual:   {actual_hash}\n"
            "STOP: do not perform the retrospective evaluation."
        )

    spec = importlib.util.spec_from_file_location(
        "frozen_endface_hybrid_dev",
        FROZEN_HYBRID_SCRIPT,
    )
    if spec is None or spec.loader is None:
        fail("Could not import the frozen hybrid implementation.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_inputs() -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, dict[str, str]],
]:
    v2_all = read_csv(V2_OBSERVATIONS)
    manual_all = read_csv(MANUAL_OBSERVATIONS)
    specimen_rows = read_csv(SPECIMENS)

    v2 = [
        row for row in v2_all
        if row["measurement_status"].strip().upper() == "VALID"
        and not is_yes(row["protocol_invalid"])
    ]
    manual = [
        row for row in manual_all
        if is_yes(row["measurement_valid"])
        and not is_yes(row["protocol_invalid"])
    ]

    if len(v2) != EXPECTED_OBSERVATIONS:
        fail(
            f"Expected {EXPECTED_OBSERVATIONS} usable V2 observations, "
            f"found {len(v2)}"
        )
    if len(manual) != EXPECTED_OBSERVATIONS:
        fail(
            f"Expected {EXPECTED_OBSERVATIONS} usable manual observations, "
            f"found {len(manual)}"
        )
    if len(specimen_rows) != EXPECTED_SPECIMENS:
        fail(
            f"Expected {EXPECTED_SPECIMENS} formal specimens, "
            f"found {len(specimen_rows)}"
        )

    specimen_by_id = {row["part_id"]: row for row in specimen_rows}
    if len(specimen_by_id) != EXPECTED_SPECIMENS:
        fail("Formal specimen IDs are not unique.")

    def verify_coverage(
        rows: list[dict[str, str]],
        round_field: str,
        label: str,
    ) -> None:
        grouped: dict[str, set[int]] = defaultdict(set)
        for row in rows:
            grouped[row["part_id"]].add(int(row[round_field]))
        if set(grouped) != set(specimen_by_id):
            fail(f"{label} specimen population does not match frozen specimen set.")
        bad = {
            pid: sorted(rounds)
            for pid, rounds in grouped.items()
            if rounds != EXPECTED_ROUNDS
        }
        if bad:
            fail(f"{label} round coverage failure: {bad}")

    verify_coverage(v2, "cv_round", "V2 CV")
    verify_coverage(manual, "manual_round", "Manual reference")

    missing_paths: list[str] = []
    for row in v2:
        raw = REPO_ROOT / row["raw_image_path"]
        blank = (
            FORMAL_V2_ROOT
            / "raw"
            / f'{row["session_id"]}_blank_reference.png'
        )
        if not raw.is_file():
            missing_paths.append(str(raw.relative_to(REPO_ROOT)))
        if not blank.is_file():
            missing_paths.append(str(blank.relative_to(REPO_ROOT)))

    if missing_paths:
        unique = sorted(set(missing_paths))
        preview = "\n".join(f"  {p}" for p in unique[:20])
        suffix = "" if len(unique) <= 20 else f"\n  ... and {len(unique)-20} more"
        fail(
            "Required V2 raw/blank images are missing:\n"
            f"{preview}{suffix}"
        )

    return v2, manual, specimen_by_id


def compute_specimen_metrics(
    observations: list[dict[str, Any]],
    manual_rows: list[dict[str, str]],
    specimen_by_id: dict[str, dict[str, str]],
    value_field: str,
    require_complete: bool = True,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manual_by_part: dict[str, dict[int, float]] = defaultdict(dict)
    for row in manual_rows:
        manual_by_part[row["part_id"]][int(row["manual_round"])] = float(
            row["reading_in"]
        )

    cv_by_part: dict[str, dict[int, float]] = defaultdict(dict)
    failures_by_part: Counter[str] = Counter()

    for row in observations:
        pid = str(row["part_id"])
        if row["passed"]:
            cv_by_part[pid][int(row["cv_round"])] = float(row[value_field])
        else:
            failures_by_part[pid] += 1

    complete_parts = [
        pid
        for pid in specimen_by_id
        if set(cv_by_part.get(pid, {})) == EXPECTED_ROUNDS
    ]

    if require_complete and len(complete_parts) != EXPECTED_SPECIMENS:
        fail(
            "The candidate did not produce 3/3 results for all 60 specimens. "
            f"Complete specimens: {len(complete_parts)}/{EXPECTED_SPECIMENS}. "
            "Availability results were written, but formal-like agreement "
            "statistics require complete three-round coverage."
        )

    specimen_rows: list[dict[str, Any]] = []
    errors: list[float] = []
    abs_errors: list[float] = []
    reposition: list[float] = []
    classifications: Counter[str] = Counter()

    for pid in sorted(complete_parts, key=int):
        manual_values = [
            manual_by_part[pid][round_number]
            for round_number in (1, 2, 3)
        ]
        cv_values = [
            cv_by_part[pid][round_number]
            for round_number in (1, 2, 3)
        ]

        manual_mean = statistics.fmean(manual_values)
        cv_mean = statistics.fmean(cv_values)
        error = cv_mean - manual_mean
        abs_error = abs(error)
        pairwise = pairwise_three(cv_values)

        errors.append(error)
        abs_errors.append(abs_error)
        reposition.extend(pairwise)

        ref_conforming = LSL_IN <= manual_mean <= USL_IN
        cv_conforming = LSL_IN <= cv_mean <= USL_IN

        if not ref_conforming and not cv_conforming:
            cls = "TRUE_NONCONFORMING"
        elif not ref_conforming and cv_conforming:
            cls = "FALSE_PASS"
        elif ref_conforming and not cv_conforming:
            cls = "FALSE_FAIL"
        else:
            cls = "TRUE_CONFORMING"
        classifications[cls] += 1

        specimen_rows.append(
            {
                "part_id": pid,
                "selection_stratum": specimen_by_id[pid]["selection_stratum"],
                "manual_1_in": manual_values[0],
                "manual_2_in": manual_values[1],
                "manual_3_in": manual_values[2],
                "manual_mean_in": manual_mean,
                "cv_1_in": cv_values[0],
                "cv_2_in": cv_values[1],
                "cv_3_in": cv_values[2],
                "cv_mean_in": cv_mean,
                "difference_in": error,
                "absolute_error_in": abs_error,
                "cv_range_in": max(cv_values) - min(cv_values),
                "pairwise_12_in": pairwise[0],
                "pairwise_13_in": pairwise[1],
                "pairwise_23_in": pairwise[2],
                "classification_outcome": cls,
                "failure_count": failures_by_part[pid],
            }
        )

    if not errors:
        fail("No complete specimens were available for analysis.")

    bias = statistics.fmean(errors)
    bias_se = statistics.stdev(errors) / math.sqrt(len(errors))
    tcrit = stats.t.ppf(0.975, df=len(errors) - 1)
    p95_abs, p95_abs_rank = empirical_nearest_rank(abs_errors, 0.95)
    p95_rep, p95_rep_rank = empirical_nearest_rank(reposition, 0.95)

    metrics = {
        "n_complete_specimens": len(complete_parts),
        "bias_in": bias,
        "bias_95_ci_lower_in": bias - tcrit * bias_se,
        "bias_95_ci_upper_in": bias + tcrit * bias_se,
        "median_signed_error_in": statistics.median(errors),
        "mae_in": statistics.fmean(abs_errors),
        "rmse_in": math.sqrt(statistics.fmean(e * e for e in errors)),
        "p95_absolute_error_in": p95_abs,
        "p95_absolute_error_rank": p95_abs_rank,
        "maximum_absolute_error_in": max(abs_errors),
        "reposition_n_pairwise": len(reposition),
        "reposition_mean_pairwise_in": statistics.fmean(reposition),
        "reposition_median_pairwise_in": statistics.median(reposition),
        "reposition_p95_pairwise_in": p95_rep,
        "reposition_p95_pairwise_rank": p95_rep_rank,
        "reposition_maximum_pairwise_in": max(reposition),
        "classification": {
            "true_nonconforming": classifications["TRUE_NONCONFORMING"],
            "false_passes": classifications["FALSE_PASS"],
            "false_fails": classifications["FALSE_FAIL"],
            "true_conforming": classifications["TRUE_CONFORMING"],
        },
    }
    return metrics, specimen_rows


def fmt(value: float) -> str:
    return f"{value:.9f}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Verify frozen implementation, datasets, and image availability only.",
    )
    args = parser.parse_args()

    hybrid = load_frozen_hybrid_module()
    v2_rows, manual_rows, specimen_by_id = validate_inputs()

    print("=" * 90)
    print("V2 ENDFACE-HYBRID RETROSPECTIVE PRECHECK")
    print("=" * 90)
    print(f"Git HEAD:                 {git_head()}")
    print(f"Estimator freeze commit:  {FREEZE_COMMIT}")
    print(f"Estimator SHA-256:         {FROZEN_HYBRID_SHA256}")
    print(f"V2 usable observations:    {len(v2_rows)}")
    print(f"Formal specimens:          {len(specimen_by_id)}")
    print("Required raw/blank images: PRESENT")
    print("Precheck: PASS")

    if args.check_only:
        return 0

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    observation_rows: list[dict[str, Any]] = []
    max_pca_reproduction_difference = 0.0
    pca_reproduction_failures: list[str] = []

    blank_cache: dict[Path, Any] = {}

    for index, row in enumerate(v2_rows, start=1):
        raw_path = REPO_ROOT / row["raw_image_path"]
        blank_path = (
            FORMAL_V2_ROOT
            / "raw"
            / f'{row["session_id"]}_blank_reference.png'
        )

        if blank_path not in blank_cache:
            blank_cache[blank_path] = hybrid._load_gray(blank_path)

        blank = blank_cache[blank_path]
        image = hybrid._load_gray(raw_path)

        segmentation = hybrid.segment_oal_case(blank, image)
        if not segmentation.passed or segmentation.centroid_xy is None:
            reason = segmentation.failure_reason or "Segmentation failed."
            pca_reproduction_failures.append(
                f'{row["cv_run_id"]}: segmentation failed: {reason}'
            )
            observation_rows.append(
                {
                    "cv_run_id": row["cv_run_id"],
                    "part_id": row["part_id"],
                    "cv_round": int(row["cv_round"]),
                    "session_id": row["session_id"],
                    "raw_image_path": row["raw_image_path"],
                    "recorded_v2_oal_in": float(row["oal_in"]),
                    "reproduced_pca_oal_in": "",
                    "pca_reproduction_difference_in": "",
                    "passed": False,
                    "failure_reason": reason,
                    "hybrid_oal_in": "",
                    "hybrid_length_pixels": "",
                    "hybrid_effective_ppi": "",
                    "hybrid_angle_degrees": "",
                    "end_min_accepted": "",
                    "end_max_accepted": "",
                }
            )
            continue

        pca = hybrid.measure_topdown_oal(
            segmentation.mask,
            minimum_fixture_width_ratio=hybrid.CASE_ONLY_FIXTURE_WIDTH_RATIO,
        )
        if (
            not pca.passed
            or pca.length_pixels is None
            or pca.angle_degrees is None
        ):
            reason = pca.failure_reason or "PCA measurement failed."
            pca_reproduction_failures.append(
                f'{row["cv_run_id"]}: PCA failed: {reason}'
            )
            reproduced = None
            pca_diff = None
        else:
            reproduced, _ = hybrid._calibrated_length(
                float(pca.length_pixels),
                segmentation.centroid_xy,
                float(pca.angle_degrees),
            )
            pca_diff = abs(reproduced - float(row["oal_in"]))
            max_pca_reproduction_difference = max(
                max_pca_reproduction_difference,
                pca_diff,
            )
            if pca_diff > PCA_REPRODUCTION_TOLERANCE_IN:
                pca_reproduction_failures.append(
                    f'{row["cv_run_id"]}: difference={pca_diff:.12g} in'
                )

        candidate = hybrid._hybrid_endface_observation(
            image,
            segmentation.mask,
            segmentation.centroid_xy,
        )

        observation_rows.append(
            {
                "cv_run_id": row["cv_run_id"],
                "part_id": row["part_id"],
                "cv_round": int(row["cv_round"]),
                "session_id": row["session_id"],
                "raw_image_path": row["raw_image_path"],
                "recorded_v2_oal_in": float(row["oal_in"]),
                "reproduced_pca_oal_in": ""
                if reproduced is None else reproduced,
                "pca_reproduction_difference_in": ""
                if pca_diff is None else pca_diff,
                "passed": bool(candidate.passed),
                "failure_reason": candidate.failure_reason or "",
                "hybrid_oal_in": ""
                if candidate.length_inches is None else candidate.length_inches,
                "hybrid_length_pixels": ""
                if candidate.length_pixels is None else candidate.length_pixels,
                "hybrid_effective_ppi": ""
                if candidate.effective_ppi is None else candidate.effective_ppi,
                "hybrid_angle_degrees": ""
                if candidate.angle_degrees is None else candidate.angle_degrees,
                "end_min_accepted": ""
                if candidate.end_min_accepted is None else candidate.end_min_accepted,
                "end_max_accepted": ""
                if candidate.end_max_accepted is None else candidate.end_max_accepted,
            }
        )

        if index % 20 == 0 or index == len(v2_rows):
            print(f"Processed {index:3d}/{len(v2_rows)} V2 images")

    obs_csv = output_dir / "v2_endface_hybrid_observations.csv"
    with obs_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(observation_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(observation_rows)

    if pca_reproduction_failures:
        failure_path = output_dir / "PCA_REPRODUCTION_FAILURE.txt"
        failure_path.write_text(
            "\n".join(pca_reproduction_failures) + "\n",
            encoding="utf-8",
        )
        fail(
            "Recorded V2 PCA reproduction did not pass. "
            f"Maximum difference={max_pca_reproduction_difference:.12f} in. "
            f"See {failure_path.relative_to(REPO_ROOT)}. "
            "Hybrid results must not be interpreted until reproduction passes."
        )

    print()
    print("=" * 90)
    print("FORMAL PCA REPRODUCTION CHECK")
    print("=" * 90)
    print(
        "Maximum regenerated-vs-recorded OAL difference: "
        f"{max_pca_reproduction_difference:.12f} in"
    )
    print("PASS: frozen formal V2 PCA measurements reproduced")

    passing_count = sum(bool(row["passed"]) for row in observation_rows)
    availability_pct = 100.0 * passing_count / EXPECTED_OBSERVATIONS
    complete_parts = 0
    by_part_pass: dict[str, set[int]] = defaultdict(set)
    for row in observation_rows:
        if row["passed"]:
            by_part_pass[str(row["part_id"])].add(int(row["cv_round"]))
    complete_parts = sum(
        rounds == EXPECTED_ROUNDS
        for rounds in by_part_pass.values()
    )

    print()
    print("=" * 90)
    print("ENDFACE-HYBRID AVAILABILITY")
    print("=" * 90)
    print(f"Valid:        {passing_count}/{EXPECTED_OBSERVATIONS}")
    print(f"Failures:     {EXPECTED_OBSERVATIONS - passing_count}")
    print(f"Availability: {availability_pct:.3f}%")
    print(
        f"Complete 3-round specimens: "
        f"{complete_parts}/{EXPECTED_SPECIMENS}"
    )

    # Always calculate the recorded V2 baseline from the preserved observation
    # values, so the comparison uses identical formulas.
    baseline_observations = [
        {
            "part_id": row["part_id"],
            "cv_round": int(row["cv_round"]),
            "passed": True,
            "recorded_oal": float(row["oal_in"]),
        }
        for row in v2_rows
    ]
    baseline_metrics, _ = compute_specimen_metrics(
        baseline_observations,
        manual_rows,
        specimen_by_id,
        "recorded_oal",
        require_complete=True,
    )

    statistics_payload: dict[str, Any] = {
        "analysis_type": "retrospective_exploratory",
        "formal_v1_v2_unchanged": True,
        "freeze_commit": FREEZE_COMMIT,
        "run_git_head": git_head(),
        "frozen_hybrid_sha256": FROZEN_HYBRID_SHA256,
        "pca_reproduction_max_difference_in":
            max_pca_reproduction_difference,
        "hybrid_availability": {
            "valid_observations": passing_count,
            "total_observations": EXPECTED_OBSERVATIONS,
            "availability_pct": availability_pct,
            "complete_three_round_specimens": complete_parts,
        },
        "recorded_v2_baseline": baseline_metrics,
    }

    if complete_parts == EXPECTED_SPECIMENS:
        hybrid_metrics, specimen_summary = compute_specimen_metrics(
            observation_rows,
            manual_rows,
            specimen_by_id,
            "hybrid_oal_in",
            require_complete=True,
        )
        statistics_payload["endface_hybrid"] = hybrid_metrics

        specimen_csv = output_dir / "v2_endface_hybrid_specimen_summary.csv"
        with specimen_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=list(specimen_summary[0].keys()),
            )
            writer.writeheader()
            writer.writerows(specimen_summary)

        worst_repeat = sorted(
            specimen_summary,
            key=lambda row: float(row["cv_range_in"]),
            reverse=True,
        )[:10]
        worst_error = sorted(
            specimen_summary,
            key=lambda row: float(row["absolute_error_in"]),
            reverse=True,
        )[:10]

        b = baseline_metrics
        h = hybrid_metrics
        summary_lines = [
            "# V2 Endface-Hybrid Retrospective Evaluation",
            "",
            "**Exploratory retrospective analysis only. Formal V1/V2 results remain unchanged.**",
            "",
            f"- Estimator freeze commit: `{FREEZE_COMMIT}`",
            f"- Frozen estimator SHA-256: `{FROZEN_HYBRID_SHA256}`",
            f"- Run Git HEAD: `{git_head()}`",
            f"- Maximum PCA reproduction difference: {max_pca_reproduction_difference:.12f} in",
            "",
            "## Availability",
            "",
            f"- Hybrid valid observations: {passing_count}/{EXPECTED_OBSERVATIONS}",
            f"- Hybrid availability: {availability_pct:.3f}%",
            f"- Complete 3-round specimens: {complete_parts}/{EXPECTED_SPECIMENS}",
            "",
            "## Primary comparison",
            "",
            "| Metric | Recorded V2 PCA | Frozen endface hybrid |",
            "|---|---:|---:|",
            f'| Mean bias (CV-manual) | {b["bias_in"]:.6f} in | {h["bias_in"]:.6f} in |',
            f'| MAE | {b["mae_in"]:.6f} in | {h["mae_in"]:.6f} in |',
            f'| RMSE | {b["rmse_in"]:.6f} in | {h["rmse_in"]:.6f} in |',
            f'| P95 absolute error | {b["p95_absolute_error_in"]:.6f} in | {h["p95_absolute_error_in"]:.6f} in |',
            f'| Maximum absolute error | {b["maximum_absolute_error_in"]:.6f} in | {h["maximum_absolute_error_in"]:.6f} in |',
            f'| P95 repositioning | {b["reposition_p95_pairwise_in"]:.6f} in | {h["reposition_p95_pairwise_in"]:.6f} in |',
            f'| Maximum repositioning | {b["reposition_maximum_pairwise_in"]:.6f} in | {h["reposition_maximum_pairwise_in"]:.6f} in |',
            "",
            "## Classification",
            "",
            f'- Recorded V2 false passes: {b["classification"]["false_passes"]}',
            f'- Recorded V2 false fails: {b["classification"]["false_fails"]}',
            f'- Hybrid false passes: {h["classification"]["false_passes"]}',
            f'- Hybrid false fails: {h["classification"]["false_fails"]}',
            "",
            "## Ten largest hybrid specimen ranges",
            "",
        ]
        for row in worst_repeat:
            summary_lines.append(
                f'- Part {row["part_id"]}: range {float(row["cv_range_in"]):.6f} in'
            )

        summary_lines.extend(
            [
                "",
                "## Ten largest hybrid absolute errors",
                "",
            ]
        )
        for row in worst_error:
            summary_lines.append(
                f'- Part {row["part_id"]}: '
                f'abs error {float(row["absolute_error_in"]):.6f} in; '
                f'bias {float(row["difference_in"]):+.6f} in'
            )

        summary_lines.extend(
            [
                "",
                "## Interpretation guardrail",
                "",
                "The estimator architecture and numerical parameters were frozen before this retrospective V2 analysis. These results may support a decision about prospective V3 validation, but they are not an independent prospective validation and must not be used to retune this frozen estimator version.",
                "",
            ]
        )

        summary_path = output_dir / "SUMMARY.md"
        summary_path.write_text("\n".join(summary_lines), encoding="utf-8")

        print()
        print("=" * 90)
        print("RETROSPECTIVE V2 COMPARISON")
        print("=" * 90)
        print(
            f'P95 repositioning: V2 PCA {b["reposition_p95_pairwise_in"]:.6f} in'
            f' -> hybrid {h["reposition_p95_pairwise_in"]:.6f} in'
        )
        print(
            f'Bias:              V2 PCA {b["bias_in"]:+.6f} in'
            f' -> hybrid {h["bias_in"]:+.6f} in'
        )
        print(
            f'RMSE:              V2 PCA {b["rmse_in"]:.6f} in'
            f' -> hybrid {h["rmse_in"]:.6f} in'
        )
        print(
            f'P95 abs error:     V2 PCA {b["p95_absolute_error_in"]:.6f} in'
            f' -> hybrid {h["p95_absolute_error_in"]:.6f} in'
        )
        print(
            f'Max abs error:     V2 PCA {b["maximum_absolute_error_in"]:.6f} in'
            f' -> hybrid {h["maximum_absolute_error_in"]:.6f} in'
        )
        print(
            f'Classification:    hybrid false pass='
            f'{h["classification"]["false_passes"]}, '
            f'false fail={h["classification"]["false_fails"]}'
        )
        print()
        print(f"Wrote: {summary_path.relative_to(REPO_ROOT)}")
        print(f"Wrote: {specimen_csv.relative_to(REPO_ROOT)}")
    else:
        print()
        print(
            "Hybrid did not provide complete 3-round coverage for all specimens. "
            "No formal-like specimen agreement/repeatability summary was produced."
        )

    json_path = output_dir / "statistics.json"
    json_path.write_text(
        json.dumps(statistics_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote: {obs_csv.relative_to(REPO_ROOT)}")
    print(f"Wrote: {json_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
