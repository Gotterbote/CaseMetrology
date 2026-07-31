"""Generate one exploratory top-down OAL diagnostic overlay."""

from pathlib import Path

import cv2

from src.diagnostics.topdown_oal_overlay import draw_topdown_oal_overlay
from src.measurement.topdown_oal import measure_topdown_oal
from src.synthetic.topdown_case_fixture import generate_topdown_scene


def main() -> None:
    output_dir = Path("data/synthetic_oal_preview")
    output_dir.mkdir(parents=True, exist_ok=True)

    scene = generate_topdown_scene(
        case_length_px=360,
        case_width_px=42,
        fixture_length_px=100,
        fixture_width_px=120,
        fixture_offset_px=20,
        angle_degrees=35.0,
        center_xy=(450, 350),
    )

    result = measure_topdown_oal(scene.mask)
    overlay = draw_topdown_oal_overlay(scene.mask, result)

    output_path = output_dir / "topdown_oal_diagnostic_overlay.png"

    if not cv2.imwrite(str(output_path), overlay):
        raise RuntimeError(f"Failed to write {output_path}")

    print(f"Passed: {result.passed}")
    print(f"Measured OAL: {result.length_pixels:.3f} px")
    print(f"Detected angle: {result.angle_degrees:.3f} degrees")
    print(f"Fixture width ratio: {result.fixture_width_ratio:.3f}")
    print(f"Overlay: {output_path.resolve()}")


if __name__ == "__main__":
    main()
