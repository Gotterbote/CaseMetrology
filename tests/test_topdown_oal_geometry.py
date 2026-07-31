from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.measurement.topdown_oal import measure_topdown_oal
from src.measurement.topdown_oal_geometry import measure_topdown_oal_geometry


def _rotated_box(
    center: tuple[float, float],
    size: tuple[float, float],
    angle_degrees: float,
) -> np.ndarray:
    return np.round(cv2.boxPoints((center, size, angle_degrees))).astype(np.int32)


def _assembly_mask(angle_degrees: float, *, endpoint_spur: bool = False) -> np.ndarray:
    mask = np.zeros((900, 900), dtype=np.uint8)
    center = (450.0, 450.0)

    case = _rotated_box(center, (520.0, 80.0), angle_degrees)
    fixture = _rotated_box(center, (145.0, 150.0), angle_degrees)
    cv2.fillConvexPoly(mask, case, 255)
    cv2.fillConvexPoly(mask, fixture, 255)

    if endpoint_spur:
        radians = np.radians(angle_degrees)
        axis = np.array([np.cos(radians), np.sin(radians)])
        perpendicular = np.array([-axis[1], axis[0]])
        end_center = np.array(center) + 260.0 * axis
        spur_center = end_center + 5.0 * axis + 28.0 * perpendicular
        spur = _rotated_box(
            (float(spur_center[0]), float(spur_center[1])),
            (18.0, 8.0),
            angle_degrees,
        )
        cv2.fillConvexPoly(mask, spur, 255)

    return mask


@pytest.mark.parametrize("angle_degrees", [0.0, 20.0, 40.0, 70.0, 90.0])
def test_geometry_measurement_passes_across_orientation(angle_degrees: float) -> None:
    result = measure_topdown_oal_geometry(_assembly_mask(angle_degrees))

    assert result.passed, result.failure_reason
    assert result.length_pixels is not None
    assert 518.0 <= result.length_pixels <= 523.0
    assert result.endpoint_min_xy is not None
    assert result.endpoint_max_xy is not None


def test_geometry_range_is_small_across_orientation() -> None:
    lengths = []
    for angle in [0.0, 20.0, 40.0, 70.0, 90.0]:
        result = measure_topdown_oal_geometry(_assembly_mask(angle))
        assert result.passed, result.failure_reason
        assert result.length_pixels is not None
        lengths.append(result.length_pixels)

    assert max(lengths) - min(lengths) < 2.0


def test_robust_end_fit_rejects_small_connected_spur() -> None:
    clean_mask = _assembly_mask(40.0)
    spur_mask = _assembly_mask(40.0, endpoint_spur=True)

    clean_geometry = measure_topdown_oal_geometry(clean_mask)
    spur_geometry = measure_topdown_oal_geometry(spur_mask)
    clean_pca = measure_topdown_oal(clean_mask)
    spur_pca = measure_topdown_oal(spur_mask)

    assert clean_geometry.passed and spur_geometry.passed
    assert clean_geometry.length_pixels is not None
    assert spur_geometry.length_pixels is not None
    assert clean_pca.length_pixels is not None
    assert spur_pca.length_pixels is not None

    geometry_shift = abs(spur_geometry.length_pixels - clean_geometry.length_pixels)
    pca_shift = abs(spur_pca.length_pixels - clean_pca.length_pixels)

    assert geometry_shift < 1.0
    assert pca_shift > geometry_shift


def test_empty_mask_fails_cleanly() -> None:
    result = measure_topdown_oal_geometry(np.zeros((200, 200), dtype=np.uint8))

    assert not result.passed
    assert result.failure_reason is not None
    assert result.length_pixels is None
