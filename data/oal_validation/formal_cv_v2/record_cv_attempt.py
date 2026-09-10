#!/usr/bin/env python3

import argparse
import csv
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path("data/oal_validation")
RUN_ORDER = ROOT / "v2_cv_run_order.csv"
OBS_FILE = ROOT / "v2_cv_observations.csv"
OBS_TEMPLATE = ROOT / "templates/cv_observations.csv"
FORMAL_ROOT = ROOT / "formal_cv_v2"

EXPECTED_COMMIT = "ee4cf97f5313afb72fa651c5b99e8c793573540b"
CAMERA_ID = "Arducam_20231211_0001"
OPERATOR = "Timmy D. Bell"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def copy_or_verify(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        if sha256(src) != sha256(dst):
            raise SystemExit(
                f"ERROR: existing formal artifact differs from source: {dst}"
            )
        return

    shutil.copy2(src, dst)


def main():
    p = argparse.ArgumentParser(
        description="Preserve and record one VALID formal CV attempt."
    )
    p.add_argument("--run-id", required=True)
    p.add_argument("--acquisition-session", required=True)
    p.add_argument("--formal-session", default="V2-CV-S001")
    args = p.parse_args()

    # ---- frozen run-order lookup ----
    with RUN_ORDER.open(newline="", encoding="utf-8") as f:
        run_rows = list(csv.DictReader(f))

    matches = [r for r in run_rows if r["cv_run_id"] == args.run_id]

    if len(matches) != 1:
        raise SystemExit(
            f"ERROR: expected exactly one run-order row for {args.run_id}"
        )

    run = matches[0]

    part_id = run["part_id"]
    cv_round = int(run["cv_round"])
    sequence = int(run["planned_sequence"])

    obs_id = f"V2-CV-OBS-R{cv_round}-{sequence:03d}"

    # ---- acquisition metadata ----
    meta_path = Path(
        "measurements/acquisition/"
        f"{args.acquisition_session}.json"
    )

    if not meta_path.is_file():
        raise SystemExit(
            f"ERROR: acquisition metadata not found: {meta_path}"
        )

    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    if meta.get("session_id") != args.acquisition_session:
        raise SystemExit("ERROR: acquisition session ID mismatch.")

    if meta.get("git_commit") != EXPECTED_COMMIT:
        raise SystemExit(
            f"ERROR: acquisition commit mismatch: {meta.get('git_commit')}"
        )

    if meta.get("control_mismatches"):
        raise SystemExit(
            f"ERROR: camera-control mismatch recorded: "
            f"{meta['control_mismatches']}"
        )

    images = meta.get("images", [])

    if len(images) != 1:
        raise SystemExit(
            "ERROR: formal attempt must contain exactly one captured image."
        )

    raw_source = Path(images[0]["relative_path"])

    if not raw_source.is_file():
        raise SystemExit(
            f"ERROR: raw acquisition image missing: {raw_source}"
        )

    # ---- persisted measurement artifacts ----
    artifact_root = (
        Path.home() / ".local/share/casemetrology/artifacts"
    )

    record_matches = list(
        artifact_root.glob(
            f"*/records/{args.acquisition_session}.json"
        )
    )

    diag_matches = list(
        artifact_root.glob(
            f"*/annotated/"
            f"{args.acquisition_session}_annotated.png"
        )
    )

    if len(record_matches) != 1:
        raise SystemExit(
            "ERROR: expected exactly one persisted measurement record."
        )

    if len(diag_matches) != 1:
        raise SystemExit(
            "ERROR: expected exactly one persisted diagnostic image."
        )

    record_source = record_matches[0]
    diag_source = diag_matches[0]

    record = json.loads(
        record_source.read_text(encoding="utf-8")
    )

    if record.get("git_commit") != EXPECTED_COMMIT:
        raise SystemExit("ERROR: measurement-record commit mismatch.")

    if str(record.get("part_id")) != str(part_id):
        raise SystemExit(
            f"ERROR: run order requires Part {part_id}, "
            f"but measurement record contains Part "
            f"{record.get('part_id')}."
        )

    if record.get("measurement_id") != args.acquisition_session:
        raise SystemExit("ERROR: measurement ID mismatch.")

    # Exceptional failures must be reviewed deliberately.
    if record.get("pipeline_passed") is not True:
        raise SystemExit(
            "STOP: frozen pipeline did not return a VALID measurement. "
            "Do not record with this helper and do not reacquire. "
            "Classify the attempt separately."
        )

    if record.get("oal_in") is None:
        raise SystemExit("ERROR: VALID record has no OAL.")

    if record.get("effective_ppi") is None:
        raise SystemExit("ERROR: VALID record has no effective PPI.")

    expected_blank = (
        FORMAL_ROOT / "raw" /
        f"{args.formal_session}_blank_reference.png"
    )

    if not expected_blank.is_file():
        raise SystemExit(
            f"ERROR: formal blank reference missing: {expected_blank}"
        )

    recorded_blank = Path(record.get("blank_reference", ""))

    if recorded_blank.resolve() != expected_blank.resolve():
        raise SystemExit(
            "ERROR: measurement used an unexpected blank reference."
        )

    # ---- observation-file sequence gate ----
    if not OBS_FILE.exists():
        shutil.copy2(OBS_TEMPLATE, OBS_FILE)

    with OBS_FILE.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        existing = list(reader)

    if any(r["cv_observation_id"] == obs_id for r in existing):
        raise SystemExit(
            f"ERROR: {obs_id} already recorded."
        )

    if any(r["cv_run_id"] == args.run_id for r in existing):
        raise SystemExit(
            f"ERROR: {args.run_id} already has a formal observation."
        )

    completed_sequences = {
        int(r["planned_sequence"])
        for r in existing
        if r["cv_round"] == str(cv_round)
        and not r["replacement_for_observation_id"].strip()
    }

    required_previous = set(range(1, sequence))

    if completed_sequences != required_previous:
        raise SystemExit(
            "ERROR: formal CV sequence is not contiguous. "
            f"Expected completed positions "
            f"{sorted(required_previous)}, found "
            f"{sorted(completed_sequences)}."
        )

    # ---- formal artifact preservation ----
    formal_raw = (
        FORMAL_ROOT / "raw" /
        f"{args.run_id}.png"
    )

    formal_meta = (
        FORMAL_ROOT / "diagnostics" /
        f"{args.run_id}_acquisition_metadata.json"
    )

    formal_record = (
        FORMAL_ROOT / "diagnostics" /
        f"{args.run_id}_record.json"
    )

    formal_diag = (
        FORMAL_ROOT / "diagnostics" /
        f"{args.run_id}_diagnostic.png"
    )

    copy_or_verify(raw_source, formal_raw)
    copy_or_verify(meta_path, formal_meta)
    copy_or_verify(record_source, formal_record)
    copy_or_verify(diag_source, formal_diag)

    captured_at = datetime.fromisoformat(
        images[0]["captured_at"]
    )

    row = {
        "cv_observation_id": obs_id,
        "cv_run_id": args.run_id,
        "part_id": part_id,
        "cv_round": str(cv_round),
        "planned_sequence": str(sequence),
        "session_id": args.formal_session,
        "laser_etched_id_verified": "YES",
        "acquisition_date": captured_at.date().isoformat(),
        "acquisition_time": captured_at.timetz().isoformat(
            timespec="microseconds"
        ),
        "operator": OPERATOR,
        "software_commit": EXPECTED_COMMIT,
        "camera_id": CAMERA_ID,
        "measurement_status": "VALID",
        "oal_in": str(record["oal_in"]),
        "effective_ppi": str(record["effective_ppi"]),
        "quality_gate_status": "PASS",
        "failure_class": "",
        "protocol_invalid": "NO",
        "invalidation_reason": "",
        "replacement_for_observation_id": "",
        "raw_image_path": str(formal_raw),
        "mask_path": "",
        "diagnostic_path": str(formal_diag),
        "notes": (
            "Single scheduled formal acquisition. "
            "No separate mask artifact produced by frozen "
            "live-cycle workflow. Local persisted measurement "
            "is authoritative."
        ),
    }

    # Atomic rewrite of observation CSV.
    tmp = OBS_FILE.with_suffix(".csv.tmp")

    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerow(row)

    tmp.replace(OBS_FILE)

    print()
    print("FORMAL CV ATTEMPT RECORDED")
    print(f"Run ID       : {args.run_id}")
    print(f"Sequence     : {sequence}")
    print(f"Part ID      : {part_id}")
    print(f"Session      : {args.formal_session}")
    print("Status       : VALID")
    print(f"OAL          : {record['oal_in']}")
    print(f"Effective PPI: {record['effective_ppi']}")
    print(f"Captured     : {images[0]['captured_at']}")


if __name__ == "__main__":
    main()
