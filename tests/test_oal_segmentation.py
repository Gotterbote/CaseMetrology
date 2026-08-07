from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.image_processing.oal_segmentation import segment_oal_case


def test_segment_oal_case_detects_single_dark_component() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(image, (100, 120), (300, 180), 80, thickness=-1)

    result = segment_oal_case(blank, image)

    assert result.passed
    assert result.failure_reason is None
    assert result.otsu_threshold is not None
    assert result.component_pixels > 0
    assert result.centroid_xy is not None

    centroid_x, centroid_y = result.centroid_xy

    assert centroid_x == pytest.approx(200.0, abs=1.0)
    assert centroid_y == pytest.approx(150.0, abs=1.0)
    assert result.mask.dtype == np.uint8
    assert set(np.unique(result.mask)).issubset({0, 255})


def test_segment_oal_case_keeps_largest_component() -> None:
    blank = np.full((300, 400), 220, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(image, (50, 100), (250, 180), 80, thickness=-1)
    cv2.rectangle(image, (330, 20), (350, 40), 80, thickness=-1)

    result = segment_oal_case(blank, image)

    assert result.passed
    assert result.centroid_xy is not None

    centroid_x, centroid_y = result.centroid_xy

    assert centroid_x < 200.0
    assert centroid_y > 100.0


def test_segment_oal_case_returns_clean_failure_without_foreground() -> None:
    blank = np.full((200, 300), 220, dtype=np.uint8)
    image = blank.copy()

    result = segment_oal_case(blank, image)

    assert not result.passed
    assert result.failure_reason == "No foreground case component was detected."
    assert result.component_pixels == 0
    assert result.centroid_xy is None
    assert np.count_nonzero(result.mask) == 0


def test_segment_oal_case_rejects_shape_mismatch() -> None:
    blank = np.zeros((200, 300), dtype=np.uint8)
    image = np.zeros((201, 300), dtype=np.uint8)

    with pytest.raises(ValueError, match="Image dimensions differ"):
        segment_oal_case(blank, image)


def test_segment_oal_case_requires_grayscale_inputs() -> None:
    blank = np.zeros((200, 300, 3), dtype=np.uint8)
    image = np.zeros((200, 300, 3), dtype=np.uint8)

    with pytest.raises(ValueError, match="two-dimensional grayscale"):
        segment_oal_case(blank, image)
