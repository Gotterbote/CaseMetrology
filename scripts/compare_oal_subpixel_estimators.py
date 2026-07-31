#!/usr/bin/env python3
"""Compare mask-based and grayscale-subpixel OAL estimators on Trials 03/05."""

from __future__ import annotations

import argparse
import csv
import hashlib
import statistics
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.diagnostics.topdown_oal_subpixel_overlay import (  # noqa: E402
    draw_topdown_oal_subpixel_overlay,
)
from src.measurement.topdown_oal import measure_topdown_oal  # noqa: E402
from src.measurement.topdown_oal_geometry import (  # noqa: E402
    measure_topdown_oal_geometry,
)
from src.measurement.topdown_oal_subpixel import (  # noqa: E402
    SubpixelEdgeDiagnostics,
    measure_topdown_oal_subpixel,
)


@dataclass(frozen=True)
class _Record:
    trial: str
    group: str
    capture: str
    mask_path: Path
    image_path: Path


def _git_value(repo_root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _records(repo_root: Path) -> list[_Record]:
    trial_03_root = repo_root / "data/oal_real/2026-07-31_trial_03_static"
    trial_05_root = repo_root / (
        "data/oal_real/2026-07-31_trial_05_controlled_orientation"
    )

    records: list[_Record] = []
    for mask_path in sorted((trial_03_root / "analysis/masks").glob("*.png")):
        cycle = mask_path.stem.removeprefix("cycle_").removesuffix("_mask")
        image_path = trial_03_root / "images" / f"static_cycle_{cycle}.png"
        records.append(
            _Record(
                trial="trial_03_static",
                group="static",
                capture=mask_path.stem,
                mask_path=mask_path,
                image_path=image_path,
            )
        )

    trial_05_masks = trial_05_root / "analysis/revised_controlled_orientation/masks"
    for mask_path in sorted(trial_05_masks.glob("*/*.png")):
        group = mask_path.parent.name
        capture_name = mask_path.stem.removesuffix("_mask")
        image_path = trial_05_root / "images" / group / f"{capture_name}.png"
        records.append(
            _Record(
                trial="trial_05_controlled_orientation",
                group=group,
                capture=mask_path.stem,
                mask_path=mask_path,
                image_path=image_path,
            )
        )
    return records


def _float(value: float | None) -> str:
    return "" if value is None else f"{value:.9f}"


def _diagnostic_value(
    diagnostic: SubpixelEdgeDiagnostics | None,
    field: str,
) -> str:
    if diagnostic is None:
        return ""
    value = getattr(diagnostic, field)
    if isinstance(value, float):
        return f"{value:.9f}"
    return str(value)


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


def _values(rows: list[dict[str, str]], field: str) -> list[float]:
    return [float(row[field]) for row in rows if row[field]]


def _median_text(values: list[float]) -> tuple[float | None, str]:
    if not values:
        return None, "NA"
    median = statistics.median(values)
    return median, f"{median:.9f}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/oal_real/2026-07-31_subpixel_estimator_comparison"),
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
            f"Expected 27 image/mask pairs (10 Trial 03 + 17 Trial 05); "
            f"found {len(records)}."
        )

    missing = [
        path
        for record in records
        for path in (record.mask_path, record.image_path)
        if not path.is_file()
    ]
    if missing:
        joined = "\n".join(str(path) for path in missing)
        raise RuntimeError(f"Required source files are missing:\n{joined}")

    rows: list[dict[str, str]] = []
    overlay_paths: dict[str, list[Path]] = defaultdict(list)

    for record in records:
        mask = cv2.imread(str(record.mask_path), cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(str(record.image_path), cv2.IMREAD_UNCHANGED)
        if mask is None:
            raise RuntimeError(f"Could not read mask: {record.mask_path}")
        if image is None:
            raise RuntimeError(f"Could not read source image: {record.image_path}")

        estimator_kwargs = {"minimum_fixture_width_ratio": 0.0}
        baseline = measure_topdown_oal(mask, **estimator_kwargs)
        binary_geometry = measure_topdown_oal_geometry(mask, **estimator_kwargs)
        subpixel = measure_topdown_oal_subpixel(
            image,
            mask,
            **estimator_kwargs,
        )

        relative_mask = record.mask_path.relative_to(repo_root)
        relative_image = record.image_path.relative_to(repo_root)
        overlay_dir = overlay_root / record.trial / record.group
        overlay_dir.mkdir(parents=True, exist_ok=True)
        overlay_path = overlay_dir / f"{record.capture}_subpixel_overlay.png"
        overlay = draw_topdown_oal_subpixel_overlay(
            image,
            mask,
            subpixel,
            baseline=baseline,
            binary_geometry=binary_geometry,
            label=f"{record.trial} / {record.group} / {record.capture}",
        )
        cv2.imwrite(str(overlay_path), overlay)
        overlay_paths[record.trial].append(overlay_path)

        subpixel_minus_baseline = None
        subpixel_minus_geometry = None
        if baseline.length_pixels is not None and subpixel.length_pixels is not None:
            subpixel_minus_baseline = subpixel.length_pixels - baseline.length_pixels
        if (
            binary_geometry.length_pixels is not None
            and subpixel.length_pixels is not None
        ):
            subpixel_minus_geometry = (
                subpixel.length_pixels - binary_geometry.length_pixels
            )

        row = {
            "trial": record.trial,
            "orientation_group": record.group,
            "capture": record.capture,
            "source_image_path": str(relative_image),
            "mask_path": str(relative_mask),
            "baseline_passed": str(baseline.passed),
            "baseline_failure_reason": baseline.failure_reason or "",
            "baseline_length_pixels": _float(baseline.length_pixels),
            "binary_geometry_passed": str(binary_geometry.passed),
            "binary_geometry_failure_reason": binary_geometry.failure_reason or "",
            "binary_geometry_length_pixels": _float(binary_geometry.length_pixels),
            "subpixel_passed": str(subpixel.passed),
            "subpixel_failure_reason": subpixel.failure_reason or "",
            "subpixel_length_pixels": _float(subpixel.length_pixels),
            "subpixel_minus_baseline_pixels": _float(subpixel_minus_baseline),
            "subpixel_minus_binary_geometry_pixels": _float(subpixel_minus_geometry),
            "subpixel_angle_degrees": _float(subpixel.angle_degrees),
            "sidewall_angle_difference_degrees": _float(
                subpixel.sidewall_angle_difference_degrees
            ),
            "end_line_angle_difference_degrees": _float(
                subpixel.end_line_angle_difference_degrees
            ),
            "end_min_perpendicular_error_degrees": _float(
                subpixel.end_min_perpendicular_error_degrees
            ),
            "end_max_perpendicular_error_degrees": _float(
                subpixel.end_max_perpendicular_error_degrees
            ),
            "sidewall_min_rms_pixels": _line_value(
                subpixel.sidewall_min_segment, "rms_pixels"
            ),
            "sidewall_max_rms_pixels": _line_value(
                subpixel.sidewall_max_segment, "rms_pixels"
            ),
            "end_min_rms_pixels": _line_value(subpixel.end_min_segment, "rms_pixels"),
            "end_max_rms_pixels": _line_value(subpixel.end_max_segment, "rms_pixels"),
            "sidewall_min_acceptance_fraction": _diagnostic_value(
                subpixel.sidewall_min_diagnostics, "accepted_fraction"
            ),
            "sidewall_max_acceptance_fraction": _diagnostic_value(
                subpixel.sidewall_max_diagnostics, "accepted_fraction"
            ),
            "end_min_acceptance_fraction": _diagnostic_value(
                subpixel.end_min_diagnostics, "accepted_fraction"
            ),
            "end_max_acceptance_fraction": _diagnostic_value(
                subpixel.end_max_diagnostics, "accepted_fraction"
            ),
            "sidewall_min_mean_contrast": _diagnostic_value(
                subpixel.sidewall_min_diagnostics, "mean_contrast"
            ),
            "sidewall_max_mean_contrast": _diagnostic_value(
                subpixel.sidewall_max_diagnostics, "mean_contrast"
            ),
            "end_min_mean_contrast": _diagnostic_value(
                subpixel.end_min_diagnostics, "mean_contrast"
            ),
            "end_max_mean_contrast": _diagnostic_value(
                subpixel.end_max_diagnostics, "mean_contrast"
            ),
            "diagnostic_flags": ";".join(subpixel.diagnostic_flags),
            "overlay_path": str(overlay_path.relative_to(repo_root)),
        }
        rows.append(row)

    results_path = output_dir / "oal_subpixel_estimator_comparison_results.csv"
    with results_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for trial, paths in overlay_paths.items():
        _make_contact_sheet(
            paths,
            output_dir / f"{trial}_subpixel_comparison_contact_sheet.png",
        )

    lines = [
        "Fixtureless OAL Grayscale Subpixel Estimator Comparison",
        "",
        f"git_commit = {source_commit}",
        f"git_status_short_before_analysis = {source_status}",
        f"source_pair_count = {len(rows)}",
        "accepted_masks_reused_without_resegmentation = true",
        "original_grayscale_source_images_used = true",
        "fixture_width_validation_gate_disabled = true",
        "comparison_scope = endpoint estimator on previously accepted objects",
        "baseline_estimator = PCA axis plus extreme binary-mask pixels",
        "binary_geometry_estimator = robust lines fitted to binary-mask boundaries",
        "candidate_estimator = robust lines fitted to subpixel grayscale edges",
        "",
    ]

    estimator_fields = (
        ("baseline", "baseline_length_pixels"),
        ("binary_geometry", "binary_geometry_length_pixels"),
        ("subpixel", "subpixel_length_pixels"),
    )
    for trial in ("trial_03_static", "trial_05_controlled_orientation"):
        trial_rows = [row for row in rows if row["trial"] == trial]
        lines.append(trial)
        for label, field in estimator_fields:
            lines.extend(_format_stats(label, _values(trial_rows, field)))
        lines.append("")

    trial_05_rows = [
        row for row in rows if row["trial"] == "trial_05_controlled_orientation"
    ]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in trial_05_rows:
        grouped[row["orientation_group"]].append(row)

    median_sets: dict[str, list[float]] = {
        "baseline": [],
        "binary_geometry": [],
        "subpixel": [],
    }
    lines.append("trial_05_orientation_group_medians")
    for group in sorted(grouped):
        group_rows = grouped[group]
        baseline_median, baseline_text = _median_text(
            _values(group_rows, "baseline_length_pixels")
        )
        geometry_median, geometry_text = _median_text(
            _values(group_rows, "binary_geometry_length_pixels")
        )
        subpixel_median, subpixel_text = _median_text(
            _values(group_rows, "subpixel_length_pixels")
        )
        for key, median in (
            ("baseline", baseline_median),
            ("binary_geometry", geometry_median),
            ("subpixel", subpixel_median),
        ):
            if median is not None:
                median_sets[key].append(median)

        lines.append(
            f"  {group}: captures={len(group_rows)}, "
            f"baseline={baseline_text}, binary_geometry={geometry_text}, "
            f"subpixel={subpixel_text}"
        )
        failed = [
            row
            for row in group_rows
            if row["baseline_passed"] != "True"
            or row["binary_geometry_passed"] != "True"
            or row["subpixel_passed"] != "True"
        ]
        for row in failed:
            lines.append(
                f"    failure {row['capture']}: "
                f"baseline={row['baseline_failure_reason'] or 'none'}; "
                f"binary_geometry={row['binary_geometry_failure_reason'] or 'none'}; "
                f"subpixel={row['subpixel_failure_reason'] or 'none'}"
            )

    lines.extend(["", "trial_05_range_among_orientation_group_medians"])
    for key in ("baseline", "binary_geometry", "subpixel"):
        values = median_sets[key]
        range_text = (
            f"{max(values) - min(values):.9f}" if len(values) >= 2 else "not_available"
        )
        lines.append(f"  {key}_groups_with_passing_values = {len(values)}")
        lines.append(f"  {key}_pixels = {range_text}")

    failed_rows = [
        row
        for row in rows
        if row["baseline_passed"] != "True"
        or row["binary_geometry_passed"] != "True"
        or row["subpixel_passed"] != "True"
    ]
    flagged_rows = [row for row in rows if row["diagnostic_flags"]]
    lines.extend(
        [
            "",
            f"failed_triplet_count = {len(failed_rows)}",
            f"subpixel_flagged_capture_count = {len(flagged_rows)}",
            "",
            "Interpretation rule:",
            "Do not accept the subpixel estimator from numerical range alone.",
            "Review every generated overlay and all edge-fit diagnostics.",
        ]
    )

    summary_path = output_dir / "oal_subpixel_estimator_comparison_summary.txt"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _write_manifest(output_dir)

    print(f"Results: {results_path.relative_to(repo_root)}")
    print(f"Summary: {summary_path.relative_to(repo_root)}")
    print(f"Overlays: {overlay_root.relative_to(repo_root)}")
    print(f"Rows: {len(rows)}")
    print(f"Failures: {len(failed_rows)}")
    print(f"Subpixel flagged captures: {len(flagged_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
