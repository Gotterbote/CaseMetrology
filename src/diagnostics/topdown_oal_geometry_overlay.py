"""Diagnostic overlay for geometry-based top-down OAL results."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from src.measurement.topdown_oal import TopDownOALResult
from src.measurement.topdown_oal_geometry import (
    FittedLineSegment,
    TopDownGeometryOALResult,
)


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


def draw_topdown_oal_geometry_overlay(
    mask: NDArray[np.uint8],
    geometry: TopDownGeometryOALResult,
    *,
    baseline: TopDownOALResult | None = None,
    label: str | None = None,
) -> NDArray[np.uint8]:
    """Draw baseline endpoints and the fitted geometry on a binary mask."""

    normalized = np.where(mask > 0, 255, 0).astype(np.uint8)
    overlay = cv2.cvtColor(normalized, cv2.COLOR_GRAY2BGR)

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
            for endpoint in (baseline.endpoint_min_xy, baseline.endpoint_max_xy):
                cv2.circle(overlay, _point(endpoint), 5, (128, 128, 128), 1)

    if geometry.passed:
        _draw_segment(overlay, geometry.sidewall_min_segment, (255, 255, 0), 2)
        _draw_segment(overlay, geometry.sidewall_max_segment, (255, 255, 0), 2)
        _draw_segment(overlay, geometry.end_min_segment, (255, 0, 255), 2)
        _draw_segment(overlay, geometry.end_max_segment, (255, 0, 255), 2)
        _draw_segment(overlay, geometry.axis_segment, (0, 255, 0), 2)

        if (
            geometry.endpoint_min_xy is not None
            and geometry.endpoint_max_xy is not None
        ):
            cv2.circle(overlay, _point(geometry.endpoint_min_xy), 6, (0, 0, 255), 2)
            cv2.circle(overlay, _point(geometry.endpoint_max_xy), 6, (0, 0, 255), 2)

    text_lines: list[str] = []
    if label:
        text_lines.append(label)
    if baseline is not None:
        baseline_text = (
            f"PCA: {baseline.length_pixels:.6f} px"
            if baseline.length_pixels is not None
            else f"PCA failed: {baseline.failure_reason}"
        )
        text_lines.append(baseline_text)
    geometry_text = (
        f"Geometry: {geometry.length_pixels:.6f} px"
        if geometry.length_pixels is not None
        else f"Geometry failed: {geometry.failure_reason}"
    )
    text_lines.append(geometry_text)
    if geometry.diagnostic_flags:
        text_lines.append("Flags: " + ", ".join(geometry.diagnostic_flags))

    y = 28
    for line in text_lines:
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 0),
            4,
            cv2.LINE_AA,
        )
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        y += 26

    return overlay
