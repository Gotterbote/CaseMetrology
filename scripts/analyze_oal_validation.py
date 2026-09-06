#!/usr/bin/env python3
"""
Formal OAL validation analysis.

Primary analysis unit:
    unique specimen (n = 60)

Frozen completed acquisition dataset:
    0c746036680cd01cc7ae5b2248cdadf8aae878cf

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
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


FROZEN_DATASET_COMMIT = "0c746036680cd01cc7ae5b2248cdadf8aae878cf"

EXPECTED_SPECIMENS = 60
EXPECTED_ROUNDS = {1, 2, 3}
EXPECTED_USABLE_MANUAL = 180
EXPECTED_USABLE_CV = 180

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
    "cv_run_order.csv",
    "manual_reference_observations.csv",
    "manual_reference_checks.csv",
    "manual_sessions.csv",
    "environmental_observations.csv",
    "cv_observations.csv",
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
    cv_run_order = read_csv(data_root / "cv_run_order.csv")
    manual = read_csv(data_root / "manual_reference_observations.csv")
    cv = read_csv(data_root / "cv_observations.csv")
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
        "strata": strata,
        "accepted_sessions": accepted_sessions,
        "deviations": deviations,
    }


def package_version(name: str) -> str:
    try:
        from importlib.metadata import version

        return version(name)
    except Exception:
        return "NOT INSTALLED"


def run_check(repo_root: Path, data_root: Path) -> None:
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
    print(f"Preserved protocol-invalid manual rows: {len(state['manual_invalid'])}")
    print(f"Usable CV observations: {len(state['cv_usable'])}")
    print(f"Accepted manual sessions: {len(state['accepted_sessions'])}")

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
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="verify immutable inputs and analysis population without outputs",
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

    if not args.check_only:
        fail(
            "Output generation is intentionally disabled in this "
            "implementation stage. Run with --check-only."
        )

    run_check(repo_root, data_root)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"CHECK FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
