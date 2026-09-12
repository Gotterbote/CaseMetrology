#!/usr/bin/env python3

from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[1]

DATA_DIR = (
    REPO
    / "data/oal_validation/post_v1_diagnostics/"
      "fixture_rocking_test/specimen146"
)

EVALUATOR = REPO / "scripts/evaluate_oal_endface_hybrid_dev.py"

# Load the already-frozen development evaluator.
spec = importlib.util.spec_from_file_location(
    "endface_hybrid_dev",
    EVALUATOR,
)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {EVALUATOR}")

module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

blank_paths = sorted(DATA_DIR.glob("fixture_rocking_blank_*.png"))
image_paths = sorted(DATA_DIR.glob("specimen146_placement_*.png"))

if len(blank_paths) != 1:
    raise RuntimeError(
        f"Expected exactly 1 current blank; found {len(blank_paths)}"
    )

if len(image_paths) != 10:
    raise RuntimeError(
        f"Expected exactly 10 placement images; found {len(image_paths)}"
    )

blank = cv2.imread(str(blank_paths[0]), cv2.IMREAD_GRAYSCALE)
if blank is None:
    raise RuntimeError(f"Could not read blank: {blank_paths[0]}")

rows = []

for placement, image_path in enumerate(image_paths, start=1):

    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise RuntimeError(f"Could not read image: {image_path}")

    observations = module._observations_for_image(
        blank,
        image,
        include_subpixel_v2=False,
    )

    for obs in observations:
        rows.append(
            {
                "placement": placement,
                "image": image_path.name,
                "estimator": obs.estimator,
                "passed": obs.passed,
                "failure_reason": obs.failure_reason or "",
                "length_pixels": obs.length_pixels,
                "length_inches": obs.length_inches,
                "effective_ppi": obs.effective_ppi,
                "angle_degrees": obs.angle_degrees,
            }
        )

csv_path = DATA_DIR / "specimen146_fixture_rocking_results.csv"

with csv_path.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "placement",
            "image",
            "estimator",
            "passed",
            "failure_reason",
            "length_pixels",
            "length_inches",
            "effective_ppi",
            "angle_degrees",
        ],
    )
    writer.writeheader()
    writer.writerows(rows)

# Previous Fixture-2 independent-placement P95 results for specimen 146.
OLD_P95 = {
    "pca": 0.003707657,
    "geometry": 0.003282319,
    "endface_hybrid": 0.003271088,
}

print()
print("=" * 92)
print("SPECIMEN 146 — ROCKING-REMOVED FIXTURE TEST")
print("=" * 92)
print(f"Blank:  {blank_paths[0].name}")
print(f"Images: {len(image_paths)}")
print()

for estimator in ("pca", "geometry", "endface_hybrid"):

    valid = [
        r
        for r in rows
        if r["estimator"] == estimator
        and r["passed"]
        and r["length_inches"] is not None
    ]

    print("-" * 92)
    print(estimator.upper())
    print("-" * 92)

    for r in valid:
        print(
            f"Placement {int(r['placement']):02d}: "
            f"{float(r['length_inches']):.9f} in"
        )

    if len(valid) < 2:
        print(f"Only {len(valid)}/10 valid observations.")
        print()
        continue

    values = np.asarray(
        [float(r["length_inches"]) for r in valid],
        dtype=np.float64,
    )

    pairwise = np.asarray(
        [
            abs(values[i] - values[j])
            for i in range(len(values))
            for j in range(i + 1, len(values))
        ],
        dtype=np.float64,
    )

    minimum = float(values.min())
    maximum = float(values.max())
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    total_range = maximum - minimum
    p95 = float(np.percentile(pairwise, 95))

    old_p95 = OLD_P95[estimator]
    reduction = 100.0 * (old_p95 - p95) / old_p95

    print()
    print(f"Valid measurements:      {len(values)}/10")
    print(f"Mean OAL:                {mean:.9f} in")
    print(f"Minimum:                 {minimum:.9f} in")
    print(f"Maximum:                 {maximum:.9f} in")
    print(f"10-placement range:      {total_range:.9f} in")
    print(f"Sample SD:               {sd:.9f} in")
    print(f"Pairwise comparisons:    {len(pairwise)}")
    print(f"NEW pairwise P95:        {p95:.9f} in")
    print(f"OLD Fixture-2 P95:       {old_p95:.9f} in")
    print(f"P95 change/reduction:    {reduction:.2f}%")

    if p95 <= 0.0010:
        result = "MAJOR BREAKTHROUGH"
    elif p95 <= 0.0015:
        result = "VERY STRONG IMPROVEMENT"
    elif p95 <= 0.0020:
        result = "MEETS ORIGINAL REPEATABILITY TARGET REGION"
    elif p95 <= 0.0025:
        result = "IMPROVED, BUT IMPORTANT RESIDUAL REMAINS"
    else:
        result = "ROCKING REMOVAL DID NOT RESOLVE PRIMARY VARIATION"

    print(f"Interpretation:          {result}")
    print()

print("=" * 92)
print(f"Results written to:")
print(csv_path)
print("=" * 92)
