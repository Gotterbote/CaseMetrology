#!/usr/bin/env python3
"""Compare PCA-extreme and geometry-fit OAL estimators on Trials 03 and 05."""

from __future__ import annotations

import argparse
import csv
import hashlib
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

# The script is executable by path, so repository-root bootstrapping must occur
# before importing the local ``src`` package.
from src.diagnostics.topdown_oal_geometry_overlay import (  # noqa: E402
    draw_topdown_oal_geometry_overlay,
)
from src.measurement.topdown_oal import measure_topdown_oal  # noqa: E402
from src.measurement.topdown_oal_geometry import (  # noqa: E402
    measure_topdown_oal_geometry,
)


def _git_value(repo_root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _records(repo_root: Path) -> list[tuple[str, str, Path]]:
    trial_03 = repo_root / "data/oal_real/2026-07-31_trial_03_static/analysis/masks"
    trial_05 = repo_root / (
        "data/oal_real/2026-07-31_trial_05_controlled_orientation/analysis/"
        "revised_controlled_orientation/masks"
    )

    records: list[tuple[str, str, Path]] = []
    for path in sorted(trial_03.glob("*.png")):
        records.append(("trial_03_static", "static", path))
    for path in sorted(trial_05.glob("*/*.png")):
        records.append(("trial_05_controlled_orientation", path.parent.name, path))
    return records


def _float(value: float | None) -> str:
    return "" if value is None else f"{value:.9f}"


def _line_value(segment: Any, field: str) -> str:
    if segment is None:
        return ""
    value = getattr(segment, field)
    if isinstance(value, float):
        return f"{value:.9f}"
    return str(value)


def _summary_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {}
    return {
        "count": float(len(values)),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "sd": statistics.stdev(values) if len(values) > 1 else 0.0,
        "minimum": min(values),
        "maximum": max(values),
        "range": max(values) - min(values),
    }


def _format_stats(name: str, values: list[float]) -> list[str]:
    stats = _summary_stats(values)
    if not stats:
        return [f"{name}: no passing measurements"]
    return [
        f"{name}:",
        f"  count = {int(stats['count'])}",
        f"  mean_pixels = {stats['mean']:.9f}",
        f"  median_pixels = {stats['median']:.9f}",
        f"  sd_pixels = {stats['sd']:.9f}",
        f"  min_pixels = {stats['minimum']:.9f}",
        f"  max_pixels = {stats['maximum']:.9f}",
        f"  range_pixels = {stats['range']:.9f}",
    ]


def _make_contact_sheet(
    overlay_paths: list[Path],
    output_path: Path,
    *,
    columns: int = 3,
    tile_width: int = 520,
) -> None:
    images: list[np.ndarray] = []
    for path in overlay_paths:
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            continue
        scale = tile_width / image.shape[1]
        resized = cv2.resize(
            image,
            (tile_width, int(round(image.shape[0] * scale))),
            interpolation=cv2.INTER_AREA,
        )
        images.append(resized)
    if not images:
        return

    tile_height = max(image.shape[0] for image in images)
    rows = (len(images) + columns - 1) // columns
    sheet = np.zeros((rows * tile_height, columns * tile_width, 3), dtype=np.uint8)
    for index, image in enumerate(images):
        row, column = divmod(index, columns)
        y = row * tile_height
        x = column * tile_width
        sheet[y : y + image.shape[0], x : x + image.shape[1]] = image
    cv2.imwrite(str(output_path), sheet)


def _write_manifest(output_dir: Path) -> None:
    manifest_path = output_dir / "sha256_manifest.txt"
    lines: list[str] = []
    for path in sorted(output_dir.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(output_dir)}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/oal_real/2026-07-31_geometry_estimator_comparison"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    source_commit = _git_value(repo_root, "rev-parse", "HEAD")
    source_status = _git_value(repo_root, "status", "--short") or "clean"

    output_dir = (
        args.output_dir
        if args.output_dir.is_absolute()
        else repo_root / args.output_dir
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    overlay_root = output_dir / "overlays"
    overlay_root.mkdir(parents=True, exist_ok=True)

    records = _records(repo_root)
    if len(records) != 27:
        raise RuntimeError(
            f"Expected 27 masks (10 Trial 03 + 17 Trial 05); found {len(records)}."
        )

    rows: list[dict[str, str]] = []
    overlay_paths: dict[str, list[Path]] = defaultdict(list)

    for trial, group, mask_path in records:
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            raise RuntimeError(f"Could not read mask: {mask_path}")

        baseline = measure_topdown_oal(mask)
        geometry = measure_topdown_oal_geometry(mask)
        difference = None
        if baseline.length_pixels is not None and geometry.length_pixels is not None:
            difference = geometry.length_pixels - baseline.length_pixels

        relative_mask = mask_path.relative_to(repo_root)
        overlay_dir = overlay_root / trial / group
        overlay_dir.mkdir(parents=True, exist_ok=True)
        overlay_path = overlay_dir / f"{mask_path.stem}_comparison_overlay.png"
        overlay = draw_topdown_oal_geometry_overlay(
            mask,
            geometry,
            baseline=baseline,
            label=f"{trial} / {group} / {mask_path.stem}",
        )
        cv2.imwrite(str(overlay_path), overlay)
        overlay_paths[trial].append(overlay_path)

        rows.append(
            {
                "trial": trial,
                "orientation_group": group,
                "capture": mask_path.stem,
                "mask_path": str(relative_mask),
                "baseline_passed": str(baseline.passed),
                "baseline_failure_reason": baseline.failure_reason or "",
                "baseline_length_pixels": _float(baseline.length_pixels),
                "geometry_passed": str(geometry.passed),
                "geometry_failure_reason": geometry.failure_reason or "",
                "geometry_length_pixels": _float(geometry.length_pixels),
                "geometry_minus_baseline_pixels": _float(difference),
                "geometry_angle_degrees": _float(geometry.angle_degrees),
                "case_width_pixels": _float(geometry.case_width_pixels),
                "fixture_width_pixels": _float(geometry.fixture_width_pixels),
                "fixture_width_ratio": _float(geometry.fixture_width_ratio),
                "sidewall_angle_difference_degrees": _float(
                    geometry.sidewall_angle_difference_degrees
                ),
                "end_line_angle_difference_degrees": _float(
                    geometry.end_line_angle_difference_degrees
                ),
                "end_min_perpendicular_error_degrees": _float(
                    geometry.end_min_perpendicular_error_degrees
                ),
                "end_max_perpendicular_error_degrees": _float(
                    geometry.end_max_perpendicular_error_degrees
                ),
                "sidewall_min_rms_pixels": _line_value(
                    geometry.sidewall_min_segment, "rms_pixels"
                ),
                "sidewall_max_rms_pixels": _line_value(
                    geometry.sidewall_max_segment, "rms_pixels"
                ),
                "end_min_rms_pixels": _line_value(
                    geometry.end_min_segment, "rms_pixels"
                ),
                "end_max_rms_pixels": _line_value(
                    geometry.end_max_segment, "rms_pixels"
                ),
                "sidewall_min_inlier_fraction": _line_value(
                    geometry.sidewall_min_segment, "inlier_fraction"
                ),
                "sidewall_max_inlier_fraction": _line_value(
                    geometry.sidewall_max_segment, "inlier_fraction"
                ),
                "end_min_inlier_fraction": _line_value(
                    geometry.end_min_segment, "inlier_fraction"
                ),
                "end_max_inlier_fraction": _line_value(
                    geometry.end_max_segment, "inlier_fraction"
                ),
                "diagnostic_flags": ";".join(geometry.diagnostic_flags),
                "overlay_path": str(overlay_path.relative_to(repo_root)),
            }
        )

    results_path = output_dir / "oal_estimator_comparison_results.csv"
    with results_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for trial, paths in overlay_paths.items():
        _make_contact_sheet(
            paths,
            output_dir / f"{trial}_comparison_contact_sheet.png",
        )

    lines = [
        "Fixtureless OAL Geometry Estimator Comparison",
        "",
        f"git_commit = {source_commit}",
        f"git_status_short_before_analysis = {source_status}",
        f"source_mask_count = {len(rows)}",
        "source_masks_reused_without_resegmentation = true",
        "baseline_estimator = PCA axis plus extreme mask pixels",
        "candidate_estimator = robust sidewalls plus fitted end faces",
        "",
    ]

    for trial in ("trial_03_static", "trial_05_controlled_orientation"):
        trial_rows = [row for row in rows if row["trial"] == trial]
        baseline_values = [
            float(row["baseline_length_pixels"])
            for row in trial_rows
            if row["baseline_length_pixels"]
        ]
        geometry_values = [
            float(row["geometry_length_pixels"])
            for row in trial_rows
            if row["geometry_length_pixels"]
        ]
        lines.append(trial)
        lines.extend(_format_stats("baseline", baseline_values))
        lines.extend(_format_stats("geometry", geometry_values))
        lines.append("")

    trial_05_rows = [
        row for row in rows if row["trial"] == "trial_05_controlled_orientation"
    ]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in trial_05_rows:
        grouped[row["orientation_group"]].append(row)

    baseline_medians: list[float] = []
    geometry_medians: list[float] = []
    lines.append("trial_05_orientation_group_medians")
    for group in sorted(grouped):
        group_rows = grouped[group]
        baseline_group = [
            float(row["baseline_length_pixels"])
            for row in group_rows
            if row["baseline_length_pixels"]
        ]
        geometry_group = [
            float(row["geometry_length_pixels"])
            for row in group_rows
            if row["geometry_length_pixels"]
        ]
        baseline_median = statistics.median(baseline_group)
        geometry_median = statistics.median(geometry_group)
        baseline_medians.append(baseline_median)
        geometry_medians.append(geometry_median)
        lines.append(
            f"  {group}: baseline={baseline_median:.9f}, "
            f"geometry={geometry_median:.9f}, "
            f"delta={geometry_median - baseline_median:.9f}"
        )

    lines.extend(
        [
            "",
            "trial_05_range_among_orientation_group_medians",
            f"  baseline_pixels = {max(baseline_medians) - min(baseline_medians):.9f}",
            f"  geometry_pixels = {max(geometry_medians) - min(geometry_medians):.9f}",
        ]
    )

    ninety_rows = [row for row in trial_05_rows if "090" in row["orientation_group"]]
    if len(ninety_rows) > 2:
        ninety_baseline = [float(row["baseline_length_pixels"]) for row in ninety_rows]
        ninety_median = statistics.median(ninety_baseline)
        candidate = max(
            ninety_rows,
            key=lambda row: abs(float(row["baseline_length_pixels"]) - ninety_median),
        )
        lines.extend(
            [
                "",
                "algorithmic_90_degree_sensitivity_candidate",
                (
                    "  selection_rule = largest absolute baseline deviation "
                    "from 90-degree median"
                ),
                f"  capture = {candidate['capture']}",
                f"  baseline_length_pixels = {candidate['baseline_length_pixels']}",
                f"  geometry_length_pixels = {candidate['geometry_length_pixels']}",
                f"  geometry_flags = {candidate['diagnostic_flags'] or 'none'}",
                (
                    "  note = retained in all primary statistics; "
                    "not automatically excluded"
                ),
            ]
        )

    failure_rows = [
        row
        for row in rows
        if row["baseline_passed"] != "True" or row["geometry_passed"] != "True"
    ]
    flagged_rows = [row for row in rows if row["diagnostic_flags"]]
    lines.extend(
        [
            "",
            f"failed_pair_count = {len(failure_rows)}",
            f"geometry_flagged_capture_count = {len(flagged_rows)}",
            "",
            "Interpretation rule:",
            "Do not accept the geometry estimator from numerical range alone.",
            "All generated overlays and residual diagnostics require visual review.",
        ]
    )

    summary_path = output_dir / "oal_estimator_comparison_summary.txt"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _write_manifest(output_dir)

    print(f"Results: {results_path.relative_to(repo_root)}")
    print(f"Summary: {summary_path.relative_to(repo_root)}")
    print(f"Overlays: {overlay_root.relative_to(repo_root)}")
    print(f"Rows: {len(rows)}")
    print(f"Failures: {len(failure_rows)}")
    print(f"Geometry flagged captures: {len(flagged_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
