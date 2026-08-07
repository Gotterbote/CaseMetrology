"""Orientation-independent gauge-block scale measurement.

The certified 1.0000024-inch dimension is the shorter in-plane dimension of
this rectangular gauge block. The analyzer estimates that dimension from the
two long physical faces, so the block may be rotated in the image plane.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

CERTIFIED_GAUGE_BLOCK_LENGTH_IN = 1.0000024
MINIMUM_COMPONENT_AREA_FRACTION = 0.01
MINIMUM_EDGE_CONTRAST = 20.0
PROFILE_STEP_PIXELS = 0.25
PROFILE_MARGIN_PIXELS = 12.0
EDGE_WINDOW_PIXELS = 8.0
EDGE_LEVEL_OFFSET_PIXELS = 4.0
LONG_AXIS_SAMPLE_COUNT = 61
LONG_AXIS_TRIM_FRACTION = 0.20


@dataclass(frozen=True)
class OrientedGaugeBlockResult:
    """Result of measuring the certified gauge-block dimension."""

    passed: bool
    failure_reason: str | None
    otsu_threshold: float | None
    measured_span_pixels: float | None
    pixels_per_inch: float | None
    inches_per_pixel: float | None
    accepted_profile_count: int
    orientation_degrees: float | None
    minimum_edge_rms_pixels: float | None
    maximum_edge_rms_pixels: float | None


def _unit(vector: NDArray[np.float64]) -> NDArray[np.float64]:
    norm = float(np.linalg.norm(vector))
    if norm <= 0.0:
        raise ValueError("Cannot normalize a zero-length vector.")
    return vector / norm


def _select_component(mask: NDArray[np.uint8]) -> NDArray[np.bool_]:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8,
    )
    image_height, image_width = mask.shape
    minimum_area = image_height * image_width * MINIMUM_COMPONENT_AREA_FRACTION
    candidates: list[tuple[int, int]] = []

    for component_id in range(1, count):
        x = int(stats[component_id, cv2.CC_STAT_LEFT])
        y = int(stats[component_id, cv2.CC_STAT_TOP])
        width = int(stats[component_id, cv2.CC_STAT_WIDTH])
        height = int(stats[component_id, cv2.CC_STAT_HEIGHT])
        area = int(stats[component_id, cv2.CC_STAT_AREA])

        touches_border = (
            x <= 0 or y <= 0 or x + width >= image_width or y + height >= image_height
        )

        if area >= minimum_area and not touches_border:
            candidates.append((area, component_id))

    if not candidates:
        raise RuntimeError("No suitable non-border gauge-block component was detected.")

    _, component_id = max(candidates)
    return labels == component_id


def _sample_bilinear(
    image: NDArray[np.float32],
    origin_xy: NDArray[np.float64],
    direction_xy: NDArray[np.float64],
    coordinates: NDArray[np.float64],
) -> NDArray[np.float64]:
    points = origin_xy[None, :] + coordinates[:, None] * direction_xy[None, :]
    map_x = points[:, 0].astype(np.float32).reshape(1, -1)
    map_y = points[:, 1].astype(np.float32).reshape(1, -1)
    sampled = cv2.remap(
        image,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=np.nan,
    )
    return sampled.reshape(-1).astype(np.float64)


def _linear_crossings(
    coordinates: NDArray[np.float64],
    values: NDArray[np.float64],
    level: float,
) -> list[float]:
    crossings: list[float] = []

    for index in range(len(coordinates) - 1):
        value_0 = float(values[index])
        value_1 = float(values[index + 1])

        if not np.isfinite(value_0) or not np.isfinite(value_1):
            continue
        if value_0 == value_1:
            continue

        difference_0 = value_0 - level
        difference_1 = value_1 - level

        if difference_0 == 0.0:
            crossing = float(coordinates[index])
        elif difference_0 * difference_1 > 0.0:
            continue
        else:
            fraction = (level - value_0) / (value_1 - value_0)
            if not 0.0 <= fraction <= 1.0:
                continue
            crossing = float(
                coordinates[index]
                + fraction * (coordinates[index + 1] - coordinates[index])
            )

        if not crossings or abs(crossing - crossings[-1]) > 1e-6:
            crossings.append(crossing)

    return crossings


def _refine_edge(
    coordinates: NDArray[np.float64],
    grayscale_values: NDArray[np.float64],
    anchor: float,
    *,
    minimum_side: bool,
) -> float | None:
    if minimum_side:
        background = (coordinates >= anchor - EDGE_WINDOW_PIXELS) & (
            coordinates <= anchor - EDGE_LEVEL_OFFSET_PIXELS
        )
        object_region = (coordinates >= anchor + EDGE_LEVEL_OFFSET_PIXELS) & (
            coordinates <= anchor + EDGE_WINDOW_PIXELS
        )
    else:
        object_region = (coordinates >= anchor - EDGE_WINDOW_PIXELS) & (
            coordinates <= anchor - EDGE_LEVEL_OFFSET_PIXELS
        )
        background = (coordinates >= anchor + EDGE_LEVEL_OFFSET_PIXELS) & (
            coordinates <= anchor + EDGE_WINDOW_PIXELS
        )

    if not np.any(background) or not np.any(object_region):
        return None

    background_level = float(np.nanmedian(grayscale_values[background]))
    object_level = float(np.nanmedian(grayscale_values[object_region]))
    contrast = abs(background_level - object_level)

    if not np.isfinite(contrast) or contrast < MINIMUM_EDGE_CONTRAST:
        return None

    target = (background_level + object_level) / 2.0
    local = (coordinates >= anchor - EDGE_WINDOW_PIXELS) & (
        coordinates <= anchor + EDGE_WINDOW_PIXELS
    )
    crossings = _linear_crossings(
        coordinates[local],
        grayscale_values[local],
        target,
    )

    if not crossings:
        return None

    return min(crossings, key=lambda crossing: abs(crossing - anchor))


def _line_rms(
    x_values: NDArray[np.float64],
    y_values: NDArray[np.float64],
    slope: float,
    intercept: float,
) -> float:
    residuals = y_values - (slope * x_values + intercept)
    return float(np.sqrt(np.mean(residuals**2)))


def measure_oriented_gauge_block(
    grayscale: NDArray[np.uint8],
    *,
    certified_length_in: float = CERTIFIED_GAUGE_BLOCK_LENGTH_IN,
) -> OrientedGaugeBlockResult:
    """Measure the certified short dimension regardless of image orientation."""

    if grayscale.ndim != 2:
        raise ValueError("grayscale must be a two-dimensional image.")
    if certified_length_in <= 0.0:
        raise ValueError("certified_length_in must be greater than zero.")

    otsu_threshold, binary_mask = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    try:
        component = _select_component(binary_mask)
    except RuntimeError as error:
        return OrientedGaugeBlockResult(
            passed=False,
            failure_reason=str(error),
            otsu_threshold=float(otsu_threshold),
            measured_span_pixels=None,
            pixels_per_inch=None,
            inches_per_pixel=None,
            accepted_profile_count=0,
            orientation_degrees=None,
            minimum_edge_rms_pixels=None,
            maximum_edge_rms_pixels=None,
        )

    rows_y, columns_x = np.nonzero(component)
    points = np.column_stack((columns_x, rows_y)).astype(np.float64)
    centroid = points.mean(axis=0)
    centered = points - centroid
    covariance = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)

    long_axis = _unit(eigenvectors[:, int(np.argmax(eigenvalues))])
    if long_axis[0] < 0.0:
        long_axis = -long_axis
    short_axis = np.asarray([-long_axis[1], long_axis[0]], dtype=np.float64)

    long_coordinates = centered @ long_axis
    short_coordinates = centered @ short_axis

    long_start, long_end = np.quantile(
        long_coordinates,
        [LONG_AXIS_TRIM_FRACTION, 1.0 - LONG_AXIS_TRIM_FRACTION],
    )
    short_start, short_end = np.quantile(
        short_coordinates,
        [0.005, 0.995],
    )

    profile_positions = np.linspace(
        float(long_start),
        float(long_end),
        LONG_AXIS_SAMPLE_COUNT,
    )
    profile_coordinates = np.arange(
        float(short_start) - PROFILE_MARGIN_PIXELS,
        float(short_end) + PROFILE_MARGIN_PIXELS + 0.5 * PROFILE_STEP_PIXELS,
        PROFILE_STEP_PIXELS,
        dtype=np.float64,
    )

    component_float = component.astype(np.float32)
    grayscale_float = grayscale.astype(np.float32)
    accepted: list[tuple[float, float, float]] = []

    for long_position in profile_positions:
        profile_origin = centroid + long_position * long_axis
        mask_values = _sample_bilinear(
            component_float,
            profile_origin,
            short_axis,
            profile_coordinates,
        )
        mask_crossings = _linear_crossings(
            profile_coordinates,
            mask_values,
            0.5,
        )

        if len(mask_crossings) < 2:
            continue

        minimum_anchor = min(mask_crossings)
        maximum_anchor = max(mask_crossings)
        grayscale_values = _sample_bilinear(
            grayscale_float,
            profile_origin,
            short_axis,
            profile_coordinates,
        )
        minimum_edge = _refine_edge(
            profile_coordinates,
            grayscale_values,
            minimum_anchor,
            minimum_side=True,
        )
        maximum_edge = _refine_edge(
            profile_coordinates,
            grayscale_values,
            maximum_anchor,
            minimum_side=False,
        )

        if minimum_edge is None or maximum_edge is None:
            continue

        accepted.append(
            (
                float(long_position),
                minimum_edge,
                maximum_edge,
            )
        )

    if len(accepted) < 10:
        return OrientedGaugeBlockResult(
            passed=False,
            failure_reason=("Insufficient valid profiles for gauge-block measurement."),
            otsu_threshold=float(otsu_threshold),
            measured_span_pixels=None,
            pixels_per_inch=None,
            inches_per_pixel=None,
            accepted_profile_count=len(accepted),
            orientation_degrees=None,
            minimum_edge_rms_pixels=None,
            maximum_edge_rms_pixels=None,
        )

    accepted_array = np.asarray(accepted, dtype=np.float64)
    long_values = accepted_array[:, 0]
    minimum_edges = accepted_array[:, 1]
    maximum_edges = accepted_array[:, 2]

    minimum_slope, minimum_intercept = np.polyfit(
        long_values,
        minimum_edges,
        1,
    )
    maximum_slope, maximum_intercept = np.polyfit(
        long_values,
        maximum_edges,
        1,
    )
    measured_span_pixels = float(maximum_intercept - minimum_intercept)

    if measured_span_pixels <= 0.0:
        return OrientedGaugeBlockResult(
            passed=False,
            failure_reason="Fitted gauge-block edge ordering is invalid.",
            otsu_threshold=float(otsu_threshold),
            measured_span_pixels=None,
            pixels_per_inch=None,
            inches_per_pixel=None,
            accepted_profile_count=len(accepted),
            orientation_degrees=None,
            minimum_edge_rms_pixels=None,
            maximum_edge_rms_pixels=None,
        )

    pixels_per_inch = measured_span_pixels / certified_length_in
    inches_per_pixel = certified_length_in / measured_span_pixels
    orientation_degrees = float(
        np.degrees(
            np.arctan2(
                long_axis[1],
                long_axis[0],
            )
        )
    )

    return OrientedGaugeBlockResult(
        passed=True,
        failure_reason=None,
        otsu_threshold=float(otsu_threshold),
        measured_span_pixels=measured_span_pixels,
        pixels_per_inch=pixels_per_inch,
        inches_per_pixel=inches_per_pixel,
        accepted_profile_count=len(accepted),
        orientation_degrees=orientation_degrees,
        minimum_edge_rms_pixels=_line_rms(
            long_values,
            minimum_edges,
            float(minimum_slope),
            float(minimum_intercept),
        ),
        maximum_edge_rms_pixels=_line_rms(
            long_values,
            maximum_edges,
            float(maximum_slope),
            float(maximum_intercept),
        ),
    )
