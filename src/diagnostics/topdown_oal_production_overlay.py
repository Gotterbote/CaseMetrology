"""Production annotation overlay for validated top-down OAL measurements.

This module is presentation-only. It does not recalculate or modify the
frozen OAL measurement result.

Visual convention:
    blue   = accepted segmentation mask
    orange = PCA OAL measurement line
    white  = measured endpoint contacts

Physical base/mouth roles are intentionally not inferred here.
"""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from src.measurement.topdown_oal_pipeline import TopDownOALPipelineResult

GrayImage = NDArray[np.uint8]
ColorImage = NDArray[np.uint8]


def _outlined_text(
    image: ColorImage,
    text: str,
    origin: tuple[int, int],
    *,
    scale: float = 0.65,
) -> None:
    """Draw readable white text with a black outline."""

    cv2.putText(
        image,
        text,
        origin,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (0, 0, 0),
        4,
        cv2.LINE_AA,
    )

    cv2.putText(
        image,
        text,
        origin,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


def draw_topdown_oal_production_overlay(
    image: GrayImage,
    result: TopDownOALPipelineResult,
) -> ColorImage:
    """Draw the validated OAL result on the original grayscale capture."""

    if image.ndim != 2:
        raise ValueError("image must be a two-dimensional grayscale image.")

    mask = result.segmentation.mask

    if mask.shape != image.shape:
        raise ValueError(
            f"Image and segmentation shapes differ: "
            f"image={image.shape}, mask={mask.shape}"
        )

    annotated = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # ------------------------------------------------------------------
    # BLUE: actual segmentation result
    # ------------------------------------------------------------------

    accepted_mask = mask > 0

    if accepted_mask.any():
        blue = np.array([255, 0, 0], dtype=np.float32)
        alpha = 0.22

        pixels = annotated[accepted_mask].astype(np.float32)

        annotated[accepted_mask] = np.clip(
            pixels * (1.0 - alpha) + blue * alpha,
            0,
            255,
        ).astype(np.uint8)

        binary = accepted_mask.astype(np.uint8) * 255

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        cv2.drawContours(
            annotated,
            contours,
            -1,
            (255, 0, 0),
            2,
            cv2.LINE_AA,
        )

    # ------------------------------------------------------------------
    # Failed measurement: show the failure but do not fabricate geometry.
    # ------------------------------------------------------------------

    if not result.passed:
        _outlined_text(
            annotated,
            "OAL: NOT EVALUATED",
            (20, 35),
            scale=0.72,
        )

        failure = (
            f"{result.failure_stage or 'unknown'}: "
            f"{result.failure_reason or 'unspecified failure'}"
        )

        _outlined_text(
            annotated,
            failure,
            (20, 68),
            scale=0.55,
        )

        return annotated

    if result.pca is None:
        raise ValueError("Passed pipeline result is missing PCA result.")

    if result.calibration is None:
        raise ValueError("Passed pipeline result is missing calibration result.")

    if result.length_inches is None:
        raise ValueError("Passed pipeline result is missing calibrated OAL.")

    pca = result.pca
    calibration = result.calibration

    if (
        pca.endpoint_min_xy is None
        or pca.endpoint_max_xy is None
        or pca.length_pixels is None
        or pca.angle_degrees is None
    ):
        raise ValueError("Passed PCA result is missing required measurement geometry.")

    endpoint_min = tuple(int(round(value)) for value in pca.endpoint_min_xy)

    endpoint_max = tuple(int(round(value)) for value in pca.endpoint_max_xy)

    # ------------------------------------------------------------------
    # ORANGE: exact PCA OAL measurement line
    # ------------------------------------------------------------------

    cv2.line(
        annotated,
        endpoint_min,
        endpoint_max,
        (0, 165, 255),
        3,
        cv2.LINE_AA,
    )

    # ------------------------------------------------------------------
    # WHITE: actual measured endpoint contacts
    #
    # Deliberately not labeled BASE/MOUTH. PCA MIN/MAX ordering is
    # mathematical and physical role classification is not required for OAL.
    # ------------------------------------------------------------------

    for endpoint in (endpoint_min, endpoint_max):
        cv2.circle(
            annotated,
            endpoint,
            8,
            (255, 255, 255),
            -1,
            cv2.LINE_AA,
        )

        cv2.circle(
            annotated,
            endpoint,
            8,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

    # ------------------------------------------------------------------
    # Measurement information
    # ------------------------------------------------------------------

    lines = [
        f"OAL: {result.length_inches:.6f} in",
        f"Pixels: {pca.length_pixels:.3f} px",
        f"Scale: {calibration.effective_ppi:.6f} px/in",
        f"Axis: {pca.angle_degrees:.3f} deg",
    ]

    y = 32

    for line in lines:
        _outlined_text(
            annotated,
            line,
            (20, y),
        )
        y += 30

    return annotated
