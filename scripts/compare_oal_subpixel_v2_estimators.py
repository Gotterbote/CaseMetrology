#!/usr/bin/env python3
"""Evaluate mask-anchored subpixel OAL Version 2 on Trials 03 and 05."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from src.diagnostics.topdown_oal_subpixel_v2_overlay import (  # noqa: E402
    draw_topdown_oal_subpixel_v2_overlay,
)
from src.measurement.topdown_oal import measure_topdown_oal  # noqa: E402
from src.measurement.topdown_oal_geometry import (  # noqa: E402
    measure_topdown_oal_geometry,
)
from src.measurement.topdown_oal_subpixel import (  # noqa: E402
    measure_topdown_oal_subpixel,
)
from src.measurement.topdown_oal_subpixel_v2 import (  # noqa: E402
    IntensityCrossingProfile,
    SubpixelV2EdgeDiagnostics,
    TopDownSubpixelV2OALResult,
    measure_topdown_oal_subpixel_v2,
)


@dataclass(frozen=True)
class _Record:
    trial: str
    group: str
    capture: str
    mask_path: Path
    image_path: Path


PRIMARY_CONFIG: dict[str, Any] = {
    "profile_half_length_pixels": 6.0,
    "profile_step_pixels": 0.25,
    "interior_plateau_limit_pixels": [-6.0, -2.0],
    "exterior_plateau_limit_pixels": [2.0, 6.0],
    "normalized_crossing": 0.50,
    "minimum_local_contrast": 30.0,
    "maximum_anchor_distance_pixels": 3.0,
    "maximum_crossing_distance_pixels": 3.0,
    "sidewall_sample_count": 72,
    "end_sample_count": 41,
    "minimum_sidewall_profile_count": 25,
    "minimum_end_profile_count": 12,
    "end_face_transverse_fraction": 0.30,
}

PCA_STATIC_SD_BENCHMARK = 0.050349452
PCA_ORIENTATION_RANGE_BENCHMARK = 1.752720470
VERSION_2_TARGET_ORIENTATION_RANGE = 1.402176376


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
        records.append(
            _Record(
                trial="trial_03_static",
                group="static",
                capture=mask_path.stem,
                mask_path=mask_path,
                image_path=trial_03_root / "images" / f"static_cycle_{cycle}.png",
            )
        )

    mask_root = trial_05_root / "analysis/revised_controlled_orientation/masks"
    for mask_path in sorted(mask_root.glob("*/*.png")):
        group = mask_path.parent.name
        capture_name = mask_path.stem.removesuffix("_mask")
        records.append(
            _Record(
                trial="trial_05_controlled_orientation",
                group=group,
                capture=mask_path.stem,
                mask_path=mask_path,
                image_path=trial_05_root / "images" / group / f"{capture_name}.png",
            )
        )
    return records


def _float(value: float | None) -> str:
    return "" if value is None else f"{value:.9f}"


def _diagnostic_value(diagnostic: SubpixelV2EdgeDiagnostics | None, field: str) -> str:
    if diagnostic is None:
        return ""
    value = getattr(diagnostic, field)
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


def _values(rows: list[dict[str, str]], field: str) -> list[float]:
    return [float(row[field]) for row in rows if row[field]]


def _median(values: list[float]) -> float | None:
    return None if not values else statistics.median(values)


def _make_contact_sheet(
    image_paths: list[Path],
    output_path: Path,
    *,
    columns: int = 3,
    tile_width: int = 520,
) -> None:
    images: list[np.ndarray] = []
    for path in image_paths:
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if image is None:
            continue
        scale = tile_width / image.shape[1]
        images.append(
            cv2.resize(
                image,
                (tile_width, int(round(image.shape[0] * scale))),
                interpolation=cv2.INTER_AREA,
            )
        )
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


def _profile_groups(
    result: TopDownSubpixelV2OALResult,
) -> tuple[tuple[str, tuple[IntensityCrossingProfile, ...]], ...]:
    return (
        ("minimum_sidewall", result.sidewall_min_profiles),
        ("maximum_sidewall", result.sidewall_max_profiles),
        ("minimum_end", result.end_min_profiles),
        ("maximum_end", result.end_max_profiles),
    )


def _profile_row(
    record: _Record,
    edge_name: str,
    index: int,
    profile: IntensityCrossingProfile,
) -> dict[str, str]:
    return {
        "trial": record.trial,
        "orientation_group": record.group,
        "capture": record.capture,
        "edge_name": edge_name,
        "profile_index": str(index),
        "accepted": str(profile.accepted),
        "rejection_reason": profile.rejection_reason or "",
        "seed_x": _float(profile.seed_xy[0]),
        "seed_y": _float(profile.seed_xy[1]),
        "anchor_x": "" if profile.anchor_xy is None else _float(profile.anchor_xy[0]),
        "anchor_y": "" if profile.anchor_xy is None else _float(profile.anchor_xy[1]),
        "normal_x": (
            ""
            if profile.outward_normal_xy is None
            else _float(profile.outward_normal_xy[0])
        ),
        "normal_y": (
            ""
            if profile.outward_normal_xy is None
            else _float(profile.outward_normal_xy[1])
        ),
        "mask_anchor_offset_pixels": _float(profile.mask_anchor_offset_pixels),
        "mask_crossing_count": str(profile.mask_crossing_count),
        "interior_intensity": _float(profile.interior_intensity),
        "exterior_intensity": _float(profile.exterior_intensity),
        "contrast": _float(profile.contrast),
        "crossing_offset_pixels": _float(profile.crossing_offset_pixels),
        "crossing_x": (
            "" if profile.crossing_xy is None else _float(profile.crossing_xy[0])
        ),
        "crossing_y": (
            "" if profile.crossing_xy is None else _float(profile.crossing_xy[1])
        ),
        "threshold_crossing_count": str(profile.threshold_crossing_count),
        "monotonicity_fraction": _float(profile.monotonicity_fraction),
    }


def _plot_profile(profile: IntensityCrossingProfile, output_path: Path) -> bool:
    if not profile.offsets_pixels or not profile.normalized_values:
        return False
    width, height = 900, 520
    margin_left, margin_right, margin_top, margin_bottom = 85, 35, 55, 70
    canvas = np.full((height, width, 3), 255, dtype=np.uint8)
    offsets = np.asarray(profile.offsets_pixels, dtype=np.float64)
    values = np.asarray(profile.normalized_values, dtype=np.float64)
    y_min = min(-0.25, float(np.min(values)) - 0.10)
    y_max = max(1.25, float(np.max(values)) + 0.10)

    def map_xy(x_value: float, y_value: float) -> tuple[int, int]:
        x = margin_left + (x_value - float(offsets.min())) / max(
            float(np.ptp(offsets)), 1e-9
        ) * (width - margin_left - margin_right)
        y = margin_top + (y_max - y_value) / max(y_max - y_min, 1e-9) * (
            height - margin_top - margin_bottom
        )
        return int(round(x)), int(round(y))

    for level in (0.0, 0.5, 1.0):
        p1 = map_xy(float(offsets.min()), level)
        p2 = map_xy(float(offsets.max()), level)
        cv2.line(canvas, p1, p2, (215, 215, 215), 1, cv2.LINE_AA)
    p1 = map_xy(0.0, y_min)
    p2 = map_xy(0.0, y_max)
    cv2.line(canvas, p1, p2, (180, 180, 180), 1, cv2.LINE_AA)

    points = [map_xy(float(x), float(y)) for x, y in zip(offsets, values)]
    for first, second in zip(points, points[1:]):
        cv2.line(canvas, first, second, (0, 0, 0), 2, cv2.LINE_AA)
    if profile.crossing_offset_pixels is not None:
        crossing = map_xy(profile.crossing_offset_pixels, 0.5)
        cv2.circle(canvas, crossing, 6, (0, 0, 255), 2, cv2.LINE_AA)

    title = f"{profile.edge_name}: {'accepted' if profile.accepted else profile.rejection_reason}"
    cv2.putText(
        canvas, title, (margin_left, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (0, 0, 0), 2
    )
    cv2.putText(
        canvas,
        "Offset from accepted-mask anchor (px)",
        (300, height - 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.58,
        (0, 0, 0),
        1,
    )
    cv2.putText(
        canvas,
        "Normalized intensity",
        (5, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (0, 0, 0),
        1,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return bool(cv2.imwrite(str(output_path), canvas))


def _write_manifest(output_dir: Path) -> None:
    manifest_path = output_dir / "sha256_manifest.txt"
    lines: list[str] = []
    for path in sorted(output_dir.rglob("*")):
        if path.is_file() and path != manifest_path:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(output_dir)}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_source_manifest(
    records: list[_Record], repo_root: Path, output_dir: Path
) -> None:
    paths = sorted(
        {path for record in records for path in (record.image_path, record.mask_path)}
    )
    lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(repo_root)}"
        for path in paths
    ]
    (output_dir / "source_files.sha256.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/oal_real/2026-07-31_subpixel_v2_estimator_comparison"),
    )
    parser.add_argument("--normalized-crossing", type=float, default=0.50)
    parser.add_argument("--minimum-local-contrast", type=float, default=30.0)
    parser.add_argument("--profile-half-length", type=float, default=6.0)
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
    profile_plot_root = output_dir / "profile_plots"
    overlay_root.mkdir(parents=True, exist_ok=True)
    profile_plot_root.mkdir(parents=True, exist_ok=True)

    config = dict(PRIMARY_CONFIG)
    config["normalized_crossing"] = args.normalized_crossing
    config["minimum_local_contrast"] = args.minimum_local_contrast
    config["profile_half_length_pixels"] = args.profile_half_length
    config["interior_plateau_limit_pixels"] = [-args.profile_half_length, -2.0]
    config["exterior_plateau_limit_pixels"] = [2.0, args.profile_half_length]
    (output_dir / "analysis_configuration.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    records = _records(repo_root)
    if len(records) != 27:
        raise RuntimeError(f"Expected 27 image/mask pairs; found {len(records)}.")
    missing = [
        path
        for record in records
        for path in (record.mask_path, record.image_path)
        if not path.is_file()
    ]
    if missing:
        raise RuntimeError(
            "Required source files are missing:\n" + "\n".join(map(str, missing))
        )

    rows: list[dict[str, str]] = []
    profile_rows: list[dict[str, str]] = []
    overlays_by_trial: dict[str, list[Path]] = defaultdict(list)
    results_by_record: list[tuple[_Record, TopDownSubpixelV2OALResult]] = []
    estimator_kwargs = {"minimum_fixture_width_ratio": 0.0}

    for record in records:
        mask = cv2.imread(str(record.mask_path), cv2.IMREAD_GRAYSCALE)
        image = cv2.imread(str(record.image_path), cv2.IMREAD_UNCHANGED)
        if mask is None or image is None:
            raise RuntimeError(f"Could not read source pair for {record.capture}.")

        baseline = measure_topdown_oal(mask, **estimator_kwargs)
        binary_geometry = measure_topdown_oal_geometry(mask, **estimator_kwargs)
        subpixel_v1 = measure_topdown_oal_subpixel(image, mask, **estimator_kwargs)
        subpixel_v2 = measure_topdown_oal_subpixel_v2(
            image,
            mask,
            **estimator_kwargs,
            **config,
        )
        results_by_record.append((record, subpixel_v2))

        overlay_dir = overlay_root / record.trial / record.group
        overlay_dir.mkdir(parents=True, exist_ok=True)
        overlay_path = overlay_dir / f"{record.capture}_subpixel_v2_overlay.png"
        overlay = draw_topdown_oal_subpixel_v2_overlay(
            image,
            mask,
            subpixel_v2,
            baseline=baseline,
            subpixel_v1=subpixel_v1,
            label=f"{record.trial} / {record.group} / {record.capture}",
        )
        cv2.imwrite(str(overlay_path), overlay)
        overlays_by_trial[record.trial].append(overlay_path)

        row = {
            "trial": record.trial,
            "orientation_group": record.group,
            "capture": record.capture,
            "source_image_path": str(record.image_path.relative_to(repo_root)),
            "mask_path": str(record.mask_path.relative_to(repo_root)),
            "baseline_passed": str(baseline.passed),
            "baseline_failure_reason": baseline.failure_reason or "",
            "baseline_length_pixels": _float(baseline.length_pixels),
            "binary_geometry_passed": str(binary_geometry.passed),
            "binary_geometry_failure_reason": binary_geometry.failure_reason or "",
            "binary_geometry_length_pixels": _float(binary_geometry.length_pixels),
            "subpixel_v1_passed": str(subpixel_v1.passed),
            "subpixel_v1_failure_reason": subpixel_v1.failure_reason or "",
            "subpixel_v1_length_pixels": _float(subpixel_v1.length_pixels),
            "subpixel_v2_passed": str(subpixel_v2.passed),
            "subpixel_v2_failure_reason": subpixel_v2.failure_reason or "",
            "subpixel_v2_length_pixels": _float(subpixel_v2.length_pixels),
            "subpixel_v2_minus_baseline_pixels": (
                ""
                if subpixel_v2.length_pixels is None or baseline.length_pixels is None
                else _float(subpixel_v2.length_pixels - baseline.length_pixels)
            ),
            "subpixel_v2_angle_degrees": _float(subpixel_v2.angle_degrees),
            "sidewall_angle_difference_degrees": _float(
                subpixel_v2.sidewall_angle_difference_degrees
            ),
            "end_line_angle_difference_degrees": _float(
                subpixel_v2.end_line_angle_difference_degrees
            ),
            "end_min_perpendicular_error_degrees": _float(
                subpixel_v2.end_min_perpendicular_error_degrees
            ),
            "end_max_perpendicular_error_degrees": _float(
                subpixel_v2.end_max_perpendicular_error_degrees
            ),
            "sidewall_min_acceptance_fraction": _diagnostic_value(
                subpixel_v2.sidewall_min_diagnostics, "acceptance_fraction"
            ),
            "sidewall_max_acceptance_fraction": _diagnostic_value(
                subpixel_v2.sidewall_max_diagnostics, "acceptance_fraction"
            ),
            "end_min_acceptance_fraction": _diagnostic_value(
                subpixel_v2.end_min_diagnostics, "acceptance_fraction"
            ),
            "end_max_acceptance_fraction": _diagnostic_value(
                subpixel_v2.end_max_diagnostics, "acceptance_fraction"
            ),
            "sidewall_min_rms_pixels": _diagnostic_value(
                subpixel_v2.sidewall_min_diagnostics, "rms_pixels"
            ),
            "sidewall_max_rms_pixels": _diagnostic_value(
                subpixel_v2.sidewall_max_diagnostics, "rms_pixels"
            ),
            "end_min_rms_pixels": _diagnostic_value(
                subpixel_v2.end_min_diagnostics, "rms_pixels"
            ),
            "end_max_rms_pixels": _diagnostic_value(
                subpixel_v2.end_max_diagnostics, "rms_pixels"
            ),
            "diagnostic_flags": ";".join(subpixel_v2.diagnostic_flags),
            "overlay_path": str(overlay_path.relative_to(repo_root)),
        }
        rows.append(row)

        for edge_name, profiles in _profile_groups(subpixel_v2):
            for index, profile in enumerate(profiles, start=1):
                profile_rows.append(_profile_row(record, edge_name, index, profile))

    result_path = output_dir / "oal_subpixel_v2_estimator_comparison_results.csv"
    with result_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    profile_path = output_dir / "oal_subpixel_v2_profile_diagnostics.csv"
    with profile_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(profile_rows[0]))
        writer.writeheader()
        writer.writerows(profile_rows)

    for trial, paths in overlays_by_trial.items():
        _make_contact_sheet(
            paths,
            output_dir / f"{trial}_subpixel_v2_comparison_contact_sheet.png",
        )

    plotted_groups: set[str] = set()
    plotted_rejections: set[str] = set()
    for record, result in results_by_record:
        if record.trial != "trial_05_controlled_orientation":
            continue
        if record.group in plotted_groups:
            continue
        plotted_groups.add(record.group)
        for edge_name, profiles in _profile_groups(result):
            accepted = next((profile for profile in profiles if profile.accepted), None)
            if accepted is None:
                continue
            path = (
                profile_plot_root / record.group / f"{edge_name}_accepted_profile.png"
            )
            _plot_profile(accepted, path)
        for _, profiles in _profile_groups(result):
            for profile in profiles:
                reason = profile.rejection_reason
                if reason and reason not in plotted_rejections:
                    path = profile_plot_root / "rejected_examples" / f"{reason}.png"
                    if _plot_profile(profile, path):
                        plotted_rejections.add(reason)

    run_metadata = {
        "execution_time_local": datetime.now().astimezone().isoformat(),
        "git_commit": source_commit,
        "git_status_short_before_analysis": source_status,
        "python_version": platform.python_version(),
        "opencv_version": cv2.__version__,
        "numpy_version": np.__version__,
        "source_pair_count": len(records),
        "development_dataset": True,
        "independent_validation": False,
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(run_metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    _write_source_manifest(records, repo_root, output_dir)

    estimator_fields = (
        ("baseline", "baseline_length_pixels"),
        ("binary_geometry", "binary_geometry_length_pixels"),
        ("subpixel_v1", "subpixel_v1_length_pixels"),
        ("subpixel_v2", "subpixel_v2_length_pixels"),
    )
    lines = [
        "Fixtureless OAL Mask-Anchored Subpixel Version 2 Development Comparison",
        "",
        f"git_commit = {source_commit}",
        f"git_status_short_before_analysis = {source_status}",
        f"source_pair_count = {len(rows)}",
        "dataset_role = development",
        "independent_validation = false",
        "accepted_masks_reused_without_resegmentation = true",
        "original_grayscale_source_images_used = true",
        "fixture_width_validation_gate_disabled = true",
        f"normalized_crossing = {config['normalized_crossing']}",
        f"minimum_local_contrast = {config['minimum_local_contrast']}",
        f"profile_half_length_pixels = {config['profile_half_length_pixels']}",
        "",
    ]

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

    median_sets: dict[str, list[float]] = {label: [] for label, _ in estimator_fields}
    v2_group_valid_counts: dict[str, int] = {}
    v2_group_medians: dict[str, float] = {}
    lines.append("trial_05_orientation_group_medians")
    for group in sorted(grouped):
        group_rows = grouped[group]
        text_parts = [f"  {group}: captures={len(group_rows)}"]
        for label, field in estimator_fields:
            values = _values(group_rows, field)
            median = _median(values)
            if median is not None:
                median_sets[label].append(median)
            text_parts.append(f"{label}={'NA' if median is None else f'{median:.9f}'}")
            if label == "subpixel_v2":
                v2_group_valid_counts[group] = len(values)
                if median is not None:
                    v2_group_medians[group] = median
        lines.append(", ".join(text_parts))
        for row in group_rows:
            if row["subpixel_v2_passed"] != "True":
                lines.append(
                    f"    failure {row['capture']}: {row['subpixel_v2_failure_reason']}"
                )

    orientation_ranges: dict[str, float | None] = {}
    lines.extend(["", "trial_05_range_among_orientation_group_medians"])
    for label, _ in estimator_fields:
        values = median_sets[label]
        value = max(values) - min(values) if len(values) >= 2 else None
        orientation_ranges[label] = value
        lines.append(f"  {label}_groups_with_passing_values = {len(values)}")
        lines.append(
            f"  {label}_pixels = {'not_available' if value is None else f'{value:.9f}'}"
        )

    trial_03_rows = [row for row in rows if row["trial"] == "trial_03_static"]
    v2_static = _summary_stats(_values(trial_03_rows, "subpixel_v2_length_pixels"))
    v2_all_valid = sum(row["subpixel_v2_passed"] == "True" for row in rows)
    v2_flags = [row["diagnostic_flags"] for row in rows if row["diagnostic_flags"]]
    flag_patterns = Counter(v2_flags)
    pooled_v2 = _values(trial_05_rows, "subpixel_v2_length_pixels")
    pooled_median = statistics.median(pooled_v2) if pooled_v2 else None

    group_count_ok = (
        all(
            count >= (4 if group == "angle_090_controlled_retake" else 2)
            for group, count in v2_group_valid_counts.items()
        )
        and len(v2_group_valid_counts) == 5
    )
    group_bias_ok = (
        pooled_median is not None
        and len(v2_group_medians) == 5
        and all(
            abs(value - pooled_median) <= 1.0 for value in v2_group_medians.values()
        )
    )
    orientation_value = orientation_ranges["subpixel_v2"]
    criteria = {
        "orientation_range_at_least_20_percent_better_than_pca": (
            orientation_value is not None
            and orientation_value <= VERSION_2_TARGET_ORIENTATION_RANGE
        ),
        "static_sd_no_worse_than_pca": (
            bool(v2_static) and v2_static["sd"] <= PCA_STATIC_SD_BENCHMARK
        ),
        "at_least_26_of_27_valid": v2_all_valid >= 26,
        "minimum_valid_count_per_orientation_group": group_count_ok,
        "no_orientation_group_median_over_1px_from_pooled_median": group_bias_ok,
        "diagnostics_not_identical_unresolved_warning_on_all_captures": not (
            len(v2_flags) == 27 and len(flag_patterns) == 1
        ),
        "clean_committed_source_before_analysis": source_status == "clean",
    }

    lines.extend(
        [
            "",
            "predefined_quantitative_candidate_criteria",
            f"  pca_static_sd_benchmark_pixels = {PCA_STATIC_SD_BENCHMARK:.9f}",
            f"  pca_orientation_range_benchmark_pixels = {PCA_ORIENTATION_RANGE_BENCHMARK:.9f}",
            f"  version_2_target_orientation_range_pixels = {VERSION_2_TARGET_ORIENTATION_RANGE:.9f}",
        ]
    )
    for name, passed in criteria.items():
        lines.append(f"  {name} = {'pass' if passed else 'fail'}")

    failed_rows = [row for row in rows if row["subpixel_v2_passed"] != "True"]
    lines.extend(
        [
            "",
            f"subpixel_v2_valid_capture_count = {v2_all_valid}",
            f"subpixel_v2_failed_capture_count = {len(failed_rows)}",
            f"subpixel_v2_flagged_capture_count = {len(v2_flags)}",
            f"subpixel_v2_distinct_flag_patterns = {len(flag_patterns)}",
            f"quantitative_candidate_criteria_all_pass = {str(all(criteria.values())).lower()}",
            "visual_review_status = pending",
            "final_candidate_acceptance = pending_visual_review",
            "",
            "Interpretation restriction:",
            "These 27 captures are development data and cannot independently validate Version 2.",
            "No method may be accepted from numerical range alone.",
        ]
    )

    summary_path = output_dir / "oal_subpixel_v2_estimator_comparison_summary.txt"
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    flag_report_path = output_dir / "oal_subpixel_v2_failure_and_flag_report.csv"
    with flag_report_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "trial",
            "orientation_group",
            "capture",
            "passed",
            "failure_reason",
            "diagnostic_flags",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "trial": row["trial"],
                    "orientation_group": row["orientation_group"],
                    "capture": row["capture"],
                    "passed": row["subpixel_v2_passed"],
                    "failure_reason": row["subpixel_v2_failure_reason"],
                    "diagnostic_flags": row["diagnostic_flags"],
                }
            )

    _write_manifest(output_dir)
    print(f"Results: {result_path.relative_to(repo_root)}")
    print(f"Profile diagnostics: {profile_path.relative_to(repo_root)}")
    print(f"Summary: {summary_path.relative_to(repo_root)}")
    print(f"Overlays: {overlay_root.relative_to(repo_root)}")
    print(f"Rows: {len(rows)}")
    print(f"Version 2 failures: {len(failed_rows)}")
    print(f"Version 2 flagged captures: {len(v2_flags)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
