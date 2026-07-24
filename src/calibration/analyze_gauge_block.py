"""Preliminary pixel-scale analysis using a certified gauge block."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import numpy as np

DEFAULT_CERTIFIED_LENGTH_IN = 1.0000024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate the vertical pixel span of a backlit certified gauge "
            "block. This is a preliminary diagnostic, not a final calibration."
        )
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to the gauge-block image.",
    )
    parser.add_argument(
        "--certified-length-in",
        type=float,
        default=DEFAULT_CERTIFIED_LENGTH_IN,
        help=(
            "Certified top-to-bottom gauge-block length in inches "
            f"(default: {DEFAULT_CERTIFIED_LENGTH_IN:.7f})."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("processed_images/calibration"),
        help="Directory for the annotated diagnostic image.",
    )
    return parser.parse_args()


def select_gauge_block_component(
    binary_mask: np.ndarray,
) -> tuple[np.ndarray, int, tuple[int, int, int, int]]:
    """Return the largest suitable non-border connected component."""
    component_count, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary_mask,
        connectivity=8,
    )

    image_height, image_width = binary_mask.shape
    minimum_area = image_height * image_width * 0.01
    candidates: list[tuple[int, int]] = []

    for component_id in range(1, component_count):
        x = int(stats[component_id, cv2.CC_STAT_LEFT])
        y = int(stats[component_id, cv2.CC_STAT_TOP])
        width = int(stats[component_id, cv2.CC_STAT_WIDTH])
        height = int(stats[component_id, cv2.CC_STAT_HEIGHT])
        area = int(stats[component_id, cv2.CC_STAT_AREA])

        touches_border = (
            x <= 0 or y <= 0 or x + width >= image_width or y + height >= image_height
        )

        if area >= minimum_area and not touches_border:
            candidates.append((area, component_id))

    if not candidates:
        raise RuntimeError("No suitable non-border gauge-block component was detected.")

    _, component_id = max(candidates)

    x = int(stats[component_id, cv2.CC_STAT_LEFT])
    y = int(stats[component_id, cv2.CC_STAT_TOP])
    width = int(stats[component_id, cv2.CC_STAT_WIDTH])
    height = int(stats[component_id, cv2.CC_STAT_HEIGHT])

    return labels, component_id, (x, y, width, height)


def main() -> None:
    args = parse_args()

    grayscale = cv2.imread(str(args.image), cv2.IMREAD_GRAYSCALE)
    color = cv2.imread(str(args.image), cv2.IMREAD_COLOR)

    if grayscale is None or color is None:
        raise RuntimeError(f"Could not read image: {args.image}")

    threshold_value, binary_mask = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    labels, component_id, bounding_box = select_gauge_block_component(binary_mask)
    x, y, width, height = bounding_box

    # Measure only through the central portion of the block width.
    # This avoids the beveled upper corners and minimizes edge artifacts.
    sample_x_start = x + round(width * 0.30)
    sample_x_end = x + round(width * 0.70)

    column_measurements: list[tuple[int, int, int, int]] = []

    for column in range(sample_x_start, sample_x_end):
        y_positions = np.flatnonzero(labels[:, column] == component_id)

        if y_positions.size < 2:
            continue

        top_y = int(y_positions[0])
        bottom_y = int(y_positions[-1])
        span_pixels = bottom_y - top_y + 1

        column_measurements.append((column, top_y, bottom_y, span_pixels))

    if not column_measurements:
        raise RuntimeError("No valid vertical gauge-block spans were found.")

    spans = np.asarray(
        [measurement[3] for measurement in column_measurements],
        dtype=np.float64,
    )

    median_span_pixels = float(np.median(spans))
    mean_span_pixels = float(np.mean(spans))
    standard_deviation_pixels = float(np.std(spans, ddof=1))
    minimum_span_pixels = int(np.min(spans))
    maximum_span_pixels = int(np.max(spans))

    representative = min(
        column_measurements,
        key=lambda measurement: abs(measurement[3] - median_span_pixels),
    )
    representative_x, top_y, bottom_y, _ = representative

    pixels_per_inch = median_span_pixels / args.certified_length_in
    inches_per_pixel = args.certified_length_in / median_span_pixels

    annotated = color.copy()

    cv2.rectangle(
        annotated,
        (x, y),
        (x + width - 1, y + height - 1),
        (0, 255, 0),
        2,
    )
    cv2.line(
        annotated,
        (representative_x, top_y),
        (representative_x, bottom_y),
        (0, 0, 255),
        2,
    )
    cv2.circle(
        annotated,
        (representative_x, top_y),
        5,
        (255, 0, 0),
        -1,
    )
    cv2.circle(
        annotated,
        (representative_x, bottom_y),
        5,
        (255, 0, 0),
        -1,
    )

    label = (
        f"Vertical span: {median_span_pixels:.1f} px | " f"{pixels_per_inch:.3f} px/in"
    )
    cv2.putText(
        annotated,
        label,
        (30, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / (f"{args.image.stem}_gauge_block_diagnostic.png")

    if not cv2.imwrite(str(output_path), annotated):
        raise RuntimeError(f"Could not save diagnostic image: {output_path}")

    print("Gauge-block pixel-scale diagnostic")
    print(f"Image: {args.image}")
    print("Certified vertical length: " f"{args.certified_length_in:.7f} in")
    print(f"Otsu threshold: {threshold_value:.1f}")
    print(f"Detected bounding box: x={x}, y={y}, w={width}, h={height}")
    print(f"Columns evaluated: {len(column_measurements)}")
    print(f"Median vertical span: {median_span_pixels:.3f} px")
    print(f"Mean vertical span: {mean_span_pixels:.3f} px")
    print("Vertical-span standard deviation: " f"{standard_deviation_pixels:.4f} px")
    print(f"Vertical-span range: {minimum_span_pixels} to " f"{maximum_span_pixels} px")
    print(f"Preliminary scale: {pixels_per_inch:.6f} px/in")
    print(f"Preliminary resolution: {inches_per_pixel:.9f} in/px")
    print(f"Annotated image: {output_path}")
    print("Status: PRELIMINARY DIAGNOSTIC — NOT FINAL CALIBRATION")


if __name__ == "__main__":
    main()
