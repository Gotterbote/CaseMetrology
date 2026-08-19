#!/usr/bin/env python3
"""Generate the frozen cv three-round CaseMetrology OAL run order.

Ordering is deterministic using SHA-256 ranking:
    SHA256("CaseMetrology|cv|<seed>|<round>|<part_id>")

If the final specimen of one round would be the first specimen of the next
round, positions 1 and 2 of the new round are swapped, exactly as specified
prospectively in the formal randomization protocol.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_INPUT = {
    "part_id",
    "laser_etched_id_verified",
    "selection_stratum",
    "selected_for_validation",
}

OUTPUT_FIELDS = [
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


def truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y"}


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def order_key(seed: str, round_number: int, part_id: str) -> str:
    token = (f"CaseMetrology|cv|{seed}|{round_number}|{part_id}").encode("utf-8")
    return hashlib.sha256(token).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--seed", default="2026081902")
    p.add_argument("--expected-specimens", type=int, default=60)
    args = p.parse_args()

    with args.input.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_INPUT - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Input missing required columns: {sorted(missing)}")
        rows = [r for r in reader if truthy(r["selected_for_validation"])]

    if len(rows) != args.expected_specimens:
        raise ValueError(
            f"Expected {args.expected_specimens} selected specimens; found {len(rows)}."
        )

    ids = [r["part_id"].strip() for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Selected part_id values are not unique.")
    for x in ids:
        int(x)

    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    commit = git_commit()
    output_rows = []
    previous_last = None

    for round_number in (1, 2, 3):
        ordered = sorted(
            rows,
            key=lambda r: (
                order_key(args.seed, round_number, r["part_id"].strip()),
                int(r["part_id"]),
            ),
        )
        if previous_last is not None and ordered[0]["part_id"].strip() == previous_last:
            if len(ordered) < 2:
                raise ValueError(
                    "Cannot prevent cross-round repetition with <2 specimens."
                )
            ordered[0], ordered[1] = ordered[1], ordered[0]

        for seq, r in enumerate(ordered, 1):
            output_rows.append(
                {
                    "cv_run_id": f"CV-R{round_number}-{seq:03d}",
                    "cv_round": round_number,
                    "planned_sequence": seq,
                    "part_id": r["part_id"].strip(),
                    "selection_stratum": r["selection_stratum"].strip(),
                    "randomization_seed": args.seed,
                    "run_order_generated_at": generated,
                    "run_order_script_commit": commit,
                    "completion_status": "PLANNED",
                    "session_id": "",
                    "notes": "",
                }
            )
        previous_last = ordered[-1]["part_id"].strip()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {len(output_rows)} planned cv observations to {args.output}")
    print(f"Randomization seed: {args.seed}")
    print(f"Script commit: {commit or '(not available)'}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
