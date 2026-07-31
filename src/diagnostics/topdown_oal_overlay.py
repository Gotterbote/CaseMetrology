"""Diagnostic overlay for exploratory top-down OAL measurements."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from src.measurement.topdown_oal import TopDownOALResult

BinaryMask = NDArray[np.uint8]
ColorImage = NDArray[np.uint8]


def draw_topdown_oal_overlay(
    mask: BinaryMask,
    result: TopDownOALResult,
) -> ColorImage:
    """Draw a monochrome OAL diagnostic overlay."""

    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional image.")

    binary = (mask > 0).astype(np.uint8) * 255

    # White backlit background with a black merged silhouette.
    overlay = np.full(
        (binary.shape[0], binary.shape[1], 3),
        255,
        dtype=np.uint8,
    )
    overlay[binary > 0] = (0, 0, 0)

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    cv2.drawContours(
        overlay,
        contours,
        -1,
        (100, 100, 100),
        1,
    )

    if not result.passed:
        cv2.putText(
            overlay,
            f"FAIL: {result.failure_reason}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )
        return overlay

    if (
        result.endpoint_min_xy is None
        or result.endpoint_max_xy is None
        or result.length_pixels is None
    ):
        raise ValueError("A passed result must contain endpoints and length.")

    endpoint_min = tuple(int(round(value)) for value in result.endpoint_min_xy)
    endpoint_max = tuple(int(round(value)) for value in result.endpoint_max_xy)

    # Axial measurement line.
    cv2.line(
        overlay,
        endpoint_min,
        endpoint_max,
        (160, 160, 160),
        2,
        cv2.LINE_AA,
    )

    # Endpoint contact markers.
    for endpoint in (endpoint_min, endpoint_max):
        cv2.circle(
            overlay,
            endpoint,
            7,
            (255, 255, 255),
            thickness=-1,
            lineType=cv2.LINE_AA,
        )
        cv2.circle(
            overlay,
            endpoint,
            7,
            (0, 0, 0),
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    angle_text = (
        "unknown" if result.angle_degrees is None else f"{result.angle_degrees:.2f} deg"
    )

    cv2.putText(
        overlay,
        f"OAL: {result.length_pixels:.2f} px",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        overlay,
        f"Axis angle: {angle_text}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    return overlay
