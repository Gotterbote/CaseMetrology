"""Mask-anchored, polarity-aware subpixel top-down OAL estimator.

The accepted binary mask provides object association, coarse geometry, and a
local boundary anchor.  The original grayscale image provides the final edge
location.  Each physical edge is defined by a fixed normalized dark-object to
bright-background intensity crossing rather than by the strongest local
gradient.
"""

from __future__ import annotations

from collections import Counter
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
class IntensityCrossingProfile:
    """One mask-anchored grayscale profile and its edge-location outcome."""

    edge_name: str
    seed_xy: PointXY
    anchor_xy: PointXY | None
    outward_normal_xy: PointXY | None
    accepted: bool
    rejection_reason: str | None
    mask_anchor_offset_pixels: float | None
    mask_crossing_count: int
    interior_intensity: float | None
    exterior_intensity: float | None
    contrast: float | None
    crossing_offset_pixels: float | None
    crossing_xy: PointXY | None
    threshold_crossing_count: int
    monotonicity_fraction: float | None
    offsets_pixels: tuple[float, ...]
    normalized_values: tuple[float, ...]


@dataclass(frozen=True)
class SubpixelV2EdgeDiagnostics:
    """Aggregate profile and robust-line diagnostics for one physical edge."""

    requested_profiles: int
    accepted_profiles: int
    rejected_profiles: int
    acceptance_fraction: float
    rms_pixels: float
    inlier_fraction: float
    mean_contrast: float
    minimum_contrast: float
    median_crossing_offset_pixels: float
    maximum_absolute_crossing_offset_pixels: float
    mean_monotonicity_fraction: float
    rejection_counts: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class TopDownSubpixelV2OALResult:
    """OAL result from mask-anchored normalized grayscale crossings."""

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
    sidewall_min_diagnostics: SubpixelV2EdgeDiagnostics | None
    sidewall_max_diagnostics: SubpixelV2EdgeDiagnostics | None
    end_min_diagnostics: SubpixelV2EdgeDiagnostics | None
    end_max_diagnostics: SubpixelV2EdgeDiagnostics | None
    sidewall_min_profiles: tuple[IntensityCrossingProfile, ...]
    sidewall_max_profiles: tuple[IntensityCrossingProfile, ...]
    end_min_profiles: tuple[IntensityCrossingProfile, ...]
    end_max_profiles: tuple[IntensityCrossingProfile, ...]
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
class _ProfileSet:
    profiles: tuple[IntensityCrossingProfile, ...]
    accepted_points_xy: NDArray[np.float64]


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


def _sample_bilinear(
    image: NDArray[np.uint8] | NDArray[np.float32],
    seed_xy: NDArray[np.float64],
    direction_xy: NDArray[np.float64],
    offsets: NDArray[np.float64],
) -> NDArray[np.float64] | None:
    coordinates = seed_xy[None, :] + offsets[:, None] * direction_xy[None, :]
    x = coordinates[:, 0]
    y = coordinates[:, 1]
    if (
        float(x.min()) < 1.0
        or float(y.min()) < 1.0
        or float(x.max()) > image.shape[1] - 2.0
        or float(y.max()) > image.shape[0] - 2.0
    ):
        return None

    sampled = cv2.remap(
        image.astype(np.float32, copy=False),
        x.astype(np.float32).reshape(1, -1),
        y.astype(np.float32).reshape(1, -1),
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return sampled.reshape(-1).astype(np.float64)


def _linear_crossings(
    offsets: NDArray[np.float64],
    values: NDArray[np.float64],
    level: float,
    *,
    rising_only: bool,
) -> list[float]:
    crossings: list[float] = []
    for index in range(values.size - 1):
        left = float(values[index])
        right = float(values[index + 1])
        if not np.isfinite(left) or not np.isfinite(right) or right == left:
            continue
        if rising_only and right <= left:
            continue
        if (left - level) * (right - level) > 0.0:
            continue
        fraction = (level - left) / (right - left)
        if not 0.0 <= fraction <= 1.0:
            continue
        crossing = float(
            offsets[index] + fraction * (offsets[index + 1] - offsets[index])
        )
        if not crossings or abs(crossing - crossings[-1]) > 1e-6:
            crossings.append(crossing)
    return crossings


def _mask_anchor(
    mask: BinaryMask,
    seed_xy: NDArray[np.float64],
    candidate_normal_xy: NDArray[np.float64],
    *,
    profile_half_length_pixels: float,
    profile_step_pixels: float,
    maximum_anchor_distance_pixels: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64], float, int] | None:
    normal = _unit(candidate_normal_xy.astype(np.float64))
    offsets = np.arange(
        -profile_half_length_pixels,
        profile_half_length_pixels + 0.5 * profile_step_pixels,
        profile_step_pixels,
        dtype=np.float64,
    )
    mask_values = _sample_bilinear(
        (mask > 0).astype(np.float32),
        seed_xy,
        normal,
        offsets,
    )
    if mask_values is None:
        return None

    crossings = _linear_crossings(offsets, mask_values, 0.5, rising_only=False)
    if not crossings:
        return None
    crossing = min(crossings, key=abs)
    if abs(crossing) > maximum_anchor_distance_pixels:
        return None

    anchor = seed_xy + crossing * normal
    probe = min(0.75, profile_half_length_pixels * 0.25)
    probe_values = _sample_bilinear(
        (mask > 0).astype(np.float32),
        anchor,
        normal,
        np.asarray([-probe, probe], dtype=np.float64),
    )
    if probe_values is None or abs(float(probe_values[0] - probe_values[1])) < 0.25:
        return None

    # Positive profile direction must point from mask interior to background.
    if float(probe_values[0]) < float(probe_values[1]):
        normal = -normal

    return anchor, normal, float(crossing), len(crossings)


def _rejected_profile(
    *,
    edge_name: str,
    seed_xy: NDArray[np.float64],
    reason: str,
    anchor_xy: NDArray[np.float64] | None = None,
    normal_xy: NDArray[np.float64] | None = None,
    mask_anchor_offset: float | None = None,
    mask_crossing_count: int = 0,
    interior: float | None = None,
    exterior: float | None = None,
    contrast: float | None = None,
    crossing_count: int = 0,
    monotonicity: float | None = None,
    offsets: NDArray[np.float64] | None = None,
    normalized: NDArray[np.float64] | None = None,
) -> IntensityCrossingProfile:
    return IntensityCrossingProfile(
        edge_name=edge_name,
        seed_xy=(float(seed_xy[0]), float(seed_xy[1])),
        anchor_xy=(
            None if anchor_xy is None else (float(anchor_xy[0]), float(anchor_xy[1]))
        ),
        outward_normal_xy=(
            None if normal_xy is None else (float(normal_xy[0]), float(normal_xy[1]))
        ),
        accepted=False,
        rejection_reason=reason,
        mask_anchor_offset_pixels=mask_anchor_offset,
        mask_crossing_count=mask_crossing_count,
        interior_intensity=interior,
        exterior_intensity=exterior,
        contrast=contrast,
        crossing_offset_pixels=None,
        crossing_xy=None,
        threshold_crossing_count=crossing_count,
        monotonicity_fraction=monotonicity,
        offsets_pixels=(
            () if offsets is None else tuple(float(value) for value in offsets)
        ),
        normalized_values=(
            () if normalized is None else tuple(float(value) for value in normalized)
        ),
    )


def _locate_profile_crossing(
    gray: GrayImage,
    mask: BinaryMask,
    seed_xy: NDArray[np.float64],
    candidate_normal_xy: NDArray[np.float64],
    *,
    edge_name: str,
    profile_half_length_pixels: float,
    profile_step_pixels: float,
    interior_plateau_limit_pixels: tuple[float, float],
    exterior_plateau_limit_pixels: tuple[float, float],
    normalized_crossing: float,
    minimum_local_contrast: float,
    maximum_anchor_distance_pixels: float,
    maximum_crossing_distance_pixels: float,
) -> IntensityCrossingProfile:
    anchored = _mask_anchor(
        mask,
        seed_xy,
        candidate_normal_xy,
        profile_half_length_pixels=profile_half_length_pixels,
        profile_step_pixels=profile_step_pixels,
        maximum_anchor_distance_pixels=maximum_anchor_distance_pixels,
    )
    if anchored is None:
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason="mask_anchor_not_found",
        )

    anchor, outward_normal, anchor_offset, mask_crossing_count = anchored
    offsets = np.arange(
        -profile_half_length_pixels,
        profile_half_length_pixels + 0.5 * profile_step_pixels,
        profile_step_pixels,
        dtype=np.float64,
    )
    values = _sample_bilinear(gray, anchor, outward_normal, offsets)
    if values is None:
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason="profile_outside_image",
            anchor_xy=anchor,
            normal_xy=outward_normal,
            mask_anchor_offset=anchor_offset,
            mask_crossing_count=mask_crossing_count,
        )

    interior_selector = (offsets >= interior_plateau_limit_pixels[0]) & (
        offsets <= interior_plateau_limit_pixels[1]
    )
    exterior_selector = (offsets >= exterior_plateau_limit_pixels[0]) & (
        offsets <= exterior_plateau_limit_pixels[1]
    )
    if (
        int(np.count_nonzero(interior_selector)) < 3
        or int(np.count_nonzero(exterior_selector)) < 3
    ):
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason="insufficient_plateau_samples",
            anchor_xy=anchor,
            normal_xy=outward_normal,
            mask_anchor_offset=anchor_offset,
            mask_crossing_count=mask_crossing_count,
        )

    interior = float(np.median(values[interior_selector]))
    exterior = float(np.median(values[exterior_selector]))
    contrast = exterior - interior
    if contrast < minimum_local_contrast:
        reason = (
            "reversed_or_indeterminate_polarity" if contrast <= 0.0 else "low_contrast"
        )
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason=reason,
            anchor_xy=anchor,
            normal_xy=outward_normal,
            mask_anchor_offset=anchor_offset,
            mask_crossing_count=mask_crossing_count,
            interior=interior,
            exterior=exterior,
            contrast=contrast,
            offsets=offsets,
        )

    normalized = (values - interior) / contrast
    central = np.abs(offsets) <= maximum_crossing_distance_pixels
    central_offsets = offsets[central]
    central_values = normalized[central]
    crossings = _linear_crossings(
        central_offsets,
        central_values,
        normalized_crossing,
        rising_only=True,
    )
    differences = np.diff(central_values)
    monotonicity = float(np.mean(differences >= 0.0)) if differences.size else 0.0

    if not crossings:
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason="normalized_crossing_not_found",
            anchor_xy=anchor,
            normal_xy=outward_normal,
            mask_anchor_offset=anchor_offset,
            mask_crossing_count=mask_crossing_count,
            interior=interior,
            exterior=exterior,
            contrast=contrast,
            crossing_count=0,
            monotonicity=monotonicity,
            offsets=offsets,
            normalized=normalized,
        )
    if len(crossings) > 1:
        return _rejected_profile(
            edge_name=edge_name,
            seed_xy=seed_xy,
            reason="multiple_normalized_crossings",
            anchor_xy=anchor,
            normal_xy=outward_normal,
            mask_anchor_offset=anchor_offset,
            mask_crossing_count=mask_crossing_count,
            interior=interior,
            exterior=exterior,
            contrast=contrast,
            crossing_count=len(crossings),
            monotonicity=monotonicity,
            offsets=offsets,
            normalized=normalized,
        )

    crossing_offset = float(crossings[0])
    crossing_xy = anchor + crossing_offset * outward_normal
    return IntensityCrossingProfile(
        edge_name=edge_name,
        seed_xy=(float(seed_xy[0]), float(seed_xy[1])),
        anchor_xy=(float(anchor[0]), float(anchor[1])),
        outward_normal_xy=(float(outward_normal[0]), float(outward_normal[1])),
        accepted=True,
        rejection_reason=None,
        mask_anchor_offset_pixels=anchor_offset,
        mask_crossing_count=mask_crossing_count,
        interior_intensity=interior,
        exterior_intensity=exterior,
        contrast=contrast,
        crossing_offset_pixels=crossing_offset,
        crossing_xy=(float(crossing_xy[0]), float(crossing_xy[1])),
        threshold_crossing_count=1,
        monotonicity_fraction=monotonicity,
        offsets_pixels=tuple(float(value) for value in offsets),
        normalized_values=tuple(float(value) for value in normalized),
    )


def _sample_seed_points(
    gray: GrayImage,
    mask: BinaryMask,
    seeds: NDArray[np.float64],
    candidate_normal_xy: NDArray[np.float64],
    *,
    edge_name: str,
    profile_half_length_pixels: float,
    profile_step_pixels: float,
    interior_plateau_limit_pixels: tuple[float, float],
    exterior_plateau_limit_pixels: tuple[float, float],
    normalized_crossing: float,
    minimum_local_contrast: float,
    maximum_anchor_distance_pixels: float,
    maximum_crossing_distance_pixels: float,
) -> _ProfileSet:
    profiles = tuple(
        _locate_profile_crossing(
            gray,
            mask,
            seed,
            candidate_normal_xy,
            edge_name=edge_name,
            profile_half_length_pixels=profile_half_length_pixels,
            profile_step_pixels=profile_step_pixels,
            interior_plateau_limit_pixels=interior_plateau_limit_pixels,
            exterior_plateau_limit_pixels=exterior_plateau_limit_pixels,
            normalized_crossing=normalized_crossing,
            minimum_local_contrast=minimum_local_contrast,
            maximum_anchor_distance_pixels=maximum_anchor_distance_pixels,
            maximum_crossing_distance_pixels=maximum_crossing_distance_pixels,
        )
        for seed in seeds
    )
    accepted = [
        np.asarray(profile.crossing_xy, dtype=np.float64)
        for profile in profiles
        if profile.accepted and profile.crossing_xy is not None
    ]
    points = (
        np.vstack(accepted).astype(np.float64)
        if accepted
        else np.empty((0, 2), dtype=np.float64)
    )
    return _ProfileSet(profiles=profiles, accepted_points_xy=points)


def _sample_segment_profiles(
    gray: GrayImage,
    mask: BinaryMask,
    segment: FittedLineSegment,
    candidate_normal_xy: NDArray[np.float64],
    *,
    edge_name: str,
    sample_count: int,
    trim_fraction: float,
    **profile_kwargs: object,
) -> _ProfileSet:
    start, end = _segment_arrays(segment)
    fractions = np.linspace(trim_fraction, 1.0 - trim_fraction, sample_count)
    seeds = start[None, :] + fractions[:, None] * (end - start)[None, :]
    return _sample_seed_points(
        gray,
        mask,
        seeds,
        candidate_normal_xy,
        edge_name=edge_name,
        **profile_kwargs,
    )


def _sample_end_profiles(
    gray: GrayImage,
    mask: BinaryMask,
    axis_point_xy: NDArray[np.float64],
    axis_xy: NDArray[np.float64],
    seed_position: float,
    *,
    edge_name: str,
    half_width_pixels: float,
    sample_count: int,
    **profile_kwargs: object,
) -> _ProfileSet:
    perpendicular = np.array([-axis_xy[1], axis_xy[0]], dtype=np.float64)
    transverse = np.linspace(-half_width_pixels, half_width_pixels, sample_count)
    seeds = (
        axis_point_xy[None, :]
        + seed_position * axis_xy[None, :]
        + transverse[:, None] * perpendicular[None, :]
    )
    return _sample_seed_points(
        gray,
        mask,
        seeds,
        axis_xy,
        edge_name=edge_name,
        **profile_kwargs,
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


def _edge_diagnostics(
    profile_set: _ProfileSet, fit: _LocalFit
) -> SubpixelV2EdgeDiagnostics:
    accepted = [profile for profile in profile_set.profiles if profile.accepted]
    rejected = [profile for profile in profile_set.profiles if not profile.accepted]
    rejection_counts = Counter(
        profile.rejection_reason or "unspecified" for profile in rejected
    )
    contrasts = [
        profile.contrast for profile in accepted if profile.contrast is not None
    ]
    offsets = [
        profile.crossing_offset_pixels
        for profile in accepted
        if profile.crossing_offset_pixels is not None
    ]
    monotonicity = [
        profile.monotonicity_fraction
        for profile in accepted
        if profile.monotonicity_fraction is not None
    ]
    return SubpixelV2EdgeDiagnostics(
        requested_profiles=len(profile_set.profiles),
        accepted_profiles=len(accepted),
        rejected_profiles=len(rejected),
        acceptance_fraction=len(accepted) / max(len(profile_set.profiles), 1),
        rms_pixels=fit.rms_pixels,
        inlier_fraction=fit.inlier_fraction,
        mean_contrast=float(np.mean(contrasts)),
        minimum_contrast=float(np.min(contrasts)),
        median_crossing_offset_pixels=float(np.median(offsets)),
        maximum_absolute_crossing_offset_pixels=float(np.max(np.abs(offsets))),
        mean_monotonicity_fraction=float(np.mean(monotonicity)),
        rejection_counts=tuple(sorted(rejection_counts.items())),
    )


def _angle_difference(first_slope: float, second_slope: float) -> float:
    return float(abs(np.degrees(np.arctan(first_slope) - np.arctan(second_slope))))


def _failed(
    reason: str,
    geometry: TopDownGeometryOALResult | None,
    *,
    sidewall_min_profiles: tuple[IntensityCrossingProfile, ...] = (),
    sidewall_max_profiles: tuple[IntensityCrossingProfile, ...] = (),
    end_min_profiles: tuple[IntensityCrossingProfile, ...] = (),
    end_max_profiles: tuple[IntensityCrossingProfile, ...] = (),
) -> TopDownSubpixelV2OALResult:
    return TopDownSubpixelV2OALResult(
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
        sidewall_min_profiles=sidewall_min_profiles,
        sidewall_max_profiles=sidewall_max_profiles,
        end_min_profiles=end_min_profiles,
        end_max_profiles=end_max_profiles,
        sidewall_angle_difference_degrees=None,
        end_line_angle_difference_degrees=None,
        end_min_perpendicular_error_degrees=None,
        end_max_perpendicular_error_degrees=None,
        diagnostic_flags=(),
        geometry_seed_length_pixels=(
            None if geometry is None else geometry.length_pixels
        ),
    )


def measure_topdown_oal_subpixel_v2(
    image: NDArray[np.uint8],
    mask: BinaryMask,
    *,
    pixels_per_inch: float | None = None,
    minimum_fixture_width_ratio: float = 1.6,
    profile_half_length_pixels: float = 6.0,
    profile_step_pixels: float = 0.25,
    interior_plateau_limit_pixels: tuple[float, float] = (-6.0, -2.0),
    exterior_plateau_limit_pixels: tuple[float, float] = (2.0, 6.0),
    normalized_crossing: float = 0.50,
    minimum_local_contrast: float = 30.0,
    maximum_anchor_distance_pixels: float = 3.0,
    maximum_crossing_distance_pixels: float = 3.0,
    sidewall_sample_count: int = 72,
    end_sample_count: int = 41,
    minimum_sidewall_profile_count: int = 25,
    minimum_end_profile_count: int = 12,
    end_face_transverse_fraction: float = 0.30,
) -> TopDownSubpixelV2OALResult:
    """Measure OAL from fixed normalized grayscale intensity crossings."""

    gray = _as_gray(image)
    if mask.ndim != 2:
        raise ValueError("mask must be a two-dimensional image.")
    if gray.shape != mask.shape:
        raise ValueError("image and mask must have identical width and height.")
    if pixels_per_inch is not None and pixels_per_inch <= 0:
        raise ValueError("pixels_per_inch must be greater than zero.")
    if profile_half_length_pixels <= 0 or profile_step_pixels <= 0:
        raise ValueError("Profile half-length and step must be greater than zero.")
    if not 0.0 < normalized_crossing < 1.0:
        raise ValueError("normalized_crossing must be in (0, 1).")
    if minimum_local_contrast <= 0:
        raise ValueError("minimum_local_contrast must be greater than zero.")
    if maximum_anchor_distance_pixels <= 0 or maximum_crossing_distance_pixels <= 0:
        raise ValueError("Maximum profile distances must be greater than zero.")
    if minimum_sidewall_profile_count < 5 or minimum_end_profile_count < 5:
        raise ValueError("Minimum profile counts must each be at least five.")

    geometry = measure_topdown_oal_geometry(
        mask,
        pixels_per_inch=pixels_per_inch,
        minimum_fixture_width_ratio=minimum_fixture_width_ratio,
    )
    if not geometry.passed:
        return _failed(
            f"Geometry initialization failed: {geometry.failure_reason}", geometry
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

    profile_kwargs: dict[str, object] = {
        "profile_half_length_pixels": profile_half_length_pixels,
        "profile_step_pixels": profile_step_pixels,
        "interior_plateau_limit_pixels": interior_plateau_limit_pixels,
        "exterior_plateau_limit_pixels": exterior_plateau_limit_pixels,
        "normalized_crossing": normalized_crossing,
        "minimum_local_contrast": minimum_local_contrast,
        "maximum_anchor_distance_pixels": maximum_anchor_distance_pixels,
        "maximum_crossing_distance_pixels": maximum_crossing_distance_pixels,
    }

    seed_origin = np.asarray(geometry.axis_point_xy, dtype=np.float64)
    seed_axis = _unit(np.asarray(geometry.axis_vector_xy, dtype=np.float64))
    seed_perpendicular = np.array([-seed_axis[1], seed_axis[0]], dtype=np.float64)

    side_min = _sample_segment_profiles(
        gray,
        mask,
        geometry.sidewall_min_segment,
        seed_perpendicular,
        edge_name="minimum_sidewall",
        sample_count=sidewall_sample_count,
        trim_fraction=0.04,
        **profile_kwargs,
    )
    side_max = _sample_segment_profiles(
        gray,
        mask,
        geometry.sidewall_max_segment,
        seed_perpendicular,
        edge_name="maximum_sidewall",
        sample_count=sidewall_sample_count,
        trim_fraction=0.04,
        **profile_kwargs,
    )
    if side_min.accepted_points_xy.shape[0] < minimum_sidewall_profile_count:
        return _failed(
            "Insufficient accepted profiles on the minimum sidewall.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
        )
    if side_max.accepted_points_xy.shape[0] < minimum_sidewall_profile_count:
        return _failed(
            "Insufficient accepted profiles on the maximum sidewall.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
        )

    try:
        side_min_fit, side_min_s, _ = _fit_points_in_frame(
            side_min.accepted_points_xy,
            seed_origin,
            seed_axis,
            seed_perpendicular,
        )
        side_max_fit, side_max_s, _ = _fit_points_in_frame(
            side_max.accepted_points_xy,
            seed_origin,
            seed_axis,
            seed_perpendicular,
        )
    except (ValueError, np.linalg.LinAlgError):
        return _failed(
            "Version 2 sidewall fitting failed.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
        )

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

    end_min = _sample_end_profiles(
        gray,
        mask,
        refined_origin,
        refined_axis,
        seed_minimum,
        edge_name="minimum_end",
        half_width_pixels=half_width,
        sample_count=end_sample_count,
        **profile_kwargs,
    )
    end_max = _sample_end_profiles(
        gray,
        mask,
        refined_origin,
        refined_axis,
        seed_maximum,
        edge_name="maximum_end",
        half_width_pixels=half_width,
        sample_count=end_sample_count,
        **profile_kwargs,
    )
    if end_min.accepted_points_xy.shape[0] < minimum_end_profile_count:
        return _failed(
            "Insufficient accepted profiles on the minimum end face.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
            end_min_profiles=end_min.profiles,
            end_max_profiles=end_max.profiles,
        )
    if end_max.accepted_points_xy.shape[0] < minimum_end_profile_count:
        return _failed(
            "Insufficient accepted profiles on the maximum end face.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
            end_min_profiles=end_min.profiles,
            end_max_profiles=end_max.profiles,
        )

    try:
        end_min_fit, end_min_t, _ = _fit_points_in_frame(
            end_min.accepted_points_xy,
            refined_origin,
            refined_perpendicular,
            refined_axis,
        )
        end_max_fit, end_max_t, _ = _fit_points_in_frame(
            end_max.accepted_points_xy,
            refined_origin,
            refined_perpendicular,
            refined_axis,
        )
    except (ValueError, np.linalg.LinAlgError):
        return _failed(
            "Version 2 end-face fitting failed.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
            end_min_profiles=end_min.profiles,
            end_max_profiles=end_max.profiles,
        )

    minimum_position = end_min_fit.intercept
    maximum_position = end_max_fit.intercept
    if maximum_position <= minimum_position:
        return _failed(
            "The Version 2 end-face ordering is invalid.",
            geometry,
            sidewall_min_profiles=side_min.profiles,
            sidewall_max_profiles=side_max.profiles,
            end_min_profiles=end_min.profiles,
            end_max_profiles=end_max.profiles,
        )

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

    side_min_diagnostics = _edge_diagnostics(side_min, side_min_fit)
    side_max_diagnostics = _edge_diagnostics(side_max, side_max_fit)
    end_min_diagnostics = _edge_diagnostics(end_min, end_min_fit)
    end_max_diagnostics = _edge_diagnostics(end_max, end_max_fit)

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
        if diagnostic.acceptance_fraction < 0.65:
            flags.append(f"{name}_high_rejected_profile_fraction")
        if diagnostic.rms_pixels > 0.75:
            flags.append(f"{name}_high_residual")
        rejection_map = dict(diagnostic.rejection_counts)
        if (
            rejection_map.get("multiple_normalized_crossings", 0)
            / max(diagnostic.requested_profiles, 1)
            > 0.10
        ):
            flags.append(f"{name}_multiple_transition_prevalence")
        if (
            rejection_map.get("low_contrast", 0) / max(diagnostic.requested_profiles, 1)
            > 0.25
        ):
            flags.append(f"{name}_low_contrast_prevalence")

    if sidewall_angle_difference > 1.0:
        flags.append("version_2_sidewalls_not_parallel")
    if end_line_angle_difference > 2.0:
        flags.append("version_2_end_faces_not_parallel")
    if end_min_perpendicular_error > 2.5:
        flags.append("version_2_minimum_end_not_perpendicular")
    if end_max_perpendicular_error > 2.5:
        flags.append("version_2_maximum_end_not_perpendicular")

    return TopDownSubpixelV2OALResult(
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
        sidewall_min_profiles=side_min.profiles,
        sidewall_max_profiles=side_max.profiles,
        end_min_profiles=end_min.profiles,
        end_max_profiles=end_max.profiles,
        sidewall_angle_difference_degrees=sidewall_angle_difference,
        end_line_angle_difference_degrees=end_line_angle_difference,
        end_min_perpendicular_error_degrees=end_min_perpendicular_error,
        end_max_perpendicular_error_degrees=end_max_perpendicular_error,
        diagnostic_flags=tuple(flags),
        geometry_seed_length_pixels=geometry.length_pixels,
    )
