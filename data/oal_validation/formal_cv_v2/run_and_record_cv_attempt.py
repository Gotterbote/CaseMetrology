#!/usr/bin/env python3

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("data/oal_validation")
RUN_ORDER = ROOT / "v2_cv_run_order.csv"
OBS_FILE = ROOT / "v2_cv_observations.csv"

FROZEN_COMMIT = "ee4cf97f5313afb72fa651c5b99e8c793573540b"


RECORDER = (
    ROOT / "formal_cv_v2/"
    "record_cv_attempt.py"
)


def git_output(*args):
    return subprocess.check_output(
        ["git", *args],
        text=True,
    ).strip()


def main():
    p = argparse.ArgumentParser(
        description=(
            "Run one frozen formal CV acquisition and "
            "automatically record it if VALID."
        )
    )
    p.add_argument("--run-id", required=True)
    p.add_argument("--part-id", required=True)
    p.add_argument("--formal-session", required=True)
    args = p.parse_args()

    blank = (
        ROOT / "formal_cv_v2/raw" /
        f"{args.formal_session}_blank_reference.png"
    )

    # --------------------------------------------------
    # Frozen repository gate
    # --------------------------------------------------
    head = git_output("rev-parse", "HEAD")

    if head != FROZEN_COMMIT:
        raise SystemExit(
            f"STOP: HEAD is {head}, expected frozen commit "
            f"{FROZEN_COMMIT}."
        )

    changed_measurement_files = git_output(
        "diff",
        "--name-only",
        "--",
        "src",
        "scripts",
        "config",
    )

    untracked_measurement_files = git_output(
        "ls-files",
        "--others",
        "--exclude-standard",
        "--",
        "src",
        "scripts",
        "config",
    )

    if changed_measurement_files or untracked_measurement_files:
        raise SystemExit(
            "STOP: uncommitted measurement-system files detected."
        )

    if not blank.is_file():
        raise SystemExit(
            f"STOP: formal blank reference missing: {blank}"
        )

    # --------------------------------------------------
    # Frozen run-order gate
    # --------------------------------------------------
    with RUN_ORDER.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    matches = [
        r for r in rows
        if r["cv_run_id"] == args.run_id
    ]

    if len(matches) != 1:
        raise SystemExit(
            f"STOP: {args.run_id} is not a unique frozen run."
        )

    run = matches[0]

    expected_part = run["part_id"]
    round_number = int(run["cv_round"])
    sequence = int(run["planned_sequence"])

    if args.part_id != expected_part:
        raise SystemExit(
            f"STOP: {args.run_id} requires Part "
            f"{expected_part}, but Part {args.part_id} "
            f"was supplied."
        )

    # --------------------------------------------------
    # Formal sequence gate
    # --------------------------------------------------
    if not OBS_FILE.is_file():
        raise SystemExit(
            "STOP: cv_observations.csv does not exist."
        )

    with OBS_FILE.open(newline="", encoding="utf-8") as f:
        observations = list(csv.DictReader(f))

    if any(
        r["cv_run_id"] == args.run_id
        for r in observations
    ):
        raise SystemExit(
            f"STOP: {args.run_id} is already formally recorded."
        )

    completed = {
        int(r["planned_sequence"])
        for r in observations
        if r["cv_round"] == str(round_number)
        and not r[
            "replacement_for_observation_id"
        ].strip()
    }

    required = set(range(1, sequence))

    if completed != required:
        raise SystemExit(
            "STOP: formal CV sequence is not contiguous.\n"
            f"Required completed positions: "
            f"{sorted(required)}\n"
            f"Actually recorded: "
            f"{sorted(completed)}"
        )

    print("=" * 55)
    print("FORMAL CV ACQUISITION GATE: PASS")
    print(f"Run ID       : {args.run_id}")
    print(f"Round        : {round_number}")
    print(f"Sequence     : {sequence}")
    print(f"Part ID      : {expected_part}")
    print(f"Frozen commit: {head[:7]}")
    print("=" * 55)
    print()

    # --------------------------------------------------
    # Execute existing frozen acquisition workflow
    # --------------------------------------------------
    command = [
        sys.executable,
        "scripts/run_live_oal_cycle.py",
        "--part-id",
        expected_part,
        "--blank-image",
        str(blank),
    ]

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    acquisition_session = None
    measurement_passed = None

    assert proc.stdout is not None

    for line in proc.stdout:
        print(line, end="")

        m = re.match(
            r"Acquisition session:\s+(.+)",
            line,
        )
        if m:
            acquisition_session = m.group(1).strip()

        m = re.match(
            r"Measurement passed:\s+(True|False)",
            line,
        )
        if m:
            measurement_passed = (
                m.group(1) == "True"
            )

    return_code = proc.wait()

    if return_code != 0:
        raise SystemExit(
            "\nSTOP: acquisition command ended abnormally. "
            "Do NOT reacquire. Review the event before "
            "continuing."
        )

    if acquisition_session is None:
        raise SystemExit(
            "\nSTOP: could not identify the acquisition "
            "session. Do NOT reacquire."
        )

    if measurement_passed is not True:
        raise SystemExit(
            "\nSYSTEM ATTEMPT COMPLETED WITHOUT A VALID "
            "MEASUREMENT.\n"
            "Do NOT reacquire. Preserve this attempt and "
            "classify it according to the frozen protocol."
        )

    # --------------------------------------------------
    # Automatically preserve + record VALID attempt
    # --------------------------------------------------
    print()
    print("=" * 55)
    print("VALID MEASUREMENT — RECORDING FORMAL ATTEMPT")
    print("=" * 55)

    record_command = [
        sys.executable,
        str(RECORDER),
        "--run-id",
        args.run_id,
        "--acquisition-session",
        acquisition_session,
        "--formal-session",
        args.formal_session,
    ]

    completed = subprocess.run(record_command)

    if completed.returncode != 0:
        raise SystemExit(
            "\nSTOP: measurement succeeded, but formal "
            "recording did not complete.\n"
            "Do NOT reacquire the specimen."
        )

    print()
    print("=" * 55)
    print("ACQUISITION + FORMAL RECORD COMPLETE")
    print(f"Run ID   : {args.run_id}")
    print(f"Part ID  : {expected_part}")
    print(f"Sequence : {sequence}")
    print("=" * 55)


if __name__ == "__main__":
    main()
