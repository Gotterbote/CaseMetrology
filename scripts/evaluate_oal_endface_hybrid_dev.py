#!/usr/bin/env python3
"""Development-only comparison of OAL estimators on non-formal image sets.

This script does not modify the frozen V1/V2 estimator modules or formal results.
It compares the frozen PCA estimator, the geometry estimator, subpixel-v2, and a
minimal experimental hybrid that keeps the geometry-derived axis and applies
subpixel localization only to the two OAL end faces.

Default inputs are post-V1, non-formal diagnostic datasets:
- controlled repositioning of specimen 121 (10 valid placements x 3 frames)
- Fixture-2 multi-specimen placements for specimens 146, 178, 187, and 197
- Fixture-2 fixed-position 10-frame sequence for specimen 146
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
import statistics
import sys
from typing import Iterable

import cv2
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.calibration.oal_spatial_calibration import (  # noqa: E402
    resolve_oal_spatial_calibration,
)
from src.image_processing.oal_segmentation import segment_oal_case  # noqa: E402
from src.measurement.topdown_oal import measure_topdown_oal  # noqa: E402
from src.measurement.topdown_oal_geometry import (  # noqa: E402
    measure_topdown_oal_geometry,
)
from src.measurement.topdown_oal_subpixel_v2 import (  # noqa: E402
    _as_gray,
    _fit_points_in_frame,
    _sample_end_profiles,
    _unit,
    measure_topdown_oal_subpixel_v2,
)


CASE_ONLY_FIXTURE_WIDTH_RATIO = 0.0

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
MINIMUM_END_PROFILE_COUNT = 12
END_FACE_TRANSVERSE_FRACTION = 0.30


@dataclass(frozen=True)
class ImageRecord:
    dataset: str
    specimen: str
    placement: str
    sequence: int
    image_path: Path
    blank_path: Path


@dataclass(frozen=True)
class EstimatorObservation:
    estimator: str
    passed: bool
    failure_reason: str | None
    length_pixels: float | None
    length_inches: float | None
    effective_ppi: float | None
    angle_degrees: float | None
    end_min_accepted: int | None = None
    end_max_accepted: int | None = None
    sidewall_min_accepted: int | None = None
    sidewall_max_accepted: int | None = None


def _load_gray(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return image


def _calibrated_length(
    length_pixels: float,
    centroid_xy: tuple[float, float],
    angle_degrees: float,
) -> tuple[float, float]:
    calibration = resolve_oal_spatial_calibration(
        centroid_xy[0],
        centroid_xy[1],
        angle_degrees,
    )
    return float(length_pixels / calibration.effective_ppi), float(
        calibration.effective_ppi
    )


def _hybrid_endface_observation(
    image: np.ndarray,
    mask: np.ndarray,
    centroid_xy: tuple[float, float],
) -> EstimatorObservation:
    geometry = measure_topdown_oal_geometry(
        mask,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )
    if not geometry.passed:
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason=f"Geometry initialization failed: {geometry.failure_reason}",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=None,
        )

    required = (
        geometry.axis_point_xy,
        geometry.axis_vector_xy,
        geometry.endpoint_min_xy,
        geometry.endpoint_max_xy,
        geometry.case_width_pixels,
        geometry.angle_degrees,
    )
    if any(value is None for value in required):
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason="Geometry initialization returned incomplete data.",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=None,
        )

    gray = _as_gray(image)
    origin = np.asarray(geometry.axis_point_xy, dtype=np.float64)
    axis = _unit(np.asarray(geometry.axis_vector_xy, dtype=np.float64))
    perpendicular = np.array([-axis[1], axis[0]], dtype=np.float64)

    seed_minimum = float(
        (np.asarray(geometry.endpoint_min_xy, dtype=np.float64) - origin) @ axis
    )
    seed_maximum = float(
        (np.asarray(geometry.endpoint_max_xy, dtype=np.float64) - origin) @ axis
    )
    half_width = float(geometry.case_width_pixels) * END_FACE_TRANSVERSE_FRACTION

    minimum_end = _sample_end_profiles(
        gray,
        mask,
        origin,
        axis,
        seed_minimum,
        edge_name="minimum_end",
        half_width_pixels=half_width,
        sample_count=END_SAMPLE_COUNT,
        **PROFILE_KWARGS,
    )
    maximum_end = _sample_end_profiles(
        gray,
        mask,
        origin,
        axis,
        seed_maximum,
        edge_name="maximum_end",
        half_width_pixels=half_width,
        sample_count=END_SAMPLE_COUNT,
        **PROFILE_KWARGS,
    )

    minimum_count = int(minimum_end.accepted_points_xy.shape[0])
    maximum_count = int(maximum_end.accepted_points_xy.shape[0])
    if minimum_count < MINIMUM_END_PROFILE_COUNT:
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason="Insufficient accepted profiles on the minimum end face.",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=float(geometry.angle_degrees),
            end_min_accepted=minimum_count,
            end_max_accepted=maximum_count,
        )
    if maximum_count < MINIMUM_END_PROFILE_COUNT:
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason="Insufficient accepted profiles on the maximum end face.",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=float(geometry.angle_degrees),
            end_min_accepted=minimum_count,
            end_max_accepted=maximum_count,
        )

    try:
        minimum_fit, _, _ = _fit_points_in_frame(
            minimum_end.accepted_points_xy,
            origin,
            perpendicular,
            axis,
        )
        maximum_fit, _, _ = _fit_points_in_frame(
            maximum_end.accepted_points_xy,
            origin,
            perpendicular,
            axis,
        )
    except (ValueError, np.linalg.LinAlgError) as exc:
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason=f"End-face fitting failed: {exc}",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=float(geometry.angle_degrees),
            end_min_accepted=minimum_count,
            end_max_accepted=maximum_count,
        )

    length_pixels = float(maximum_fit.intercept - minimum_fit.intercept)
    if length_pixels <= 0.0:
        return EstimatorObservation(
            estimator="endface_hybrid",
            passed=False,
            failure_reason="The fitted end-face ordering is invalid.",
            length_pixels=None,
            length_inches=None,
            effective_ppi=None,
            angle_degrees=float(geometry.angle_degrees),
            end_min_accepted=minimum_count,
            end_max_accepted=maximum_count,
        )

    length_inches, effective_ppi = _calibrated_length(
        length_pixels,
        centroid_xy,
        float(geometry.angle_degrees),
    )
    return EstimatorObservation(
        estimator="endface_hybrid",
        passed=True,
        failure_reason=None,
        length_pixels=length_pixels,
        length_inches=length_inches,
        effective_ppi=effective_ppi,
        angle_degrees=float(geometry.angle_degrees),
        end_min_accepted=minimum_count,
        end_max_accepted=maximum_count,
    )


def _observations_for_image(
    blank: np.ndarray,
    image: np.ndarray,
    *,
    include_subpixel_v2: bool,
) -> list[EstimatorObservation]:
    segmentation = segment_oal_case(blank, image)
    if not segmentation.passed or segmentation.centroid_xy is None:
        reason = segmentation.failure_reason or "Segmentation failed."
        return [
            EstimatorObservation(
                estimator=name,
                passed=False,
                failure_reason=reason,
                length_pixels=None,
                length_inches=None,
                effective_ppi=None,
                angle_degrees=None,
            )
            for name in (("pca", "geometry", "subpixel_v2", "endface_hybrid") if include_subpixel_v2 else ("pca", "geometry", "endface_hybrid"))
        ]

    mask = segmentation.mask
    centroid = segmentation.centroid_xy
    observations: list[EstimatorObservation] = []

    pca = measure_topdown_oal(
        mask,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )
    if pca.passed and pca.length_pixels is not None and pca.angle_degrees is not None:
        length_inches, ppi = _calibrated_length(
            float(pca.length_pixels), centroid, float(pca.angle_degrees)
        )
        observations.append(
            EstimatorObservation(
                estimator="pca",
                passed=True,
                failure_reason=None,
                length_pixels=float(pca.length_pixels),
                length_inches=length_inches,
                effective_ppi=ppi,
                angle_degrees=float(pca.angle_degrees),
            )
        )
    else:
        observations.append(
            EstimatorObservation(
                estimator="pca",
                passed=False,
                failure_reason=pca.failure_reason,
                length_pixels=None,
                length_inches=None,
                effective_ppi=None,
                angle_degrees=None,
            )
        )

    geometry = measure_topdown_oal_geometry(
        mask,
        minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
    )
    if (
        geometry.passed
        and geometry.length_pixels is not None
        and geometry.angle_degrees is not None
    ):
        length_inches, ppi = _calibrated_length(
            float(geometry.length_pixels), centroid, float(geometry.angle_degrees)
        )
        observations.append(
            EstimatorObservation(
                estimator="geometry",
                passed=True,
                failure_reason=None,
                length_pixels=float(geometry.length_pixels),
                length_inches=length_inches,
                effective_ppi=ppi,
                angle_degrees=float(geometry.angle_degrees),
            )
        )
    else:
        observations.append(
            EstimatorObservation(
                estimator="geometry",
                passed=False,
                failure_reason=geometry.failure_reason,
                length_pixels=None,
                length_inches=None,
                effective_ppi=None,
                angle_degrees=None,
            )
        )

    if include_subpixel_v2:
        subpixel = measure_topdown_oal_subpixel_v2(
            image,
            mask,
            minimum_fixture_width_ratio=CASE_ONLY_FIXTURE_WIDTH_RATIO,
        )
        if (
            subpixel.passed
            and subpixel.length_pixels is not None
            and subpixel.angle_degrees is not None
        ):
            length_inches, ppi = _calibrated_length(
                float(subpixel.length_pixels), centroid, float(subpixel.angle_degrees)
            )
            observations.append(
                EstimatorObservation(
                    estimator="subpixel_v2",
                    passed=True,
                    failure_reason=None,
                    length_pixels=float(subpixel.length_pixels),
                    length_inches=length_inches,
                    effective_ppi=ppi,
                    angle_degrees=float(subpixel.angle_degrees),
                    end_min_accepted=sum(
                        profile.accepted for profile in subpixel.end_min_profiles
                    ),
                    end_max_accepted=sum(
                        profile.accepted for profile in subpixel.end_max_profiles
                    ),
                    sidewall_min_accepted=sum(
                        profile.accepted for profile in subpixel.sidewall_min_profiles
                    ),
                    sidewall_max_accepted=sum(
                        profile.accepted for profile in subpixel.sidewall_max_profiles
                    ),
                )
            )
        else:
            observations.append(
                EstimatorObservation(
                    estimator="subpixel_v2",
                    passed=False,
                    failure_reason=subpixel.failure_reason,
                    length_pixels=None,
                    length_inches=None,
                    effective_ppi=None,
                    angle_degrees=None,
                    end_min_accepted=sum(
                        profile.accepted for profile in subpixel.end_min_profiles
                    ),
                    end_max_accepted=sum(
                        profile.accepted for profile in subpixel.end_max_profiles
                    ),
                    sidewall_min_accepted=sum(
                        profile.accepted for profile in subpixel.sidewall_min_profiles
                    ),
                    sidewall_max_accepted=sum(
                        profile.accepted for profile in subpixel.sidewall_max_profiles
                    ),
                )
            )

    observations.append(_hybrid_endface_observation(image, mask, centroid))
    return observations


def _single_png(directory: Path) -> Path:
    paths = sorted(directory.glob("*.png"))
    if len(paths) != 1:
        raise RuntimeError(f"Expected exactly one PNG in {directory}; found {len(paths)}")
    return paths[0]


def _repositioning_records(repo_root: Path) -> list[ImageRecord]:
    root = repo_root / "data/oal_validation/post_v1_diagnostics/repositioning"
    blank = _single_png(root / "raw/postv1_reposition_blank_20260908_174240")
    rows = list(csv.DictReader((root / "controlled_repositioning_results.csv").open()))
    records: list[ImageRecord] = []
    for row in rows:
        records.append(
            ImageRecord(
                dataset="controlled_repositioning",
                specimen="121",
                placement=row["placement"],
                sequence=int(row["sequence"]),
                image_path=repo_root / row["image"],
                blank_path=blank,
            )
        )
    return records


def _fixture2_records(repo_root: Path) -> list[ImageRecord]:
    root = repo_root / "data/oal_validation/post_v1_diagnostics/fixture2_multispecimen_dev"
    blank = _single_png(root / "raw/fixture2_multispecimen_blank_20260909_181600")
    records: list[ImageRecord] = []

    for specimen in ("146", "178", "187", "197"):
        for placement in ("p01", "p02", "p03"):
            directories = sorted((root / "raw").glob(f"fixture2_multispecimen_{specimen}_{placement}_*"))
            if len(directories) != 1:
                raise RuntimeError(
                    f"Expected one directory for specimen {specimen} {placement}; "
                    f"found {len(directories)}"
                )
            records.append(
                ImageRecord(
                    dataset="fixture2_multispecimen",
                    specimen=specimen,
                    placement=placement.upper(),
                    sequence=1,
                    image_path=_single_png(directories[0]),
                    blank_path=blank,
                )
            )

    fixed_directory = root / "raw/fixture2_146_fixed10_20260909_183042"
    for sequence, image_path in enumerate(sorted(fixed_directory.glob("*.png")), start=1):
        records.append(
            ImageRecord(
                dataset="fixture2_fixed10",
                specimen="146",
                placement="FIXED",
                sequence=sequence,
                image_path=image_path,
                blank_path=blank,
            )
        )
    return records


def _pairwise_absolute(values: Iterable[float]) -> list[float]:
    sequence = list(values)
    return [
        abs(sequence[left] - sequence[right])
        for left in range(len(sequence))
        for right in range(left + 1, len(sequence))
    ]


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=np.float64), 0.95))


def _fmt(value: float | None) -> str:
    return "NA" if value is None else f"{value:.9f}"


def _write_summary(rows: list[dict[str, str]], output_path: Path) -> None:
    preferred = ("pca", "geometry", "subpixel_v2", "endface_hybrid")
    present = {row["estimator"] for row in rows}
    estimators = tuple(name for name in preferred if name in present)
    lines = [
        "# Endface Hybrid Development Comparison",
        "",
        "Development-only analysis. Formal V1/V2 results remain unchanged.",
        "",
        "## Controlled repositioning — specimen 121",
        "",
    ]

    for estimator in estimators:
        selected = [
            row
            for row in rows
            if row["dataset"] == "controlled_repositioning"
            and row["estimator"] == estimator
        ]
        passing = [row for row in selected if row["passed"] == "True"]
        placements: dict[str, list[float]] = {}
        for row in passing:
            placements.setdefault(row["placement"], []).append(float(row["oal_in"]))
        within = [
            difference
            for values in placements.values()
            for difference in _pairwise_absolute(values)
        ]
        placement_means = [statistics.fmean(values) for values in placements.values()]
        between = _pairwise_absolute(placement_means)
        lines.extend(
            [
                f"### {estimator}",
                f"- availability: {len(passing)}/{len(selected)}",
                f"- within-placement P95 pairwise: {_fmt(_p95(within))} in",
                f"- within-placement maximum pairwise: {_fmt(max(within) if within else None)} in",
                f"- placement-mean range: {_fmt((max(placement_means) - min(placement_means)) if placement_means else None)} in",
                f"- between-placement P95 pairwise: {_fmt(_p95(between))} in",
                f"- between-placement maximum pairwise: {_fmt(max(between) if between else None)} in",
                "",
            ]
        )

    lines.extend(["## Fixture-2 independent placements", ""])
    for specimen in ("146", "178", "187", "197"):
        lines.extend([f"### Specimen {specimen}", ""])
        for estimator in estimators:
            selected = [
                row
                for row in rows
                if row["dataset"] == "fixture2_multispecimen"
                and row["specimen"] == specimen
                and row["estimator"] == estimator
            ]
            values = [float(row["oal_in"]) for row in selected if row["passed"] == "True"]
            pairwise = _pairwise_absolute(values)
            lines.append(
                f"- {estimator}: availability {len(values)}/{len(selected)}; "
                f"range {_fmt((max(values) - min(values)) if values else None)} in; "
                f"P95 pairwise {_fmt(_p95(pairwise))} in; "
                f"max pairwise {_fmt(max(pairwise) if pairwise else None)} in"
            )
        lines.append("")

    lines.extend(["## Specimen 146 fixed-position 10-frame sequence", ""])
    for estimator in estimators:
        selected = [
            row
            for row in rows
            if row["dataset"] == "fixture2_fixed10" and row["estimator"] == estimator
        ]
        values = [float(row["oal_in"]) for row in selected if row["passed"] == "True"]
        pairwise = _pairwise_absolute(values)
        lines.append(
            f"- {estimator}: availability {len(values)}/{len(selected)}; "
            f"range {_fmt((max(values) - min(values)) if values else None)} in; "
            f"P95 pairwise {_fmt(_p95(pairwise))} in; "
            f"max pairwise {_fmt(max(pairwise) if pairwise else None)} in"
        )

    lines.extend(
        [
            "",
            "## Interpretation guardrail",
            "",
            "These datasets are development/diagnostic evidence only. They may be used to choose or reject an estimator architecture, but they do not replace prospective validation of a subsequently frozen estimator.",
            "",
        ]
    )
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT
        / "data/oal_validation/post_v1_diagnostics/endface_hybrid_dev",
    )
    parser.add_argument(
        "--include-subpixel-v2",
        action="store_true",
        help="Also run the slower existing subpixel-v2 estimator.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    records = _repositioning_records(REPO_ROOT) + _fixture2_records(REPO_ROOT)
    rows: list[dict[str, str]] = []
    blank_cache: dict[Path, np.ndarray] = {}

    for record in records:
        blank = blank_cache.setdefault(record.blank_path, _load_gray(record.blank_path))
        image = _load_gray(record.image_path)
        for observation in _observations_for_image(
            blank, image, include_subpixel_v2=args.include_subpixel_v2
        ):
            rows.append(
                {
                    "dataset": record.dataset,
                    "specimen": record.specimen,
                    "placement": record.placement,
                    "sequence": str(record.sequence),
                    "image": str(record.image_path.relative_to(REPO_ROOT)),
                    "estimator": observation.estimator,
                    "passed": str(observation.passed),
                    "failure_reason": observation.failure_reason or "",
                    "oal_in": ""
                    if observation.length_inches is None
                    else f"{observation.length_inches:.12f}",
                    "length_pixels": ""
                    if observation.length_pixels is None
                    else f"{observation.length_pixels:.12f}",
                    "effective_ppi": ""
                    if observation.effective_ppi is None
                    else f"{observation.effective_ppi:.12f}",
                    "angle_degrees": ""
                    if observation.angle_degrees is None
                    else f"{observation.angle_degrees:.12f}",
                    "end_min_accepted": ""
                    if observation.end_min_accepted is None
                    else str(observation.end_min_accepted),
                    "end_max_accepted": ""
                    if observation.end_max_accepted is None
                    else str(observation.end_max_accepted),
                    "sidewall_min_accepted": ""
                    if observation.sidewall_min_accepted is None
                    else str(observation.sidewall_min_accepted),
                    "sidewall_max_accepted": ""
                    if observation.sidewall_max_accepted is None
                    else str(observation.sidewall_max_accepted),
                }
            )

    csv_path = output_dir / "endface_hybrid_observations.csv"
    fieldnames = list(rows[0].keys())
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    summary_path = output_dir / "SUMMARY.md"
    _write_summary(rows, summary_path)

    print(f"Wrote: {csv_path.relative_to(REPO_ROOT)}")
    print(f"Wrote: {summary_path.relative_to(REPO_ROOT)}")
    print()
    print(summary_path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
