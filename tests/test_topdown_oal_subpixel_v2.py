from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.measurement.topdown_oal import measure_topdown_oal
from src.measurement.topdown_oal_subpixel_v2 import (
    _linear_crossings,
    _locate_profile_crossing,
    measure_topdown_oal_subpixel_v2,
)


def _scene(
    *,
    angle_degrees: float,
    center_xy: tuple[float, float] = (450.0, 450.0),
    length_pixels: float = 520.0,
    width_pixels: float = 100.0,
    object_level: int = 35,
    background_level: int = 225,
    scale: int = 4,
) -> tuple[np.ndarray, np.ndarray]:
    size = 900
    high_size = size * scale
    image = np.full((high_size, high_size), background_level, dtype=np.uint8)
    rectangle = (
        (center_xy[0] * scale, center_xy[1] * scale),
        (length_pixels * scale, width_pixels * scale),
        angle_degrees,
    )
    corners = cv2.boxPoints(rectangle).astype(np.int32)
    cv2.fillConvexPoly(image, corners, object_level, lineType=cv2.LINE_AA)
    image = cv2.GaussianBlur(image, (0, 0), sigmaX=2.0, sigmaY=2.0)
    image = cv2.resize(image, (size, size), interpolation=cv2.INTER_AREA)
    mask = np.where(image < (object_level + background_level) / 2, 255, 0).astype(
        np.uint8
    )
    return image, mask


@pytest.mark.parametrize("angle", [0.0, 20.0, 40.0, 70.0, 90.0])
def test_version_2_oal_is_orientation_invariant(angle: float) -> None:
    image, mask = _scene(angle_degrees=angle)
    result = measure_topdown_oal_subpixel_v2(
        image, mask, minimum_fixture_width_ratio=0.0
    )
    assert result.passed, result.failure_reason
    assert result.length_pixels == pytest.approx(520.0, abs=0.55)


def test_version_2_has_small_orientation_range() -> None:
    lengths: list[float] = []
    for angle in (0.0, 20.0, 40.0, 70.0, 90.0):
        image, mask = _scene(angle_degrees=angle)
        result = measure_topdown_oal_subpixel_v2(
            image, mask, minimum_fixture_width_ratio=0.0
        )
        assert result.passed, result.failure_reason
        assert result.length_pixels is not None
        lengths.append(result.length_pixels)
    assert max(lengths) - min(lengths) < 0.40


def test_version_2_is_stable_under_fractional_translation() -> None:
    lengths: list[float] = []
    for shift in (0.0, 0.2, 0.4, 0.6, 0.8):
        image, mask = _scene(
            angle_degrees=40.0,
            center_xy=(450.0 + shift, 450.0 - 0.5 * shift),
        )
        result = measure_topdown_oal_subpixel_v2(
            image, mask, minimum_fixture_width_ratio=0.0
        )
        assert result.passed, result.failure_reason
        assert result.length_pixels is not None
        lengths.append(result.length_pixels)
    assert float(np.std(lengths, ddof=1)) < 0.12


def test_version_2_rejects_low_contrast_profiles() -> None:
    image, mask = _scene(angle_degrees=20.0, object_level=118, background_level=138)
    result = measure_topdown_oal_subpixel_v2(
        image, mask, minimum_fixture_width_ratio=0.0
    )
    assert not result.passed
    assert result.failure_reason is not None
    assert "profiles" in result.failure_reason.lower()


def test_profile_locator_rejects_reversed_grayscale_polarity() -> None:
    image = np.full((101, 101), 25, dtype=np.uint8)
    image[:, :50] = 225
    mask = np.zeros((101, 101), dtype=np.uint8)
    mask[:, :50] = 255
    profile = _locate_profile_crossing(
        image,
        mask,
        np.asarray([49.5, 50.0]),
        np.asarray([1.0, 0.0]),
        edge_name="test",
        profile_half_length_pixels=6.0,
        profile_step_pixels=0.25,
        interior_plateau_limit_pixels=(-6.0, -2.0),
        exterior_plateau_limit_pixels=(2.0, 6.0),
        normalized_crossing=0.5,
        minimum_local_contrast=30.0,
        maximum_anchor_distance_pixels=3.0,
        maximum_crossing_distance_pixels=3.0,
    )
    assert not profile.accepted
    assert profile.rejection_reason == "reversed_or_indeterminate_polarity"


def test_linear_crossing_interpolates_subpixel_location() -> None:
    offsets = np.asarray([-1.0, 0.0, 1.0], dtype=np.float64)
    values = np.asarray([0.0, 0.2, 1.0], dtype=np.float64)
    crossings = _linear_crossings(offsets, values, 0.5, rising_only=True)
    assert crossings == pytest.approx([0.375])


def test_profile_locator_rejects_multiple_normalized_crossings() -> None:
    image = np.full((101, 101), 220, dtype=np.uint8)
    image[:, :48] = 30
    image[:, 49:51] = 210
    image[:, 51:53] = 40
    image[:, 54:] = 220
    mask = np.zeros((101, 101), dtype=np.uint8)
    mask[:, :51] = 255
    profile = _locate_profile_crossing(
        image,
        mask,
        np.asarray([50.5, 50.0]),
        np.asarray([1.0, 0.0]),
        edge_name="test",
        profile_half_length_pixels=6.0,
        profile_step_pixels=0.25,
        interior_plateau_limit_pixels=(-6.0, -2.0),
        exterior_plateau_limit_pixels=(2.0, 6.0),
        normalized_crossing=0.5,
        minimum_local_contrast=30.0,
        maximum_anchor_distance_pixels=3.0,
        maximum_crossing_distance_pixels=3.0,
    )
    assert not profile.accepted
    assert profile.rejection_reason == "multiple_normalized_crossings"


def test_profile_locator_rejects_distant_mask_boundary() -> None:
    image = np.full((101, 101), 225, dtype=np.uint8)
    image[:, :40] = 30
    mask = np.zeros((101, 101), dtype=np.uint8)
    mask[:, :40] = 255
    profile = _locate_profile_crossing(
        image,
        mask,
        np.asarray([49.0, 50.0]),
        np.asarray([1.0, 0.0]),
        edge_name="test",
        profile_half_length_pixels=12.0,
        profile_step_pixels=0.25,
        interior_plateau_limit_pixels=(-6.0, -2.0),
        exterior_plateau_limit_pixels=(2.0, 6.0),
        normalized_crossing=0.5,
        minimum_local_contrast=30.0,
        maximum_anchor_distance_pixels=3.0,
        maximum_crossing_distance_pixels=3.0,
    )
    assert not profile.accepted
    assert profile.rejection_reason == "mask_anchor_not_found"


def test_version_2_recovers_from_binary_endpoint_spur() -> None:
    image, mask = _scene(angle_degrees=0.0)
    clean = measure_topdown_oal_subpixel_v2(
        image, mask, minimum_fixture_width_ratio=0.0
    )
    assert clean.passed, clean.failure_reason

    modified = mask.copy()
    rows, columns = np.nonzero(modified)
    center_y = int(round(float(np.mean(rows))))
    maximum_x = int(columns.max())
    modified[center_y - 1 : center_y + 2, maximum_x + 1 : maximum_x + 5] = 255

    baseline = measure_topdown_oal(modified, minimum_fixture_width_ratio=0.0)
    recovered = measure_topdown_oal_subpixel_v2(
        image, modified, minimum_fixture_width_ratio=0.0
    )
    assert baseline.passed
    assert recovered.passed, recovered.failure_reason
    assert clean.length_pixels is not None
    assert recovered.length_pixels == pytest.approx(clean.length_pixels, abs=0.20)


def test_version_2_converts_to_inches() -> None:
    image, mask = _scene(angle_degrees=70.0)
    result = measure_topdown_oal_subpixel_v2(
        image,
        mask,
        minimum_fixture_width_ratio=0.0,
        pixels_per_inch=400.0,
    )
    assert result.passed, result.failure_reason
    assert result.length_pixels is not None
    assert result.length_inches == pytest.approx(result.length_pixels / 400.0)


def test_version_2_accepts_bgr_image() -> None:
    image, mask = _scene(angle_degrees=20.0)
    bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    result = measure_topdown_oal_subpixel_v2(bgr, mask, minimum_fixture_width_ratio=0.0)
    assert result.passed, result.failure_reason


def test_version_2_requires_matching_image_and_mask_shape() -> None:
    image, mask = _scene(angle_degrees=0.0)
    with pytest.raises(ValueError, match="identical"):
        measure_topdown_oal_subpixel_v2(
            image[:-1], mask, minimum_fixture_width_ratio=0.0
        )
