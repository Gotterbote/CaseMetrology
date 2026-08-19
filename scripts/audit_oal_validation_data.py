#!/usr/bin/env python3
"""Audit CaseMetrology formal OAL validation data for structural integrity.

Run now with --self-test to verify the script itself without generating or
using any official formal-validation data.

Later:
  python scripts/audit_oal_validation_data.py --root data/oal_validation --stage pre_measurement
  python scripts/audit_oal_validation_data.py --root data/oal_validation --stage analysis_ready
"""

from __future__ import annotations

import argparse
import csv
import tempfile
import sys
from collections import defaultdict
from pathlib import Path

MANUAL_SEED = "2026081901"
CV_SEED = "2026081902"
VALID_CV_STATUS = {"VALID", "SYSTEM_FAILURE", "PROTOCOL_INVALID"}

SPECIMEN_REQUIRED = {
    "part_id",
    "laser_etched_id_verified",
    "screening_reading_in",
    "screening_class",
    "selection_stratum",
    "selected_for_validation",
    "selection_seed",
    "selection_order",
    "selection_timestamp",
    "selection_script_commit",
    "notes",
}
MANUAL_RUN_REQUIRED = {
    "manual_run_id",
    "manual_round",
    "planned_sequence",
    "part_id",
    "selection_stratum",
    "randomization_seed",
    "run_order_generated_at",
    "run_order_script_commit",
    "completion_status",
    "session_id",
    "notes",
}
CV_RUN_REQUIRED = {
    "cv_run_id",
    "cv_round",
    "planned_sequence",
    "part_id",
    "selection_stratum",
    "randomization_seed",
    "run_order_generated_at",
    "run_order_script_commit",
    "completion_status",
    "session_id",
    "notes",
}

RAW_FILES = {
    "manual_reference_observations.csv",
    "manual_reference_checks.csv",
    "manual_sessions.csv",
    "environmental_observations.csv",
    "cv_observations.csv",
    "protocol_deviations.csv",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def require_columns(path: Path, required: set[str]) -> list[dict[str, str]]:
    fields, rows = read_csv(path)
    missing = required - set(fields)
    if missing:
        raise AssertionError(f"{path}: missing columns {sorted(missing)}")
    return rows


def audit_core(root: Path, expected_specimens: int = 60) -> list[str]:
    messages: list[str] = []
    specimens = require_columns(
        root / "formal_validation_specimens.csv", SPECIMEN_REQUIRED
    )
    selected = [
        r
        for r in specimens
        if r["selected_for_validation"].strip().lower() in {"1", "true", "yes", "y"}
    ]
    if len(selected) != expected_specimens:
        raise AssertionError(
            f"Expected {expected_specimens} selected specimens; found {len(selected)}."
        )
    ids = [r["part_id"].strip() for r in selected]
    if len(ids) != len(set(ids)):
        raise AssertionError("Duplicate part_id in formal validation sample.")
    selected_ids = set(ids)
    messages.append(f"PASS: {len(selected_ids)} unique frozen specimens")

    def audit_run(path: Path, round_field: str, seed: str, id_field: str) -> None:
        required = MANUAL_RUN_REQUIRED if "manual" in path.name else CV_RUN_REQUIRED
        rows = require_columns(path, required)
        if len(rows) != expected_specimens * 3:
            raise AssertionError(
                f"{path}: expected {expected_specimens*3} rows; found {len(rows)}."
            )
        by_round = defaultdict(list)
        run_ids = set()
        for r in rows:
            run_id = r[id_field].strip()
            if not run_id or run_id in run_ids:
                raise AssertionError(
                    f"{path}: blank or duplicate {id_field}: {run_id!r}"
                )
            run_ids.add(run_id)
            rnd = int(r[round_field])
            seq = int(r["planned_sequence"])
            pid = r["part_id"].strip()
            if pid not in selected_ids:
                raise AssertionError(f"{path}: unauthorized part_id {pid}")
            if r["randomization_seed"].strip() != seed:
                raise AssertionError(
                    f"{path}: unexpected seed {r['randomization_seed']!r}"
                )
            by_round[rnd].append((seq, pid))
        if set(by_round) != {1, 2, 3}:
            raise AssertionError(
                f"{path}: rounds are {sorted(by_round)}, expected [1,2,3]."
            )
        previous_last = None
        for rnd in (1, 2, 3):
            ordered = sorted(by_round[rnd])
            if [s for s, _ in ordered] != list(range(1, expected_specimens + 1)):
                raise AssertionError(f"{path}: sequence problem in round {rnd}.")
            round_ids = [pid for _, pid in ordered]
            if set(round_ids) != selected_ids or len(round_ids) != expected_specimens:
                raise AssertionError(
                    f"{path}: specimen coverage problem in round {rnd}."
                )
            if previous_last is not None and round_ids[0] == previous_last:
                raise AssertionError(
                    f"{path}: immediate cross-round repeat at round {rnd}."
                )
            previous_last = round_ids[-1]
        messages.append(f"PASS: {path.name} has 3 complete randomized rounds")

    audit_run(
        root / "manual_run_order.csv", "manual_round", MANUAL_SEED, "manual_run_id"
    )
    audit_run(root / "cv_run_order.csv", "cv_round", CV_SEED, "cv_run_id")
    return messages


def audit_analysis_ready(root: Path) -> list[str]:
    messages = []
    for name in RAW_FILES:
        if not (root / name).exists():
            raise AssertionError(f"Missing formal raw-data file: {root/name}")

    # Basic CV status and specimen checks.
    _, cv_rows = read_csv(root / "cv_observations.csv")
    _, specimen_rows = read_csv(root / "formal_validation_specimens.csv")
    selected_ids = {
        r["part_id"].strip()
        for r in specimen_rows
        if r["selected_for_validation"].strip().lower() in {"1", "true", "yes", "y"}
    }
    for r in cv_rows:
        pid = r.get("part_id", "").strip()
        if pid and pid not in selected_ids:
            raise AssertionError(f"cv_observations.csv: unauthorized part_id {pid}")
        status = r.get("measurement_status", "").strip()
        if status and status not in VALID_CV_STATUS:
            raise AssertionError(f"cv_observations.csv: invalid status {status!r}")
        if status == "VALID" and not r.get("oal_in", "").strip():
            raise AssertionError("cv_observations.csv: VALID row missing oal_in")

    messages.append("PASS: formal raw-data files present and basic CV statuses valid")
    return messages


def build_self_test(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    specimen_fields = list(SPECIMEN_REQUIRED)
    with (root / "formal_validation_specimens.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(f, fieldnames=specimen_fields)
        w.writeheader()
        for i in range(1, 61):
            w.writerow(
                {
                    "part_id": i,
                    "laser_etched_id_verified": "true",
                    "screening_reading_in": "1.0000",
                    "screening_class": "mock",
                    "selection_stratum": "mock",
                    "selected_for_validation": "true",
                    "selection_seed": "selftest",
                    "selection_order": i,
                    "selection_timestamp": "2026-08-19T00:00:00-05:00",
                    "selection_script_commit": "mock",
                    "notes": "",
                }
            )

    def write_run(path: Path, manual: bool) -> None:
        fields = list(MANUAL_RUN_REQUIRED if manual else CV_RUN_REQUIRED)
        # Preserve the protocol header order:
        fields = (
            [
                "manual_run_id",
                "manual_round",
                "planned_sequence",
                "part_id",
                "selection_stratum",
                "randomization_seed",
                "run_order_generated_at",
                "run_order_script_commit",
                "completion_status",
                "session_id",
                "notes",
            ]
            if manual
            else [
                "cv_run_id",
                "cv_round",
                "planned_sequence",
                "part_id",
                "selection_stratum",
                "randomization_seed",
                "run_order_generated_at",
                "run_order_script_commit",
                "completion_status",
                "session_id",
                "notes",
            ]
        )
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            seed = MANUAL_SEED if manual else CV_SEED
            rid = "MAN" if manual else "CV"
            round_field = "manual_round" if manual else "cv_round"
            id_field = "manual_run_id" if manual else "cv_run_id"
            for rnd in (1, 2, 3):
                # Rotate so cross-round first/last are definitely different.
                ids = list(range(1, 61))
                shift = (rnd - 1) * 7
                ids = ids[shift:] + ids[:shift]
                for seq, pid in enumerate(ids, 1):
                    w.writerow(
                        {
                            id_field: f"{rid}-R{rnd}-{seq:03d}",
                            round_field: rnd,
                            "planned_sequence": seq,
                            "part_id": pid,
                            "selection_stratum": "mock",
                            "randomization_seed": seed,
                            "run_order_generated_at": "2026-08-19T00:00:00-05:00",
                            "run_order_script_commit": "mock",
                            "completion_status": "PLANNED",
                            "session_id": "",
                            "notes": "",
                        }
                    )

    write_run(root / "manual_run_order.csv", True)
    write_run(root / "cv_run_order.csv", False)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("data/oal_validation"))
    p.add_argument(
        "--stage",
        choices={"pre_measurement", "analysis_ready"},
        default="pre_measurement",
    )
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()

    if args.self_test:
        with tempfile.TemporaryDirectory() as td:
            mock = Path(td) / "oal_validation"
            build_self_test(mock)
            for msg in audit_core(mock):
                print(msg)
        print("SELF-TEST PASS")
        return 0

    messages = audit_core(args.root)
    if args.stage == "analysis_ready":
        messages.extend(audit_analysis_ready(args.root))
    for msg in messages:
        print(msg)
    print(f"AUDIT PASS: stage={args.stage}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError) as exc:
        print(f"AUDIT FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
