"""Deterministic segmentation for real top-down OAL case images."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class OALSegmentationResult:
    """Result of blank-reference OAL case segmentation."""

    passed: bool
    failure_reason: str | None
    otsu_threshold: float | None
    mask: NDArray[np.uint8]
    centroid_xy: tuple[float, float] | None
    component_pixels: int


def segment_oal_case(
    blank: NDArray[np.uint8],
    image: NDArray[np.uint8],
) -> OALSegmentationResult:
    """Segment the case using the proven blank-subtraction pipeline."""

    if blank.ndim != 2 or image.ndim != 2:
        raise ValueError("blank and image must be two-dimensional grayscale images.")

    if blank.shape != image.shape:
        raise ValueError(
            f"Image dimensions differ: blank={blank.shape}, image={image.shape}"
        )

    darkening = cv2.subtract(blank, image)
    blurred = cv2.GaussianBlur(darkening, (5, 5), 0)

    threshold, mask = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    kernel = np.ones((3, 3), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8),
        connectivity=8,
    )

    if count <= 1:
        return OALSegmentationResult(
            passed=False,
            failure_reason="No foreground case component was detected.",
            otsu_threshold=float(threshold),
            mask=np.zeros_like(mask),
            centroid_xy=None,
            component_pixels=0,
        )

    areas = stats[1:, cv2.CC_STAT_AREA]
    largest_label = int(np.argmax(areas)) + 1
    component = labels == largest_label
    component_mask = component.astype(np.uint8) * 255

    rows_y, columns_x = np.nonzero(component)

    centroid_x = float(columns_x.mean())
    centroid_y = float(rows_y.mean())

    return OALSegmentationResult(
        passed=True,
        failure_reason=None,
        otsu_threshold=float(threshold),
        mask=component_mask,
        centroid_xy=(centroid_x, centroid_y),
        component_pixels=int(component.sum()),
    )
