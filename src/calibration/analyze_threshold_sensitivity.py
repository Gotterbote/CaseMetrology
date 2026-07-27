"""Evaluate gauge-block measurement sensitivity to binary threshold choice."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

CERTIFIED_LENGTH_IN = 1.0000024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Measure a gauge block across a range of fixed grayscale "
            "thresholds to evaluate threshold sensitivity."
        )
    )
    parser.add_argument(
        "image",
        type=Path,
        help="Path to a centered gauge-block image.",
    )
    parser.add_argument(
        "--minimum",
        type=int,
        default=70,
        help="Minimum threshold value (default: 70).",
    )
    parser.add_argument(
        "--maximum",
        type=int,
        default=130,
        help="Maximum threshold value (default: 130).",
    )
    parser.add_argument(
        "--step",
        type=int,
        default=5,
        help="Threshold increment (default: 5).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("measurements/calibration"),
        help="Directory for CSV and summary reports.",
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


def measure_at_threshold(
    grayscale: np.ndarray,
    threshold_value: int,
) -> dict[str, float | int]:
    _, mask = cv2.threshold(
        grayscale,
        threshold_value,
        255,
        cv2.THRESH_BINARY_INV,
    )

    labels, component_id, bounding_box = select_component(mask)
    x, _, width, _ = bounding_box

    sample_start = x + round(width * 0.30)
    sample_end = x + round(width * 0.70)

    spans: list[int] = []

    for column in range(sample_start, sample_end):
        positions = np.flatnonzero(labels[:, column] == component_id)

        if positions.size >= 2:
            spans.append(int(positions[-1] - positions[0] + 1))

    if not spans:
        raise RuntimeError(
            f"No valid vertical spans found at threshold {threshold_value}."
        )

    span_array = np.asarray(spans, dtype=np.float64)
    mean_span = float(np.mean(span_array))
    median_span = float(np.median(span_array))

    return {
        "threshold": threshold_value,
        "columns_evaluated": len(spans),
        "median_span_px": median_span,
        "mean_span_px": mean_span,
        "within_image_sd_px": float(np.std(span_array, ddof=1)),
        "minimum_span_px": int(np.min(span_array)),
        "maximum_span_px": int(np.max(span_array)),
        "pixels_per_inch": mean_span / CERTIFIED_LENGTH_IN,
        "inches_per_pixel": CERTIFIED_LENGTH_IN / mean_span,
    }


def main() -> None:
    args = parse_args()

    if not 0 <= args.minimum <= 255:
        raise ValueError("--minimum must be between 0 and 255")

    if not 0 <= args.maximum <= 255:
        raise ValueError("--maximum must be between 0 and 255")

    if args.minimum > args.maximum:
        raise ValueError("--minimum cannot exceed --maximum")

    if args.step < 1:
        raise ValueError("--step must be at least 1")

    grayscale = cv2.imread(str(args.image), cv2.IMREAD_GRAYSCALE)

    if grayscale is None:
        raise RuntimeError(f"Could not read image: {args.image}")

    otsu_threshold, _ = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    thresholds = range(
        args.minimum,
        args.maximum + 1,
        args.step,
    )
    results = [measure_at_threshold(grayscale, threshold) for threshold in thresholds]

    mean_spans = np.asarray(
        [float(result["mean_span_px"]) for result in results],
        dtype=np.float64,
    )

    span_range_px = float(np.ptp(mean_spans))
    overall_mean_px = float(np.mean(mean_spans))
    nominal_inches_per_pixel = CERTIFIED_LENGTH_IN / overall_mean_px
    equivalent_range_in = span_range_px * nominal_inches_per_pixel

    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    stem = args.image.stem

    csv_path = args.output_dir / (f"{stem}_threshold_sensitivity_{timestamp}.csv")
    report_path = args.output_dir / (f"{stem}_threshold_sensitivity_{timestamp}.txt")

    fieldnames = list(results[0].keys())

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    report_lines = [
        "CaseMetrology Threshold-Sensitivity Analysis",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Image: {args.image}",
        f"Certified gauge-block length: {CERTIFIED_LENGTH_IN:.7f} in",
        f"Otsu-selected threshold: {otsu_threshold:.1f}",
        (
            f"Threshold range tested: {args.minimum} to "
            f"{args.maximum} in steps of {args.step}"
        ),
        "",
        "=== SUMMARY ===",
        f"Minimum mean span: {np.min(mean_spans):.6f} px",
        f"Maximum mean span: {np.max(mean_spans):.6f} px",
        f"Mean-span range: {span_range_px:.6f} px",
        f"Equivalent dimensional range: {equivalent_range_in:.9f} in",
        "",
        "Interpretation:",
        "  This evaluates sensitivity of the integer-pixel measurement",
        "  result to the selected binary threshold.",
        "  It does not establish final accuracy or uncertainty.",
        "",
        f"Detailed CSV: {csv_path}",
    ]

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print("Threshold  Mean span (px)  Median (px)  Within-image SD (px)")

    for result in results:
        print(
            f"{int(result['threshold']):9d}"
            f"{float(result['mean_span_px']):16.6f}"
            f"{float(result['median_span_px']):13.3f}"
            f"{float(result['within_image_sd_px']):22.6f}"
        )

    print()
    print("\n".join(report_lines))
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
