#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from v3_freeze_common import REPO, verify_freeze_manifest

FORMAL = REPO / "data/oal_validation/v3_formal"
ALLOWED = {"V3-CV-S001", "V3-CV-S002", "V3-CV-S003"}


def main() -> None:
    p = argparse.ArgumentParser(description="Capture one frozen V3 formal blank reference.")
    p.add_argument("--session", required=True, choices=sorted(ALLOWED))
    p.add_argument(
        "--confirm-empty-fixture",
        action="store_true",
        help="Required operator declaration that no specimen is present.",
    )
    args = p.parse_args()

    if not args.confirm_empty_fixture:
        raise SystemExit("STOP: confirm the measurement position is empty.")

    verify_freeze_manifest()

    raw_dir = FORMAL / "raw"
    diag_dir = FORMAL / "diagnostics"
    raw_dir.mkdir(parents=True, exist_ok=True)
    diag_dir.mkdir(parents=True, exist_ok=True)

    dst = raw_dir / f"{args.session}_blank_reference.png"
    meta_dst = diag_dir / f"{args.session}_blank_acquisition_metadata.json"

    if dst.exists() or meta_dst.exists():
        raise SystemExit(f"STOP: blank reference already exists for {args.session}.")

    label = args.session.lower().replace("-", "_") + "_blank_reference"
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
        raise SystemExit("STOP: blank acquisition did not contain exactly one image.")

    source = REPO / images[0]["relative_path"]
    if not source.is_file():
        raise SystemExit(f"STOP: source blank image missing: {source}")

    shutil.copy2(source, dst)
    shutil.copy2(meta_path, meta_dst)

    print()
    print("V3 FORMAL BLANK RECORDED")
    print(f"Session: {args.session}")
    print(f"Blank:   {dst.relative_to(REPO)}")


if __name__ == "__main__":
    main()
