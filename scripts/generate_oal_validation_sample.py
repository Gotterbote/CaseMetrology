#!/usr/bin/env python3
"""Deterministically select the frozen CaseMetrology OAL validation sample.

This script DOES NOT define stratum boundaries or allocations. Those must be
frozen prospectively in the input data and allocation JSON before this script
is used for the official selection.

Selection within each stratum uses SHA-256 ranking rather than a library PRNG:
    SHA256("CaseMetrology|selection|<seed>|<stratum>|<part_id>")
This makes the ordering deterministic across Python/library versions.

Official use:
- provide the full screened population CSV;
- provide an explicit allocation JSON whose counts sum to 60;
- provide an explicit selection seed;
- commit this script before generating the official sample.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_INPUT = {
    "part_id",
    "laser_etched_id_verified",
    "screening_reading_in",
    "screening_class",
    "selection_stratum",
    "eligible_for_validation",
    "exclusion_reason",
    "notes",
}

OUTPUT_FIELDS = [
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
]


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def rank_key(seed: str, stratum: str, part_id: str) -> str:
    token = f"CaseMetrology|selection|{seed}|{stratum}|{part_id}".encode("utf-8")
    return hashlib.sha256(token).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_INPUT - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Input is missing required columns: {sorted(missing)}")
        return list(reader)


def load_allocation(path: Path) -> dict[str, int]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict) or not obj:
        raise ValueError("Allocation JSON must be a nonempty object.")
    allocation: dict[str, int] = {}
    for key, value in obj.items():
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"Allocation for {key!r} must be a nonnegative integer.")
        allocation[str(key)] = value
    return allocation


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--allocation", required=True, type=Path)
    p.add_argument(
        "--seed", required=True, help="Prospectively declared selection seed."
    )
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--expected-population", type=int, default=235)
    p.add_argument("--expected-selected", type=int, default=60)
    args = p.parse_args()

    rows = read_csv(args.input)
    if args.expected_population and len(rows) != args.expected_population:
        raise ValueError(
            f"Expected {args.expected_population} screened rows; found {len(rows)}."
        )

    ids = [r["part_id"].strip() for r in rows]
    if any(not x for x in ids):
        raise ValueError("Blank part_id found.")
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate part_id found in screening population.")
    for x in ids:
        int(x)

    allocation = load_allocation(args.allocation)
    if sum(allocation.values()) != args.expected_selected:
        raise ValueError(
            f"Allocation totals {sum(allocation.values())}; "
            f"expected {args.expected_selected}."
        )

    eligible = [
        r
        for r in rows
        if truthy(r["eligible_for_validation"])
        and truthy(r["laser_etched_id_verified"])
    ]

    selected: list[dict[str, str]] = []
    for stratum, count in allocation.items():
        candidates = [r for r in eligible if r["selection_stratum"].strip() == stratum]
        if len(candidates) < count:
            raise ValueError(
                f"Stratum {stratum!r}: need {count}, only {len(candidates)} eligible."
            )
        ordered = sorted(
            candidates,
            key=lambda r: (
                rank_key(args.seed, stratum, r["part_id"].strip()),
                int(r["part_id"]),
            ),
        )
        selected.extend(ordered[:count])

    if len({r["part_id"].strip() for r in selected}) != args.expected_selected:
        raise ValueError("Selected specimen IDs are not unique.")

    selected = sorted(
        selected,
        key=lambda r: (
            hashlib.sha256(
                f"CaseMetrology|selection-final|{args.seed}|{r['part_id'].strip()}".encode()
            ).hexdigest(),
            int(r["part_id"]),
        ),
    )

    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    commit = git_commit()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for order, r in enumerate(selected, 1):
            writer.writerow(
                {
                    "part_id": r["part_id"].strip(),
                    "laser_etched_id_verified": r["laser_etched_id_verified"].strip(),
                    "screening_reading_in": r["screening_reading_in"].strip(),
                    "screening_class": r["screening_class"].strip(),
                    "selection_stratum": r["selection_stratum"].strip(),
                    "selected_for_validation": "true",
                    "selection_seed": args.seed,
                    "selection_order": order,
                    "selection_timestamp": timestamp,
                    "selection_script_commit": commit,
                    "notes": r["notes"].strip(),
                }
            )

    print(f"Wrote {len(selected)} selected specimens to {args.output}")
    print(f"Selection seed: {args.seed}")
    print(f"Script commit: {commit or '(not available)'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
