import numpy as np

from src.synthetic.topdown_case_fixture import generate_topdown_scene


def test_topdown_scene_is_created() -> None:
    scene = generate_topdown_scene(angle_degrees=90.0)

    assert scene.image.shape == (700, 900)
    assert scene.mask.shape == (700, 900)
    assert np.count_nonzero(scene.mask) > 0


def test_fixture_region_is_wider_than_case_region() -> None:
    scene = generate_topdown_scene(
        angle_degrees=0.0,
        fixture_offset_px=0,
    )

    mask = scene.mask > 0
    column_widths = mask.sum(axis=0)

    nonzero_columns = np.where(column_widths > 0)[0]
    left = int(nonzero_columns.min())
    right = int(nonzero_columns.max())
    mid = (left + right) // 2

    left_case_width = int(column_widths[left + 20])
    right_case_width = int(column_widths[right - 20])
    center_fixture_width = int(column_widths[mid])

    assert center_fixture_width > left_case_width
    assert center_fixture_width > right_case_width
