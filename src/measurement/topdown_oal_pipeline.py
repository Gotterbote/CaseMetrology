"""Validated raw-image pipeline for top-down OAL measurement.

This module combines the validated real-image segmentation routine with the
frozen geometry OAL estimator. The geometry estimator itself is not modified.

The real-image segmentation produces a case-only mask, so the historical
synthetic-fixture width gate is intentionally disabled here.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from src.image_processing.oal_segmentation import (
    OALSegmentationResult,
    segment_oal_case,
)
from src.measurement.topdown_oal_geometry import (
    TopDownGeometryOALResult,
    measure_topdown_oal_geometry,
)

CASE_ONLY_FIXTURE_WIDTH_RATIO = 0.0


@dataclass(frozen=True)
class TopDownOALPipelineResult:
    """Combined segmentation and geometry-estimator result."""

    passed: bool
    failure_stage: str | None
    failure_reason: str | None
    segmentation: OALSegmentationResult
    geometry: TopDownGeometryOALResult | None


def measure_topdown_oal_image(
    blank: NDArray[np.uint8],
    image: NDArray[np.uint8],
    *,
    pixels_per_inch: float | None = None,
) -> TopDownOALPipelineResult:
    """Measure OAL from a raw grayscale image and its blank reference."""

    segmentation = segment_oal_case(blank, image)

    if not segmentation.passed:
        return TopDownOALPipelineResult(
            passed=False,
            failure_stage="segmentation",
            failure_reason=segmentation.failure_reason,
            segmentation=segmentation,
            geometry=None,
        )

    geometry = measure_topdown_oal_geometry(
        segmentation.mask,
        pixels_per_inch=pixels_per_inch,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )

    if not geometry.passed:
        return TopDownOALPipelineResult(
            passed=False,
            failure_stage="geometry",
            failure_reason=geometry.failure_reason,
            segmentation=segmentation,
            geometry=geometry,
        )

    return TopDownOALPipelineResult(
        passed=True,
        failure_stage=None,
        failure_reason=None,
        segmentation=segmentation,
        geometry=geometry,
    )
