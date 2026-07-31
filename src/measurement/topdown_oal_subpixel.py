"""Subpixel grayscale-edge OAL estimator initialized by an accepted mask.

The binary mask is used only to identify the accepted object and initialize the
case geometry. Final sidewall and end-face locations are measured from the
original grayscale image by locating local intensity-gradient maxima at
subpixel resolution and robustly fitting the resulting edge points.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

from .topdown_oal import BinaryMask
from .topdown_oal_geometry import (
    FittedLineSegment,
    TopDownGeometryOALResult,
    measure_topdown_oal_geometry,
)

GrayImage = NDArray[np.uint8]
PointXY = tuple[float, float]


@dataclass(frozen=True)
class SubpixelEdgeDiagnostics:
    """Quality metrics for one sampled physical edge."""

    requested_points: int
    accepted_points: int
    accepted_fraction: float
    rms_pixels: float
    inlier_fraction: float
    mean_contrast: float
    minimum_contrast: float
    median_gradient: float
    maximum_seed_correction_pixels: float


@dataclass(frozen=True)
class TopDownSubpixelOALResult:
    """Subpixel OAL result and diagnostics for all fitted physical edges."""

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
    sidewall_min_diagnostics: SubpixelEdgeDiagnostics | None
    sidewall_max_diagnostics: SubpixelEdgeDiagnostics | None
    end_min_diagnostics: SubpixelEdgeDiagnostics | None
    end_max_diagnostics: SubpixelEdgeDiagnostics | None
    sidewall_angle_difference_degrees: float | None
    end_line_angle_difference_degrees: float | None
    end_min_perpendicular_error_degrees: float | None
    end_max_perpendicular_error_degrees: float | None
    diagnostic_flags: tuple[str, ...]
    geometry_seed_length_pixels: float | None


@dataclass(frozen=True)
class _LocalFit:
    slope: float
    intercept: float
    rms_pixels: float
    inlier_fraction: float
    point_count: int


@dataclass(frozen=True)
class _EdgeSampleSet:
    points_xy: NDArray[np.float64]
    contrasts: NDArray[np.float64]
    gradients: NDArray[np.float64]
    corrections: NDArray[np.float64]
    requested_points: int


def _as_gray(image: NDArray[np.uint8]) -> GrayImage:
    if image.ndim == 2:
        return image.astype(np.uint8, copy=False)
    if image.ndim == 3 and image.shape[2] in (3, 4):
        code = cv2.COLOR_BGRA2GRAY if image.shape[2] == 4 else cv2.COLOR_BGR2GRAY
        return cv2.cvtColor(image, code)
    raise ValueError("image must be a grayscale, BGR, or BGRA image.")


def _unit(vector: NDArray[np.float64]) -> NDArray[np.float64]:
    norm = float(np.linalg.norm(vector))
    if norm <= 1e-12:
        raise ValueError("A zero-length direction vector is invalid.")
    return vector / norm


def _segment_arrays(
    segment: FittedLineSegment,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    return (
        np.asarray(segment.start_xy, dtype=np.float64),
        np.asarray(segment.end_xy, dtype=np.float64),
    )


def _bilinear_profile(
    gray: GrayImage,
    seed_xy: NDArray[np.float64],
    normal_xy: NDArray[np.float64],
    offsets: NDArray[np.float64],
) -> NDArray[np.float64] | None:
    coordinates = seed_xy[None, :] + offsets[:, None] * normal_xy[None, :]
    x = coordinates[:, 0]
    y = coordinates[:, 1]
    if (
        float(x.min()) < 1.0
        or float(y.min()) < 1.0
        or float(x.max()) > gray.shape[1] - 2.0
        or float(y.max()) > gray.shape[0] - 2.0
    ):
        return None

    map_x = x.astype(np.float32).reshape(1, -1)
    map_y = y.astype(np.float32).reshape(1, -1)
    sampled = cv2.remap(
        gray.astype(np.float32, copy=False),
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return sampled.reshape(-1).astype(np.float64)


def _subpixel_edge_from_profile(
    gray: GrayImage,
    seed_xy: NDArray[np.float64],
    normal_xy: NDArray[np.float64],
    *,
    search_radius_pixels: float,
    profile_step_pixels: float,
    profile_sigma_pixels: float,
    minimum_contrast: float,
    minimum_gradient: float,
) -> tuple[NDArray[np.float64], float, float, float] | None:
    offsets = np.arange(
        -search_radius_pixels,
        search_radius_pixels + 0.5 * profile_step_pixels,
        profile_step_pixels,
        dtype=np.float64,
    )
    values = _bilinear_profile(gray, seed_xy, normal_xy, offsets)
    if values is None or values.size < 9:
        return None

    sigma_samples = max(profile_sigma_pixels / profile_step_pixels, 0.1)
    smoothed = cv2.GaussianBlur(
        values.reshape(1, -1),
        (0, 0),
        sigmaX=sigma_samples,
        sigmaY=0.0,
        borderType=cv2.BORDER_REPLICATE,
    ).reshape(-1)
    gradient = np.gradient(smoothed, profile_step_pixels)
    magnitude = np.abs(gradient)

    guard = max(2, int(round(0.75 / profile_step_pixels)))
    search = magnitude.copy()
    search[:guard] = -np.inf
    search[-guard:] = -np.inf
    index = int(np.argmax(search))
    peak = float(magnitude[index])

    outer_count = max(2, int(round(1.0 / profile_step_pixels)))
    contrast = float(
        abs(np.mean(smoothed[:outer_count]) - np.mean(smoothed[-outer_count:]))
    )
    if contrast < minimum_contrast or peak < minimum_gradient:
        return None

    correction_samples = 0.0
    if 0 < index < magnitude.size - 1:
        left = float(magnitude[index - 1])
        center = float(magnitude[index])
        right = float(magnitude[index + 1])
        denominator = left - 2.0 * center + right
        if abs(denominator) > 1e-12:
            correction_samples = 0.5 * (left - right) / denominator
            correction_samples = float(np.clip(correction_samples, -1.0, 1.0))

    correction = float(offsets[index] + correction_samples * profile_step_pixels)
    point = seed_xy + correction * normal_xy
    return point, contrast, peak, correction


def _sample_segment_edge(
    gray: GrayImage,
    segment: FittedLineSegment,
    search_normal_xy: NDArray[np.float64],
    *,
    sample_count: int,
    trim_fraction: float,
    search_radius_pixels: float,
    profile_step_pixels: float,
    profile_sigma_pixels: float,
    minimum_contrast: float,
    minimum_gradient: float,
) -> _EdgeSampleSet:
    start, end = _segment_arrays(segment)
    fractions = np.linspace(trim_fraction, 1.0 - trim_fraction, sample_count)
    seeds = start[None, :] + fractions[:, None] * (end - start)[None, :]

    points: list[NDArray[np.float64]] = []
    contrasts: list[float] = []
    gradients: list[float] = []
    corrections: list[float] = []
    normal = _unit(search_normal_xy.astype(np.float64))

    for seed in seeds:
        located = _subpixel_edge_from_profile(
            gray,
            seed,
            normal,
            search_radius_pixels=search_radius_pixels,
            profile_step_pixels=profile_step_pixels,
            profile_sigma_pixels=profile_sigma_pixels,
            minimum_contrast=minimum_contrast,
            minimum_gradient=minimum_gradient,
        )
        if located is None:
            continue
        point, contrast, gradient, correction = located
        points.append(point)
        contrasts.append(contrast)
        gradients.append(gradient)
        corrections.append(correction)

    point_array = (
        np.vstack(points).astype(np.float64)
        if points
        else np.empty((0, 2), dtype=np.float64)
    )
    return _EdgeSampleSet(
        points_xy=point_array,
        contrasts=np.asarray(contrasts, dtype=np.float64),
        gradients=np.asarray(gradients, dtype=np.float64),
        corrections=np.asarray(corrections, dtype=np.float64),
        requested_points=sample_count,
    )


def _sample_end_edge(
    gray: GrayImage,
    axis_point_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    seed_position: float,
    *,
    half_width_pixels: float,
    sample_count: int,
    search_radius_pixels: float,
    profile_step_pixels: float,
    profile_sigma_pixels: float,
    minimum_contrast: float,
    minimum_gradient: float,
) -> _EdgeSampleSet:
    perpendicular = np.array([-axis_xy[1], axis_xy[0]], dtype=np.float64)
    transverse = np.linspace(-half_width_pixels, half_width_pixels, sample_count)
    seeds = (
        axis_point_xy[None, :]
        + seed_position * axis_xy[None, :]
        + transverse[:, None] * perpendicular[None, :]
    )

    points: list[NDArray[np.float64]] = []
    contrasts: list[float] = []
    gradients: list[float] = []
    corrections: list[float] = []
    for seed in seeds:
        located = _subpixel_edge_from_profile(
            gray,
            seed,
            axis_xy,
            search_radius_pixels=search_radius_pixels,
            profile_step_pixels=profile_step_pixels,
            profile_sigma_pixels=profile_sigma_pixels,
            minimum_contrast=minimum_contrast,
            minimum_gradient=minimum_gradient,
        )
        if located is None:
            continue
        point, contrast, gradient, correction = located
        points.append(point)
        contrasts.append(contrast)
        gradients.append(gradient)
        corrections.append(correction)

    point_array = (
        np.vstack(points).astype(np.float64)
        if points
        else np.empty((0, 2), dtype=np.float64)
    )
    return _EdgeSampleSet(
        points_xy=point_array,
        contrasts=np.asarray(contrasts, dtype=np.float64),
        gradients=np.asarray(gradients, dtype=np.float64),
        corrections=np.asarray(corrections, dtype=np.float64),
        requested_points=sample_count,
    )


def _robust_fit(
    independent: NDArray[np.float64], dependent: NDArray[np.float64]
) -> _LocalFit:
    x = np.asarray(independent, dtype=np.float64)
    y = np.asarray(dependent, dtype=np.float64)
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise ValueError("Fit inputs must be equal-length 1-D arrays.")
    if x.size < 5:
        raise ValueError("At least five edge points are required.")

    design = np.column_stack((x, np.ones_like(x)))
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)

    for _ in range(30):
        residuals = y - design @ coefficients
        center = float(np.median(residuals))
        mad = float(np.median(np.abs(residuals - center)))
        scale = max(1.4826 * mad, 0.03)
        threshold = 1.345 * scale
        absolute = np.abs(residuals - center)
        weights = np.ones_like(absolute)
        outside = absolute > threshold
        weights[outside] = threshold / absolute[outside]
        root = np.sqrt(weights)
        updated, *_ = np.linalg.lstsq(design * root[:, None], y * root, rcond=None)
        if float(np.linalg.norm(updated - coefficients)) < 1e-11:
            coefficients = updated
            break
        coefficients = updated

    residuals = y - design @ coefficients
    center = float(np.median(residuals))
    mad = float(np.median(np.abs(residuals - center)))
    scale = max(1.4826 * mad, 0.03)
    inliers = np.abs(residuals - center) <= 2.5 * scale
    if int(np.count_nonzero(inliers)) < 3:
        inliers = np.ones_like(residuals, dtype=bool)

    return _LocalFit(
        slope=float(coefficients[0]),
        intercept=float(coefficients[1]),
        rms_pixels=float(np.sqrt(np.mean(np.square(residuals[inliers])))),
        inlier_fraction=float(np.mean(inliers)),
        point_count=int(x.size),
    )


def _fit_points_in_frame(
    points_xy: NDArray[np.float64],
    origin_xy: NDArray[np.float64],
    independent_axis_xy: NDArray[np.float64],
    dependent_axis_xy: NDArray[np.float64],
) -> tuple[_LocalFit, NDArray[np.float64], NDArray[np.float64]]:
    relative = points_xy - origin_xy
    independent = relative @ independent_axis_xy
    dependent = relative @ dependent_axis_xy
    return _robust_fit(independent, dependent), independent, dependent


def _segment_from_local_fit(
    fit: _LocalFit,
    origin_xy: NDArray[np.float64],
    independent_axis_xy: NDArray[np.float64],
    dependent_axis_xy: NDArray[np.float64],
    minimum_independent: float,
    maximum_independent: float,
) -> FittedLineSegment:
    def point(value: float) -> NDArray[np.float64]:
        return (
            origin_xy
            + value * independent_axis_xy
            + (fit.slope * value + fit.intercept) * dependent_axis_xy
        )

    start = point(minimum_independent)
    end = point(maximum_independent)
    return FittedLineSegment(
        start_xy=(float(start[0]), float(start[1])),
        end_xy=(float(end[0]), float(end[1])),
        rms_pixels=fit.rms_pixels,
        inlier_fraction=fit.inlier_fraction,
        point_count=fit.point_count,
    )


def _diagnostics(samples: _EdgeSampleSet, fit: _LocalFit) -> SubpixelEdgeDiagnostics:
    accepted = int(samples.points_xy.shape[0])
    return SubpixelEdgeDiagnostics(
        requested_points=samples.requested_points,
        accepted_points=accepted,
        accepted_fraction=accepted / max(samples.requested_points, 1),
        rms_pixels=fit.rms_pixels,
        inlier_fraction=fit.inlier_fraction,
        mean_contrast=float(np.mean(samples.contrasts)),
        minimum_contrast=float(np.min(samples.contrasts)),
        median_gradient=float(np.median(samples.gradients)),
        maximum_seed_correction_pixels=float(np.max(np.abs(samples.corrections))),
    )


def _angle_difference(first_slope: float, second_slope: float) -> float:
    return float(abs(np.degrees(np.arctan(first_slope) - np.arctan(second_slope))))


def _failed(
    reason: str,
    geometry: TopDownGeometryOALResult | None,
) -> TopDownSubpixelOALResult:
    return TopDownSubpixelOALResult(
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
        sidewall_min_diagnostics=None,
        sidewall_max_diagnostics=None,
        end_min_diagnostics=None,
        end_max_diagnostics=None,
        sidewall_angle_difference_degrees=None,
        end_line_angle_difference_degrees=None,
        end_min_perpendicular_error_degrees=None,
        end_max_perpendicular_error_degrees=None,
        diagnostic_flags=(),
        geometry_seed_length_pixels=(
            None if geometry is None else geometry.length_pixels
        ),
    )


def measure_topdown_oal_subpixel(
    image: NDArray[np.uint8],
    mask: BinaryMask,
    *,
    pixels_per_inch: float | None = None,
    minimum_fixture_width_ratio: float = 1.6,
    search_radius_pixels: float = 5.0,
    profile_step_pixels: float = 0.20,
    profile_sigma_pixels: float = 0.65,
    minimum_contrast: float = 12.0,
    minimum_gradient: float = 3.0,
    sidewall_sample_count: int = 72,
    end_sample_count: int = 41,
    minimum_edge_acceptance_fraction: float = 0.65,
    end_face_transverse_fraction: float = 0.30,
) -> TopDownSubpixelOALResult:
    """Measure OAL from subpixel grayscale edges using an accepted mask seed."""

    gray = _as_gray(image)
    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional image.")
    if gray.shape != mask.shape:
        raise ValueError("image and mask must have identical width and height.")
    if pixels_per_inch is not None and pixels_per_inch <= 0:
        raise ValueError("pixels_per_inch must be greater than zero.")
    if search_radius_pixels <= 0 or profile_step_pixels <= 0:
        raise ValueError("Search radius and profile step must be greater than zero.")
    if not 0.0 < minimum_edge_acceptance_fraction <= 1.0:
        raise ValueError("minimum_edge_acceptance_fraction must be in (0, 1].")

    geometry = measure_topdown_oal_geometry(
        mask,
        pixels_per_inch=pixels_per_inch,
        minimum_fixture_width_ratio=minimum_fixture_width_ratio,
    )
    if not geometry.passed:
        return _failed(
            f"Geometry initialization failed: {geometry.failure_reason}",
            geometry,
        )
    if (
        geometry.axis_point_xy is None
        or geometry.axis_vector_xy is None
        or geometry.endpoint_min_xy is None
        or geometry.endpoint_max_xy is None
        or geometry.sidewall_min_segment is None
        or geometry.sidewall_max_segment is None
        or geometry.case_width_pixels is None
    ):
        return _failed("Geometry initialization returned incomplete data.", geometry)

    seed_origin = np.asarray(geometry.axis_point_xy, dtype=np.float64)
    seed_axis = _unit(np.asarray(geometry.axis_vector_xy, dtype=np.float64))
    seed_perpendicular = np.array([-seed_axis[1], seed_axis[0]], dtype=np.float64)

    side_min = _sample_segment_edge(
        gray,
        geometry.sidewall_min_segment,
        seed_perpendicular,
        sample_count=sidewall_sample_count,
        trim_fraction=0.04,
        search_radius_pixels=search_radius_pixels,
        profile_step_pixels=profile_step_pixels,
        profile_sigma_pixels=profile_sigma_pixels,
        minimum_contrast=minimum_contrast,
        minimum_gradient=minimum_gradient,
    )
    side_max = _sample_segment_edge(
        gray,
        geometry.sidewall_max_segment,
        seed_perpendicular,
        sample_count=sidewall_sample_count,
        trim_fraction=0.04,
        search_radius_pixels=search_radius_pixels,
        profile_step_pixels=profile_step_pixels,
        profile_sigma_pixels=profile_sigma_pixels,
        minimum_contrast=minimum_contrast,
        minimum_gradient=minimum_gradient,
    )

    required_side = int(
        np.ceil(sidewall_sample_count * minimum_edge_acceptance_fraction)
    )
    if side_min.points_xy.shape[0] < required_side:
        return _failed(
            "Insufficient subpixel points on the minimum sidewall.", geometry
        )
    if side_max.points_xy.shape[0] < required_side:
        return _failed(
            "Insufficient subpixel points on the maximum sidewall.", geometry
        )

    try:
        side_min_fit, side_min_s, _ = _fit_points_in_frame(
            side_min.points_xy,
            seed_origin,
            seed_axis,
            seed_perpendicular,
        )
        side_max_fit, side_max_s, _ = _fit_points_in_frame(
            side_max.points_xy,
            seed_origin,
            seed_axis,
            seed_perpendicular,
        )
    except (ValueError, np.linalg.LinAlgError):
        return _failed("Subpixel sidewall fitting failed.", geometry)

    center_slope = 0.5 * (side_min_fit.slope + side_max_fit.slope)
    center_intercept = 0.5 * (side_min_fit.intercept + side_max_fit.intercept)
    refined_axis = _unit(seed_axis + center_slope * seed_perpendicular)
    refined_origin = seed_origin + center_intercept * seed_perpendicular
    refined_perpendicular = np.array(
        [-refined_axis[1], refined_axis[0]], dtype=np.float64
    )

    seed_minimum = float(
        (np.asarray(geometry.endpoint_min_xy, dtype=np.float64) - refined_origin)
        @ refined_axis
    )
    seed_maximum = float(
        (np.asarray(geometry.endpoint_max_xy, dtype=np.float64) - refined_origin)
        @ refined_axis
    )
    half_width = geometry.case_width_pixels * end_face_transverse_fraction

    end_min = _sample_end_edge(
        gray,
        refined_origin,
        refined_axis,
        seed_minimum,
        half_width_pixels=half_width,
        sample_count=end_sample_count,
        search_radius_pixels=search_radius_pixels,
        profile_step_pixels=profile_step_pixels,
        profile_sigma_pixels=profile_sigma_pixels,
        minimum_contrast=minimum_contrast,
        minimum_gradient=minimum_gradient,
    )
    end_max = _sample_end_edge(
        gray,
        refined_origin,
        refined_axis,
        seed_maximum,
        half_width_pixels=half_width,
        sample_count=end_sample_count,
        search_radius_pixels=search_radius_pixels,
        profile_step_pixels=profile_step_pixels,
        profile_sigma_pixels=profile_sigma_pixels,
        minimum_contrast=minimum_contrast,
        minimum_gradient=minimum_gradient,
    )

    required_end = int(np.ceil(end_sample_count * minimum_edge_acceptance_fraction))
    if end_min.points_xy.shape[0] < required_end:
        return _failed(
            "Insufficient subpixel points on the minimum end face.", geometry
        )
    if end_max.points_xy.shape[0] < required_end:
        return _failed(
            "Insufficient subpixel points on the maximum end face.", geometry
        )

    try:
        end_min_fit, end_min_t, _ = _fit_points_in_frame(
            end_min.points_xy,
            refined_origin,
            refined_perpendicular,
            refined_axis,
        )
        end_max_fit, end_max_t, _ = _fit_points_in_frame(
            end_max.points_xy,
            refined_origin,
            refined_perpendicular,
            refined_axis,
        )
    except (ValueError, np.linalg.LinAlgError):
        return _failed("Subpixel end-face fitting failed.", geometry)

    minimum_position = end_min_fit.intercept
    maximum_position = end_max_fit.intercept
    if maximum_position <= minimum_position:
        return _failed("The subpixel end-face ordering is invalid.", geometry)

    endpoint_min = refined_origin + minimum_position * refined_axis
    endpoint_max = refined_origin + maximum_position * refined_axis
    length_pixels = maximum_position - minimum_position
    length_inches = None if pixels_per_inch is None else length_pixels / pixels_per_inch

    sidewall_min_segment = _segment_from_local_fit(
        side_min_fit,
        seed_origin,
        seed_axis,
        seed_perpendicular,
        float(np.min(side_min_s)),
        float(np.max(side_min_s)),
    )
    sidewall_max_segment = _segment_from_local_fit(
        side_max_fit,
        seed_origin,
        seed_axis,
        seed_perpendicular,
        float(np.min(side_max_s)),
        float(np.max(side_max_s)),
    )
    end_min_segment = _segment_from_local_fit(
        end_min_fit,
        refined_origin,
        refined_perpendicular,
        refined_axis,
        float(np.min(end_min_t)),
        float(np.max(end_min_t)),
    )
    end_max_segment = _segment_from_local_fit(
        end_max_fit,
        refined_origin,
        refined_perpendicular,
        refined_axis,
        float(np.min(end_max_t)),
        float(np.max(end_max_t)),
    )
    axis_segment = FittedLineSegment(
        start_xy=(float(endpoint_min[0]), float(endpoint_min[1])),
        end_xy=(float(endpoint_max[0]), float(endpoint_max[1])),
        rms_pixels=0.0,
        inlier_fraction=1.0,
        point_count=2,
    )

    side_min_diagnostics = _diagnostics(side_min, side_min_fit)
    side_max_diagnostics = _diagnostics(side_max, side_max_fit)
    end_min_diagnostics = _diagnostics(end_min, end_min_fit)
    end_max_diagnostics = _diagnostics(end_max, end_max_fit)

    sidewall_angle_difference = _angle_difference(
        side_min_fit.slope, side_max_fit.slope
    )
    end_line_angle_difference = _angle_difference(end_min_fit.slope, end_max_fit.slope)
    end_min_perpendicular_error = float(abs(np.degrees(np.arctan(end_min_fit.slope))))
    end_max_perpendicular_error = float(abs(np.degrees(np.arctan(end_max_fit.slope))))

    flags: list[str] = []
    diagnostics_by_name = (
        ("minimum_sidewall", side_min_diagnostics),
        ("maximum_sidewall", side_max_diagnostics),
        ("minimum_end", end_min_diagnostics),
        ("maximum_end", end_max_diagnostics),
    )
    for name, diagnostic in diagnostics_by_name:
        if diagnostic.accepted_fraction < 0.80:
            flags.append(f"{name}_low_acceptance")
        if diagnostic.rms_pixels > 0.40:
            flags.append(f"{name}_high_residual")
        if diagnostic.minimum_contrast < minimum_contrast * 1.25:
            flags.append(f"{name}_low_contrast_margin")
        if diagnostic.maximum_seed_correction_pixels > search_radius_pixels * 0.80:
            flags.append(f"{name}_near_search_limit")

    if sidewall_angle_difference > 0.75:
        flags.append("subpixel_sidewalls_not_parallel")
    if end_line_angle_difference > 1.25:
        flags.append("subpixel_end_faces_not_parallel")
    if end_min_perpendicular_error > 2.0:
        flags.append("subpixel_minimum_end_not_perpendicular")
    if end_max_perpendicular_error > 2.0:
        flags.append("subpixel_maximum_end_not_perpendicular")

    return TopDownSubpixelOALResult(
        passed=True,
        failure_reason=None,
        length_pixels=float(length_pixels),
        length_inches=(None if length_inches is None else float(length_inches)),
        angle_degrees=float(np.degrees(np.arctan2(refined_axis[1], refined_axis[0]))),
        axis_point_xy=(float(refined_origin[0]), float(refined_origin[1])),
        axis_vector_xy=(float(refined_axis[0]), float(refined_axis[1])),
        endpoint_min_xy=(float(endpoint_min[0]), float(endpoint_min[1])),
        endpoint_max_xy=(float(endpoint_max[0]), float(endpoint_max[1])),
        axis_segment=axis_segment,
        sidewall_min_segment=sidewall_min_segment,
        sidewall_max_segment=sidewall_max_segment,
        end_min_segment=end_min_segment,
        end_max_segment=end_max_segment,
        sidewall_min_diagnostics=side_min_diagnostics,
        sidewall_max_diagnostics=side_max_diagnostics,
        end_min_diagnostics=end_min_diagnostics,
        end_max_diagnostics=end_max_diagnostics,
        sidewall_angle_difference_degrees=sidewall_angle_difference,
        end_line_angle_difference_degrees=end_line_angle_difference,
        end_min_perpendicular_error_degrees=end_min_perpendicular_error,
        end_max_perpendicular_error_degrees=end_max_perpendicular_error,
        diagnostic_flags=tuple(flags),
        geometry_seed_length_pixels=geometry.length_pixels,
    )
