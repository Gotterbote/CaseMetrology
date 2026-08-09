"""Audit OAL population-screening data before validation-sample selection."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_MIN_PART_ID = 1
EXPECTED_MAX_PART_ID = 235
LSL_IN = 0.990
USL_IN = 1.010


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit CaseMetrology OAL screening data for completeness, "
            "traceability, duplicates, missing records, and population summary."
        )
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        help="Completed OAL screening CSV to audit.",
    )
    return parser.parse_args()


def clean(value: str | None) -> str:
    return "" if value is None else value.strip()


def main() -> int:
    args = parse_args()

    if not args.csv_path.is_file():
        print(f"ERROR: file not found: {args.csv_path}")
        return 2

    with args.csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)

        required_columns = {
            "part_id",
            "laser_etched_id_verified",
            "screening_reading_in",
            "screening_date",
            "screening_time",
            "screening_operator",
            "caliper_serial_number",
            "session_id",
        }

        actual_columns = set(reader.fieldnames or [])
        missing_columns = sorted(required_columns - actual_columns)

        if missing_columns:
            print("FAIL: required columns are missing:")
            for column in missing_columns:
                print(f"  - {column}")
            return 1

        rows = list(reader)

    issues: list[str] = []
    part_ids: list[int] = []
    readings: list[float] = []
    row_records: list[tuple[int, int, float]] = []
    sessions: defaultdict[str, int] = defaultdict(int)

    for row_number, row in enumerate(rows, start=2):
        raw_part_id = clean(row.get("part_id"))
        raw_reading = clean(row.get("screening_reading_in"))

        # Ignore completely unused template rows.
        if not raw_part_id and not raw_reading:
            continue

        try:
            part_id = int(raw_part_id)
        except ValueError:
            issues.append(f"row {row_number}: invalid part_id {raw_part_id!r}")
            continue

        part_ids.append(part_id)

        if not EXPECTED_MIN_PART_ID <= part_id <= EXPECTED_MAX_PART_ID:
            issues.append(
                f"row {row_number}: part_id {part_id} outside "
                f"{EXPECTED_MIN_PART_ID}-{EXPECTED_MAX_PART_ID}"
            )

        if not raw_reading:
            issues.append(
                f"row {row_number}: part_id {part_id} has no screening reading"
            )
            continue

        try:
            reading = float(raw_reading)
        except ValueError:
            issues.append(
                f"row {row_number}: part_id {part_id} has nonnumeric "
                f"screening reading {raw_reading!r}"
            )
            continue

        if not math.isfinite(reading):
            issues.append(f"row {row_number}: part_id {part_id} has non-finite reading")
            continue

        readings.append(reading)
        row_records.append((row_number, part_id, reading))

        verified = clean(row.get("laser_etched_id_verified")).lower()
        if verified not in {"yes", "y", "true", "1"}:
            issues.append(f"row {row_number}: part_id {part_id} laser ID not verified")

        for field in (
            "screening_date",
            "screening_time",
            "screening_operator",
            "caliper_serial_number",
            "session_id",
        ):
            if not clean(row.get(field)):
                issues.append(f"row {row_number}: part_id {part_id} missing {field}")

        session_id = clean(row.get("session_id"))
        if session_id:
            sessions[session_id] += 1

    counts = Counter(part_ids)
    duplicates = sorted(part_id for part_id, count in counts.items() if count > 1)

    expected_ids = set(range(EXPECTED_MIN_PART_ID, EXPECTED_MAX_PART_ID + 1))
    observed_ids = {
        part_id
        for part_id in part_ids
        if EXPECTED_MIN_PART_ID <= part_id <= EXPECTED_MAX_PART_ID
    }
    missing_ids = sorted(expected_ids - observed_ids)

    print("=== OAL SCREENING AUDIT ===")
    print(f"Source: {args.csv_path}")
    print(f"Expected population: {len(expected_ids)}")
    print(f"Rows with part IDs: {len(part_ids)}")
    print(f"Unique valid part IDs: {len(observed_ids)}")
    print(f"Valid numeric readings: {len(readings)}")
    print()

    print("=== COMPLETENESS ===")
    print(f"Missing IDs: {len(missing_ids)}")
    if missing_ids:
        print("  " + ", ".join(map(str, missing_ids)))

    print(f"Duplicate IDs: {len(duplicates)}")
    if duplicates:
        for part_id in duplicates:
            print(f"  part_id {part_id}: {counts[part_id]} records")

    print()
    print("=== TRACEABILITY / DATA ISSUES ===")
    print(f"Issue count: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")

    if readings:
        sorted_readings = sorted(readings)

        below_lsl = sum(value < LSL_IN for value in readings)
        in_spec = sum(LSL_IN <= value <= USL_IN for value in readings)
        above_usl = sum(value > USL_IN for value in readings)

        print()
        print("=== POPULATION SUMMARY ===")
        print(f"Count: {len(readings)}")
        print(f"Mean: {statistics.fmean(readings):.6f} in")
        print(f"Median: {statistics.median(readings):.6f} in")

        if len(readings) > 1:
            print(f"Sample SD: {statistics.stdev(readings):.6f} in")
        else:
            print("Sample SD: N/A")

        print(f"Minimum: {min(readings):.6f} in")
        print(f"Maximum: {max(readings):.6f} in")
        print(f"Range: {max(readings) - min(readings):.6f} in")

        if len(sorted_readings) >= 4:
            quartiles = statistics.quantiles(
                sorted_readings,
                n=4,
                method="inclusive",
            )
            print(f"Q1: {quartiles[0]:.6f} in")
            print(f"Q3: {quartiles[2]:.6f} in")

        print(f"Below LSL ({LSL_IN:.3f}): {below_lsl}")
        print(f"In specification " f"({LSL_IN:.3f}-{USL_IN:.3f}): {in_spec}")
        print(f"Above USL ({USL_IN:.3f}): {above_usl}")

    print()
    print("=== SESSION COUNTS ===")
    if sessions:
        for session_id in sorted(sessions):
            print(f"{session_id}: {sessions[session_id]}")
    else:
        print("No populated session IDs.")

    complete = (
        len(observed_ids) == len(expected_ids)
        and not missing_ids
        and not duplicates
        and len(readings) == len(expected_ids)
        and not issues
    )

    print()
    print("=== DISPOSITION ===")
    if complete:
        print(
            "PASS: screening dataset is complete and eligible for "
            "population characterization and stratification."
        )
        return 0

    print("HOLD: screening dataset is not yet eligible for formal " "stratification.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
