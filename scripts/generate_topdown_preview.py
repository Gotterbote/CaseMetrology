from pathlib import Path

import cv2

from src.synthetic.topdown_case_fixture import generate_topdown_scene


def main() -> None:
    output_dir = Path("data/synthetic_oal_preview")
    output_dir.mkdir(parents=True, exist_ok=True)

    preview = generate_topdown_scene(
        case_length_px=360,
        case_width_px=42,
        fixture_length_px=100,
        fixture_width_px=120,
        fixture_offset_px=0,
        angle_degrees=90.0,
        center_xy=(450, 350),
    )

    cv2.imwrite(str(output_dir / "topdown_preview.png"), preview.image)
    cv2.imwrite(str(output_dir / "topdown_preview_mask.png"), preview.mask)

    rotated = generate_topdown_scene(
        case_length_px=360,
        case_width_px=42,
        fixture_length_px=100,
        fixture_width_px=120,
        fixture_offset_px=20,
        angle_degrees=35.0,
        center_xy=(450, 350),
    )

    cv2.imwrite(
        str(output_dir / "topdown_rotated_preview.png"),
        rotated.image,
    )
    cv2.imwrite(
        str(output_dir / "topdown_rotated_preview_mask.png"),
        rotated.mask,
    )

    print("Synthetic preview files written to:")
    print(output_dir.resolve())


if __name__ == "__main__":
    main()
