"""Diagnostic overlay for mask-anchored subpixel OAL Version 2."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from src.measurement.topdown_oal import TopDownOALResult
from src.measurement.topdown_oal_geometry import FittedLineSegment
from src.measurement.topdown_oal_subpixel import TopDownSubpixelOALResult
from src.measurement.topdown_oal_subpixel_v2 import (
    IntensityCrossingProfile,
    TopDownSubpixelV2OALResult,
)


def _point(point_xy: tuple[float, float]) -> tuple[int, int]:
    return int(round(point_xy[0])), int(round(point_xy[1]))


def _base_image(image: NDArray[np.uint8]) -> NDArray[np.uint8]:
    if image.ndim == 2:
        return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if image.ndim == 3 and image.shape[2] == 3:
        return image.copy()
    if image.ndim == 3 and image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    raise ValueError("image must be grayscale, BGR, or BGRA.")


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


def _draw_profiles(
    image: NDArray[np.uint8], profiles: tuple[IntensityCrossingProfile, ...]
) -> None:
    for profile in profiles:
        if profile.accepted and profile.crossing_xy is not None:
            cv2.circle(image, _point(profile.crossing_xy), 2, (0, 255, 255), -1)
        elif profile.anchor_xy is not None:
            x, y = _point(profile.anchor_xy)
            cv2.line(image, (x - 2, y - 2), (x + 2, y + 2), (0, 0, 255), 1)
            cv2.line(image, (x - 2, y + 2), (x + 2, y - 2), (0, 0, 255), 1)


def draw_topdown_oal_subpixel_v2_overlay(
    image: NDArray[np.uint8],
    mask: NDArray[np.uint8],
    result: TopDownSubpixelV2OALResult,
    *,
    baseline: TopDownOALResult | None = None,
    subpixel_v1: TopDownSubpixelOALResult | None = None,
    label: str | None = None,
) -> NDArray[np.uint8]:
    """Draw the accepted contour, profile points, fitted lines, and axes."""

    overlay = _base_image(image)
    contour_source = np.where(mask > 0, 255, 0).astype(np.uint8)
    contours, _ = cv2.findContours(
        contour_source, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(overlay, contours, -1, (170, 170, 170), 1, cv2.LINE_AA)

    if baseline is not None and baseline.passed:
        if (
            baseline.endpoint_min_xy is not None
            and baseline.endpoint_max_xy is not None
        ):
            cv2.line(
                overlay,
                _point(baseline.endpoint_min_xy),
                _point(baseline.endpoint_max_xy),
                (120, 120, 120),
                1,
                cv2.LINE_AA,
            )
    if subpixel_v1 is not None and subpixel_v1.passed:
        _draw_segment(overlay, subpixel_v1.axis_segment, (0, 165, 255), 1)

    profile_groups = (
        result.sidewall_min_profiles,
        result.sidewall_max_profiles,
        result.end_min_profiles,
        result.end_max_profiles,
    )
    for profiles in profile_groups:
        _draw_profiles(overlay, profiles)

    if result.passed:
        _draw_segment(overlay, result.sidewall_min_segment, (255, 255, 0), 2)
        _draw_segment(overlay, result.sidewall_max_segment, (255, 255, 0), 2)
        _draw_segment(overlay, result.end_min_segment, (255, 0, 255), 2)
        _draw_segment(overlay, result.end_max_segment, (255, 0, 255), 2)
        _draw_segment(overlay, result.axis_segment, (0, 255, 0), 2)
        if result.endpoint_min_xy is not None and result.endpoint_max_xy is not None:
            cv2.circle(overlay, _point(result.endpoint_min_xy), 5, (0, 0, 255), 2)
            cv2.circle(overlay, _point(result.endpoint_max_xy), 5, (0, 0, 255), 2)

    lines: list[str] = []
    if label:
        lines.append(label)
    if baseline is not None:
        lines.append(
            f"PCA: {baseline.length_pixels:.6f} px"
            if baseline.length_pixels is not None
            else f"PCA failed: {baseline.failure_reason}"
        )
    if subpixel_v1 is not None:
        lines.append(
            f"Subpixel V1: {subpixel_v1.length_pixels:.6f} px"
            if subpixel_v1.length_pixels is not None
            else f"Subpixel V1 failed: {subpixel_v1.failure_reason}"
        )
    lines.append(
        f"Subpixel V2: {result.length_pixels:.6f} px"
        if result.length_pixels is not None
        else f"Subpixel V2 failed: {result.failure_reason}"
    )
    if result.diagnostic_flags:
        lines.append("Flags: " + ", ".join(result.diagnostic_flags))

    y = 28
    for line in lines:
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.56,
            (0, 0, 0),
            4,
            cv2.LINE_AA,
        )
        cv2.putText(
            overlay,
            line,
            (15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.56,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
        y += 23
    return overlay
