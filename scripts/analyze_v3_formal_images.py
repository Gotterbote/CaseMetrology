#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

import cv2

from v3_freeze_common import REPO, verify_freeze_manifest

FORMAL = REPO / "data/oal_validation/v3_formal"
OBS = FORMAL / "v3_cv_observations.csv"
HYBRID_SOURCE = REPO / "scripts/evaluate_oal_endface_hybrid_dev.py"


def load_hybrid_module():
    spec = importlib.util.spec_from_file_location("v3_frozen_hybrid", HYBRID_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load frozen Endface Hybrid source.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    verify_freeze_manifest()

    with OBS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    if len(rows) != 180:
        raise SystemExit(f"STOP: expected 180 scheduled rows; found {len(rows)}.")

    incomplete = [
        (r["round"], r["sequence"], r["specimen_id"])
        for r in rows if not r["image_path"].strip()
    ]
    if incomplete:
        raise SystemExit(
            f"STOP: formal acquisition is incomplete ({len(incomplete)} images missing)."
        )

    module = load_hybrid_module()
    diag_dir = FORMAL / "diagnostics"
    diag_dir.mkdir(parents=True, exist_ok=True)

    primary_valid = 0
    pca_valid = 0
    geometry_valid = 0

    for row in rows:
        session = row["session_id"]
        blank_path = FORMAL / "raw" / f"{session}_blank_reference.png"
        image_path = REPO / row["image_path"]

        blank = cv2.imread(str(blank_path), cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if blank is None or image is None:
            raise SystemExit(
                f"STOP: could not load formal image/blank for "
                f"round {row['round']} sequence {row['sequence']}."
            )

        observations = module._observations_for_image(
            blank, image, include_subpixel_v2=False
        )
        by_name = {o.estimator: o for o in observations}

        hybrid = by_name["endface_hybrid"]
        pca = by_name["pca"]
        geometry = by_name["geometry"]

        row["endface_hybrid_in"] = (
            "" if hybrid.length_inches is None else f"{hybrid.length_inches:.12f}"
        )
        row["pca_in"] = "" if pca.length_inches is None else f"{pca.length_inches:.12f}"
        row["geometry_in"] = (
            "" if geometry.length_inches is None else f"{geometry.length_inches:.12f}"
        )

        if hybrid.passed:
            row["validity"] = "VALID"
            row["invalid_reason"] = ""
            primary_valid += 1
        else:
            row["validity"] = "ESTIMATOR_FAILURE"
            row["invalid_reason"] = hybrid.failure_reason or "Endface Hybrid failure"

        pca_valid += int(pca.passed)
        geometry_valid += int(geometry.passed)

        run_id = f"V3-CV-R{int(row['round'])}-{int(row['sequence']):03d}"
        detail = {
            "analysis_timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
            "run_id": run_id,
            "session_id": session,
            "specimen_id": row["specimen_id"],
            "image_path": row["image_path"],
            "blank_path": str(blank_path.relative_to(REPO)),
            "estimators": {name: asdict(obs) for name, obs in by_name.items()},
        }
        (diag_dir / f"{run_id}_estimator_results.json").write_text(
            json.dumps(detail, indent=2) + "\n", encoding="utf-8"
        )

    tmp = OBS.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(OBS)

    print("=" * 64)
    print("V3 FROZEN ESTIMATOR PROCESSING COMPLETE")
    print(f"Endface Hybrid availability: {primary_valid}/180")
    print(f"PCA availability:            {pca_valid}/180")
    print(f"Geometry availability:       {geometry_valid}/180")
    print("=" * 64)


if __name__ == "__main__":
    main()
