"""Preliminary subpixel gauge-block edge analysis."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

CERTIFIED_LENGTH_IN = 1.0000024
WINDOW_RADIUS = 8
LEVEL_OFFSET_START = 4
MINIMUM_EDGE_CONTRAST = 20.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate the certified vertical gauge-block dimension using "
            "local grayscale midpoint crossings at subpixel resolution."
        )
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to a centered, backlit gauge-block image.",
    )
    parser.add_argument(
        "--output-image-dir",
        type=Path,
        default=Path("processed_images/calibration"),
        help="Directory for the annotated diagnostic image.",
    )
    parser.add_argument(
        "--output-data-dir",
        type=Path,
        default=Path("measurements/calibration"),
        help="Directory for the detailed per-column CSV.",
    )
    return parser.parse_args()


def select_component(
    mask: np.ndarray,
) -> tuple[np.ndarray, int, tuple[int, int, int, int]]:
    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8,
    )

    image_height, image_width = mask.shape
    minimum_area = image_height * image_width * 0.01
    candidates: list[tuple[int, int]] = []

    for component_id in range(1, count):
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
        raise RuntimeError("No suitable gauge-block component detected.")

    _, component_id = max(candidates)

    x = int(stats[component_id, cv2.CC_STAT_LEFT])
    y = int(stats[component_id, cv2.CC_STAT_TOP])
    width = int(stats[component_id, cv2.CC_STAT_WIDTH])
    height = int(stats[component_id, cv2.CC_STAT_HEIGHT])

    return labels, component_id, (x, y, width, height)


def interpolate_crossing(
    profile: np.ndarray,
    approximate_edge: int,
    background_level: float,
    object_level: float,
) -> float | None:
    target_level = (background_level + object_level) / 2.0

    search_start = max(0, approximate_edge - WINDOW_RADIUS)
    search_end = min(len(profile) - 2, approximate_edge + WINDOW_RADIUS)

    candidates: list[tuple[float, float]] = []

    for index in range(search_start, search_end + 1):
        value_0 = float(profile[index])
        value_1 = float(profile[index + 1])

        difference_0 = value_0 - target_level
        difference_1 = value_1 - target_level

        if difference_0 == 0:
            crossing = float(index)
        elif difference_0 * difference_1 > 0:
            continue
        elif value_1 == value_0:
            continue
        else:
            fraction = (target_level - value_0) / (value_1 - value_0)
            crossing = float(index) + fraction

        distance = abs(crossing - approximate_edge)
        candidates.append((distance, crossing))

    if not candidates:
        return None

    return min(candidates)[1]


def estimate_edge(
    profile: np.ndarray,
    approximate_edge: int,
    edge_type: str,
) -> tuple[float, float] | None:
    profile_length = len(profile)

    if edge_type == "top":
        background_start = approximate_edge - WINDOW_RADIUS
        background_end = approximate_edge - LEVEL_OFFSET_START
        object_start = approximate_edge + LEVEL_OFFSET_START
        object_end = approximate_edge + WINDOW_RADIUS
    elif edge_type == "bottom":
        object_start = approximate_edge - WINDOW_RADIUS
        object_end = approximate_edge - LEVEL_OFFSET_START
        background_start = approximate_edge + LEVEL_OFFSET_START
        background_end = approximate_edge + WINDOW_RADIUS
    else:
        raise ValueError(f"Unsupported edge type: {edge_type}")

    if (
        background_start < 0
        or object_start < 0
        or background_end >= profile_length
        or object_end >= profile_length
    ):
        return None

    background_values = profile[background_start : background_end + 1]
    object_values = profile[object_start : object_end + 1]

    background_level = float(np.median(background_values))
    object_level = float(np.median(object_values))
    contrast = abs(background_level - object_level)

    if contrast < MINIMUM_EDGE_CONTRAST:
        return None

    crossing = interpolate_crossing(
        profile,
        approximate_edge,
        background_level,
        object_level,
    )

    if crossing is None:
        return None

    return crossing, contrast


def main() -> None:
    args = parse_args()

    grayscale = cv2.imread(str(args.image), cv2.IMREAD_GRAYSCALE)
    color = cv2.imread(str(args.image), cv2.IMREAD_COLOR)

    if grayscale is None or color is None:
        raise RuntimeError(f"Could not read image: {args.image}")

    otsu_threshold, mask = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    labels, component_id, bounding_box = select_component(mask)
    x, y, width, height = bounding_box

    sample_start = x + round(width * 0.30)
    sample_end = x + round(width * 0.70)

    rows: list[dict[str, float | int]] = []

    for column in range(sample_start, sample_end):
        component_positions = np.flatnonzero(labels[:, column] == component_id)

        if component_positions.size < 2:
            continue

        approximate_top = int(component_positions[0])
        approximate_bottom = int(component_positions[-1])
        profile = grayscale[:, column].astype(np.float64)

        top_result = estimate_edge(
            profile,
            approximate_top,
            "top",
        )
        bottom_result = estimate_edge(
            profile,
            approximate_bottom,
            "bottom",
        )

        if top_result is None or bottom_result is None:
            continue

        top_y, top_contrast = top_result
        bottom_y, bottom_contrast = bottom_result
        span = bottom_y - top_y

        rows.append(
            {
                "column_x": column,
                "top_y_subpixel": top_y,
                "bottom_y_subpixel": bottom_y,
                "span_px": span,
                "top_contrast": top_contrast,
                "bottom_contrast": bottom_contrast,
            }
        )

    if len(rows) < 10:
        raise RuntimeError("Insufficient valid columns for subpixel analysis.")

    columns = np.asarray(
        [float(row["column_x"]) for row in rows],
        dtype=np.float64,
    )
    top_edges = np.asarray(
        [float(row["top_y_subpixel"]) for row in rows],
        dtype=np.float64,
    )
    bottom_edges = np.asarray(
        [float(row["bottom_y_subpixel"]) for row in rows],
        dtype=np.float64,
    )
    spans = np.asarray(
        [float(row["span_px"]) for row in rows],
        dtype=np.float64,
    )

    top_slope, top_intercept = np.polyfit(columns, top_edges, 1)
    bottom_slope, bottom_intercept = np.polyfit(
        columns,
        bottom_edges,
        1,
    )

    center_x = float(np.mean(columns))
    fitted_top_center = top_slope * center_x + top_intercept
    fitted_bottom_center = bottom_slope * center_x + bottom_intercept
    fitted_center_span = fitted_bottom_center - fitted_top_center

    mean_span = float(np.mean(spans))
    median_span = float(np.median(spans))
    span_sd = float(np.std(spans, ddof=1))
    span_minimum = float(np.min(spans))
    span_maximum = float(np.max(spans))
    span_range = span_maximum - span_minimum
    median_absolute_deviation = float(np.median(np.abs(spans - median_span)))

    pixels_per_inch = fitted_center_span / CERTIFIED_LENGTH_IN
    inches_per_pixel = CERTIFIED_LENGTH_IN / fitted_center_span

    top_angle = float(np.degrees(np.arctan(top_slope)))
    bottom_angle = float(np.degrees(np.arctan(bottom_slope)))

    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")

    args.output_data_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_data_dir / (
        f"{args.image.stem}_subpixel_columns_{timestamp}.csv"
    )

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    annotated = color.copy()

    cv2.rectangle(
        annotated,
        (x, y),
        (x + width - 1, y + height - 1),
        (0, 255, 0),
        2,
    )

    line_start_x = int(round(columns[0]))
    line_end_x = int(round(columns[-1]))

    fitted_top_start = int(round(top_slope * line_start_x + top_intercept))
    fitted_top_end = int(round(top_slope * line_end_x + top_intercept))
    fitted_bottom_start = int(round(bottom_slope * line_start_x + bottom_intercept))
    fitted_bottom_end = int(round(bottom_slope * line_end_x + bottom_intercept))

    cv2.line(
        annotated,
        (line_start_x, fitted_top_start),
        (line_end_x, fitted_top_end),
        (255, 0, 0),
        2,
    )
    cv2.line(
        annotated,
        (line_start_x, fitted_bottom_start),
        (line_end_x, fitted_bottom_end),
        (255, 0, 0),
        2,
    )

    center_x_integer = int(round(center_x))
    cv2.line(
        annotated,
        (center_x_integer, int(round(fitted_top_center))),
        (center_x_integer, int(round(fitted_bottom_center))),
        (0, 0, 255),
        2,
    )

    label = (
        f"Subpixel span: {fitted_center_span:.4f} px | " f"{pixels_per_inch:.3f} px/in"
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

    args.output_image_dir.mkdir(parents=True, exist_ok=True)
    image_path = args.output_image_dir / (f"{args.image.stem}_subpixel_diagnostic.png")

    if not cv2.imwrite(str(image_path), annotated):
        raise RuntimeError(f"Could not save diagnostic image: {image_path}")

    print("CaseMetrology Subpixel Gauge-Block Diagnostic")
    print(f"Image: {args.image}")
    print(f"Certified vertical length: {CERTIFIED_LENGTH_IN:.7f} in")
    print(f"Otsu threshold used for component detection: {otsu_threshold:.1f}")
    print(f"Detected bounding box: x={x}, y={y}, w={width}, h={height}")
    print(f"Valid columns evaluated: {len(rows)}")
    print(f"Mean subpixel span: {mean_span:.6f} px")
    print(f"Median subpixel span: {median_span:.6f} px")
    print(f"Subpixel span SD across columns: {span_sd:.6f} px")
    print(f"Subpixel median absolute deviation: {median_absolute_deviation:.6f} px")
    print(f"Subpixel span range: {span_minimum:.6f} to " f"{span_maximum:.6f} px")
    print(f"Subpixel peak-to-peak range: {span_range:.6f} px")
    print(f"Top-edge fitted angle: {top_angle:.6f} degrees")
    print(f"Bottom-edge fitted angle: {bottom_angle:.6f} degrees")
    print(f"Fitted center span: {fitted_center_span:.6f} px")
    print(f"Preliminary scale: {pixels_per_inch:.6f} px/in")
    print(f"Preliminary resolution: {inches_per_pixel:.9f} in/px")
    print(f"Per-column CSV: {csv_path}")
    print(f"Annotated image: {image_path}")
    print("Status: PRELIMINARY SUBPIXEL DIAGNOSTIC")


if __name__ == "__main__":
    main()
