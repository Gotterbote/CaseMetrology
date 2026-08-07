from __future__ import annotations

import cv2
import numpy as np
import pytest

from src.calibration.oriented_gauge_block import measure_oriented_gauge_block


def _gauge_block_image(angle_degrees: float) -> np.ndarray:
    image = np.full((1200, 1400), 225, dtype=np.uint8)

    # Approximate 1.375 x 1.000 inch block at 500 px/in.
    rect = ((700.0, 600.0), (687.5, 500.0), angle_degrees)
    box = cv2.boxPoints(rect).astype(np.int32)

    cv2.fillConvexPoly(image, box, 70)

    return image


@pytest.mark.parametrize("angle", [0.0, 30.0, 45.0, 90.0])
def test_oriented_gauge_block_measures_rotated_standard(angle: float) -> None:
    image = _gauge_block_image(angle)

    result = measure_oriented_gauge_block(
        image,
        certified_length_in=1.0,
    )

    assert result.passed, result.failure_reason
    assert result.measured_span_pixels is not None
    assert result.pixels_per_inch is not None
    assert result.accepted_profile_count >= 10
    assert result.measured_span_pixels == pytest.approx(500.0, abs=2.0)


def test_oriented_gauge_block_0_and_90_agree() -> None:
    zero = measure_oriented_gauge_block(
        _gauge_block_image(0.0),
        certified_length_in=1.0,
    )
    ninety = measure_oriented_gauge_block(
        _gauge_block_image(90.0),
        certified_length_in=1.0,
    )

    assert zero.passed
    assert ninety.passed
    assert zero.pixels_per_inch == pytest.approx(
        ninety.pixels_per_inch,
        abs=0.5,
    )


def test_oriented_gauge_block_rejects_invalid_scale() -> None:
    image = _gauge_block_image(0.0)

    with pytest.raises(ValueError, match="certified_length_in"):
        measure_oriented_gauge_block(
            image,
            certified_length_in=0.0,
        )
