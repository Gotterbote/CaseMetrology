from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np
from numpy.typing import NDArray

GrayImage = NDArray[np.uint8]


@dataclass(frozen=True)
class TopDownScene:
    image: GrayImage
    mask: GrayImage
    case_length_px: int
    case_width_px: int
    fixture_length_px: int
    fixture_width_px: int
    fixture_offset_px: int
    angle_degrees: float
    center_xy: tuple[int, int]


def generate_topdown_scene(
    *,
    image_size_xy: tuple[int, int] = (900, 700),
    case_length_px: int = 360,
    case_width_px: int = 42,
    fixture_length_px: int = 100,
    fixture_width_px: int = 120,
    fixture_offset_px: int = 0,
    angle_degrees: float = 90.0,
    center_xy: tuple[int, int] = (450, 350),
    background_value: int = 255,
    foreground_value: int = 0,
) -> TopDownScene:
    width, height = image_size_xy
    cx, cy = center_xy

    base_mask = np.zeros((height, width), dtype=np.uint8)

    # Case: straight-wall, unheaded cylinder viewed from the top.
    case_left = int(round(cx - case_length_px / 2))
    case_right = int(round(cx + case_length_px / 2))
    case_top = int(round(cy - case_width_px / 2))
    case_bottom = int(round(cy + case_width_px / 2))

    cv2.rectangle(
        base_mask,
        (case_left, case_top),
        (case_right, case_bottom),
        255,
        thickness=-1,
    )

    # Fixture: square / wider region crossing the middle.
    fixture_center_x = int(round(cx + fixture_offset_px))
    fixture_left = int(round(fixture_center_x - fixture_length_px / 2))
    fixture_right = int(round(fixture_center_x + fixture_length_px / 2))
    fixture_top = int(round(cy - fixture_width_px / 2))
    fixture_bottom = int(round(cy + fixture_width_px / 2))

    cv2.rectangle(
        base_mask,
        (fixture_left, fixture_top),
        (fixture_right, fixture_bottom),
        255,
        thickness=-1,
    )

    # Rotate the entire assembly together.
    rotation = cv2.getRotationMatrix2D(center_xy, angle_degrees, 1.0)
    mask = cv2.warpAffine(
        base_mask,
        rotation,
        (width, height),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

    image = np.full((height, width), background_value, dtype=np.uint8)
    image[mask > 0] = foreground_value

    return TopDownScene(
        image=image,
        mask=mask,
        case_length_px=case_length_px,
        case_width_px=case_width_px,
        fixture_length_px=fixture_length_px,
        fixture_width_px=fixture_width_px,
        fixture_offset_px=fixture_offset_px,
        angle_degrees=angle_degrees,
        center_xy=center_xy,
    )
