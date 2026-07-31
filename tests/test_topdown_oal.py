from __future__ import annotations

import pytest

from src.measurement.topdown_oal import measure_topdown_oal
from src.synthetic.topdown_case_fixture import generate_topdown_scene


@pytest.mark.parametrize(
    ("angle_degrees", "fixture_offset_px"),
    [
        (0.0, 0),
        (45.0, 0),
        (90.0, 0),
        (35.0, -50),
        (35.0, 50),
    ],
)
def test_oal_is_orientation_and_fixture_offset_invariant(
    angle_degrees: float,
    fixture_offset_px: int,
) -> None:
    scene = generate_topdown_scene(
        case_length_px=360,
        case_width_px=42,
        fixture_length_px=100,
        fixture_width_px=120,
        fixture_offset_px=fixture_offset_px,
        angle_degrees=angle_degrees,
    )

    result = measure_topdown_oal(scene.mask)

    assert result.passed, result.failure_reason
    assert result.length_pixels == pytest.approx(360.0, abs=2.0)
