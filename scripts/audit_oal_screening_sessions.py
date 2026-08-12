"""Audit OAL screening-session controls and specimen/session linkage."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from collections import Counter
from pathlib import Path

EXPECTED_CALIPER_SERIAL = "B23090910"
EXPECTED_REFERENCE_IN = 1.0000024
ARITHMETIC_TOLERANCE_IN = 0.0000005

REFERENCE_FIELDS = [
    "pre_1_in",
    "pre_2_in",
    "pre_3_in",
    "pre_4_in",
    "pre_5_in",
    "post_1_in",
    "post_2_in",
    "post_3_in",
    "post_4_in",
    "post_5_in",
]

REQUIRED_COLUMNS = {
    "session_id",
    "session_date",
    "session_start_time",
    "session_end_time",
    "operator",
    "caliper_serial_number",
    "reference_standard_in",
    *REFERENCE_FIELDS,
    "pre_mean_in",
    "pre_range_in",
    "post_mean_in",
    "post_range_in",
    "session_status",
    "notes",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit CaseMetrology OAL screening-session reference checks "
            "and optionally verify specimen/session linkage."
        )
    )
    parser.add_argument(
        "sessions_csv",
        type=Path,
        help="OAL screening-session CSV to audit.",
    )
    parser.add_argument(
        "--screening-csv",
        type=Path,
        help="Optional specimen screening CSV for session-link verification.",
    )
    return parser.parse_args()


def clean(value: str | None) -> str:
    return "" if value is None else value.strip()


def parse_number(
    value: str | None,
    *,
    row_number: int,
    field: str,
    issues: list[str],
) -> float | None:
    raw = clean(value)

    if not raw:
        issues.append(f"row {row_number}: missing {field}")
        return None

    try:
        number = float(raw)
    except ValueError:
        issues.append(f"row {row_number}: invalid {field} {raw!r}")
        return None

    if not math.isfinite(number):
        issues.append(f"row {row_number}: non-finite {field}")
        return None

    return number


def verify_derived_value(
    recorded: float | None,
    calculated: float,
    *,
    row_number: int,
    field: str,
    issues: list[str],
) -> None:
    if recorded is None:
        return

    if abs(recorded - calculated) > ARITHMETIC_TOLERANCE_IN:
        issues.append(
            f"row {row_number}: {field}={recorded:.7f} does not match "
            f"calculated value {calculated:.7f}"
        )


def main() -> int:
    args = parse_args()

    if not args.sessions_csv.is_file():
        print(f"ERROR: file not found: {args.sessions_csv}")
        return 2

    with args.sessions_csv.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)

        actual_columns = set(reader.fieldnames or [])
        missing_columns = sorted(REQUIRED_COLUMNS - actual_columns)

        if missing_columns:
            print("FAIL: required session columns are missing:")
            for column in missing_columns:
                print(f"  - {column}")
            return 1

        rows = list(reader)

    issues: list[str] = []
    session_ids: list[str] = []
    valid_session_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=2):
        # Ignore a completely unused row.
        if not any(clean(value) for value in row.values()):
            continue

        session_id = clean(row.get("session_id"))

        if not session_id:
            issues.append(f"row {row_number}: missing session_id")
            continue

        session_ids.append(session_id)

        for field in (
            "session_date",
            "session_start_time",
            "session_end_time",
            "operator",
            "caliper_serial_number",
            "reference_standard_in",
            "session_status",
        ):
            if not clean(row.get(field)):
                issues.append(f"row {row_number}: session {session_id} missing {field}")

        caliper_serial = clean(row.get("caliper_serial_number"))
        if caliper_serial and caliper_serial != EXPECTED_CALIPER_SERIAL:
            issues.append(
                f"row {row_number}: session {session_id} caliper serial "
                f"{caliper_serial!r} does not match expected "
                f"{EXPECTED_CALIPER_SERIAL!r}"
            )

        reference_standard = parse_number(
            row.get("reference_standard_in"),
            row_number=row_number,
            field="reference_standard_in",
            issues=issues,
        )

        if (
            reference_standard is not None
            and abs(reference_standard - EXPECTED_REFERENCE_IN)
            > ARITHMETIC_TOLERANCE_IN
        ):
            issues.append(
                f"row {row_number}: session {session_id} reference standard "
                f"{reference_standard:.7f} does not match expected "
                f"{EXPECTED_REFERENCE_IN:.7f}"
            )

        pre_values: list[float] = []
        post_values: list[float] = []

        for field in REFERENCE_FIELDS[:5]:
            value = parse_number(
                row.get(field),
                row_number=row_number,
                field=field,
                issues=issues,
            )
            if value is not None:
                pre_values.append(value)

        for field in REFERENCE_FIELDS[5:]:
            value = parse_number(
                row.get(field),
                row_number=row_number,
                field=field,
                issues=issues,
            )
            if value is not None:
                post_values.append(value)

        pre_mean = parse_number(
            row.get("pre_mean_in"),
            row_number=row_number,
            field="pre_mean_in",
            issues=issues,
        )
        pre_range = parse_number(
            row.get("pre_range_in"),
            row_number=row_number,
            field="pre_range_in",
            issues=issues,
        )
        post_mean = parse_number(
            row.get("post_mean_in"),
            row_number=row_number,
            field="post_mean_in",
            issues=issues,
        )
        post_range = parse_number(
            row.get("post_range_in"),
            row_number=row_number,
            field="post_range_in",
            issues=issues,
        )

        if len(pre_values) == 5:
            calculated_pre_mean = statistics.fmean(pre_values)
            calculated_pre_range = max(pre_values) - min(pre_values)

            verify_derived_value(
                pre_mean,
                calculated_pre_mean,
                row_number=row_number,
                field="pre_mean_in",
                issues=issues,
            )
            verify_derived_value(
                pre_range,
                calculated_pre_range,
                row_number=row_number,
                field="pre_range_in",
                issues=issues,
            )

        if len(post_values) == 5:
            calculated_post_mean = statistics.fmean(post_values)
            calculated_post_range = max(post_values) - min(post_values)

            verify_derived_value(
                post_mean,
                calculated_post_mean,
                row_number=row_number,
                field="post_mean_in",
                issues=issues,
            )
            verify_derived_value(
                post_range,
                calculated_post_range,
                row_number=row_number,
                field="post_range_in",
                issues=issues,
            )

        row_issue_prefix = f"row {row_number}:"
        row_has_issue = any(issue.startswith(row_issue_prefix) for issue in issues)

        if not row_has_issue:
            valid_session_ids.add(session_id)

    counts = Counter(session_ids)
    duplicate_session_ids = sorted(
        session_id for session_id, count in counts.items() if count > 1
    )

    if duplicate_session_ids:
        for session_id in duplicate_session_ids:
            issues.append(
                f"duplicate session_id {session_id!r}: " f"{counts[session_id]} records"
            )
            valid_session_ids.discard(session_id)

    print("=== OAL SCREENING SESSION AUDIT ===")
    print(f"Source: {args.sessions_csv}")
    print(f"Populated session records: {len(session_ids)}")
    print(f"Unique valid sessions: {len(valid_session_ids)}")
    print(f"Duplicate session IDs: {len(duplicate_session_ids)}")

    linked_specimen_count = 0
    linkage_issues: list[str] = []

    if args.screening_csv is not None:
        if not args.screening_csv.is_file():
            print(f"ERROR: screening file not found: {args.screening_csv}")
            return 2

        with args.screening_csv.open(
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as handle:
            screening_reader = csv.DictReader(handle)

            required_screening_columns = {
                "part_id",
                "screening_reading_in",
                "session_id",
            }

            screening_columns = set(screening_reader.fieldnames or [])
            missing_screening_columns = sorted(
                required_screening_columns - screening_columns
            )

            if missing_screening_columns:
                print("FAIL: required screening columns are missing:")
                for column in missing_screening_columns:
                    print(f"  - {column}")
                return 1

            for row_number, row in enumerate(screening_reader, start=2):
                reading = clean(row.get("screening_reading_in"))

                # Only completed specimen measurements require linkage.
                if not reading:
                    continue

                linked_specimen_count += 1

                part_id = clean(row.get("part_id"))
                session_id = clean(row.get("session_id"))

                if not session_id:
                    linkage_issues.append(
                        f"screening row {row_number}: part_id {part_id} "
                        "has measurement but no session_id"
                    )
                elif session_id not in valid_session_ids:
                    linkage_issues.append(
                        f"screening row {row_number}: part_id {part_id} "
                        f"references invalid or missing session "
                        f"{session_id!r}"
                    )

        print()
        print("=== SPECIMEN / SESSION LINKAGE ===")
        print(f"Measured specimen rows: {linked_specimen_count}")
        print(f"Linkage issues: {len(linkage_issues)}")

        for issue in linkage_issues:
            print(f"  - {issue}")

    print()
    print("=== SESSION DATA ISSUES ===")
    print(f"Issue count: {len(issues)}")

    for issue in issues:
        print(f"  - {issue}")

    complete = len(session_ids) > 0 and not issues and not linkage_issues

    print()
    print("=== DISPOSITION ===")

    if complete:
        print(
            "PASS: screening-session controls are complete and "
            "all measured specimens are traceably linked."
        )
        return 0

    print(
        "HOLD: screening-session controls are not yet complete "
        "for final screening disposition."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
