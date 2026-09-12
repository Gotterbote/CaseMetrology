#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from v3_freeze_common import REPO, verify_freeze_manifest

FORMAL = REPO / "data/oal_validation/v3_formal"
RUN_ORDER = FORMAL / "v3_cv_run_orders.csv"
OBS = FORMAL / "v3_cv_observations.csv"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Capture one scheduled V3 formal image without calculating OAL."
    )
    p.add_argument("--round", type=int, required=True, choices=(1, 2, 3))
    p.add_argument("--sequence", type=int, required=True)
    p.add_argument("--specimen-id", required=True)
    args = p.parse_args()

    verify_freeze_manifest()

    with RUN_ORDER.open(newline="", encoding="utf-8") as f:
        schedule = list(csv.DictReader(f))

    matches = [
        r for r in schedule
        if int(r["round"]) == args.round and int(r["sequence"]) == args.sequence
    ]
    if len(matches) != 1:
        raise SystemExit("STOP: requested round/sequence is not unique in frozen order.")

    run = matches[0]
    expected = str(run["specimen_id"])
    session = run["planned_session"]

    if str(args.specimen_id) != expected:
        raise SystemExit(
            f"STOP: Round {args.round} sequence {args.sequence} requires "
            f"specimen {expected}; supplied {args.specimen_id}."
        )

    blank = FORMAL / "raw" / f"{session}_blank_reference.png"
    if not blank.is_file():
        raise SystemExit(f"STOP: session blank does not exist: {blank.relative_to(REPO)}")

    with OBS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    targets = [
        r for r in rows
        if int(r["round"]) == args.round and int(r["sequence"]) == args.sequence
    ]
    if len(targets) != 1:
        raise SystemExit("STOP: observation row is not unique.")

    row = targets[0]
    if row["image_path"].strip():
        raise SystemExit("STOP: this scheduled observation already has an image.")

    previous = [
        r for r in rows
        if int(r["round"]) == args.round and int(r["sequence"]) < args.sequence
    ]
    incomplete = [
        int(r["sequence"]) for r in previous
        if not r["image_path"].strip()
    ]
    if incomplete:
        raise SystemExit(f"STOP: earlier sequence positions are incomplete: {incomplete}")

    run_id = f"V3-CV-R{args.round}-{args.sequence:03d}"
    label = f"{run_id}_part_{expected}".lower().replace("-", "_")

    print("=" * 64)
    print("V3 FORMAL CAPTURE GATE: PASS")
    print(f"Session      : {session}")
    print(f"Round        : {args.round}")
    print(f"Sequence     : {args.sequence}")
    print(f"Specimen     : {expected}")
    print("OAL result   : BLINDED — no estimator is executed during acquisition")
    print("=" * 64)

    command = [
        sys.executable,
        "src/acquisition/capture_research.py",
        "--label", label,
        "--count", "1",
    ]
    completed = subprocess.run(
        command, cwd=REPO, check=True, capture_output=True, text=True
    )
    print(completed.stdout, end="")

    m = re.search(r"^Metadata saved to:\s+(.+)$", completed.stdout, re.MULTILINE)
    if m is None:
        raise SystemExit("STOP: could not identify acquisition metadata.")

    meta_path = REPO / m.group(1).strip()
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    if meta.get("control_mismatches"):
        raise SystemExit(f"STOP: camera-control mismatch: {meta['control_mismatches']}")

    images = meta.get("images", [])
    if len(images) != 1:
        raise SystemExit("STOP: acquisition did not contain exactly one image.")

    source = REPO / images[0]["relative_path"]
    if not source.is_file():
        raise SystemExit(f"STOP: raw image missing: {source}")

    raw_dir = FORMAL / "raw"
    diag_dir = FORMAL / "diagnostics"
    raw_dir.mkdir(parents=True, exist_ok=True)
    diag_dir.mkdir(parents=True, exist_ok=True)

    dst = raw_dir / f"{run_id}_part_{expected}.png"
    meta_dst = diag_dir / f"{run_id}_acquisition_metadata.json"

    if dst.exists() or meta_dst.exists():
        raise SystemExit("STOP: formal artifact path already exists.")

    shutil.copy2(source, dst)
    shutil.copy2(meta_path, meta_dst)

    row["timestamp"] = images[0]["captured_at"]
    row["image_path"] = str(dst.relative_to(REPO))
    row["validity"] = "CAPTURED"
    row["invalid_reason"] = ""
    row["notes"] = (
        "Prospective V3 capture-only acquisition. "
        "Estimator results intentionally blinded until all 180 images are acquired."
    )

    tmp = OBS.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(OBS)

    print()
    print("FORMAL V3 IMAGE RECORDED")
    print(f"Run ID   : {run_id}")
    print(f"Specimen : {expected}")
    print(f"Image    : {dst.relative_to(REPO)}")
    print("No OAL value was calculated or displayed.")


if __name__ == "__main__":
    main()
