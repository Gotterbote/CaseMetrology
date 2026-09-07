#!/usr/bin/env python3
"""Write formal CaseMetrology OAL validation results.

This script contains no statistical model or acceptance logic.
It imports the frozen analysis implementation from
scripts/analyze_oal_validation.py and serializes the resulting
derived data and formal statistics.

It never modifies raw acquisition data.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

from analyze_oal_validation import (
    EXPECTED_SPECIMENS,
    FROZEN_DATASET_COMMIT,
    build_core_analysis,
    build_extended_analysis,
    package_version,
    validate_dataset,
    verify_frozen_inputs,
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def git_commit(repo_root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        text=True,
    ).strip()


def require_clean_worktree(repo_root: Path) -> None:
    status = subprocess.check_output(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        text=True,
    )
    if status.strip():
        fail(
            "Formal result generation requires a clean Git worktree."
        )


def csv_value(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "YES" if value else "NO"
    if isinstance(value, float):
        if not math.isfinite(value):
            fail("Attempted to write non-finite CSV value")
        return format(value, ".12g")
    return str(value)


def write_csv(
    path: Path,
    fields: list[str],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()

        for row in rows:
            writer.writerow(
                {
                    field: csv_value(row.get(field))
                    for field in fields
                }
            )


def write_json(path: Path, value: object) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(
            value,
            handle,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        handle.write("\n")


def calculate(
    repo_root: Path,
    data_root: Path,
):
    input_hashes = verify_frozen_inputs(
        repo_root,
        data_root,
    )
    state = validate_dataset(data_root)
    core = build_core_analysis(state)
    extended = build_extended_analysis(state, core)

    return input_hashes, state, core, extended


def build_json_payload(
    repo_root: Path,
    input_hashes: dict[str, str],
    core: dict[str, object],
    extended: dict[str, object],
) -> dict[str, object]:
    bland_altman = dict(extended["bland_altman"])

    # Specimen-level plotting values already exist in the joined
    # derived dataset and need not be duplicated in the summary JSON.
    bland_altman.pop("magnitudes_in", None)
    bland_altman.pop("differences_in", None)

    return {
        "analysis_metadata": {
            "project": "CaseMetrology",
            "measurement_characteristic": "OAL",
            "primary_analysis_unit": "unique_specimen",
            "n_specimens": EXPECTED_SPECIMENS,
            "frozen_acquisition_dataset_commit":
                FROZEN_DATASET_COMMIT,
            "analysis_code_commit":
                git_commit(repo_root),
            "python_version":
                platform.python_version(),
            "numpy_version":
                package_version("numpy"),
            "pandas_version":
                package_version("pandas"),
            "scipy_version":
                package_version("scipy"),
            "matplotlib_version":
                package_version("matplotlib"),
            "input_sha256":
                input_hashes,
        },
        "reference_uncertainty":
            core["reference_uncertainty"],
        "primary_agreement":
            core["primary_agreement"],
        "cv_availability":
            extended["availability"],
        "cv_repositioning_repeatability":
            core["cv_repositioning"],
        "specimen_repeatability":
            extended["repeatability"],
        "bland_altman":
            bland_altman,
        "regression":
            extended["regression"],
        "classification":
            extended["classification"],
        "stratum_summaries":
            extended["stratum_summaries"],
        "primary_criteria":
            extended["criteria"],
        "zero_false_pass_preference":
            extended["zero_false_pass_preference"],
        "overall_interpretation":
            extended["overall_interpretation"],
    }


def write_results(
    repo_root: Path,
    data_root: Path,
) -> Path:
    require_clean_worktree(repo_root)

    output_dir = data_root / "derived"

    if output_dir.exists():
        fail(
            f"Refusing to overwrite existing formal output directory: "
            f"{output_dir}"
        )

    input_hashes, state, core, extended = calculate(
        repo_root,
        data_root,
    )

    temp_dir = Path(
        tempfile.mkdtemp(
            prefix=".derived-",
            dir=data_root,
        )
    )

    try:
        # ---------------------------------------------------------
        # Prospectively defined manual specimen summary
        # ---------------------------------------------------------

        manual_rows = []

        for row in core["manual_summary"]:
            result = dict(row)
            result["reference_status"] = "ACCEPTED"
            manual_rows.append(result)

        write_csv(
            temp_dir / "manual_reference_summary.csv",
            [
                "part_id",
                "manual_1_in",
                "manual_2_in",
                "manual_3_in",
                "manual_mean_in",
                "manual_sd_in",
                "manual_range_in",
                "manual_n_valid",
                "reference_status",
            ],
            manual_rows,
        )

        # ---------------------------------------------------------
        # Prospectively defined CV specimen summary
        # ---------------------------------------------------------

        analysis_by_part = {
            row["part_id"]: row
            for row in extended["analysis_rows"]
        }

        cv_rows = []

        for row in core["cv_summary"]:
            result = dict(row)
            analysis_row = analysis_by_part[row["part_id"]]

            result["cv_n_system_failures"] = (
                analysis_row["cv_failure_count"]
            )
            result["cv_complete"] = (
                int(row["cv_n_valid"]) == 3
                and
                int(analysis_row["cv_failure_count"]) == 0
            )

            cv_rows.append(result)

        write_csv(
            temp_dir / "cv_summary.csv",
            [
                "part_id",
                "cv_1_in",
                "cv_2_in",
                "cv_3_in",
                "cv_mean_in",
                "cv_sd_in",
                "cv_range_in",
                "cv_n_valid",
                "cv_n_system_failures",
                "cv_complete",
            ],
            cv_rows,
        )

        # ---------------------------------------------------------
        # Prospectively defined joined specimen analysis
        # ---------------------------------------------------------

        write_csv(
            temp_dir / "oal_validation_analysis.csv",
            [
                "part_id",
                "selection_stratum",
                "manual_mean_in",
                "manual_sd_in",
                "cv_mean_in",
                "cv_sd_in",
                "difference_in",
                "absolute_error_in",
                "percent_error",
                "cv_n_valid",
                "cv_failure_count",
                "analysis_included",
                "exclusion_reason",
            ],
            extended["analysis_rows"],
        )

        # ---------------------------------------------------------
        # Classification summary
        # ---------------------------------------------------------

        classification = extended["classification"]

        classification_rows = [
            {
                "metric": "true_nonconforming",
                "value": classification["true_nonconforming"],
            },
            {
                "metric": "false_passes",
                "value": classification["false_passes"],
            },
            {
                "metric": "false_fails",
                "value": classification["false_fails"],
            },
            {
                "metric": "true_conforming",
                "value": classification["true_conforming"],
            },
            {
                "metric": "sensitivity_detect_nonconforming",
                "value":
                    classification[
                        "sensitivity_detect_nonconforming"
                    ],
            },
            {
                "metric": "specificity_conforming",
                "value":
                    classification[
                        "specificity_conforming"
                    ],
            },
            {
                "metric": "uncertainty_overlap_count",
                "value":
                    classification[
                        "uncertainty_overlap_count"
                    ],
            },
        ]

        write_csv(
            temp_dir / "classification_summary.csv",
            ["metric", "value"],
            classification_rows,
        )

        # ---------------------------------------------------------
        # Frozen stratum summary
        # ---------------------------------------------------------

        write_csv(
            temp_dir / "stratum_summary.csv",
            [
                "selection_stratum",
                "n_specimens",
                "valid_cv_observations",
                "system_failures",
                "mean_signed_error_in",
                "median_signed_error_in",
                "mae_in",
                "maximum_absolute_error_in",
                "reference_conforming_count",
                "cv_conforming_count",
                "true_nonconforming",
                "false_passes",
                "false_fails",
                "true_conforming",
                "uncertainty_overlap_count",
            ],
            extended["stratum_summaries"],
        )

        # ---------------------------------------------------------
        # Repeatability summary
        # ---------------------------------------------------------

        repeatability_rows = []

        for method in ("manual", "cv"):
            for metric, value in (
                extended["repeatability"][method].items()
            ):
                repeatability_rows.append(
                    {
                        "method": method,
                        "metric": metric,
                        "value": value,
                    }
                )

        for metric, value in core["cv_repositioning"].items():
            repeatability_rows.append(
                {
                    "method": "cv_repositioning",
                    "metric": metric,
                    "value": value,
                }
            )

        write_csv(
            temp_dir / "repeatability_summary.csv",
            ["method", "metric", "value"],
            repeatability_rows,
        )

        # ---------------------------------------------------------
        # Frozen validation criteria
        # ---------------------------------------------------------

        units = {
            "cv_availability": "%",
            "cv_repositioning_p95": "in",
            "absolute_mean_bias": "in",
            "rmse": "in",
            "p95_absolute_specimen_error": "in",
            "maximum_absolute_specimen_error": "in",
        }

        criteria_rows = []

        for name, criterion in extended["criteria"].items():
            criteria_rows.append(
                {
                    "criterion": name,
                    "observed": criterion["observed"],
                    "target": criterion["target"],
                    "relation": criterion["relation"],
                    "unit": units[name],
                    "status": criterion["status"],
                }
            )

        false_pass = extended["zero_false_pass_preference"]

        criteria_rows.append(
            {
                "criterion": "zero_false_pass_preference",
                "observed":
                    false_pass["observed_false_passes"],
                "target":
                    false_pass["preferred"],
                "relation": "preferred_equal",
                "unit": "count",
                "status":
                    false_pass["status"],
            }
        )

        write_csv(
            temp_dir / "criteria_summary.csv",
            [
                "criterion",
                "observed",
                "target",
                "relation",
                "unit",
                "status",
            ],
            criteria_rows,
        )

        # ---------------------------------------------------------
        # Complete machine-readable formal result record
        # ---------------------------------------------------------

        payload = build_json_payload(
            repo_root,
            input_hashes,
            core,
            extended,
        )

        write_json(
            temp_dir / "formal_validation_statistics.json",
            payload,
        )

        temp_dir.rename(output_dir)

    except Exception:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        raise

    return output_dir


def print_results(
    core: dict[str, object],
    extended: dict[str, object],
) -> None:
    p = core["primary_agreement"]
    u = core["reference_uncertainty"]
    r = core["cv_repositioning"]
    ba = extended["bland_altman"]
    reg = extended["regression"]
    cls = extended["classification"]

    print()
    print("=== FORMAL OAL VALIDATION RESULTS ===")
    print(f"Specimen-level agreement n: {p['n']}")
    print(
        "CV availability: "
        f"{extended['availability']['availability_pct']:.3f}%"
    )

    print()
    print("Primary dimensional agreement:")
    print(f"  Mean bias (CV - manual): {p['bias_in']:.6f} in")
    print(
        "  Bias 95% CI: "
        f"[{p['bias_95_ci_lower_in']:.6f}, "
        f"{p['bias_95_ci_upper_in']:.6f}] in"
    )
    print(
        f"  Median signed error: "
        f"{p['median_signed_error_in']:.6f} in"
    )
    print(f"  MAE: {p['mae_in']:.6f} in")
    print(f"  RMSE: {p['rmse_in']:.6f} in")
    print(
        f"  P95 absolute error: "
        f"{p['p95_absolute_error_in']:.6f} in"
    )
    print(
        f"  Maximum absolute error: "
        f"{p['maximum_absolute_error_in']:.6f} in"
    )

    print()
    print("Reference uncertainty:")
    print(
        f"  Pooled manual SD: "
        f"{u['pooled_manual_sd_in']:.6f} in"
    )
    print(
        f"  Expanded U_ref (k=2): "
        f"{u['expanded_u_ref_k2_in']:.6f} in"
    )

    print()
    print("CV repositioning repeatability:")
    print(
        f"  P95 pairwise difference: "
        f"{r['p95_pairwise_difference_in']:.6f} in"
    )
    print(
        f"  Maximum pairwise difference: "
        f"{r['maximum_pairwise_difference_in']:.6f} in"
    )

    print()
    print("Bland-Altman:")
    print(f"  Lower LOA: {ba['loa_lower_in']:.6f} in")
    print(f"  Upper LOA: {ba['loa_upper_in']:.6f} in")

    print()
    print("Regression / correlation:")
    print(f"  Slope: {reg['slope']:.6f}")
    print(f"  Intercept: {reg['intercept_in']:.6f} in")
    print(f"  Pearson r: {reg['pearson_r']:.6f}")
    print(f"  R-squared: {reg['r_squared']:.6f}")

    print()
    print("Classification:")
    print(
        f"  True nonconforming: "
        f"{cls['true_nonconforming']}"
    )
    print(f"  False passes: {cls['false_passes']}")
    print(f"  False fails: {cls['false_fails']}")
    print(
        f"  True conforming: "
        f"{cls['true_conforming']}"
    )

    sensitivity = cls["sensitivity_detect_nonconforming"]
    specificity = cls["specificity_conforming"]

    if sensitivity is not None:
        print(
            "  Sensitivity detecting nonconforming: "
            f"{100.0 * sensitivity:.2f}%"
        )

    if specificity is not None:
        print(
            "  Specificity for conforming: "
            f"{100.0 * specificity:.2f}%"
        )

    print(
        "  Reference uncertainty-overlap flags: "
        f"{cls['uncertainty_overlap_count']}"
    )

    print()
    print("=== PRESPECIFIED CRITERIA ===")

    for name, criterion in extended["criteria"].items():
        print(f"{name}: {criterion['status']}")

    print(
        "zero_false_pass_preference: "
        f"{extended['zero_false_pass_preference']['status']}"
    )

    print()
    print(
        "Overall interpretation: "
        f"{extended['overall_interpretation']}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/oal_validation"),
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--check",
        action="store_true",
        help="calculate everything in memory without writing results",
    )

    mode.add_argument(
        "--write",
        action="store_true",
        help="write the formal derived result package",
    )

    args = parser.parse_args()

    repo_root = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    ).resolve()

    data_root = args.root.resolve()

    if args.check:
        calculate(repo_root, data_root)
        print("RESULT WRITER CHECK PASS")
        print("No formal result files were created.")
        return 0

    output_dir = write_results(repo_root, data_root)

    _, _, core, extended = calculate(
        repo_root,
        data_root,
    )

    print("FORMAL RESULT GENERATION PASS")
    print(f"Derived results: {output_dir}")

    print_results(core, extended)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"RESULT GENERATION FAIL: {exc}")
        raise SystemExit(1)
