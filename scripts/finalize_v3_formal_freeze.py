#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import subprocess

from v3_freeze_common import REPO, git, sha256_file

EXPECTED_HYBRID_HASH = (
    "3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af"
)

FILES = [
    "data/oal_validation/formal_validation_specimens.csv",
    "data/oal_validation/v3_formal/v3_manual_stability_run_order.csv",
    "data/oal_validation/v3_formal/v3_cv_run_orders.csv",
    "docs/research/v3_formal_validation/V3_FORMAL_VALIDATION_PLAN.md",
    "docs/research/v3_formal_validation/V3_ACQUISITION_AND_ANALYSIS_IMPLEMENTATION.md",
    "scripts/evaluate_oal_endface_hybrid_dev.py",
    "scripts/v3_freeze_common.py",
    "scripts/capture_v3_formal_blank.py",
    "scripts/run_v3_formal_capture.py",
    "scripts/analyze_v3_formal_images.py",
    "scripts/finalize_v3_formal_freeze.py",
    "src/calibration/oal_spatial_calibration.py",
    "src/image_processing/oal_segmentation.py",
    "src/measurement/topdown_oal.py",
    "src/measurement/topdown_oal_geometry.py",
    "src/measurement/topdown_oal_subpixel_v2.py",
    "src/acquisition/apply_locked_controls.py",
    "src/acquisition/capture_research.py",
    "config/udev/99-case-metrology-camera.rules",
]

MANIFEST = REPO / "docs/research/v3_formal_validation/V3_MEASUREMENT_SYSTEM_MANIFEST.sha256"
EVIDENCE_JSON = REPO / "docs/research/v3_formal_validation/V3_FINAL_FREEZE_EVIDENCE.json"
EVIDENCE_MD = REPO / "docs/research/v3_formal_validation/V3_FINAL_FREEZE_EVIDENCE.md"


def main() -> None:
    status = git("status", "--porcelain")
    if status:
        raise SystemExit(
            "STOP: commit the V3 configuration package first; repository is not clean.\n"
            + status
        )

    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", "cdd76a7", "HEAD"],
        cwd=REPO,
    ).returncode != 0:
        raise SystemExit("STOP: V3 development baseline cdd76a7 is not an ancestor.")

    missing = [rel for rel in FILES if not (REPO / rel).is_file()]
    if missing:
        raise SystemExit("STOP: required frozen files missing:\n" + "\n".join(missing))

    hybrid_hash = sha256_file(REPO / "scripts/evaluate_oal_endface_hybrid_dev.py")
    if hybrid_hash != EXPECTED_HYBRID_HASH:
        raise SystemExit(
            "STOP: Endface Hybrid source no longer matches the selected development freeze."
        )

    hashes = {rel: sha256_file(REPO / rel) for rel in FILES}
    MANIFEST.write_text(
        "".join(f"{hashes[rel]}  {rel}\n" for rel in sorted(hashes)),
        encoding="utf-8",
    )

    evidence = {
        "freeze_finalized_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": "FROZEN_PRE_ACQUISITION",
        "configuration_commit": git("rev-parse", "HEAD"),
        "development_baseline": "cdd76a7942b16f4c2aaf7b6f0b653f3589a77986",
        "primary_estimator": "Endface Hybrid",
        "primary_estimator_sha256": hybrid_hash,
        "historical_comparator": "PCA",
        "secondary_estimator": "Geometry",
        "formal_specimens": 60,
        "formal_cv_placements": 180,
        "acquisition_mode": "capture-only; estimator-blinded until all 180 images acquired",
        "files": hashes,
    }
    EVIDENCE_JSON.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    EVIDENCE_MD.write_text(
        f"""# CaseMetrology V3 Final Freeze Evidence

Status: **FROZEN — PRE-ACQUISITION**

Freeze finalized: {evidence['freeze_finalized_at']}

Configuration commit: `{evidence['configuration_commit']}`

Development baseline: `{evidence['development_baseline']}`

Primary estimator: **Endface Hybrid**

Primary estimator SHA-256:

`{hybrid_hash}`

Acquisition mode:

**Capture-only formal acquisition. No OAL estimator is executed or displayed during
the 180 prospective formal placements. Frozen Endface Hybrid, PCA, and Geometry
are applied to the same retained images only after acquisition is complete.**

The SHA-256 manifest `V3_MEASUREMENT_SYSTEM_MANIFEST.sha256` is the authoritative
measurement-system freeze record.
""",
        encoding="utf-8",
    )

    print("PASS: V3 measurement-system manifest generated")
    print(f"Configuration commit: {evidence['configuration_commit']}")
    print(f"Endface Hybrid hash:  {hybrid_hash}")
    print("FINAL FREEZE EVIDENCE READY TO COMMIT")


if __name__ == "__main__":
    main()
