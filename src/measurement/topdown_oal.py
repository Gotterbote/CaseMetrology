"""Exploratory top-down OAL measurement for a merged case/fixture silhouette."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

BinaryMask = NDArray[np.uint8]


@dataclass(frozen=True)
class TopDownOALResult:
    passed: bool
    failure_reason: str | None
    length_pixels: float | None
    length_inches: float | None
    angle_degrees: float | None
    endpoint_min_xy: tuple[float, float] | None
    endpoint_max_xy: tuple[float, float] | None
    case_width_pixels: float | None
    fixture_width_pixels: float | None
    fixture_width_ratio: float | None
    largest_component_pixels: int
    second_component_pixels: int


def _largest_component(
    mask: BinaryMask,
) -> tuple[BinaryMask, int, int]:
    binary = (mask > 0).astype(np.uint8)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary,
        connectivity=8,
    )

    if count <= 1:
        return np.zeros_like(binary), 0, 0

    areas = stats[1:, cv2.CC_STAT_AREA]
    largest_index = int(np.argmax(areas))
    largest_label = largest_index + 1
    largest_area = int(areas[largest_index])

    remaining = np.delete(areas, largest_index)
    second_area = int(remaining.max()) if remaining.size else 0

    component = (labels == largest_label).astype(np.uint8)
    return component, largest_area, second_area


def _touches_border(mask: BinaryMask, margin: int) -> bool:
    edge = margin + 1

    return bool(
        mask[:edge, :].any()
        or mask[-edge:, :].any()
        or mask[:, :edge].any()
        or mask[:, -edge:].any()
    )


def _points_xy(mask: BinaryMask) -> NDArray[np.float64]:
    rows_y, columns_x = np.nonzero(mask)

    return np.column_stack((columns_x, rows_y)).astype(np.float64)


def _pca_axis(
    points_xy: NDArray[np.float64],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    float,
]:
    centroid = points_xy.mean(axis=0)
    centered = points_xy - centroid
    covariance = np.cov(centered, rowvar=False)

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]

    major = float(eigenvalues[order[0]])
    minor = float(max(eigenvalues[order[1]], 1e-12))

    axis = eigenvectors[:, order[0]].astype(np.float64)
    axis /= np.linalg.norm(axis)

    if axis[0] < 0 or (abs(axis[0]) < 1e-12 and axis[1] < 0):
        axis = -axis

    return centroid, axis, major / minor


def _width_profile(
    points_xy: NDArray[np.float64],
    centroid_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.int64],
]:
    perpendicular = np.array(
        [-axis_xy[1], axis_xy[0]],
        dtype=np.float64,
    )

    relative = points_xy - centroid_xy
    longitudinal = relative @ axis_xy
    transverse = relative @ perpendicular

    minimum = float(longitudinal.min())
    bins = np.floor(longitudinal - minimum).astype(np.int64)
    bin_count = int(bins.max()) + 1

    minimum_transverse = np.full(
        bin_count,
        np.inf,
        dtype=np.float64,
    )
    maximum_transverse = np.full(
        bin_count,
        -np.inf,
        dtype=np.float64,
    )

    np.minimum.at(minimum_transverse, bins, transverse)
    np.maximum.at(maximum_transverse, bins, transverse)

    widths = maximum_transverse - minimum_transverse
    return widths, bins


def measure_topdown_oal(
    mask: BinaryMask,
    *,
    pixels_per_inch: float | None = None,
    border_margin_pixels: int = 5,
    minimum_component_pixels: int = 1000,
    maximum_second_component_fraction: float = 0.02,
    minimum_axis_ratio: float = 2.0,
    minimum_fixture_width_ratio: float = 1.6,
) -> TopDownOALResult:
    """Measure OAL from the merged case-and-fixture binary silhouette."""

    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional image.")

    if pixels_per_inch is not None and pixels_per_inch <= 0:
        raise ValueError("pixels_per_inch must be greater than zero.")

    component, largest_area, second_area = _largest_component(mask)

    def failed(reason: str) -> TopDownOALResult:
        return TopDownOALResult(
            passed=False,
            failure_reason=reason,
            length_pixels=None,
            length_inches=None,
            angle_degrees=None,
            endpoint_min_xy=None,
            endpoint_max_xy=None,
            case_width_pixels=None,
            fixture_width_pixels=None,
            fixture_width_ratio=None,
            largest_component_pixels=largest_area,
            second_component_pixels=second_area,
        )

    if largest_area < minimum_component_pixels:
        return failed("No sufficiently large assembly was detected.")

    if second_area > (largest_area * maximum_second_component_fraction):
        return failed("A second significant object was detected.")

    if _touches_border(
        component,
        border_margin_pixels,
    ):
        return failed("The assembly touches the image border.")

    points = _points_xy(component)
    centroid, initial_axis, axis_ratio = _pca_axis(points)

    if axis_ratio < minimum_axis_ratio:
        return failed("The detected silhouette is not sufficiently elongated.")

    widths, point_bins = _width_profile(
        points,
        centroid,
        initial_axis,
    )

    valid_widths = widths[np.isfinite(widths)]

    if valid_widths.size < 10:
        return failed("Insufficient silhouette width-profile data.")

    case_width = float(np.percentile(valid_widths, 25))
    fixture_width = float(np.percentile(valid_widths, 95))
    fixture_ratio = fixture_width / max(
        case_width,
        1e-12,
    )

    if fixture_ratio < minimum_fixture_width_ratio:
        return failed("The expected wider fixture region was not detected.")

    case_like_bins = widths <= case_width * 1.35
    exposed_case_points = points[case_like_bins[point_bins]]

    if exposed_case_points.shape[0] < 100:
        return failed("Insufficient exposed case pixels were detected.")

    refined_centroid, refined_axis, _ = _pca_axis(exposed_case_points)

    projections = (points - refined_centroid) @ refined_axis

    minimum_projection = float(projections.min())
    maximum_projection = float(projections.max())

    length_pixels = maximum_projection - minimum_projection

    endpoint_min = refined_centroid + minimum_projection * refined_axis
    endpoint_max = refined_centroid + maximum_projection * refined_axis

    angle_degrees = float(
        np.degrees(
            np.arctan2(
                refined_axis[1],
                refined_axis[0],
            )
        )
    )

    length_inches = None if pixels_per_inch is None else length_pixels / pixels_per_inch

    return TopDownOALResult(
        passed=True,
        failure_reason=None,
        length_pixels=float(length_pixels),
        length_inches=(None if length_inches is None else float(length_inches)),
        angle_degrees=angle_degrees,
        endpoint_min_xy=(
            float(endpoint_min[0]),
            float(endpoint_min[1]),
        ),
        endpoint_max_xy=(
            float(endpoint_max[0]),
            float(endpoint_max[1]),
        ),
        case_width_pixels=case_width,
        fixture_width_pixels=fixture_width,
        fixture_width_ratio=float(fixture_ratio),
        largest_component_pixels=largest_area,
        second_component_pixels=second_area,
    )
