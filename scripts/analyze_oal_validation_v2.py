#!/usr/bin/env python3
"""
Formal OAL validation analysis.

Primary analysis unit:
    unique specimen (n = 60)

Frozen completed acquisition dataset:
    9c4a0a00dc519e22f074e1cbdb1dadb9030fb34f

This script must never modify raw acquisition data.

The initial --check-only mode verifies:
- frozen input-file identity;
- formal specimen population;
- manual and CV usable observation populations;
- round coverage;
- run-order linkage;
- accepted manual sessions;
- frozen strata;
- documented protocol-invalid manual observations.

Statistical output generation will occur only through an explicit
analysis/write mode after this implementation gate has passed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
import platform
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from scipy import stats


FROZEN_DATASET_COMMIT = "9c4a0a00dc519e22f074e1cbdb1dadb9030fb34f"

EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}
EXPECTED_USABLE_MANUAL = 180
EXPECTED_USABLE_CV = 180

# Prospectively frozen 2026-09-05 reference-uncertainty terms.
U_CAL_IN = 0.000063
DISPLAY_INCREMENT_IN = 0.0005

LSL_IN = 0.9900
USL_IN = 1.0100

TARGET_AVAILABILITY_PCT = 99.0
TARGET_ABS_BIAS_IN = 0.001
TARGET_RMSE_IN = 0.002
TARGET_P95_ABS_ERROR_IN = 0.003
TARGET_MAX_ABS_ERROR_IN = 0.004
TARGET_P95_REPOSITION_IN = 0.002

EXPECTED_STRATA = {
    "below_lsl": 8,
    "near_lsl_in_spec": 14,
    "central_nominal": 16,
    "near_usl_in_spec": 14,
    "above_usl": 8,
}

INPUT_FILES = (
    "formal_validation_specimens.csv",
    "manual_run_order.csv",
    "v2_cv_run_order.csv",
    "manual_reference_observations.csv",
    "manual_reference_checks.csv",
    "manual_sessions.csv",
    "environmental_observations.csv",
    "v2_cv_observations.csv",
    "protocol_deviations.csv",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_blob_bytes(repo_root: Path, commit: str, repo_path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{repo_path}"],
            cwd=repo_root,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace")
        fail(
            f"Could not read {repo_path!r} from frozen commit "
            f"{commit}: {stderr.strip()}"
        )


def verify_frozen_inputs(
    repo_root: Path,
    data_root: Path,
) -> dict[str, str]:
    hashes: dict[str, str] = {}

    for filename in INPUT_FILES:
        working_path = data_root / filename
        if not working_path.is_file():
            fail(f"Required input file missing: {working_path}")

        repo_path = working_path.relative_to(repo_root).as_posix()

        working_hash = sha256_file(working_path)
        frozen_bytes = git_blob_bytes(
            repo_root,
            FROZEN_DATASET_COMMIT,
            repo_path,
        )
        frozen_hash = sha256_bytes(frozen_bytes)

        if working_hash != frozen_hash:
            fail(
                "Frozen input mismatch:\n"
                f"  file: {repo_path}\n"
                f"  working SHA-256: {working_hash}\n"
                f"  frozen SHA-256:  {frozen_hash}\n"
                f"  frozen commit:   {FROZEN_DATASET_COMMIT}"
            )

        hashes[repo_path] = working_hash

    return hashes


def is_yes(value: str) -> bool:
    return value.strip().upper() in {"YES", "TRUE", "1"}


def manual_row_is_usable(row: dict[str, str]) -> bool:
    return (
        is_yes(row["measurement_valid"])
        and not is_yes(row["protocol_invalid"])
    )


def cv_row_is_usable(row: dict[str, str]) -> bool:
    return (
        row["measurement_status"].strip().upper() == "VALID"
        and not is_yes(row["protocol_invalid"])
    )


def assert_unique(values: list[str], label: str) -> None:
    counts = Counter(values)
    duplicates = {key: count for key, count in counts.items() if count != 1}
    if duplicates:
        fail(f"{label} contains duplicate/non-unique values: {duplicates}")


def verify_round_coverage(
    rows: list[dict[str, str]],
    round_field: str,
    label: str,
) -> None:
    by_part: dict[str, set[int]] = defaultdict(set)

    for row in rows:
        by_part[row["part_id"]].add(int(row[round_field]))

    if len(by_part) != EXPECTED_SPECIMENS:
        fail(
            f"{label}: expected {EXPECTED_SPECIMENS} unique parts, "
            f"found {len(by_part)}"
        )

    bad = {
        part_id: sorted(rounds)
        for part_id, rounds in by_part.items()
        if rounds != EXPECTED_ROUNDS
    }

    if bad:
        fail(f"{label}: incomplete round coverage: {bad}")


def verify_run_order_linkage(
    run_order: list[dict[str, str]],
    observations: list[dict[str, str]],
    run_id_field: str,
    round_field: str,
    label: str,
) -> None:
    if len(run_order) != 180:
        fail(f"{label}: run order must contain exactly 180 rows")

    run_by_id: dict[str, dict[str, str]] = {}

    for row in run_order:
        run_id = row[run_id_field]
        if run_id in run_by_id:
            fail(f"{label}: duplicate run-order ID {run_id}")
        run_by_id[run_id] = row

    usable_ids = [row[run_id_field] for row in observations]
    assert_unique(usable_ids, f"{label} usable observation run IDs")

    if set(usable_ids) != set(run_by_id):
        missing = sorted(set(run_by_id) - set(usable_ids))
        unexpected = sorted(set(usable_ids) - set(run_by_id))
        fail(
            f"{label}: usable observations do not exactly cover run order\n"
            f"missing={missing}\n"
            f"unexpected={unexpected}"
        )

    for obs in observations:
        run_id = obs[run_id_field]
        planned = run_by_id[run_id]

        for field in ("part_id", "planned_sequence"):
            if obs[field] != planned[field]:
                fail(
                    f"{label}: {run_id} {field} mismatch: "
                    f"observation={obs[field]!r}, "
                    f"run_order={planned[field]!r}"
                )

        if obs[round_field] != planned[round_field]:
            fail(
                f"{label}: {run_id} {round_field} mismatch: "
                f"observation={obs[round_field]!r}, "
                f"run_order={planned[round_field]!r}"
            )


def validate_dataset(
    data_root: Path,
) -> dict[str, object]:
    specimens = read_csv(data_root / "formal_validation_specimens.csv")
    manual_run_order = read_csv(data_root / "manual_run_order.csv")
    cv_run_order = read_csv(data_root / "v2_cv_run_order.csv")
    manual = read_csv(data_root / "manual_reference_observations.csv")
    cv = read_csv(data_root / "v2_cv_observations.csv")
    manual_sessions = read_csv(data_root / "manual_sessions.csv")
    deviations = read_csv(data_root / "protocol_deviations.csv")

    if len(specimens) != EXPECTED_SPECIMENS:
        fail(
            f"Expected {EXPECTED_SPECIMENS} frozen specimens, "
            f"found {len(specimens)}"
        )

    specimen_ids = [row["part_id"] for row in specimens]
    assert_unique(specimen_ids, "formal specimen part_id")

    strata = Counter(row["selection_stratum"] for row in specimens)
    if dict(strata) != EXPECTED_STRATA:
        fail(
            f"Frozen stratum counts differ from expected values: {dict(strata)}"
        )

    manual_usable = [row for row in manual if manual_row_is_usable(row)]
    manual_invalid = [row for row in manual if is_yes(row["protocol_invalid"])]
    cv_usable = [row for row in cv if cv_row_is_usable(row)]

    if len(manual_usable) != EXPECTED_USABLE_MANUAL:
        fail(
            f"Expected {EXPECTED_USABLE_MANUAL} usable manual observations, "
            f"found {len(manual_usable)}"
        )

    if len(cv_usable) != EXPECTED_USABLE_CV:
        fail(
            f"Expected {EXPECTED_USABLE_CV} usable CV observations, "
            f"found {len(cv_usable)}"
        )

    if len(manual_invalid) != 2:
        fail(
            f"Expected exactly 2 protocol-invalid manual observations, "
            f"found {len(manual_invalid)}"
        )

    expected_invalid_ids = {
        "MAN-S002-INV-001",
        "MAN-S002-INV-002",
    }
    actual_invalid_ids = {
        row["manual_observation_id"]
        for row in manual_invalid
    }

    if actual_invalid_ids != expected_invalid_ids:
        fail(
            "Protocol-invalid manual observation IDs differ from the "
            f"documented set: {sorted(actual_invalid_ids)}"
        )

    verify_round_coverage(
        manual_usable,
        "manual_round",
        "manual",
    )
    verify_round_coverage(
        cv_usable,
        "cv_round",
        "CV",
    )

    verify_run_order_linkage(
        manual_run_order,
        manual_usable,
        "manual_run_id",
        "manual_round",
        "manual",
    )

    verify_run_order_linkage(
        cv_run_order,
        cv_usable,
        "cv_run_id",
        "cv_round",
        "CV",
    )

    accepted_sessions = {
        row["session_id"]
        for row in manual_sessions
        if (
            row["session_status"].strip().upper() == "ACCEPTED"
            and row["review_required"].strip().upper() == "NO"
        )
    }

    if accepted_sessions != {"MAN-S001", "MAN-S002", "MAN-S003"}:
        fail(
            "Manual sessions are not exactly the three accepted, "
            f"non-review sessions: {sorted(accepted_sessions)}"
        )

    usable_manual_sessions = {
        row["session_id"] for row in manual_usable
    }
    if not usable_manual_sessions <= accepted_sessions:
        fail(
            "Usable manual observations reference non-accepted sessions: "
            f"{sorted(usable_manual_sessions - accepted_sessions)}"
        )

    open_deviations = [
        row["deviation_id"]
        for row in deviations
        if row["review_status"].strip().upper() != "CLOSED"
    ]

    if open_deviations:
        fail(f"Open protocol deviations remain: {open_deviations}")

    specimen_set = set(specimen_ids)

    manual_part_set = {row["part_id"] for row in manual_usable}
    cv_part_set = {row["part_id"] for row in cv_usable}

    if manual_part_set != specimen_set:
        fail("Usable manual population does not match frozen specimen set")

    if cv_part_set != specimen_set:
        fail("Usable CV population does not match frozen specimen set")

    return {
        "specimens": specimens,
        "manual_usable": manual_usable,
        "manual_invalid": manual_invalid,
        "cv_usable": cv_usable,
        "cv_all": cv,
        "strata": strata,
        "accepted_sessions": accepted_sessions,
        "deviations": deviations,
    }



def sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        fail("Sample SD requires at least two observations")
    return statistics.stdev(values)


def empirical_nearest_rank(
    values: list[float],
    probability: float,
) -> tuple[float, int]:
    if not values:
        fail("Cannot calculate percentile for empty values")

    if not 0.0 < probability <= 1.0:
        fail(f"Invalid percentile probability: {probability}")

    ordered = sorted(values)
    rank = math.ceil(probability * len(ordered))

    return ordered[rank - 1], rank


def group_by_part_and_round(
    rows: list[dict[str, str]],
    round_field: str,
    value_field: str,
) -> dict[str, dict[int, float]]:
    grouped: dict[str, dict[int, float]] = defaultdict(dict)

    for row in rows:
        part_id = row["part_id"]
        round_number = int(row[round_field])
        value = float(row[value_field])

        if not math.isfinite(value):
            fail(
                f"Non-finite {value_field} for part {part_id}, "
                f"round {round_number}"
            )

        if round_number in grouped[part_id]:
            fail(
                f"Duplicate usable value for part {part_id}, "
                f"round {round_number}"
            )

        grouped[part_id][round_number] = value

    return grouped


def build_core_analysis(
    state: dict[str, object],
) -> dict[str, object]:
    specimens = state["specimens"]
    manual_usable = state["manual_usable"]
    cv_usable = state["cv_usable"]

    specimen_by_id = {
        row["part_id"]: row
        for row in specimens
    }

    manual_by_part = group_by_part_and_round(
        manual_usable,
        "manual_round",
        "reading_in",
    )

    cv_by_part = group_by_part_and_round(
        cv_usable,
        "cv_round",
        "oal_in",
    )

    manual_summary: list[dict[str, object]] = []
    cv_summary: list[dict[str, object]] = []
    joined: list[dict[str, object]] = []

    for part_id in sorted(specimen_by_id, key=int):
        manual_values = [
            manual_by_part[part_id][1],
            manual_by_part[part_id][2],
            manual_by_part[part_id][3],
        ]

        cv_values = [
            cv_by_part[part_id][1],
            cv_by_part[part_id][2],
            cv_by_part[part_id][3],
        ]

        manual_mean = statistics.fmean(manual_values)
        cv_mean = statistics.fmean(cv_values)

        manual_sd = sample_sd(manual_values)
        cv_sd = sample_sd(cv_values)

        manual_range = max(manual_values) - min(manual_values)
        cv_range = max(cv_values) - min(cv_values)

        difference = cv_mean - manual_mean
        absolute_error = abs(difference)

        manual_summary.append(
            {
                "part_id": part_id,
                "manual_1_in": manual_values[0],
                "manual_2_in": manual_values[1],
                "manual_3_in": manual_values[2],
                "manual_mean_in": manual_mean,
                "manual_sd_in": manual_sd,
                "manual_range_in": manual_range,
                "manual_n_valid": 3,
            }
        )

        cv_summary.append(
            {
                "part_id": part_id,
                "cv_1_in": cv_values[0],
                "cv_2_in": cv_values[1],
                "cv_3_in": cv_values[2],
                "cv_mean_in": cv_mean,
                "cv_sd_in": cv_sd,
                "cv_range_in": cv_range,
                "cv_n_valid": 3,
            }
        )

        joined.append(
            {
                "part_id": part_id,
                "selection_stratum":
                    specimen_by_id[part_id]["selection_stratum"],
                "manual_mean_in": manual_mean,
                "manual_sd_in": manual_sd,
                "cv_mean_in": cv_mean,
                "cv_sd_in": cv_sd,
                "difference_in": difference,
                "absolute_error_in": absolute_error,
            }
        )

    if len(manual_summary) != EXPECTED_SPECIMENS:
        fail("Manual specimen summary does not contain exactly 60 rows")

    if len(cv_summary) != EXPECTED_SPECIMENS:
        fail("CV specimen summary does not contain exactly 60 rows")

    if len(joined) != EXPECTED_SPECIMENS:
        fail("Joined analysis population does not contain exactly 60 rows")

    # -------------------------------------------------------------
    # Frozen pooled manual repeatability term:
    #
    # s_p = sqrt(
    #     sum_i sum_j (M_ij - M_bar_i)^2
    #     /
    #     [60 * (3 - 1)]
    # )
    # -------------------------------------------------------------

    manual_mean_by_part = {
        row["part_id"]: row["manual_mean_in"]
        for row in manual_summary
    }

    residual_sum_squares = 0.0

    for row in manual_usable:
        value = float(row["reading_in"])
        mean_value = manual_mean_by_part[row["part_id"]]
        residual = value - mean_value
        residual_sum_squares += residual * residual

    pooled_manual_sd = math.sqrt(
        residual_sum_squares
        /
        (EXPECTED_SPECIMENS * (3 - 1))
    )

    # Frozen 2026-09-05 reference uncertainty.
    u_res = DISPLAY_INCREMENT_IN / math.sqrt(12.0)
    u_rep = pooled_manual_sd / math.sqrt(3.0)

    u_ref = math.sqrt(
        U_CAL_IN**2
        + u_res**2
        + u_rep**2
    )

    expanded_u_ref = 2.0 * u_ref

    # -------------------------------------------------------------
    # Primary specimen-level agreement.
    # -------------------------------------------------------------

    errors = [
        float(row["difference_in"])
        for row in joined
    ]

    absolute_errors = [
        float(row["absolute_error_in"])
        for row in joined
    ]

    bias = statistics.fmean(errors)
    median_signed_error = statistics.median(errors)
    signed_error_sd = sample_sd(errors)

    bias_standard_error = (
        signed_error_sd
        /
        math.sqrt(EXPECTED_SPECIMENS)
    )

    t_critical = stats.t.ppf(
        0.975,
        df=EXPECTED_SPECIMENS - 1,
    )

    bias_ci_lower = (
        bias
        - t_critical * bias_standard_error
    )

    bias_ci_upper = (
        bias
        + t_critical * bias_standard_error
    )

    mae = statistics.fmean(absolute_errors)

    rmse = math.sqrt(
        statistics.fmean(
            error * error
            for error in errors
        )
    )

    p95_absolute_error, p95_absolute_error_rank = (
        empirical_nearest_rank(
            absolute_errors,
            0.95,
        )
    )

    if p95_absolute_error_rank != 57:
        fail(
            "Frozen specimen-error P95 rank must equal 57 "
            f"for n=60; obtained {p95_absolute_error_rank}"
        )

    maximum_absolute_error = max(absolute_errors)

    # -------------------------------------------------------------
    # Formal CV repositioning repeatability:
    # three pairwise differences per specimen = 180.
    # -------------------------------------------------------------

    reposition_differences: list[float] = []

    for row in cv_summary:
        c1 = float(row["cv_1_in"])
        c2 = float(row["cv_2_in"])
        c3 = float(row["cv_3_in"])

        reposition_differences.extend(
            (
                abs(c1 - c2),
                abs(c1 - c3),
                abs(c2 - c3),
            )
        )

    if len(reposition_differences) != 180:
        fail(
            "Expected 180 CV repositioning pairwise differences, "
            f"found {len(reposition_differences)}"
        )

    reposition_p95, reposition_p95_rank = (
        empirical_nearest_rank(
            reposition_differences,
            0.95,
        )
    )

    if reposition_p95_rank != 171:
        fail(
            "Frozen repositioning P95 rank must equal 171 "
            f"for n=180; obtained {reposition_p95_rank}"
        )

    core = {
        "manual_summary": manual_summary,
        "cv_summary": cv_summary,
        "joined": joined,
        "reference_uncertainty": {
            "u_cal_in": U_CAL_IN,
            "u_res_in": u_res,
            "pooled_manual_sd_in": pooled_manual_sd,
            "u_rep_in": u_rep,
            "u_ref_in": u_ref,
            "expanded_u_ref_k2_in": expanded_u_ref,
        },
        "primary_agreement": {
            "n": EXPECTED_SPECIMENS,
            "bias_in": bias,
            "median_signed_error_in": median_signed_error,
            "signed_error_sd_in": signed_error_sd,
            "bias_95_ci_lower_in": bias_ci_lower,
            "bias_95_ci_upper_in": bias_ci_upper,
            "mae_in": mae,
            "rmse_in": rmse,
            "p95_absolute_error_in": p95_absolute_error,
            "p95_absolute_error_rank":
                p95_absolute_error_rank,
            "maximum_absolute_error_in":
                maximum_absolute_error,
        },
        "cv_repositioning": {
            "n_pairwise": len(reposition_differences),
            "mean_pairwise_difference_in":
                statistics.fmean(reposition_differences),
            "median_pairwise_difference_in":
                statistics.median(reposition_differences),
            "p95_pairwise_difference_in":
                reposition_p95,
            "p95_pairwise_difference_rank":
                reposition_p95_rank,
            "maximum_pairwise_difference_in":
                max(reposition_differences),
        },
    }

    # Nothing in this computation layer is allowed to silently
    # produce NaN or infinity.
    def verify_finite(value: object, path: str) -> None:
        if isinstance(value, float):
            if not math.isfinite(value):
                fail(f"Non-finite computed result: {path}")
        elif isinstance(value, dict):
            for key, child in value.items():
                verify_finite(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                verify_finite(child, f"{path}[{index}]")

    verify_finite(core, "core")

    return core




def verify_finite_tree(value: object, path: str = "result") -> None:
    if isinstance(value, float):
        if not math.isfinite(value):
            fail(f"Non-finite computed result: {path}")

    elif isinstance(value, dict):
        for key, child in value.items():
            verify_finite_tree(child, f"{path}.{key}")

    elif isinstance(value, list):
        for index, child in enumerate(value):
            verify_finite_tree(child, f"{path}[{index}]")


def threshold_status(
    observed: float,
    threshold: float,
    relation: str,
) -> str:
    if relation == "<=":
        return "MET" if observed <= threshold else "NOT_MET"

    if relation == ">=":
        return "MET" if observed >= threshold else "NOT_MET"

    fail(f"Unsupported threshold relation: {relation}")


def build_extended_analysis(
    state: dict[str, object],
    core: dict[str, object],
) -> dict[str, object]:

    joined = core["joined"]
    manual_summary = core["manual_summary"]
    cv_summary = core["cv_summary"]

    primary = core["primary_agreement"]
    reference_uncertainty = core["reference_uncertainty"]
    repositioning = core["cv_repositioning"]

    expanded_u_ref = float(
        reference_uncertainty["expanded_u_ref_k2_in"]
    )

    # =============================================================
    # CV availability
    #
    # Frozen SAP:
    #
    # Availability =
    # N_VALID / (N_VALID + N_SYSTEM_FAILURE) * 100
    #
    # PROTOCOL_INVALID does not enter this denominator.
    # =============================================================

    cv_all = state["cv_all"]

    cv_status_counts = Counter(
        row["measurement_status"].strip().upper()
        for row in cv_all
    )

    n_cv_valid = cv_status_counts["VALID"]
    n_cv_system_failure = cv_status_counts["SYSTEM_FAILURE"]

    availability_denominator = (
        n_cv_valid
        + n_cv_system_failure
    )

    if availability_denominator == 0:
        fail("CV availability denominator is zero")

    availability_pct = (
        100.0
        * n_cv_valid
        / availability_denominator
    )

    # System failures by specimen are retained for stratum summaries.
    cv_system_failures_by_part: Counter[str] = Counter()

    for row in cv_all:
        if (
            row["measurement_status"].strip().upper()
            == "SYSTEM_FAILURE"
        ):
            cv_system_failures_by_part[row["part_id"]] += 1

    # =============================================================
    # Bland-Altman agreement
    # =============================================================

    errors = [
        float(row["difference_in"])
        for row in joined
    ]

    magnitudes = [
        (
            float(row["cv_mean_in"])
            + float(row["manual_mean_in"])
        )
        / 2.0
        for row in joined
    ]

    if len(errors) != EXPECTED_SPECIMENS:
        fail("Bland-Altman population is not exactly 60 specimens")

    bias = statistics.fmean(errors)
    error_sd = sample_sd(errors)

    loa_lower = bias - 1.96 * error_sd
    loa_upper = bias + 1.96 * error_sd

    # Approximate standard error for each Bland-Altman limit.
    n = EXPECTED_SPECIMENS

    loa_standard_error = (
        error_sd
        * math.sqrt(
            (1.0 / n)
            + ((1.96**2) / (2.0 * (n - 1)))
        )
    )

    loa_t_critical = stats.t.ppf(
        0.975,
        df=n - 1,
    )

    loa_lower_ci_lower = (
        loa_lower
        - loa_t_critical * loa_standard_error
    )

    loa_lower_ci_upper = (
        loa_lower
        + loa_t_critical * loa_standard_error
    )

    loa_upper_ci_lower = (
        loa_upper
        - loa_t_critical * loa_standard_error
    )

    loa_upper_ci_upper = (
        loa_upper
        + loa_t_critical * loa_standard_error
    )

    bland_altman = {
        "n": n,
        "bias_in": bias,
        "difference_sd_in": error_sd,
        "loa_lower_in": loa_lower,
        "loa_upper_in": loa_upper,
        "loa_standard_error_in": loa_standard_error,
        "loa_lower_95_ci_lower_in": loa_lower_ci_lower,
        "loa_lower_95_ci_upper_in": loa_lower_ci_upper,
        "loa_upper_95_ci_lower_in": loa_upper_ci_lower,
        "loa_upper_95_ci_upper_in": loa_upper_ci_upper,
        "magnitudes_in": magnitudes,
        "differences_in": errors,
    }

    # =============================================================
    # Regression / correlation
    #
    # These remain secondary diagnostic agreement evidence.
    # =============================================================

    manual_means = [
        float(row["manual_mean_in"])
        for row in joined
    ]

    cv_means = [
        float(row["cv_mean_in"])
        for row in joined
    ]

    regression_result = stats.linregress(
        manual_means,
        cv_means,
    )

    regression_df = n - 2

    regression_t_critical = stats.t.ppf(
        0.975,
        df=regression_df,
    )

    slope = float(regression_result.slope)
    intercept = float(regression_result.intercept)

    slope_stderr = float(regression_result.stderr)

    intercept_stderr = float(
        regression_result.intercept_stderr
    )

    slope_ci_lower = (
        slope
        - regression_t_critical * slope_stderr
    )

    slope_ci_upper = (
        slope
        + regression_t_critical * slope_stderr
    )

    intercept_ci_lower = (
        intercept
        - regression_t_critical * intercept_stderr
    )

    intercept_ci_upper = (
        intercept
        + regression_t_critical * intercept_stderr
    )

    pearson_result = stats.pearsonr(
        manual_means,
        cv_means,
    )

    pearson_r = float(pearson_result.statistic)
    pearson_p = float(pearson_result.pvalue)

    regression = {
        "n": n,
        "slope": slope,
        "slope_95_ci_lower": slope_ci_lower,
        "slope_95_ci_upper": slope_ci_upper,
        "intercept_in": intercept,
        "intercept_95_ci_lower_in": intercept_ci_lower,
        "intercept_95_ci_upper_in": intercept_ci_upper,
        "pearson_r": pearson_r,
        "pearson_p_value": pearson_p,
        "r_squared": pearson_r**2,
    }

    # =============================================================
    # Primary point-estimate specification classification
    #
    # 0.9900 <= OAL <= 1.0100 is conforming.
    #
    # Nonconforming is treated as the "positive" condition for
    # sensitivity/specificity.
    # =============================================================

    analysis_rows: list[dict[str, object]] = []

    classification_counts: Counter[str] = Counter()

    for row in joined:
        result = dict(row)

        manual_mean = float(row["manual_mean_in"])
        cv_mean = float(row["cv_mean_in"])
        difference = float(row["difference_in"])

        reference_conforming = (
            LSL_IN <= manual_mean <= USL_IN
        )

        cv_conforming = (
            LSL_IN <= cv_mean <= USL_IN
        )

        uncertainty_overlap = (
            abs(manual_mean - LSL_IN) <= expanded_u_ref
            or
            abs(manual_mean - USL_IN) <= expanded_u_ref
        )

        if (
            not reference_conforming
            and not cv_conforming
        ):
            classification = "TRUE_NONCONFORMING"

        elif (
            not reference_conforming
            and cv_conforming
        ):
            classification = "FALSE_PASS"

        elif (
            reference_conforming
            and not cv_conforming
        ):
            classification = "FALSE_FAIL"

        else:
            classification = "TRUE_CONFORMING"

        classification_counts[classification] += 1

        result.update(
            {
                "percent_error":
                    100.0 * difference / manual_mean,
                "reference_conforming":
                    reference_conforming,
                "cv_conforming":
                    cv_conforming,
                "classification_outcome":
                    classification,
                "uncertainty_overlap_flag":
                    uncertainty_overlap,
                "cv_n_valid": 3,
                "cv_failure_count":
                    cv_system_failures_by_part[
                        row["part_id"]
                    ],
                "analysis_included": True,
                "exclusion_reason": "",
            }
        )

        analysis_rows.append(result)

    if len(analysis_rows) != EXPECTED_SPECIMENS:
        fail(
            "Classification population is not exactly "
            "60 specimens"
        )

    true_nonconforming = (
        classification_counts["TRUE_NONCONFORMING"]
    )

    false_passes = (
        classification_counts["FALSE_PASS"]
    )

    false_fails = (
        classification_counts["FALSE_FAIL"]
    )

    true_conforming = (
        classification_counts["TRUE_CONFORMING"]
    )

    sensitivity_denominator = (
        true_nonconforming
        + false_passes
    )

    specificity_denominator = (
        true_conforming
        + false_fails
    )

    sensitivity_nonconforming = (
        true_nonconforming
        / sensitivity_denominator
        if sensitivity_denominator
        else None
    )

    specificity_conforming = (
        true_conforming
        / specificity_denominator
        if specificity_denominator
        else None
    )

    uncertainty_overlap_count = sum(
        bool(row["uncertainty_overlap_flag"])
        for row in analysis_rows
    )

    classification = {
        "n": len(analysis_rows),
        "true_nonconforming": true_nonconforming,
        "false_passes": false_passes,
        "false_fails": false_fails,
        "true_conforming": true_conforming,
        "sensitivity_detect_nonconforming":
            sensitivity_nonconforming,
        "specificity_conforming":
            specificity_conforming,
        "uncertainty_overlap_count":
            uncertainty_overlap_count,
    }

    # =============================================================
    # Manual and CV specimen-level repeatability summaries
    # =============================================================

    manual_sds = [
        float(row["manual_sd_in"])
        for row in manual_summary
    ]

    manual_ranges = [
        float(row["manual_range_in"])
        for row in manual_summary
    ]

    cv_sds = [
        float(row["cv_sd_in"])
        for row in cv_summary
    ]

    cv_ranges = [
        float(row["cv_range_in"])
        for row in cv_summary
    ]

    manual_sd_p95, manual_sd_rank = empirical_nearest_rank(
        manual_sds,
        0.95,
    )

    manual_range_p95, manual_range_rank = (
        empirical_nearest_rank(
            manual_ranges,
            0.95,
        )
    )

    cv_sd_p95, cv_sd_rank = empirical_nearest_rank(
        cv_sds,
        0.95,
    )

    cv_range_p95, cv_range_rank = (
        empirical_nearest_rank(
            cv_ranges,
            0.95,
        )
    )

    for rank in (
        manual_sd_rank,
        manual_range_rank,
        cv_sd_rank,
        cv_range_rank,
    ):
        if rank != 57:
            fail(
                "Specimen repeatability P95 rank "
                f"must equal 57; obtained {rank}"
            )

    repeatability = {
        "manual": {
            "n_specimens": EXPECTED_SPECIMENS,
            "mean_sd_in": statistics.fmean(manual_sds),
            "median_sd_in": statistics.median(manual_sds),
            "p95_sd_in": manual_sd_p95,
            "max_sd_in": max(manual_sds),
            "mean_range_in":
                statistics.fmean(manual_ranges),
            "median_range_in":
                statistics.median(manual_ranges),
            "p95_range_in": manual_range_p95,
            "max_range_in": max(manual_ranges),
            "pooled_sd_in":
                float(
                    reference_uncertainty[
                        "pooled_manual_sd_in"
                    ]
                ),
        },
        "cv": {
            "n_specimens": EXPECTED_SPECIMENS,
            "mean_sd_in": statistics.fmean(cv_sds),
            "median_sd_in": statistics.median(cv_sds),
            "p95_sd_in": cv_sd_p95,
            "max_sd_in": max(cv_sds),
            "mean_range_in":
                statistics.fmean(cv_ranges),
            "median_range_in":
                statistics.median(cv_ranges),
            "p95_range_in": cv_range_p95,
            "max_range_in": max(cv_ranges),
        },
    }

    # =============================================================
    # Five frozen sampling-stratum summaries
    #
    # Strata are NEVER reassigned from formal manual measurements.
    # =============================================================

    stratum_order = (
        "below_lsl",
        "near_lsl_in_spec",
        "central_nominal",
        "near_usl_in_spec",
        "above_usl",
    )

    stratum_summaries: list[dict[str, object]] = []

    for stratum in stratum_order:
        rows = [
            row
            for row in analysis_rows
            if row["selection_stratum"] == stratum
        ]

        if len(rows) != EXPECTED_STRATA[stratum]:
            fail(
                f"Stratum {stratum} count changed: "
                f"expected {EXPECTED_STRATA[stratum]}, "
                f"found {len(rows)}"
            )

        stratum_errors = [
            float(row["difference_in"])
            for row in rows
        ]

        stratum_abs_errors = [
            float(row["absolute_error_in"])
            for row in rows
        ]

        outcomes = Counter(
            str(row["classification_outcome"])
            for row in rows
        )

        stratum_summaries.append(
            {
                "selection_stratum": stratum,
                "n_specimens": len(rows),
                "valid_cv_observations":
                    sum(
                        int(row["cv_n_valid"])
                        for row in rows
                    ),
                "system_failures":
                    sum(
                        int(row["cv_failure_count"])
                        for row in rows
                    ),
                "mean_signed_error_in":
                    statistics.fmean(stratum_errors),
                "median_signed_error_in":
                    statistics.median(stratum_errors),
                "mae_in":
                    statistics.fmean(
                        stratum_abs_errors
                    ),
                "maximum_absolute_error_in":
                    max(stratum_abs_errors),
                "reference_conforming_count":
                    sum(
                        bool(row["reference_conforming"])
                        for row in rows
                    ),
                "cv_conforming_count":
                    sum(
                        bool(row["cv_conforming"])
                        for row in rows
                    ),
                "true_nonconforming":
                    outcomes["TRUE_NONCONFORMING"],
                "false_passes":
                    outcomes["FALSE_PASS"],
                "false_fails":
                    outcomes["FALSE_FAIL"],
                "true_conforming":
                    outcomes["TRUE_CONFORMING"],
                "uncertainty_overlap_count":
                    sum(
                        bool(
                            row[
                                "uncertainty_overlap_flag"
                            ]
                        )
                        for row in rows
                    ),
            }
        )

    # =============================================================
    # Primary prespecified target evaluation
    # =============================================================

    criteria = {
        "cv_availability": {
            "observed": availability_pct,
            "target": TARGET_AVAILABILITY_PCT,
            "relation": ">=",
            "status": threshold_status(
                availability_pct,
                TARGET_AVAILABILITY_PCT,
                ">=",
            ),
        },
        "cv_repositioning_p95": {
            "observed":
                float(
                    repositioning[
                        "p95_pairwise_difference_in"
                    ]
                ),
            "target": TARGET_P95_REPOSITION_IN,
            "relation": "<=",
            "status": threshold_status(
                float(
                    repositioning[
                        "p95_pairwise_difference_in"
                    ]
                ),
                TARGET_P95_REPOSITION_IN,
                "<=",
            ),
        },
        "absolute_mean_bias": {
            "observed": abs(float(primary["bias_in"])),
            "target": TARGET_ABS_BIAS_IN,
            "relation": "<=",
            "status": threshold_status(
                abs(float(primary["bias_in"])),
                TARGET_ABS_BIAS_IN,
                "<=",
            ),
        },
        "rmse": {
            "observed": float(primary["rmse_in"]),
            "target": TARGET_RMSE_IN,
            "relation": "<=",
            "status": threshold_status(
                float(primary["rmse_in"]),
                TARGET_RMSE_IN,
                "<=",
            ),
        },
        "p95_absolute_specimen_error": {
            "observed":
                float(
                    primary[
                        "p95_absolute_error_in"
                    ]
                ),
            "target": TARGET_P95_ABS_ERROR_IN,
            "relation": "<=",
            "status": threshold_status(
                float(
                    primary[
                        "p95_absolute_error_in"
                    ]
                ),
                TARGET_P95_ABS_ERROR_IN,
                "<=",
            ),
        },
        "maximum_absolute_specimen_error": {
            "observed":
                float(
                    primary[
                        "maximum_absolute_error_in"
                    ]
                ),
            "target": TARGET_MAX_ABS_ERROR_IN,
            "relation": "<=",
            "status": threshold_status(
                float(
                    primary[
                        "maximum_absolute_error_in"
                    ]
                ),
                TARGET_MAX_ABS_ERROR_IN,
                "<=",
            ),
        },
    }

    primary_thresholds_met = all(
        result["status"] == "MET"
        for result in criteria.values()
    )

    zero_false_pass_preference_met = (
        false_passes == 0
    )

    # The SAP states that any confirmed false pass blocks an
    # unconditional acceptance conclusion unless prospectively
    # defensible treatment has already been established.
    if not primary_thresholds_met:
        overall_interpretation = (
            "ONE_OR_MORE_PRIMARY_TARGETS_NOT_MET"
        )

    elif not zero_false_pass_preference_met:
        overall_interpretation = (
            "PRIMARY_NUMERIC_TARGETS_MET_BUT_FALSE_PASS_"
            "BLOCKS_UNCONDITIONAL_ACCEPTANCE"
        )

    else:
        overall_interpretation = (
            "ALL_PRIMARY_NUMERIC_TARGETS_MET_AND_"
            "ZERO_FALSE_PASS_PREFERENCE_MET"
        )

    extended = {
        "availability": {
            "n_valid": n_cv_valid,
            "n_system_failure": n_cv_system_failure,
            "denominator": availability_denominator,
            "availability_pct": availability_pct,
        },
        "bland_altman": bland_altman,
        "regression": regression,
        "classification": classification,
        "repeatability": repeatability,
        "stratum_summaries": stratum_summaries,
        "analysis_rows": analysis_rows,
        "criteria": criteria,
        "zero_false_pass_preference": {
            "observed_false_passes": false_passes,
            "preferred": 0,
            "status":
                "MET"
                if zero_false_pass_preference_met
                else "NOT_MET",
        },
        "overall_interpretation":
            overall_interpretation,
    }

    verify_finite_tree(extended)

    return extended

def package_version(name: str) -> str:
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return "NOT INSTALLED"


def run_check(
    repo_root: Path,
    data_root: Path,
    compute: bool = False,
) -> None:
    print("=== FORMAL OAL ANALYSIS IMPLEMENTATION CHECK ===")
    print(f"Python: {platform.python_version()}")
    print(f"NumPy: {package_version('numpy')}")
    print(f"pandas: {package_version('pandas')}")
    print(f"SciPy: {package_version('scipy')}")
    print(f"matplotlib: {package_version('matplotlib')}")

    print()
    print("=== FROZEN INPUT IDENTITY ===")
    hashes = verify_frozen_inputs(repo_root, data_root)

    for path, digest in hashes.items():
        print(f"PASS {path}")
        print(f"  SHA-256 {digest}")

    print()
    print("=== ANALYSIS POPULATION ===")
    state = validate_dataset(data_root)

    print(f"Frozen specimens: {len(state['specimens'])}")
    print(f"Usable manual observations: {len(state['manual_usable'])}")
    print(
        "Preserved protocol-invalid manual rows: "
        f"{len(state['manual_invalid'])}"
    )
    print(f"Usable CV observations: {len(state['cv_usable'])}")
    print(
        "Accepted manual sessions: "
        f"{len(state['accepted_sessions'])}"
    )

    print()
    print("Frozen strata:")

    for name in (
        "below_lsl",
        "near_lsl_in_spec",
        "central_nominal",
        "near_usl_in_spec",
        "above_usl",
    ):
        print(f"  {name}: {state['strata'][name]}")

    print()
    print("PASS: frozen input files match acquisition commit")
    print("PASS: formal analysis population resolves correctly")
    print("PASS: protocol-invalid observations remain excluded")
    print("PASS: all 60 specimens have three usable rounds per method")
    print("PASS: usable observations exactly cover frozen run orders")
    print("PASS: manual sessions are accepted")
    print("PASS: no unresolved protocol deviations")

    if compute:
        core = build_core_analysis(state)
        build_extended_analysis(state, core)

        print()
        print("=== CORE STATISTICAL IMPLEMENTATION ===")
        print("PASS: 60 manual specimen summaries computed in memory")
        print("PASS: 60 CV specimen summaries computed in memory")
        print("PASS: CV - manual specimen errors computed in memory")
        print("PASS: pooled manual repeatability computed")
        print("PASS: frozen reference uncertainty model computed")
        print("PASS: bias and 95% t confidence interval computed")
        print("PASS: MAE and RMSE computed")
        print("PASS: nearest-rank specimen P95 uses rank 57")
        print("PASS: maximum absolute error computed")
        print("PASS: 180 CV repositioning differences computed")
        print("PASS: nearest-rank repositioning P95 uses rank 171")
        print("PASS: all computed quantities are finite")

        print()
        print("=== EXTENDED STATISTICAL IMPLEMENTATION ===")
        print("PASS: frozen CV availability computed")
        print("PASS: Bland-Altman bias and limits computed")
        print("PASS: 95% confidence intervals for limits computed")
        print("PASS: OLS regression and coefficient CIs computed")
        print("PASS: Pearson correlation and R-squared computed")
        print("PASS: primary point-estimate classification computed")
        print("PASS: false-pass and false-fail accounting computed")
        print("PASS: sensitivity and specificity computed where defined")
        print("PASS: uncertainty-overlap flags computed separately")
        print("PASS: manual repeatability summaries computed")
        print("PASS: CV specimen repeatability summaries computed")
        print("PASS: five frozen stratum summaries computed")
        print("PASS: primary performance criteria evaluated")
        print("PASS: no numerical validation results were displayed")

    print()
    print("CHECK PASS")
    print("No statistical analysis outputs were created.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Formal CaseMetrology OAL validation analysis"
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/oal_validation"),
        help="formal OAL validation data root",
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--check-only",
        action="store_true",
        help=(
            "verify immutable inputs and analysis population "
            "without statistical calculations or outputs"
        ),
    )

    mode.add_argument(
        "--compute-check",
        action="store_true",
        help=(
            "execute frozen core statistical formulas in memory "
            "without printing results or creating output files"
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    repo_root = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            text=True,
        ).strip()
    ).resolve()

    data_root = args.root.resolve()

    if not data_root.is_relative_to(repo_root):
        fail(f"Data root is outside repository: {data_root}")

    if args.check_only:
        run_check(
            repo_root,
            data_root,
            compute=False,
        )
        return 0

    if args.compute_check:
        run_check(
            repo_root,
            data_root,
            compute=True,
        )
        return 0

    fail("No analysis mode selected")



if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"CHECK FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
