"""Persistent artifacts for validated OAL measurements.

A completed measurement is persisted locally before any network transport.

Each artifact pair contains:
    - annotated PNG
    - JSON measurement record

The JSON stores SHA-256 hashes for both the source image and annotated image.
"""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import numpy as np
from numpy.typing import NDArray

from src.diagnostics.topdown_oal_production_overlay import (
    draw_topdown_oal_production_overlay,
)
from src.measurement.topdown_oal_pipeline import TopDownOALPipelineResult

GrayImage = NDArray[np.uint8]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def _git_commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def save_oal_measurement_artifacts(
    *,
    image: GrayImage,
    source_image_path: Path,
    blank_reference_path: Path,
    result: TopDownOALPipelineResult,
    output_root: Path,
    part_id: str,
    measurement_id: str,
    timestamp: datetime | None = None,
) -> tuple[Path, Path]:
    """Persist annotated image and JSON record for one OAL measurement."""

    timestamp = timestamp or datetime.now().astimezone()

    date_dir = output_root / timestamp.strftime("%Y-%m-%d")
    annotated_dir = date_dir / "annotated"
    record_dir = date_dir / "records"

    annotated_dir.mkdir(parents=True, exist_ok=True)
    record_dir.mkdir(parents=True, exist_ok=True)

    annotated_path = annotated_dir / f"{measurement_id}_annotated.png"

    record_path = record_dir / f"{measurement_id}.json"

    overlay = draw_topdown_oal_production_overlay(
        image,
        result,
    )

    if not cv2.imwrite(str(annotated_path), overlay):
        raise RuntimeError(f"Failed to save annotated image: {annotated_path}")

    pca = result.pca
    calibration = result.calibration

    packet: dict[str, object] = {
        "schema_version": "1.0",
        "measurement_id": measurement_id,
        "part_id": part_id,
        "timestamp": timestamp.isoformat(),
        "measurement_characteristic": "OAL",
        "pipeline": "topdown_oal_pipeline",
        "measurement_status": ("MEASURED" if result.passed else "NOT_EVALUATED"),
        "pipeline_passed": result.passed,
        "failure_stage": result.failure_stage,
        "failure_reason": result.failure_reason,
        "oal_in": result.length_inches,
        "source_image": str(source_image_path),
        "blank_reference": str(blank_reference_path),
        "annotated_image": str(annotated_path),
        "source_image_sha256": _sha256(source_image_path),
        "annotated_image_sha256": _sha256(annotated_path),
        "git_commit": _git_commit(),
        "physical_endpoint_roles": None,
    }

    if result.segmentation.centroid_xy is not None:
        packet["centroid_xy"] = list(result.segmentation.centroid_xy)

    if pca is not None:
        packet.update(
            {
                "oal_pixels": pca.length_pixels,
                "axis_angle_deg": pca.angle_degrees,
                "endpoint_min_xy": (
                    None if pca.endpoint_min_xy is None else list(pca.endpoint_min_xy)
                ),
                "endpoint_max_xy": (
                    None if pca.endpoint_max_xy is None else list(pca.endpoint_max_xy)
                ),
                "largest_component_pixels": (pca.largest_component_pixels),
                "second_component_pixels": (pca.second_component_pixels),
            }
        )

    if calibration is not None:
        packet["effective_ppi"] = calibration.effective_ppi

    # Write atomically: temporary file first, then rename.
    temporary_path = record_path.with_suffix(".json.tmp")

    temporary_path.write_text(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    temporary_path.replace(record_path)

    return annotated_path, record_path
