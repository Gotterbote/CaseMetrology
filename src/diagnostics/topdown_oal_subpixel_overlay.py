"""Diagnostic overlay for grayscale subpixel OAL measurements."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from src.measurement.topdown_oal import TopDownOALResult
from src.measurement.topdown_oal_geometry import (
    FittedLineSegment,
    TopDownGeometryOALResult,
)
from src.measurement.topdown_oal_subpixel import TopDownSubpixelOALResult


def _point(point_xy: tuple[float, float]) -> tuple[int, int]:
    return int(round(point_xy[0])), int(round(point_xy[1]))


def _draw_segment(
    image: NDArray[np.uint8],
    segment: FittedLineSegment | None,
    color: tuple[int, int, int],
    thickness: int,
) -> None:
    if segment is None:
        return
    cv2.line(
        image,
        _point(segment.start_xy),
        _point(segment.end_xy),
        color,
        thickness,
        cv2.LINE_AA,
    )


def _base_image(image: NDArray[np.uint8]) -> NDArray[np.uint8]:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 3:
        return image.copy()
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    raise ValueError("image must be grayscale, BGR, or BGRA.")


def draw_topdown_oal_subpixel_overlay(
    image: NDArray[np.uint8],
    mask: NDArray[np.uint8],
    result: TopDownSubpixelOALResult,
    *,
    baseline: TopDownOALResult | None = None,
    binary_geometry: TopDownGeometryOALResult | None = None,
    label: str | None = None,
) -> NDArray[np.uint8]:
    """Draw accepted-mask contour and all three OAL estimators."""

    overlay = _base_image(image)
    contour_source = np.where(mask > 0, 255, 0).astype(np.uint8)
    contours, _ = cv2.findContours(
        contour_source,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    cv2.drawContours(overlay, contours, -1, (180, 180, 180), 1, cv2.LINE_AA)

    if baseline is not None and baseline.passed:
        if (
            baseline.endpoint_min_xy is not None
            and baseline.endpoint_max_xy is not None
        ):
            cv2.line(
                overlay,
                _point(baseline.endpoint_min_xy),
                _point(baseline.endpoint_max_xy),
                (128, 128, 128),
                1,
                cv2.LINE_AA,
            )

    if binary_geometry is not None and binary_geometry.passed:
        _draw_segment(overlay, binary_geometry.axis_segment, (0, 165, 255), 1)

    if result.passed:
        _draw_segment(overlay, result.sidewall_min_segment, (255, 255, 0), 2)
        _draw_segment(overlay, result.sidewall_max_segment, (255, 255, 0), 2)
        _draw_segment(overlay, result.end_min_segment, (255, 0, 255), 2)
        _draw_segment(overlay, result.end_max_segment, (255, 0, 255), 2)
        _draw_segment(overlay, result.axis_segment, (0, 255, 0), 2)
        if result.endpoint_min_xy is not None and result.endpoint_max_xy is not None:
            cv2.circle(overlay, _point(result.endpoint_min_xy), 5, (0, 0, 255), 2)
            cv2.circle(overlay, _point(result.endpoint_max_xy), 5, (0, 0, 255), 2)

    text_lines: list[str] = []
    if label:
        text_lines.append(label)
    if baseline is not None:
        text_lines.append(
            f"PCA: {baseline.length_pixels:.6f} px"
            if baseline.length_pixels is not None
            else f"PCA failed: {baseline.failure_reason}"
        )
    if binary_geometry is not None:
        text_lines.append(
            f"Binary geometry: {binary_geometry.length_pixels:.6f} px"
            if binary_geometry.length_pixels is not None
            else f"Binary geometry failed: {binary_geometry.failure_reason}"
        )
    text_lines.append(
        f"Subpixel: {result.length_pixels:.6f} px"
        if result.length_pixels is not None
        else f"Subpixel failed: {result.failure_reason}"
    )
    if result.diagnostic_flags:
        text_lines.append("Flags: " + ", ".join(result.diagnostic_flags))

    y = 28
    for line in text_lines:
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (0, 0, 0),
            4,
            cv2.LINE_AA,
        )
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        y += 24

    return overlay
