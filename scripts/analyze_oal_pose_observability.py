#!/usr/bin/env python3
"""Final diagnostic test of independent pose observability for OAL.

This script does NOT tune or modify any estimator. It extracts a small,
predeclared set of image cues that are physically plausible indicators of
placement / perspective / out-of-plane pose and asks whether those cues track
the already-frozen endface-hybrid placement-to-placement OAL changes.

Development evidence is reported separately for:
- final Fixture-2 multi-specimen development data (146, 178, 187, 197),
- earlier controlled repositioning data for specimen 121 (supplementary), and
- the fixed-position 10-frame sequence for specimen 146 (noise control).

Formal V2 is used only as a retrospective mechanism check. It must not be used
to fit a correction or change the frozen estimator.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
import hashlib
import importlib.util
import math
from pathlib import Path
import statistics
import sys
from typing import Any

import numpy as np
from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.image_processing.oal_segmentation import segment_oal_case  # noqa: E402
from src.measurement.topdown_oal_geometry import (  # noqa: E402
    _profile_extremes,
    measure_topdown_oal_geometry,
)
from src.measurement.topdown_oal_subpixel_v2 import (  # noqa: E402
    _as_gray,
    _sample_end_profiles,
    _unit,
)

FROZEN_HYBRID_SCRIPT = REPO_ROOT / "scripts/evaluate_oal_endface_hybrid_dev.py"
FROZEN_HYBRID_SHA256 = (
    "3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af"
)

DATA_ROOT = REPO_ROOT / "data/oal_validation"
DEV_CSV = (
    DATA_ROOT
    / "post_v1_diagnostics/endface_hybrid_dev/endface_hybrid_observations.csv"
)
V2_HYBRID_CSV = (
    DATA_ROOT
    / "derived_v2/endface_hybrid_retrospective/v2_endface_hybrid_observations.csv"
)
V2_RAW_ROOT = DATA_ROOT / "formal_cv_v2/raw"

OUTPUT_DIR = DATA_ROOT / "derived_v2/pose_observability_diagnostics"

CASE_ONLY_FIXTURE_WIDTH_RATIO = 0.0

# These must remain identical to the pre-frozen hybrid development implementation.
PROFILE_KWARGS: dict[str, object] = {
    "profile_half_length_pixels": 6.0,
    "profile_step_pixels": 0.25,
    "interior_plateau_limit_pixels": (-6.0, -2.0),
    "exterior_plateau_limit_pixels": (2.0, 6.0),
    "normalized_crossing": 0.50,
    "minimum_local_contrast": 30.0,
    "maximum_anchor_distance_pixels": 3.0,
    "maximum_crossing_distance_pixels": 3.0,
}
END_SAMPLE_COUNT = 41
END_FACE_TRANSVERSE_FRACTION = 0.30

# Predeclared cue set. Do not add cues after seeing results from this run.
CUES = (
    "centroid_x_px",
    "centroid_y_px",
    "in_plane_tilt_deg",
    "case_width_px",
    "body_width_gradient_norm",
    "body_width_ratio_mouth_to_base",
    "endface_skew_difference",
    "endface_sharpness_log_ratio",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_frozen_helpers():
    actual = sha256_file(FROZEN_HYBRID_SCRIPT)
    if actual != FROZEN_HYBRID_SHA256:
        fail(
            "Frozen hybrid hash mismatch. STOP.\n"
            f"Expected: {FROZEN_HYBRID_SHA256}\n"
            f"Actual:   {actual}"
        )
    spec = importlib.util.spec_from_file_location(
        "frozen_endface_hybrid_dev_pose_diag",
        FROZEN_HYBRID_SCRIPT,
    )
    if spec is None or spec.loader is None:
        fail("Could not import frozen hybrid helper script.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        fail(f"Missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def passed(value: str) -> bool:
    return value.strip().lower() in {"true", "yes", "1"}


def _segment_slope_s_of_t(
    segment: Any,
    origin: np.ndarray,
    axis: np.ndarray,
) -> tuple[float, float]:
    """Return line slope ds/dt and mean s in an oriented local frame."""
    perpendicular = np.asarray([-axis[1], axis[0]], dtype=np.float64)
    a = np.asarray(segment.start_xy, dtype=np.float64) - origin
    b = np.asarray(segment.end_xy, dtype=np.float64) - origin
    sa, ta = float(a @ axis), float(a @ perpendicular)
    sb, tb = float(b @ axis), float(b @ perpendicular)
    if abs(tb - ta) <= 1e-12:
        return float("nan"), 0.5 * (sa + sb)
    return (sb - sa) / (tb - ta), 0.5 * (sa + sb)


def _median_transition_sharpness(profile_set: Any) -> float:
    """Median normalized intensity-transition slope across accepted profiles."""
    values: list[float] = []
    for profile in profile_set.profiles:
        if not profile.accepted:
            continue
        normalized = np.asarray(profile.normalized_values, dtype=np.float64)
        offsets = np.asarray(profile.offsets_pixels, dtype=np.float64)
        if normalized.size < 2 or offsets.size != normalized.size:
            continue
        delta_offsets = np.diff(offsets)
        valid_step = np.abs(delta_offsets) > 1e-12
        if not np.any(valid_step):
            continue
        slopes = np.full(delta_offsets.shape, np.nan, dtype=np.float64)
        slopes[valid_step] = np.diff(normalized)[valid_step] / delta_offsets[valid_step]
        mid = 0.5 * (normalized[:-1] + normalized[1:])
        local = (mid >= 0.10) & (mid <= 0.90) & np.isfinite(slopes) & (slopes > 0.0)
        if np.any(local):
            values.append(float(np.max(slopes[local])))
    if not values:
        return float("nan")
    return float(statistics.median(values))


def extract_cues(
    helper: Any,
    blank: np.ndarray,
    image: np.ndarray,
) -> dict[str, float]:
    segmentation = segment_oal_case(blank, image)
    if not segmentation.passed or segmentation.centroid_xy is None:
        fail(f"Segmentation failed: {segmentation.failure_reason}")

    geometry = measure_topdown_oal_geometry(
        segmentation.mask,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )
    if not geometry.passed:
        fail(f"Geometry failed: {geometry.failure_reason}")

    required = (
        geometry.axis_point_xy,
        geometry.axis_vector_xy,
        geometry.endpoint_min_xy,
        geometry.endpoint_max_xy,
        geometry.case_width_pixels,
        geometry.end_min_segment,
        geometry.end_max_segment,
    )
    if any(value is None for value in required):
        fail("Geometry returned incomplete pose-cue data.")

    origin = np.asarray(geometry.axis_point_xy, dtype=np.float64)
    axis = _unit(np.asarray(geometry.axis_vector_xy, dtype=np.float64))

    # Orient the local longitudinal axis toward the top of the image (mouth).
    # This makes signed taper/skew cues comparable from image to image.
    if axis[1] > 0.0:
        axis = -axis

    perpendicular = np.asarray([-axis[1], axis[0]], dtype=np.float64)

    endpoint_a = np.asarray(geometry.endpoint_min_xy, dtype=np.float64)
    endpoint_b = np.asarray(geometry.endpoint_max_xy, dtype=np.float64)
    sa = float((endpoint_a - origin) @ axis)
    sb = float((endpoint_b - origin) @ axis)
    base_s = min(sa, sb)
    mouth_s = max(sa, sb)
    projected_span = mouth_s - base_s
    if projected_span <= 1.0:
        fail("Invalid projected span for pose-cue extraction.")

    # Silhouette width-profile cue, restricted to central body to avoid head/mouth
    # end geometry. Width gradient is normalized by mean width and by using z in
    # [0,1], so it is dimensionless and comparable across specimens.
    ys, xs = np.nonzero(segmentation.mask)
    points = np.column_stack((xs, ys)).astype(np.float64)
    centers, _, _, widths = _profile_extremes(points, origin, axis)
    z = (centers - base_s) / projected_span
    body = (z >= 0.20) & (z <= 0.80) & np.isfinite(widths)
    if int(np.sum(body)) < 20:
        fail("Insufficient central body width-profile data.")
    body_z = z[body]
    body_w = widths[body]
    q05, q95 = np.quantile(body_w, [0.05, 0.95])
    keep = (body_w >= q05) & (body_w <= q95)
    body_z = body_z[keep]
    body_w = body_w[keep]
    slope, _ = np.polyfit(body_z, body_w, 1)
    mean_width = float(np.mean(body_w))
    width_gradient_norm = float(slope / mean_width)

    def width_band(low: float, high: float) -> float:
        selected = (z >= low) & (z <= high) & np.isfinite(widths)
        if not np.any(selected):
            return float("nan")
        return float(np.median(widths[selected]))

    base_width = width_band(0.20, 0.30)
    mouth_width = width_band(0.70, 0.80)
    width_ratio = float(mouth_width / base_width)

    # Signed end-face skew in the same oriented local frame. Identify the base
    # and mouth segments by their projected longitudinal midpoint.
    first_slope, first_mid_s = _segment_slope_s_of_t(
        geometry.end_min_segment, origin, axis
    )
    second_slope, second_mid_s = _segment_slope_s_of_t(
        geometry.end_max_segment, origin, axis
    )
    if first_mid_s <= second_mid_s:
        base_slope, mouth_slope = first_slope, second_slope
    else:
        base_slope, mouth_slope = second_slope, first_slope
    endface_skew_difference = float(mouth_slope - base_slope)

    # Normalized grayscale sharpness asymmetry between physical ends. This is a
    # depth/focus cue; it does not use the end-to-end separation.
    gray = _as_gray(image)
    half_width = float(geometry.case_width_pixels) * END_FACE_TRANSVERSE_FRACTION
    base_profiles = _sample_end_profiles(
        gray,
        segmentation.mask,
        origin,
        axis,
        base_s,
        edge_name="pose_base_end",
        half_width_pixels=half_width,
        sample_count=END_SAMPLE_COUNT,
        **PROFILE_KWARGS,
    )
    mouth_profiles = _sample_end_profiles(
        gray,
        segmentation.mask,
        origin,
        axis,
        mouth_s,
        edge_name="pose_mouth_end",
        half_width_pixels=half_width,
        sample_count=END_SAMPLE_COUNT,
        **PROFILE_KWARGS,
    )
    base_sharp = _median_transition_sharpness(base_profiles)
    mouth_sharp = _median_transition_sharpness(mouth_profiles)
    if base_sharp > 0.0 and mouth_sharp > 0.0 and math.isfinite(base_sharp) and math.isfinite(mouth_sharp):
        sharpness_log_ratio = float(math.log(mouth_sharp / base_sharp))
    else:
        sharpness_log_ratio = float("nan")

    # Signed in-plane tilt from image vertical. For an upward-pointing axis,
    # zero is vertical, positive tilts toward image right.
    in_plane_tilt = float(math.degrees(math.atan2(axis[0], -axis[1])))

    return {
        "centroid_x_px": float(segmentation.centroid_xy[0]),
        "centroid_y_px": float(segmentation.centroid_xy[1]),
        "in_plane_tilt_deg": in_plane_tilt,
        "case_width_px": float(geometry.case_width_pixels),
        "body_width_gradient_norm": width_gradient_norm,
        "body_width_ratio_mouth_to_base": width_ratio,
        "endface_skew_difference": endface_skew_difference,
        "endface_sharpness_log_ratio": sharpness_log_ratio,
    }


def correlation_rows(
    observations: list[dict[str, Any]],
    *,
    group_name: str,
) -> list[dict[str, Any]]:
    """Within-specimen centered correlations between cue and hybrid OAL."""
    by_specimen: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in observations:
        by_specimen[str(row["specimen"])].append(row)

    centered: list[dict[str, float]] = []
    for specimen, rows in by_specimen.items():
        if len(rows) < 2:
            continue
        mean_oal = statistics.fmean(float(row["hybrid_oal_in"]) for row in rows)
        cue_means = {
            cue: statistics.fmean(float(row[cue]) for row in rows if math.isfinite(float(row[cue])))
            for cue in CUES
            if any(math.isfinite(float(row[cue])) for row in rows)
        }
        for row in rows:
            item: dict[str, float] = {"oal": float(row["hybrid_oal_in"]) - mean_oal}
            for cue in CUES:
                value = float(row[cue])
                mean = cue_means.get(cue, float("nan"))
                item[cue] = value - mean if math.isfinite(value) and math.isfinite(mean) else float("nan")
            centered.append(item)

    results: list[dict[str, Any]] = []
    for cue in CUES:
        pairs = [(row[cue], row["oal"]) for row in centered if math.isfinite(row[cue])]
        if len(pairs) < 3:
            pearson = spearman = float("nan")
            n = len(pairs)
        else:
            x = np.asarray([p[0] for p in pairs], dtype=np.float64)
            y = np.asarray([p[1] for p in pairs], dtype=np.float64)
            n = len(pairs)
            if np.std(x) <= 1e-15 or np.std(y) <= 1e-15:
                pearson = spearman = float("nan")
            else:
                pearson = float(stats.pearsonr(x, y).statistic)
                spearman = float(stats.spearmanr(x, y).statistic)
        results.append(
            {
                "group": group_name,
                "cue": cue,
                "n_centered_observations": n,
                "pearson_r": pearson,
                "spearman_rho": spearman,
            }
        )
    return results


def collapse_development_frames(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["dataset"], row["specimen"], row["placement"])].append(row)

    collapsed: list[dict[str, Any]] = []
    numeric = ("hybrid_oal_in",) + CUES
    for (dataset, specimen, placement), members in sorted(grouped.items()):
        item: dict[str, Any] = {
            "dataset": dataset,
            "specimen": specimen,
            "placement": placement,
            "frame_count": len(members),
        }
        for name in numeric:
            values = [float(row[name]) for row in members if math.isfinite(float(row[name]))]
            item[name] = statistics.fmean(values) if values else float("nan")
        collapsed.append(item)
    return collapsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--development-only",
        action="store_true",
        help="Run non-formal development datasets only; skip formal V2 mechanism check.",
    )
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    helper = load_frozen_helpers()
    dev_rows = read_csv(DEV_CSV)
    hybrid_dev = [row for row in dev_rows if row["estimator"] == "endface_hybrid" and passed(row["passed"])]

    blank_paths = {
        "controlled_repositioning": REPO_ROOT
        / "data/oal_validation/post_v1_diagnostics/repositioning/raw/"
          "postv1_reposition_blank_20260908_174240/"
          "postv1_reposition_blank_20260908_174242_592657_01.png",
        "fixture2_multispecimen": REPO_ROOT
        / "data/oal_validation/post_v1_diagnostics/fixture2_multispecimen_dev/raw/"
          "fixture2_multispecimen_blank_20260909_181600/"
          "fixture2_multispecimen_blank_20260909_181602_877235_01.png",
        "fixture2_fixed10": REPO_ROOT
        / "data/oal_validation/post_v1_diagnostics/fixture2_multispecimen_dev/raw/"
          "fixture2_multispecimen_blank_20260909_181600/"
          "fixture2_multispecimen_blank_20260909_181602_877235_01.png",
    }

    blank_cache: dict[Path, np.ndarray] = {}
    observations: list[dict[str, Any]] = []

    print("=" * 90)
    print("POSE OBSERVABILITY — DEVELOPMENT DATA")
    print("=" * 90)

    for index, row in enumerate(hybrid_dev, start=1):
        dataset = row["dataset"]
        if dataset not in blank_paths:
            continue
        image_path = REPO_ROOT / row["image"]
        blank_path = blank_paths[dataset]
        if not image_path.is_file() or not blank_path.is_file():
            fail(f"Missing development image or blank: {image_path} / {blank_path}")
        if blank_path not in blank_cache:
            blank_cache[blank_path] = helper._load_gray(blank_path)
        image = helper._load_gray(image_path)
        cues = extract_cues(helper, blank_cache[blank_path], image)
        observations.append(
            {
                "source": "development",
                "dataset": dataset,
                "specimen": row["specimen"],
                "placement": row["placement"],
                "sequence": int(row["sequence"]),
                "image": row["image"],
                "hybrid_oal_in": float(row["oal_in"]),
                **cues,
            }
        )
        if index % 20 == 0:
            print(f"Processed {index}/{len(hybrid_dev)} development images")

    collapsed = collapse_development_frames(observations)
    final_fixture = [row for row in collapsed if row["dataset"] == "fixture2_multispecimen"]
    controlled = [row for row in collapsed if row["dataset"] == "controlled_repositioning"]
    fixed_frames = [row for row in observations if row["dataset"] == "fixture2_fixed10"]

    correlations = []
    correlations.extend(correlation_rows(final_fixture, group_name="final_fixture2_development"))
    correlations.extend(correlation_rows(controlled, group_name="controlled_repositioning_121"))

    print(f"Final Fixture-2 development placements: {len(final_fixture)}")
    print(f"Controlled repositioning placements:    {len(controlled)}")
    print(f"Fixed-position 146 frames:              {len(fixed_frames)}")

    formal_observations: list[dict[str, Any]] = []
    if not args.development_only:
        v2_rows = read_csv(V2_HYBRID_CSV)
        v2 = [row for row in v2_rows if passed(row["passed"])]
        if len(v2) != 180:
            fail(f"Expected 180 passing V2 hybrid rows; found {len(v2)}")

        print()
        print("=" * 90)
        print("POSE OBSERVABILITY — FORMAL V2 MECHANISM CHECK")
        print("=" * 90)
        print("Formal V2 is diagnostic only and must not be used to fit a correction.")

        for index, row in enumerate(v2, start=1):
            image_path = REPO_ROOT / row["raw_image_path"]
            blank_path = V2_RAW_ROOT / f'{row["session_id"]}_blank_reference.png'
            if not image_path.is_file() or not blank_path.is_file():
                fail(f"Missing V2 image or blank: {image_path} / {blank_path}")
            if blank_path not in blank_cache:
                blank_cache[blank_path] = helper._load_gray(blank_path)
            image = helper._load_gray(image_path)
            cues = extract_cues(helper, blank_cache[blank_path], image)
            formal_observations.append(
                {
                    "source": "formal_v2_diagnostic",
                    "dataset": "formal_v2",
                    "specimen": row["part_id"],
                    "placement": f'R{row["cv_round"]}',
                    "sequence": 1,
                    "image": row["raw_image_path"],
                    "hybrid_oal_in": float(row["hybrid_oal_in"]),
                    **cues,
                }
            )
            if index % 20 == 0 or index == len(v2):
                print(f"Processed {index}/{len(v2)} V2 images")

        correlations.extend(correlation_rows(formal_observations, group_name="formal_v2_diagnostic"))

    args.output_dir.mkdir(parents=True, exist_ok=True)

    all_obs = observations + formal_observations
    obs_path = args.output_dir / "pose_observability_observations.csv"
    with obs_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_obs[0].keys()))
        writer.writeheader()
        writer.writerows(all_obs)

    collapsed_path = args.output_dir / "development_placement_means.csv"
    with collapsed_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(collapsed[0].keys()))
        writer.writeheader()
        writer.writerows(collapsed)

    corr_path = args.output_dir / "pose_cue_correlations.csv"
    with corr_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(correlations[0].keys()))
        writer.writeheader()
        writer.writerows(correlations)

    # Fixed-position noise-control ranges.
    fixed_ranges: dict[str, float] = {}
    if fixed_frames:
        for name in ("hybrid_oal_in",) + CUES:
            vals = [float(row[name]) for row in fixed_frames if math.isfinite(float(row[name]))]
            if vals:
                fixed_ranges[name] = max(vals) - min(vals)

    lines = [
        "# OAL Pose-Observability Diagnostic",
        "",
        "**Diagnostic only. No estimator or calibration parameters are modified.**",
        "",
        "## Predeclared independent cues",
        "",
        "- centroid x/y: fixture-relative image-position proxies",
        "- in-plane tilt: 2-D orientation control",
        "- case width: apparent scale/depth proxy",
        "- normalized body-width gradient and mouth/base width ratio: perspective/taper proxies",
        "- end-face skew difference: projected end-face geometry proxy",
        "- end-face sharpness log-ratio: depth/focus asymmetry proxy",
        "",
        "## Correlations with within-specimen centered frozen-hybrid OAL",
        "",
        "| Group | Cue | n | Pearson r | Spearman rho |",
        "|---|---|---:|---:|---:|",
    ]
    for row in correlations:
        lines.append(
            f'| {row["group"]} | {row["cue"]} | {row["n_centered_observations"]} | '
            f'{float(row["pearson_r"]):+.4f} | {float(row["spearman_rho"]):+.4f} |'
        )

    lines.extend(["", "## Fixed-position specimen 146 noise control", ""])
    for name, value in fixed_ranges.items():
        lines.append(f"- {name} range: {value:.9f}")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            "A cue is not a correction merely because it correlates retrospectively. A software pose-compensation path is credible only if a physically interpretable cue is visible in non-formal development data, exhibits the same relationship in the V2 mechanism check, and can be parameterized using non-formal data alone before any prospective V3 validation. Formal V2 must not be used to fit correction coefficients.",
            "",
        ]
    )
    summary_path = args.output_dir / "SUMMARY.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")

    print()
    print("=" * 90)
    print("POSE-CUE CORRELATION SUMMARY")
    print("=" * 90)
    for group in ("final_fixture2_development", "controlled_repositioning_121", "formal_v2_diagnostic"):
        selected = [row for row in correlations if row["group"] == group]
        if not selected:
            continue
        print(group)
        for row in sorted(selected, key=lambda r: abs(float(r["pearson_r"])), reverse=True):
            print(
                f'  {row["cue"]:<34} '
                f'Pearson {float(row["pearson_r"]):+7.4f}  '
                f'Spearman {float(row["spearman_rho"]):+7.4f}'
            )
        print()

    def display_path(path: Path) -> str:
        try:
            return str(path.relative_to(REPO_ROOT))
        except ValueError:
            return str(path)

    print(f"Wrote: {display_path(summary_path)}")
    print(f"Wrote: {display_path(corr_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
