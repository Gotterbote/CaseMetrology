from __future__ import annotations

import numpy as np

from src.diagnostics.topdown_oal_overlay import draw_topdown_oal_overlay
from src.measurement.topdown_oal import measure_topdown_oal
from src.synthetic.topdown_case_fixture import generate_topdown_scene


def test_overlay_is_created_for_passed_measurement() -> None:
    scene = generate_topdown_scene(
        case_length_px=360,
        fixture_offset_px=20,
        angle_degrees=35.0,
    )

    result = measure_topdown_oal(scene.mask)
    overlay = draw_topdown_oal_overlay(scene.mask, result)

    assert result.passed, result.failure_reason
    assert overlay.shape == (700, 900, 3)
    assert overlay.dtype == np.uint8
    assert np.any(overlay != 255)


def test_overlay_is_created_for_failed_measurement() -> None:
    empty_mask = np.zeros((700, 900), dtype=np.uint8)

    result = measure_topdown_oal(empty_mask)
    overlay = draw_topdown_oal_overlay(empty_mask, result)

    assert not result.passed
    assert overlay.shape == (700, 900, 3)
    assert overlay.dtype == np.uint8
    assert np.any(overlay != 255)
