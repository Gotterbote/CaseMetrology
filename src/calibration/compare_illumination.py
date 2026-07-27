"""Compare backlight uniformity before and after installing a locator fixture."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare two empty-backlight images and quantify illumination "
            "changes introduced by a fixture or locator."
        )
    )
    parser.add_argument(
        "reference_image",
        type=Path,
        help="Empty-backlight image captured without the locator.",
    )
    parser.add_argument(
        "comparison_image",
        type=Path,
        help="Empty-backlight image captured with the locator installed.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("measurements/fixture_validation"),
        help="Directory for reports and difference images.",
    )
    return parser.parse_args()


def image_statistics(image: np.ndarray) -> dict[str, float]:
    return {
        "mean_intensity": float(np.mean(image)),
        "standard_deviation": float(np.std(image, ddof=1)),
        "minimum_intensity": float(np.min(image)),
        "maximum_intensity": float(np.max(image)),
        "percent_below_25": float(np.mean(image < 25) * 100.0),
        "percent_above_250": float(np.mean(image > 250) * 100.0),
    }


def region_statistics(
    reference: np.ndarray,
    comparison: np.ndarray,
) -> dict[str, float]:
    difference = comparison.astype(np.float64) - reference.astype(np.float64)
    absolute_difference = np.abs(difference)

    return {
        "mean_signed_difference": float(np.mean(difference)),
        "mean_absolute_difference": float(np.mean(absolute_difference)),
        "root_mean_square_difference": float(np.sqrt(np.mean(np.square(difference)))),
        "maximum_absolute_difference": float(np.max(absolute_difference)),
        "percent_abs_difference_over_5": float(
            np.mean(absolute_difference > 5.0) * 100.0
        ),
        "percent_abs_difference_over_10": float(
            np.mean(absolute_difference > 10.0) * 100.0
        ),
        "percent_abs_difference_over_20": float(
            np.mean(absolute_difference > 20.0) * 100.0
        ),
    }


def main() -> None:
    args = parse_args()

    reference = cv2.imread(
        str(args.reference_image),
        cv2.IMREAD_GRAYSCALE,
    )
    comparison = cv2.imread(
        str(args.comparison_image),
        cv2.IMREAD_GRAYSCALE,
    )

    if reference is None:
        raise RuntimeError(f"Could not read reference image: {args.reference_image}")

    if comparison is None:
        raise RuntimeError(f"Could not read comparison image: {args.comparison_image}")

    if reference.shape != comparison.shape:
        raise RuntimeError(
            "Images must have identical dimensions. "
            f"Reference: {reference.shape}; comparison: {comparison.shape}"
        )

    image_height, image_width = reference.shape

    # Central region represents the area most likely to contain the
    # calibration reference and measured parts.
    roi_x_start = round(image_width * 0.20)
    roi_x_end = round(image_width * 0.80)
    roi_y_start = round(image_height * 0.20)
    roi_y_end = round(image_height * 0.80)

    reference_roi = reference[
        roi_y_start:roi_y_end,
        roi_x_start:roi_x_end,
    ]
    comparison_roi = comparison[
        roi_y_start:roi_y_end,
        roi_x_start:roi_x_end,
    ]

    reference_stats = image_statistics(reference)
    comparison_stats = image_statistics(comparison)
    full_frame_difference = region_statistics(reference, comparison)
    central_roi_difference = region_statistics(
        reference_roi,
        comparison_roi,
    )

    signed_difference = comparison.astype(np.int16) - reference.astype(np.int16)
    absolute_difference = np.abs(signed_difference).astype(np.uint8)

    enhanced_difference = cv2.normalize(
        absolute_difference,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    )

    annotated = cv2.cvtColor(
        enhanced_difference,
        cv2.COLOR_GRAY2BGR,
    )
    cv2.rectangle(
        annotated,
        (roi_x_start, roi_y_start),
        (roi_x_end - 1, roi_y_end - 1),
        (0, 255, 0),
        2,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    output_stem = f"illumination_comparison_{timestamp}"

    difference_path = args.output_dir / (f"{output_stem}_absolute_difference.png")
    report_path = args.output_dir / f"{output_stem}.txt"
    csv_path = args.output_dir / f"{output_stem}.csv"

    if not cv2.imwrite(str(difference_path), annotated):
        raise RuntimeError(f"Could not save difference image: {difference_path}")

    rows = [
        {
            "region": "full_frame",
            **full_frame_difference,
        },
        {
            "region": "central_60_percent",
            **central_roi_difference,
        },
    ]

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    report_lines = [
        "CaseMetrology Locator Illumination Comparison",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Reference image: {args.reference_image}",
        f"Comparison image: {args.comparison_image}",
        f"Image resolution: {image_width} x {image_height}",
        "",
        "=== REFERENCE IMAGE ===",
        *[f"{name}: {value:.6f}" for name, value in reference_stats.items()],
        "",
        "=== COMPARISON IMAGE ===",
        *[f"{name}: {value:.6f}" for name, value in comparison_stats.items()],
        "",
        "=== FULL-FRAME DIFFERENCE ===",
        *[f"{name}: {value:.6f}" for name, value in full_frame_difference.items()],
        "",
        "=== CENTRAL 60% REGION DIFFERENCE ===",
        *[f"{name}: {value:.6f}" for name, value in central_roi_difference.items()],
        "",
        "Interpretation:",
        "  This analysis quantifies illumination changes between two",
        "  empty-backlight images. It does not determine whether a locator",
        "  is acceptable without visual inspection of the measurement area.",
        "",
        f"Detailed CSV: {csv_path}",
        f"Difference image: {difference_path}",
    ]

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(report_lines))
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
