"""Check whether a case centroid is inside a defined image-space target."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blank", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--target-x", required=True, type=float)
    parser.add_argument("--target-y", required=True, type=float)
    parser.add_argument("--tolerance", default=5.0, type=float)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    blank = cv2.imread(str(args.blank), cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(str(args.image), cv2.IMREAD_GRAYSCALE)

    if blank is None:
        raise RuntimeError(f"Could not read blank image: {args.blank}")

    if image is None:
        raise RuntimeError(f"Could not read case image: {args.image}")

    if blank.shape != image.shape:
        raise RuntimeError(
            f"Image dimensions differ: blank={blank.shape}, image={image.shape}"
        )

    darkening = cv2.subtract(blank, image)
    blurred = cv2.GaussianBlur(darkening, (5, 5), 0)

    threshold, mask = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    kernel = np.ones((3, 3), dtype=np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        (mask > 0).astype(np.uint8),
        connectivity=8,
    )

    if count <= 1:
        raise RuntimeError("No foreground case component was detected.")

    areas = stats[1:, cv2.CC_STAT_AREA]
    largest_label = int(np.argmax(areas)) + 1
    component = labels == largest_label
    component_mask = component.astype(np.uint8) * 255

    rows_y, columns_x = np.nonzero(component)

    centroid_x = float(columns_x.mean())
    centroid_y = float(rows_y.mean())

    delta_x = centroid_x - args.target_x
    delta_y = centroid_y - args.target_y

    passed = abs(delta_x) <= args.tolerance and abs(delta_y) <= args.tolerance

    horizontal_instruction = ""
    vertical_instruction = ""

    if delta_x < -args.tolerance:
        horizontal_instruction = "Move case right."
    elif delta_x > args.tolerance:
        horizontal_instruction = "Move case left."

    if delta_y < -args.tolerance:
        vertical_instruction = "Move case downward."
    elif delta_y > args.tolerance:
        vertical_instruction = "Move case upward."

    args.output_dir.mkdir(parents=True, exist_ok=True)

    overlay = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    target_point = (
        int(round(args.target_x)),
        int(round(args.target_y)),
    )
    measured_point = (
        int(round(centroid_x)),
        int(round(centroid_y)),
    )

    tolerance = int(round(args.tolerance))

    cv2.rectangle(
        overlay,
        (
            target_point[0] - tolerance,
            target_point[1] - tolerance,
        ),
        (
            target_point[0] + tolerance,
            target_point[1] + tolerance,
        ),
        (128, 128, 128),
        2,
    )

    cv2.drawMarker(
        overlay,
        target_point,
        (0, 0, 0),
        cv2.MARKER_CROSS,
        24,
        2,
    )

    cv2.circle(
        overlay,
        measured_point,
        7,
        (255, 255, 255),
        -1,
    )
    cv2.circle(
        overlay,
        measured_point,
        7,
        (0, 0, 0),
        2,
    )

    status = "PASS" if passed else "FAIL"

    cv2.putText(
        overlay,
        f"Placement: {status}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        overlay,
        f"Centroid: ({centroid_x:.3f}, {centroid_y:.3f})",
        (20, 68),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.imwrite(
        str(args.output_dir / "placement_mask.png"),
        component_mask,
    )
    cv2.imwrite(
        str(args.output_dir / "placement_overlay.png"),
        overlay,
    )

    print(f"Otsu threshold: {threshold:.3f}")
    print(f"Measured centroid: ({centroid_x:.3f}, {centroid_y:.3f})")
    print(f"Target centroid: ({args.target_x:.3f}, {args.target_y:.3f})")
    print(f"Delta X: {delta_x:+.3f} px")
    print(f"Delta Y: {delta_y:+.3f} px")
    print(f"Tolerance: +/- {args.tolerance:.3f} px")
    print(f"Placement status: {status}")

    if not passed:
        for instruction in (
            horizontal_instruction,
            vertical_instruction,
        ):
            if instruction:
                print(instruction)


if __name__ == "__main__":
    main()
