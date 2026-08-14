"""Tests for production OAL overlays and persistent measurement artifacts."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from src.diagnostics.oal_measurement_artifacts import (
    save_oal_measurement_artifacts,
)
from src.diagnostics.topdown_oal_production_overlay import (
    draw_topdown_oal_production_overlay,
)
from src.measurement.topdown_oal_pipeline import (
    measure_topdown_oal_image,
)


def _synthetic_blank_and_case() -> tuple[np.ndarray, np.ndarray]:
    blank = np.full((500, 700), 240, dtype=np.uint8)
    image = blank.copy()

    # Simple elongated dark specimen.
    cv2.rectangle(
        image,
        (250, 100),
        (390, 400),
        40,
        thickness=-1,
    )

    return blank, image


def test_production_overlay_preserves_image_shape() -> None:
    blank, image = _synthetic_blank_and_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed

    overlay = draw_topdown_oal_production_overlay(
        image,
        result,
    )

    assert overlay.shape == (
        image.shape[0],
        image.shape[1],
        3,
    )
    assert overlay.dtype == np.uint8


def test_measurement_artifacts_are_persisted_with_hashes(
    tmp_path: Path,
    monkeypatch,
) -> None:
    blank, image = _synthetic_blank_and_case()

    blank_path = tmp_path / "blank.png"
    image_path = tmp_path / "case.png"

    assert cv2.imwrite(str(blank_path), blank)
    assert cv2.imwrite(str(image_path), image)

    result = measure_topdown_oal_image(blank, image)

    assert result.passed

    # Avoid coupling this unit test to the repository's actual HEAD.
    monkeypatch.setattr(
        "src.diagnostics.oal_measurement_artifacts._git_commit",
        lambda: "test-commit",
    )

    annotated_path, record_path = save_oal_measurement_artifacts(
        image=image,
        source_image_path=image_path,
        blank_reference_path=blank_path,
        result=result,
        output_root=tmp_path / "output",
        part_id="test-part",
        measurement_id="test-measurement",
    )

    assert annotated_path.is_file()
    assert record_path.is_file()

    record = record_path.read_text(encoding="utf-8")

    assert '"measurement_id": "test-measurement"' in record
    assert '"part_id": "test-part"' in record
    assert '"pipeline_passed": true' in record
    assert '"git_commit": "test-commit"' in record
    assert '"source_image_sha256"' in record
    assert '"annotated_image_sha256"' in record
    assert '"physical_endpoint_roles": null' in record
