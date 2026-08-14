from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.calibration.oal_spatial_calibration import (
    ppi_0_at,
    ppi_90_at,
    resolve_oal_spatial_calibration,
)
from src.measurement.topdown_oal import measure_topdown_oal
from src.measurement.topdown_oal_pipeline import measure_topdown_oal_image


def _blank_and_horizontal_case() -> tuple[np.ndarray, np.ndarray]:
    blank = np.full((1088, 1456), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(
        image,
        (540, 610),
        (1060, 690),
        80,
        thickness=-1,
    )

    return blank, image


def _blank_and_vertical_case() -> tuple[np.ndarray, np.ndarray]:
    blank = np.full((1088, 1456), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(
        image,
        (760, 390),
        (840, 910),
        80,
        thickness=-1,
    )

    return blank, image


def test_calibration_maps_horizontal_oal_to_historical_ppi_90() -> None:
    result = resolve_oal_spatial_calibration(
        800.0,
        650.0,
        0.0,
    )

    assert result.effective_ppi == pytest.approx(
        ppi_90_at(800.0, 650.0),
    )


def test_calibration_maps_vertical_oal_to_historical_ppi_0() -> None:
    result = resolve_oal_spatial_calibration(
        800.0,
        650.0,
        90.0,
    )

    assert result.effective_ppi == pytest.approx(
        ppi_0_at(800.0, 650.0),
    )


def test_pipeline_measures_case_only_image_with_pca() -> None:
    blank, image = _blank_and_horizontal_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed, result.failure_reason
    assert result.pca is not None
    assert result.pca.length_pixels == pytest.approx(520.0, abs=1.0)


def test_pipeline_intentionally_disables_fixture_width_gate() -> None:
    blank, image = _blank_and_horizontal_case()

    pipeline = measure_topdown_oal_image(blank, image)

    direct_default = measure_topdown_oal(
        pipeline.segmentation.mask,
    )

    assert pipeline.passed
    assert not direct_default.passed
    assert direct_default.failure_reason == (
        "The expected wider fixture region was not detected."
    )


def test_pipeline_uses_segmentation_centroid_for_calibration() -> None:
    blank, image = _blank_and_horizontal_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed
    assert result.segmentation.centroid_xy is not None
    assert result.calibration is not None

    centroid_x, centroid_y = result.segmentation.centroid_xy

    assert result.calibration.centroid_x_px == pytest.approx(centroid_x)
    assert result.calibration.centroid_y_px == pytest.approx(centroid_y)


def test_horizontal_pipeline_uses_corrected_principal_direction() -> None:
    blank, image = _blank_and_horizontal_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed
    assert result.pca is not None
    assert result.calibration is not None
    assert result.pca.angle_degrees == pytest.approx(0.0, abs=0.1)

    centroid_x, centroid_y = result.segmentation.centroid_xy

    assert result.calibration.effective_ppi == pytest.approx(
        ppi_90_at(centroid_x, centroid_y),
        rel=1e-6,
    )


def test_vertical_pipeline_uses_corrected_principal_direction() -> None:
    blank, image = _blank_and_vertical_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed
    assert result.pca is not None
    assert result.calibration is not None
    assert abs(result.pca.angle_degrees) == pytest.approx(
        90.0,
        abs=0.1,
    )

    centroid_x, centroid_y = result.segmentation.centroid_xy

    assert result.calibration.effective_ppi == pytest.approx(
        ppi_0_at(centroid_x, centroid_y),
        rel=1e-6,
    )


def test_pipeline_converts_pca_pixels_to_inches() -> None:
    blank, image = _blank_and_horizontal_case()

    result = measure_topdown_oal_image(blank, image)

    assert result.passed
    assert result.pca is not None
    assert result.calibration is not None
    assert result.length_inches is not None

    expected = result.pca.length_pixels / result.calibration.effective_ppi

    assert result.length_inches == pytest.approx(expected)


def test_pipeline_reports_segmentation_failure() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    result = measure_topdown_oal_image(blank, image)

    assert not result.passed
    assert result.failure_stage == "segmentation"
    assert result.pca is None
    assert result.calibration is None
    assert result.length_inches is None


def test_pipeline_reports_pca_failure() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(
        image,
        (145, 140),
        (155, 150),
        80,
        thickness=-1,
    )

    result = measure_topdown_oal_image(blank, image)

    assert not result.passed
    assert result.failure_stage == "pca"
    assert result.pca is not None
    assert result.calibration is None
    assert result.length_inches is None


def test_calibration_rejects_nonfinite_inputs() -> None:
    with pytest.raises(ValueError, match="finite"):
        resolve_oal_spatial_calibration(
            float("nan"),
            650.0,
            90.0,
        )
