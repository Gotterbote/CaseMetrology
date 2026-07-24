"""Evaluate fixed-setup gauge-block image acquisition repeatability."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from hashlib import sha256
from pathlib import Path

import cv2
import numpy as np

CERTIFIED_LENGTH_IN = 1.0000024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate repeatability across gauge-block images captured "
            "without moving the camera, block, lens, or lighting."
        )
    )
    parser.add_argument(
        "images",
        nargs="+",
        type=Path,
        help="Gauge-block image paths.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("measurements/calibration"),
        help="Directory for CSV and text reports.",
    )
    return parser.parse_args()


def measure_image(path: Path) -> dict[str, float | int | str]:
    grayscale = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

    if grayscale is None:
        raise RuntimeError(f"Could not read image: {path}")

    threshold_value, binary_mask = cv2.threshold(
        grayscale,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    count, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary_mask,
        connectivity=8,
    )

    image_height, image_width = grayscale.shape
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
        raise RuntimeError(f"No gauge block detected in {path}")

    _, component_id = max(candidates)

    x = int(stats[component_id, cv2.CC_STAT_LEFT])
    width = int(stats[component_id, cv2.CC_STAT_WIDTH])

    sample_start = x + round(width * 0.30)
    sample_end = x + round(width * 0.70)

    spans: list[int] = []

    for column in range(sample_start, sample_end):
        positions = np.flatnonzero(labels[:, column] == component_id)

        if positions.size >= 2:
            spans.append(int(positions[-1] - positions[0] + 1))

    if not spans:
        raise RuntimeError(f"No valid spans found in {path}")

    span_array = np.asarray(spans, dtype=np.float64)

    return {
        "filename": path.name,
        "sha256": sha256(path.read_bytes()).hexdigest(),
        "otsu_threshold": float(threshold_value),
        "columns_evaluated": len(spans),
        "median_span_px": float(np.median(span_array)),
        "mean_span_px": float(np.mean(span_array)),
        "within_image_sd_px": float(np.std(span_array, ddof=1)),
        "minimum_span_px": int(np.min(span_array)),
        "maximum_span_px": int(np.max(span_array)),
    }


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results = [measure_image(path) for path in args.images]
    mean_spans = np.asarray(
        [float(result["mean_span_px"]) for result in results],
        dtype=np.float64,
    )

    overall_mean_px = float(np.mean(mean_spans))
    between_image_sd_px = float(np.std(mean_spans, ddof=1))
    peak_to_peak_px = float(np.ptp(mean_spans))

    inches_per_pixel = CERTIFIED_LENGTH_IN / overall_mean_px
    between_image_sd_in = between_image_sd_px * inches_per_pixel
    peak_to_peak_in = peak_to_peak_px * inches_per_pixel

    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")
    csv_path = args.output_dir / (f"fixed_setup_repeatability_{timestamp}.csv")
    report_path = args.output_dir / (f"fixed_setup_repeatability_{timestamp}.txt")

    fieldnames = list(results[0].keys())

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    report_lines = [
        "CaseMetrology Fixed-Setup Acquisition Repeatability",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Images evaluated: {len(results)}",
        f"Certified gauge-block length: {CERTIFIED_LENGTH_IN:.7f} in",
        "",
        "=== BETWEEN-IMAGE RESULTS ===",
        f"Overall mean span: {overall_mean_px:.6f} px",
        f"Between-image standard deviation: {between_image_sd_px:.6f} px",
        f"Peak-to-peak variation: {peak_to_peak_px:.6f} px",
        f"Calculated inches per pixel: {inches_per_pixel:.9f} in/px",
        f"Between-image standard deviation: {between_image_sd_in:.9f} in",
        f"Peak-to-peak variation: {peak_to_peak_in:.9f} in",
        "",
        "Interpretation:",
        "  This evaluates repeated image acquisition with the gauge block,",
        "  camera, lens, lighting, and fixture left undisturbed.",
        "  It does not evaluate removal-and-replacement repeatability,",
        "  dimensional accuracy, temperature effects, or final uncertainty.",
        "",
        f"Detailed CSV: {csv_path}",
    ]

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print("\n".join(report_lines))
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
