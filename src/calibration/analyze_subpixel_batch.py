"""Batch subpixel repeatability analysis for gauge-block image sequences."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

DEFAULT_CERTIFIED_LENGTH_IN = 1.0000024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the validated subpixel gauge-block analysis across an image "
            "sequence and calculate between-image repeatability."
        )
    )
    parser.add_argument(
        "images",
        nargs="+",
        type=Path,
        help="Gauge-block images to analyze.",
    )
    parser.add_argument(
        "--test-name",
        required=True,
        help=("Meaningful test name, such as " "'lexan_repositioning_repeatability'."),
    )
    parser.add_argument(
        "--mode",
        choices=["fixed_setup", "repositioning"],
        required=True,
        help="Experimental condition represented by the image sequence.",
    )
    parser.add_argument(
        "--certified-length-in",
        type=float,
        default=DEFAULT_CERTIFIED_LENGTH_IN,
        help=(
            "Certified gauge-block length in inches "
            f"(default: {DEFAULT_CERTIFIED_LENGTH_IN:.7f})."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("measurements/calibration"),
        help="Directory for the CSV and summary report.",
    )
    return parser.parse_args()


def sanitize_name(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip())
    sanitized = sanitized.strip("_").lower()

    if not sanitized:
        raise ValueError("The test name contains no usable characters.")

    return sanitized


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def parse_float(pattern: str, output: str, field_name: str) -> float:
    match = re.search(pattern, output)

    if match is None:
        raise RuntimeError(f"Could not parse {field_name} from analyzer output.")

    return float(match.group(1))


def parse_integer(pattern: str, output: str, field_name: str) -> int:
    match = re.search(pattern, output)

    if match is None:
        raise RuntimeError(f"Could not parse {field_name} from analyzer output.")

    return int(match.group(1))


def get_git_state() -> tuple[str, bool]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )

    return commit, dirty


def analyze_image(path: Path) -> dict[str, str | int | float]:
    if not path.exists():
        raise RuntimeError(f"Image does not exist: {path}")

    result = subprocess.run(
        [
            sys.executable,
            "src/calibration/analyze_subpixel_gauge_block.py",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    output = result.stdout

    return {
        "filename": path.name,
        "relative_path": str(path),
        "sha256": sha256_file(path),
        "valid_columns": parse_integer(
            r"Valid columns evaluated:\s+(\d+)",
            output,
            "valid columns",
        ),
        "mean_span_px": parse_float(
            r"Mean subpixel span:\s+([0-9.]+)",
            output,
            "mean subpixel span",
        ),
        "median_span_px": parse_float(
            r"Median subpixel span:\s+([0-9.]+)",
            output,
            "median subpixel span",
        ),
        "within_image_sd_px": parse_float(
            r"Subpixel span SD across columns:\s+([0-9.]+)",
            output,
            "within-image standard deviation",
        ),
        "top_edge_angle_deg": parse_float(
            r"Top-edge fitted angle:\s+(-?[0-9.]+)",
            output,
            "top-edge angle",
        ),
        "bottom_edge_angle_deg": parse_float(
            r"Bottom-edge fitted angle:\s+(-?[0-9.]+)",
            output,
            "bottom-edge angle",
        ),
        "fitted_center_span_px": parse_float(
            r"Fitted center span:\s+([0-9.]+)",
            output,
            "fitted center span",
        ),
    }


def main() -> None:
    args = parse_args()

    if len(args.images) < 2:
        raise ValueError("At least two images are required.")

    if args.certified_length_in <= 0:
        raise ValueError("--certified-length-in must be positive.")

    test_name = sanitize_name(args.test_name)
    git_commit, git_dirty = get_git_state()

    rows = [analyze_image(path) for path in args.images]

    spans = np.asarray(
        [float(row["fitted_center_span_px"]) for row in rows],
        dtype=np.float64,
    )
    top_angles = np.asarray(
        [float(row["top_edge_angle_deg"]) for row in rows],
        dtype=np.float64,
    )
    bottom_angles = np.asarray(
        [float(row["bottom_edge_angle_deg"]) for row in rows],
        dtype=np.float64,
    )

    mean_span_px = float(np.mean(spans))
    median_span_px = float(np.median(spans))
    sample_sd_px = float(np.std(spans, ddof=1))
    minimum_span_px = float(np.min(spans))
    maximum_span_px = float(np.max(spans))
    peak_to_peak_px = float(np.ptp(spans))

    inches_per_pixel = args.certified_length_in / mean_span_px
    sample_sd_in = sample_sd_px * inches_per_pixel
    peak_to_peak_in = peak_to_peak_px * inches_per_pixel

    for row in rows:
        span_px = float(row["fitted_center_span_px"])
        row["deviation_from_mean_px"] = span_px - mean_span_px
        row["deviation_from_mean_in"] = (span_px - mean_span_px) * inches_per_pixel

    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S")

    csv_path = args.output_dir / f"{test_name}_{timestamp}.csv"
    report_path = args.output_dir / f"{test_name}_{timestamp}.txt"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=list(rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(rows)

    if args.mode == "fixed_setup":
        interpretation = [
            "  This evaluates repeated image acquisition and subpixel",
            "  measurement with the gauge block, camera, lens, lighting,",
            "  and fixture left undisturbed.",
        ]
    else:
        interpretation = [
            "  This evaluates combined gauge-block removal, replacement,",
            "  fixture seating, image acquisition, and subpixel measurement",
            "  repeatability.",
        ]

    report_lines = [
        "CaseMetrology Subpixel Batch Repeatability Analysis",
        f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Test name: {test_name}",
        f"Test mode: {args.mode}",
        f"Images evaluated: {len(rows)}",
        f"Certified gauge-block length: {args.certified_length_in:.7f} in",
        f"Git commit: {git_commit}",
        f"Git working tree dirty: {git_dirty}",
        "",
        "=== BETWEEN-IMAGE RESULTS ===",
        f"Mean fitted span: {mean_span_px:.6f} px",
        f"Median fitted span: {median_span_px:.6f} px",
        f"Minimum fitted span: {minimum_span_px:.6f} px",
        f"Maximum fitted span: {maximum_span_px:.6f} px",
        f"Between-image standard deviation: {sample_sd_px:.6f} px",
        f"Peak-to-peak variation: {peak_to_peak_px:.6f} px",
        f"Calculated inches per pixel: {inches_per_pixel:.9f} in/px",
        f"Between-image standard deviation: {sample_sd_in:.9f} in",
        f"Peak-to-peak variation: {peak_to_peak_in:.9f} in",
        "",
        "=== ALIGNMENT RESULTS ===",
        f"Mean top-edge angle: {float(np.mean(top_angles)):.6f} degrees",
        ("Mean bottom-edge angle: " f"{float(np.mean(bottom_angles)):.6f} degrees"),
        (
            "Mean edge-angle difference: "
            f"{float(np.mean(bottom_angles - top_angles)):.6f} degrees"
        ),
        "",
        "Interpretation:",
        *interpretation,
        "",
        "  These results do not by themselves establish dimensional",
        "  accuracy, temperature compensation, operator reproducibility,",
        "  or total measurement uncertainty.",
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
