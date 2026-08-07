from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.measurement.topdown_oal_geometry import measure_topdown_oal_geometry
from src.measurement.topdown_oal_pipeline import measure_topdown_oal_image


def _blank_and_case() -> tuple[np.ndarray, np.ndarray]:
    blank = np.full((900, 900), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(
        image,
        (190, 410),
        (710, 490),
        80,
        thickness=-1,
    )

    return blank, image


def test_pipeline_measures_case_only_image() -> None:
    blank, image = _blank_and_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed, result.failure_reason
    assert result.geometry is not None
    assert result.geometry.length_pixels == pytest.approx(520.0, abs=1.0)


def test_pipeline_intentionally_disables_fixture_width_gate() -> None:
    blank, image = _blank_and_case()

    pipeline = measure_topdown_oal_image(blank, image)

    direct_default = measure_topdown_oal_geometry(
        pipeline.segmentation.mask,
    )

    assert pipeline.passed
    assert not direct_default.passed
    assert direct_default.failure_reason == (
        "The expected wider fixture region was not detected."
    )


def test_pipeline_converts_pixels_to_inches() -> None:
    blank, image = _blank_and_case()

    result = measure_topdown_oal_image(
        blank,
        image,
        pixels_per_inch=520.0,
    )

    assert result.passed
    assert result.geometry is not None
    assert result.geometry.length_inches == pytest.approx(1.0, abs=0.002)


def test_pipeline_reports_segmentation_failure() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    result = measure_topdown_oal_image(blank, image)

    assert not result.passed
    assert result.failure_stage == "segmentation"
    assert result.geometry is None


def test_pipeline_reports_geometry_failure() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(image, (145, 140), (155, 150), 80, thickness=-1)

    result = measure_topdown_oal_image(blank, image)

    assert not result.passed
    assert result.failure_stage == "geometry"
    assert result.geometry is not None


def test_pipeline_rejects_invalid_scale() -> None:
    blank, image = _blank_and_case()

    with pytest.raises(ValueError, match="pixels_per_inch"):
        measure_topdown_oal_image(
            blank,
            image,
            pixels_per_inch=-1.0,
        )
