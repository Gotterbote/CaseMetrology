"""Geometry-based top-down OAL measurement for a merged case/fixture mask.

The existing PCA estimator is intentionally left unchanged.  PCA is used here
only to initialize a local coordinate frame.  Final OAL is the axial distance
between two robustly fitted physical end-face lines, using the center axis
obtained from robust fits of the two straight case sidewalls.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .topdown_oal import (
    BinaryMask,
    _largest_component,
    _pca_axis,
    _points_xy,
    _touches_border,
    _width_profile,
)

PointXY = tuple[float, float]


@dataclass(frozen=True)
class FittedLineSegment:
    """Image-space segment plus robust-fit quality diagnostics."""

    start_xy: PointXY
    end_xy: PointXY
    rms_pixels: float
    inlier_fraction: float
    point_count: int


@dataclass(frozen=True)
class TopDownGeometryOALResult:
    passed: bool
    failure_reason: str | None
    length_pixels: float | None
    length_inches: float | None
    angle_degrees: float | None
    axis_point_xy: PointXY | None
    axis_vector_xy: PointXY | None
    endpoint_min_xy: PointXY | None
    endpoint_max_xy: PointXY | None
    axis_segment: FittedLineSegment | None
    sidewall_min_segment: FittedLineSegment | None
    sidewall_max_segment: FittedLineSegment | None
    end_min_segment: FittedLineSegment | None
    end_max_segment: FittedLineSegment | None
    case_width_pixels: float | None
    fixture_width_pixels: float | None
    fixture_width_ratio: float | None
    sidewall_angle_difference_degrees: float | None
    end_line_angle_difference_degrees: float | None
    end_min_perpendicular_error_degrees: float | None
    end_max_perpendicular_error_degrees: float | None
    diagnostic_flags: tuple[str, ...]
    largest_component_pixels: int
    second_component_pixels: int


@dataclass(frozen=True)
class _RobustLine:
    slope: float
    intercept: float
    rms_pixels: float
    inlier_fraction: float
    point_count: int


def _robust_linear_fit(
    independent: NDArray[np.float64],
    dependent: NDArray[np.float64],
    *,
    maximum_iterations: int = 30,
    huber_tuning: float = 1.345,
) -> _RobustLine:
    """Fit y = slope*x + intercept using deterministic Huber IRLS."""

    x = np.asarray(independent, dtype=np.float64)
    y = np.asarray(dependent, dtype=np.float64)

    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("Line-fit inputs must be equal-length 1-D arrays.")
    if x.size < 3:
        raise ValueError("At least three points are required for a line fit.")

    design = np.column_stack((x, np.ones_like(x)))
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)

    for _ in range(maximum_iterations):
        residuals = y - design @ coefficients
        center = float(np.median(residuals))
        mad = float(np.median(np.abs(residuals - center)))
        scale = max(1.4826 * mad, 0.25)
        threshold = huber_tuning * scale

        absolute = np.abs(residuals - center)
        weights = np.ones_like(absolute)
        outliers = absolute > threshold
        weights[outliers] = threshold / absolute[outliers]

        root_weights = np.sqrt(weights)
        weighted_design = design * root_weights[:, None]
        weighted_y = y * root_weights
        updated, *_ = np.linalg.lstsq(
            weighted_design,
            weighted_y,
            rcond=None,
        )

        if np.linalg.norm(updated - coefficients) < 1e-10:
            coefficients = updated
            break
        coefficients = updated

    residuals = y - design @ coefficients
    center = float(np.median(residuals))
    mad = float(np.median(np.abs(residuals - center)))
    scale = max(1.4826 * mad, 0.25)
    inliers = np.abs(residuals - center) <= (2.5 * scale)
    if not np.any(inliers):
        inliers = np.ones_like(residuals, dtype=bool)

    return _RobustLine(
        slope=float(coefficients[0]),
        intercept=float(coefficients[1]),
        rms_pixels=float(np.sqrt(np.mean(np.square(residuals[inliers])))),
        inlier_fraction=float(np.mean(inliers)),
        point_count=int(x.size),
    )


def _profile_extremes(
    points_xy: NDArray[np.float64],
    origin_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
]:
    """Return transverse minimum/maximum for one-pixel axial bins."""

    perpendicular = np.array([-axis_xy[1], axis_xy[0]], dtype=np.float64)
    relative = points_xy - origin_xy
    longitudinal = relative @ axis_xy
    transverse = relative @ perpendicular

    start = float(longitudinal.min())
    bins = np.floor(longitudinal - start).astype(np.int64)
    count = int(bins.max()) + 1
    minimum = np.full(count, np.inf, dtype=np.float64)
    maximum = np.full(count, -np.inf, dtype=np.float64)
    np.minimum.at(minimum, bins, transverse)
    np.maximum.at(maximum, bins, transverse)

    centers = start + np.arange(count, dtype=np.float64) + 0.5
    widths = maximum - minimum
    valid = np.isfinite(widths)
    return centers[valid], minimum[valid], maximum[valid], widths[valid]


def _end_profiles(
    points_xy: NDArray[np.float64],
    axis_point_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    *,
    transverse_half_width: float,
) -> tuple[
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.float64],
]:
    """Return axial minimum/maximum for central transverse bins."""

    perpendicular = np.array([-axis_xy[1], axis_xy[0]], dtype=np.float64)
    relative = points_xy - axis_point_xy
    longitudinal = relative @ axis_xy
    transverse = relative @ perpendicular

    selected = np.abs(transverse) <= transverse_half_width
    longitudinal = longitudinal[selected]
    transverse = transverse[selected]
    if longitudinal.size < 20:
        raise ValueError("Insufficient central pixels for end-face fitting.")

    start = float(transverse.min())
    bins = np.floor(transverse - start).astype(np.int64)
    count = int(bins.max()) + 1
    minimum = np.full(count, np.inf, dtype=np.float64)
    maximum = np.full(count, -np.inf, dtype=np.float64)
    np.minimum.at(minimum, bins, longitudinal)
    np.maximum.at(maximum, bins, longitudinal)

    centers = start + np.arange(count, dtype=np.float64) + 0.5
    valid = np.isfinite(minimum) & np.isfinite(maximum)
    return centers[valid], minimum[valid], maximum[valid]


def _point_from_local(
    origin_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    longitudinal: float,
    transverse: float,
) -> NDArray[np.float64]:
    perpendicular = np.array([-axis_xy[1], axis_xy[0]], dtype=np.float64)
    return origin_xy + longitudinal * axis_xy + transverse * perpendicular


def _segment_for_t_of_s(
    fit: _RobustLine,
    origin_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    minimum_s: float,
    maximum_s: float,
) -> FittedLineSegment:
    start = _point_from_local(
        origin_xy,
        axis_xy,
        minimum_s,
        fit.slope * minimum_s + fit.intercept,
    )
    end = _point_from_local(
        origin_xy,
        axis_xy,
        maximum_s,
        fit.slope * maximum_s + fit.intercept,
    )
    return FittedLineSegment(
        start_xy=(float(start[0]), float(start[1])),
        end_xy=(float(end[0]), float(end[1])),
        rms_pixels=fit.rms_pixels,
        inlier_fraction=fit.inlier_fraction,
        point_count=fit.point_count,
    )


def _segment_for_s_of_t(
    fit: _RobustLine,
    origin_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    minimum_t: float,
    maximum_t: float,
) -> FittedLineSegment:
    start = _point_from_local(
        origin_xy,
        axis_xy,
        fit.slope * minimum_t + fit.intercept,
        minimum_t,
    )
    end = _point_from_local(
        origin_xy,
        axis_xy,
        fit.slope * maximum_t + fit.intercept,
        maximum_t,
    )
    return FittedLineSegment(
        start_xy=(float(start[0]), float(start[1])),
        end_xy=(float(end[0]), float(end[1])),
        rms_pixels=fit.rms_pixels,
        inlier_fraction=fit.inlier_fraction,
        point_count=fit.point_count,
    )


def _slope_angle_difference(first: float, second: float) -> float:
    return float(abs(np.degrees(np.arctan(first) - np.arctan(second))))


def measure_topdown_oal_geometry(
    mask: BinaryMask,
    *,
    pixels_per_inch: float | None = None,
    border_margin_pixels: int = 5,
    minimum_component_pixels: int = 1000,
    maximum_second_component_fraction: float = 0.02,
    minimum_axis_ratio: float = 2.0,
    minimum_fixture_width_ratio: float = 1.6,
    sidewall_minimum_width_fraction: float = 0.70,
    sidewall_maximum_width_fraction: float = 1.35,
    end_face_transverse_fraction: float = 0.35,
) -> TopDownGeometryOALResult:
    """Measure OAL from fitted sidewalls and fitted physical end faces."""

    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional image.")
    if pixels_per_inch is not None and pixels_per_inch <= 0:
        raise ValueError("pixels_per_inch must be greater than zero.")

    component, largest_area, second_area = _largest_component(mask)

    def failed(reason: str) -> TopDownGeometryOALResult:
        return TopDownGeometryOALResult(
            passed=False,
            failure_reason=reason,
            length_pixels=None,
            length_inches=None,
            angle_degrees=None,
            axis_point_xy=None,
            axis_vector_xy=None,
            endpoint_min_xy=None,
            endpoint_max_xy=None,
            axis_segment=None,
            sidewall_min_segment=None,
            sidewall_max_segment=None,
            end_min_segment=None,
            end_max_segment=None,
            case_width_pixels=None,
            fixture_width_pixels=None,
            fixture_width_ratio=None,
            sidewall_angle_difference_degrees=None,
            end_line_angle_difference_degrees=None,
            end_min_perpendicular_error_degrees=None,
            end_max_perpendicular_error_degrees=None,
            diagnostic_flags=(),
            largest_component_pixels=largest_area,
            second_component_pixels=second_area,
        )

    if largest_area < minimum_component_pixels:
        return failed("No sufficiently large assembly was detected.")
    if second_area > largest_area * maximum_second_component_fraction:
        return failed("A second significant object was detected.")
    if _touches_border(component, border_margin_pixels):
        return failed("The assembly touches the image border.")

    points = _points_xy(component)
    centroid, initial_axis, axis_ratio = _pca_axis(points)
    if axis_ratio < minimum_axis_ratio:
        return failed("The detected silhouette is not sufficiently elongated.")

    widths, point_bins = _width_profile(points, centroid, initial_axis)
    valid_widths = widths[np.isfinite(widths)]
    if valid_widths.size < 10:
        return failed("Insufficient silhouette width-profile data.")

    case_width = float(np.percentile(valid_widths, 25))
    fixture_width = float(np.percentile(valid_widths, 95))
    fixture_ratio = fixture_width / max(case_width, 1e-12)
    if fixture_ratio < minimum_fixture_width_ratio:
        return failed("The expected wider fixture region was not detected.")

    case_like_bins = widths <= case_width * sidewall_maximum_width_fraction
    exposed_case_points = points[case_like_bins[point_bins]]
    if exposed_case_points.shape[0] < 100:
        return failed("Insufficient exposed case pixels were detected.")

    refined_centroid, refined_axis, _ = _pca_axis(exposed_case_points)
    centers, lower, upper, refined_widths = _profile_extremes(
        points,
        refined_centroid,
        refined_axis,
    )

    wall_bins = (refined_widths >= case_width * sidewall_minimum_width_fraction) & (
        refined_widths <= case_width * sidewall_maximum_width_fraction
    )
    wall_s = centers[wall_bins]
    wall_lower = lower[wall_bins]
    wall_upper = upper[wall_bins]
    if wall_s.size < 20:
        return failed("Insufficient straight-sidewall profile data.")

    low_limit, high_limit = np.quantile(wall_s, [0.05, 0.95])
    central = (wall_s >= low_limit) & (wall_s <= high_limit)

    try:
        lower_fit = _robust_linear_fit(wall_s[central], wall_lower[central])
        upper_fit = _robust_linear_fit(wall_s[central], wall_upper[central])
    except (ValueError, np.linalg.LinAlgError):
        return failed("The straight sidewalls could not be fitted.")

    center_slope = 0.5 * (lower_fit.slope + upper_fit.slope)
    center_intercept = 0.5 * (lower_fit.intercept + upper_fit.intercept)
    initial_perpendicular = np.array(
        [-refined_axis[1], refined_axis[0]],
        dtype=np.float64,
    )
    axis_vector = refined_axis + center_slope * initial_perpendicular
    axis_vector /= np.linalg.norm(axis_vector)
    axis_point = refined_centroid + center_intercept * initial_perpendicular

    try:
        end_t, end_minimum, end_maximum = _end_profiles(
            points,
            axis_point,
            axis_vector,
            transverse_half_width=case_width * end_face_transverse_fraction,
        )
        minimum_end_fit = _robust_linear_fit(end_t, end_minimum)
        maximum_end_fit = _robust_linear_fit(end_t, end_maximum)
    except (ValueError, np.linalg.LinAlgError):
        return failed("The physical end faces could not be fitted.")

    minimum_position = minimum_end_fit.intercept
    maximum_position = maximum_end_fit.intercept
    if maximum_position <= minimum_position:
        return failed("The fitted end-face ordering is invalid.")

    endpoint_minimum = axis_point + minimum_position * axis_vector
    endpoint_maximum = axis_point + maximum_position * axis_vector
    length_pixels = maximum_position - minimum_position
    length_inches = None if pixels_per_inch is None else length_pixels / pixels_per_inch

    sidewall_angle_difference = _slope_angle_difference(
        lower_fit.slope,
        upper_fit.slope,
    )
    end_line_angle_difference = _slope_angle_difference(
        minimum_end_fit.slope,
        maximum_end_fit.slope,
    )
    minimum_end_perpendicular_error = float(
        abs(np.degrees(np.arctan(minimum_end_fit.slope)))
    )
    maximum_end_perpendicular_error = float(
        abs(np.degrees(np.arctan(maximum_end_fit.slope)))
    )

    flags: list[str] = []
    if sidewall_angle_difference > 2.0:
        flags.append("sidewalls_not_parallel")
    if end_line_angle_difference > 3.0:
        flags.append("end_faces_not_parallel")
    if minimum_end_perpendicular_error > 5.0:
        flags.append("minimum_end_not_perpendicular")
    if maximum_end_perpendicular_error > 5.0:
        flags.append("maximum_end_not_perpendicular")
    if lower_fit.rms_pixels > 1.5:
        flags.append("minimum_sidewall_high_residual")
    if upper_fit.rms_pixels > 1.5:
        flags.append("maximum_sidewall_high_residual")
    if minimum_end_fit.rms_pixels > 1.5:
        flags.append("minimum_end_high_residual")
    if maximum_end_fit.rms_pixels > 1.5:
        flags.append("maximum_end_high_residual")

    wall_minimum_s = float(wall_s[central].min())
    wall_maximum_s = float(wall_s[central].max())
    minimum_t = float(end_t.min())
    maximum_t = float(end_t.max())

    lower_segment = _segment_for_t_of_s(
        lower_fit,
        refined_centroid,
        refined_axis,
        wall_minimum_s,
        wall_maximum_s,
    )
    upper_segment = _segment_for_t_of_s(
        upper_fit,
        refined_centroid,
        refined_axis,
        wall_minimum_s,
        wall_maximum_s,
    )
    minimum_end_segment = _segment_for_s_of_t(
        minimum_end_fit,
        axis_point,
        axis_vector,
        minimum_t,
        maximum_t,
    )
    maximum_end_segment = _segment_for_s_of_t(
        maximum_end_fit,
        axis_point,
        axis_vector,
        minimum_t,
        maximum_t,
    )
    axis_segment = FittedLineSegment(
        start_xy=(float(endpoint_minimum[0]), float(endpoint_minimum[1])),
        end_xy=(float(endpoint_maximum[0]), float(endpoint_maximum[1])),
        rms_pixels=0.0,
        inlier_fraction=1.0,
        point_count=2,
    )

    return TopDownGeometryOALResult(
        passed=True,
        failure_reason=None,
        length_pixels=float(length_pixels),
        length_inches=(None if length_inches is None else float(length_inches)),
        angle_degrees=float(np.degrees(np.arctan2(axis_vector[1], axis_vector[0]))),
        axis_point_xy=(float(axis_point[0]), float(axis_point[1])),
        axis_vector_xy=(float(axis_vector[0]), float(axis_vector[1])),
        endpoint_min_xy=(
            float(endpoint_minimum[0]),
            float(endpoint_minimum[1]),
        ),
        endpoint_max_xy=(
            float(endpoint_maximum[0]),
            float(endpoint_maximum[1]),
        ),
        axis_segment=axis_segment,
        sidewall_min_segment=lower_segment,
        sidewall_max_segment=upper_segment,
        end_min_segment=minimum_end_segment,
        end_max_segment=maximum_end_segment,
        case_width_pixels=case_width,
        fixture_width_pixels=fixture_width,
        fixture_width_ratio=float(fixture_ratio),
        sidewall_angle_difference_degrees=sidewall_angle_difference,
        end_line_angle_difference_degrees=end_line_angle_difference,
        end_min_perpendicular_error_degrees=minimum_end_perpendicular_error,
        end_max_perpendicular_error_degrees=maximum_end_perpendicular_error,
        diagnostic_flags=tuple(flags),
        largest_component_pixels=largest_area,
        second_component_pixels=second_area,
    )
