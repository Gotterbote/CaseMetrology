"""Validated raw-image pipeline for top-down OAL measurement.

This module combines the frozen real-image segmentation routine, the frozen
PCA/extreme-mask OAL pixel-length estimator, and the prospectively corrected
spatial/directional calibration integration.

The real-image segmentation produces a case-only mask, so the historical
synthetic-fixture width gate is intentionally disabled here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from src.calibration.oal_spatial_calibration import (
    OALSpatialCalibrationResult,
    resolve_oal_spatial_calibration,
)
from src.image_processing.oal_segmentation import (
    OALSegmentationResult,
    segment_oal_case,
)
from src.measurement.topdown_oal import (
    TopDownOALResult,
    measure_topdown_oal,
)

CASE_ONLY_FIXTURE_WIDTH_RATIO = 0.0


@dataclass(frozen=True)
class TopDownOALPipelineResult:
    """Combined segmentation, PCA-estimator, and calibration result."""

    passed: bool
    failure_stage: str | None
    failure_reason: str | None
    segmentation: OALSegmentationResult
    pca: TopDownOALResult | None
    calibration: OALSpatialCalibrationResult | None
    length_inches: float | None


def measure_topdown_oal_image(
    blank: NDArray[np.uint8],
    image: NDArray[np.uint8],
) -> TopDownOALPipelineResult:
    """Measure calibrated OAL from a grayscale image and blank reference."""

    segmentation = segment_oal_case(blank, image)

    if not segmentation.passed:
        return TopDownOALPipelineResult(
            passed=False,
            failure_stage="segmentation",
            failure_reason=segmentation.failure_reason,
            segmentation=segmentation,
            pca=None,
            calibration=None,
            length_inches=None,
        )

    pca = measure_topdown_oal(
        segmentation.mask,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )

    if not pca.passed:
        return TopDownOALPipelineResult(
            passed=False,
            failure_stage="pca",
            failure_reason=pca.failure_reason,
            segmentation=segmentation,
            pca=pca,
            calibration=None,
            length_inches=None,
        )

    if (
        segmentation.centroid_xy is None
        or pca.angle_degrees is None
        or pca.length_pixels is None
    ):
        raise RuntimeError("Passed OAL results are missing required values.")

    centroid_x, centroid_y = segmentation.centroid_xy

    calibration = resolve_oal_spatial_calibration(
        centroid_x,
        centroid_y,
        pca.angle_degrees,
    )

    length_inches = pca.length_pixels / calibration.effective_ppi

    return TopDownOALPipelineResult(
        passed=True,
        failure_stage=None,
        failure_reason=None,
        segmentation=segmentation,
        pca=pca,
        calibration=calibration,
        length_inches=float(length_inches),
    )
