#!/usr/bin/env python3

from __future__ import annotations

import csv
import itertools
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np


REPO = Path.home() / "CaseMetrology"

BASE = (
    REPO
    / "data"
    / "oal_validation"
    / "post_v1_diagnostics"
    / "fixture_rocking_test"
)

REFERENCE_ANALYZER = REPO / "scripts/analyze_fixture_rocking_test_146.py"

REFERENCE_BLANK = (
    BASE
    / "specimen146"
    / "fixture_rocking_blank_20260911_211535_189415.png"
)

SPECIMENS = [146, 121, 178, 187, 197]
NEW_SPECIMENS = [121, 178, 187, 197]

ESTIMATORS = [
    "pca",
    "geometry",
    "endface_hybrid",
]

# Previously verified specimen-146 V3 results.
EXPECTED_146_P95 = {
    "pca": 0.001640535,
    "geometry": 0.001844171,
    "endface_hybrid": 0.001486210,
}

SUMMARY_CSV = BASE / "fixture_rocking_generalization_summary.csv"
PAIRWISE_CSV = BASE / "fixture_rocking_generalization_pairwise.csv"


def stop(message: str):
    raise RuntimeError(f"\nSTOP: {message}")


def result_csv(specimen: int) -> Path:
    return (
        BASE
        / f"specimen{specimen}"
        / f"specimen{specimen}_fixture_rocking_results.csv"
    )


def placement_files(specimen: int):
    d = BASE / f"specimen{specimen}"
    return sorted(
        d.glob(f"specimen{specimen}_placement_*.png")
    )


def generate_new_specimen_results(specimen: int, source: str):
    """
    Run the proven specimen-146 analyzer with ONLY:
      - DATA_DIR changed
      - placement filename prefix changed
      - output CSV filename changed

    Estimator logic is untouched.
    """

    data_dir = BASE / f"specimen{specimen}"

    if not data_dir.exists():
        stop(f"missing directory for specimen {specimen}")

    images = placement_files(specimen)

    if len(images) != 10:
        stop(
            f"specimen {specimen} has {len(images)} placement images; "
            "expected exactly 10"
        )

    existing_blanks = sorted(
        data_dir.glob("fixture_rocking_blank_*.png")
    )

    if existing_blanks:
        stop(
            f"specimen {specimen} already contains a blank reference. "
            "Refusing to introduce ambiguity."
        )

    output_csv = result_csv(specimen)

    if output_csv.exists():
        stop(
            f"{output_csv} already exists. "
            "Refusing to overwrite prior analysis."
        )

    blank_link = data_dir / REFERENCE_BLANK.name

    # Give the unchanged analyzer access to the exact 146 blank.
    blank_link.symlink_to(REFERENCE_BLANK)

    modified = source

    modified = modified.replace(
        "fixture_rocking_test/specimen146",
        f"fixture_rocking_test/specimen{specimen}",
    )

    modified = modified.replace(
        'glob("specimen146_placement_*.png")',
        f'glob("specimen{specimen}_placement_*.png")',
    )

    modified = modified.replace(
        "specimen146_fixture_rocking_results.csv",
        f"specimen{specimen}_fixture_rocking_results.csv",
    )

    # Temporary script is deliberately created INSIDE scripts/
    # so any __file__-relative repo logic remains unchanged.
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix=f"_fixture_generalization_{specimen}_",
            dir=REPO / "scripts",
            delete=False,
        ) as f:
            f.write(modified)
            temp_path = Path(f.name)

        completed = subprocess.run(
            [sys.executable, str(temp_path)],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        log_path = (
            data_dir
            / f"specimen{specimen}_fixture_rocking_analysis.log"
        )

        log_path.write_text(completed.stdout)

        if completed.returncode != 0:
            print(completed.stdout)
            stop(
                f"frozen analyzer failed for specimen {specimen}; "
                f"return code {completed.returncode}"
            )

        if not output_csv.exists():
            stop(
                f"analyzer completed but did not create {output_csv}"
            )

    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()

        if blank_link.is_symlink():
            blank_link.unlink()


def find_wide_field(fields, estimator):
    lower = {f.lower(): f for f in fields}

    candidates = {
        "pca": [
            "pca",
            "pca_oal",
            "pca_oal_in",
            "pca_measurement",
        ],
        "geometry": [
            "geometry",
            "geometry_oal",
            "geometry_oal_in",
            "geometry_measurement",
        ],
        "endface_hybrid": [
            "endface_hybrid",
            "endface_hybrid_oal",
            "endface_hybrid_oal_in",
            "hybrid",
            "hybrid_oal",
            "hybrid_oal_in",
        ],
    }

    for candidate in candidates[estimator]:
        if candidate in lower:
            return lower[candidate]

    for field in fields:
        x = field.lower()

        if any(
            bad in x
            for bad in ("valid", "status", "error", "path", "image")
        ):
            continue

        if estimator == "pca":
            match = "pca" in x

        elif estimator == "geometry":
            match = "geometry" in x

        else:
            match = (
                ("endface" in x and "hybrid" in x)
                or x.startswith("hybrid")
            )

        if match and ("oal" in x or "measurement" in x):
            return field

    return None


def parse_float(value):
    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    try:
        x = float(value)
    except ValueError:
        return None

    if not np.isfinite(x):
        return None

    return x


def load_measurements(specimen: int):
    path = result_csv(specimen)

    if not path.exists():
        stop(f"missing results CSV for specimen {specimen}: {path}")

    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []

    if not rows:
        stop(f"empty results CSV for specimen {specimen}")

    results = {
        estimator: []
        for estimator in ESTIMATORS
    }

    # First try wide format: one row per placement with one
    # measurement column for each estimator.
    detected = {
        est: find_wide_field(fields, est)
        for est in ESTIMATORS
    }

    if all(detected.values()):
        placement_field = next(
            (
                f for f in fields
                if f.lower() == "placement"
            ),
            None,
        )

        for row_index, row in enumerate(rows, start=1):
            if placement_field:
                try:
                    placement = int(float(row[placement_field]))
                except Exception:
                    placement = row_index
            else:
                placement = row_index

            for estimator in ESTIMATORS:
                value = parse_float(row[detected[estimator]])

                if value is not None:
                    results[estimator].append(
                        (placement, value)
                    )

        return results

    # Otherwise support long format:
    # placement | estimator | value/oal
    estimator_field = next(
        (
            f for f in fields
            if f.lower() in ("estimator", "method")
        ),
        None,
    )

    placement_field = next(
        (
            f for f in fields
            if f.lower() == "placement"
        ),
        None,
    )

    value_field = next(
        (
            f for f in fields
            if (
                "oal" in f.lower()
                or f.lower() in (
                    "value",
                    "measurement",
                    "measurement_in",
                    "length_inches",
                )
            )
        ),
        None,
    )

    if estimator_field and value_field:
        for row_index, row in enumerate(rows, start=1):
            name = str(row[estimator_field]).strip().lower()
            value = parse_float(row[value_field])

            if value is None:
                continue

            if placement_field:
                try:
                    placement = int(float(row[placement_field]))
                except Exception:
                    placement = row_index
            else:
                placement = row_index

            aliases = {
                "pca": "pca",
                "geometry": "geometry",
                "endface_hybrid": "endface_hybrid",
                "hybrid": "endface_hybrid",
                "endface hybrid": "endface_hybrid",
            }

            estimator = aliases.get(name)

            if estimator:
                results[estimator].append(
                    (placement, value)
                )

        return results

    stop(
        f"Could not identify estimator measurement columns in "
        f"{path.name}. Fields were: {fields}"
    )


def pairwise_differences(values):
    return np.asarray(
        [
            abs(a - b)
            for a, b in itertools.combinations(values, 2)
        ],
        dtype=float,
    )


def summarize(values):
    values = np.asarray(values, dtype=float)

    pairwise = pairwise_differences(values)

    return {
        "n": len(values),
        "mean": float(np.mean(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "range": float(np.ptp(values)),
        "sd": (
            float(np.std(values, ddof=1))
            if len(values) > 1
            else float("nan")
        ),
        "pairwise_n": len(pairwise),
        "pairwise_p95": (
            float(np.percentile(pairwise, 95))
            if len(pairwise)
            else float("nan")
        ),
        "pairwise_max": (
            float(np.max(pairwise))
            if len(pairwise)
            else float("nan")
        ),
        "pairwise": pairwise,
    }


def main():
    print("=" * 88)
    print("V3 FIXTURE-STABILITY GENERALIZATION ANALYSIS")
    print("=" * 88)

    if not REFERENCE_ANALYZER.exists():
        stop("reference 146 analyzer is missing")

    if not REFERENCE_BLANK.exists():
        stop("reference 146 blank is missing")

    # Confirm all raw image sets before doing anything.
    for specimen in SPECIMENS:
        count = len(placement_files(specimen))

        print(
            f"Specimen {specimen}: "
            f"{count}/10 placement images"
        )

        if count != 10:
            stop(
                f"specimen {specimen} image count is {count}, "
                "not 10"
            )

    reference_source = REFERENCE_ANALYZER.read_text()

    # We deliberately do NOT rerun specimen 146.
    if not result_csv(146).exists():
        stop(
            "existing specimen-146 results CSV is missing. "
            "146 will not be silently recalculated."
        )

    print()
    print(
        "Using existing specimen-146 results as the "
        "locked reference."
    )

    # Generate result CSVs for new specimens only.
    # If a prior run already generated a result CSV successfully,
    # reuse it rather than rerunning the frozen estimators.
    for specimen in NEW_SPECIMENS:
        print()

        if result_csv(specimen).exists():
            print(
                f"Reusing existing frozen-estimator results: "
                f"specimen {specimen}"
            )
            continue

        print(
            f"Running frozen estimator analysis: "
            f"specimen {specimen}"
        )

        generate_new_specimen_results(
            specimen,
            reference_source,
        )

        print(
            f"PASS: specimen {specimen} results created"
        )

    print()
    print("=" * 88)
    print("SPECIMEN-SPECIFIC RESULTS")
    print("=" * 88)

    all_results = {}
    summary_rows = []
    pairwise_rows = []

    for specimen in SPECIMENS:
        measurements = load_measurements(specimen)
        all_results[specimen] = measurements

        print()
        print("-" * 88)
        print(f"SPECIMEN {specimen}")
        print("-" * 88)

        for estimator in ESTIMATORS:
            entries = measurements[estimator]

            entries = sorted(
                entries,
                key=lambda x: x[0],
            )

            values = [x[1] for x in entries]

            if not values:
                print(
                    f"{estimator:16s}: "
                    "0/10 valid — NO RESULT"
                )
                continue

            stats = summarize(values)

            summary_rows.append(
                {
                    "scope": "specimen",
                    "specimen": specimen,
                    "estimator": estimator,
                    "valid_n": stats["n"],
                    "mean_oal_in": stats["mean"],
                    "min_oal_in": stats["min"],
                    "max_oal_in": stats["max"],
                    "range_in": stats["range"],
                    "sample_sd_in": stats["sd"],
                    "pairwise_n": stats["pairwise_n"],
                    "pairwise_p95_in": stats["pairwise_p95"],
                    "pairwise_max_in": stats["pairwise_max"],
                }
            )

            for delta in stats["pairwise"]:
                pairwise_rows.append(
                    {
                        "specimen": specimen,
                        "estimator": estimator,
                        "abs_pairwise_difference_in": float(delta),
                    }
                )

            print()
            print(estimator.upper())
            print(
                f"  Valid:             "
                f"{stats['n']}/10"
            )
            print(
                f"  Mean OAL:          "
                f"{stats['mean']:.9f} in"
            )
            print(
                f"  Range:             "
                f"{stats['range']:.9f} in"
            )
            print(
                f"  Sample SD:         "
                f"{stats['sd']:.9f} in"
            )
            print(
                f"  Pairwise P95:      "
                f"{stats['pairwise_p95']:.9f} in"
            )
            print(
                f"  Pairwise maximum:  "
                f"{stats['pairwise_max']:.9f} in"
            )

    # --------------------------------------------------
    # 146 REPRODUCTION CHECK
    # --------------------------------------------------

    print()
    print("=" * 88)
    print("SPECIMEN-146 REFERENCE CHECK")
    print("=" * 88)

    for estimator in ESTIMATORS:
        values = [
            x[1]
            for x in all_results[146][estimator]
        ]

        stats = summarize(values)

        observed = stats["pairwise_p95"]
        expected = EXPECTED_146_P95[estimator]
        difference = abs(observed - expected)

        print(
            f"{estimator:16s} "
            f"observed={observed:.9f}  "
            f"expected={expected:.9f}  "
            f"difference={difference:.12f}"
        )

        if difference > 5e-9:
            stop(
                f"specimen-146 {estimator} P95 does not "
                "reproduce the previously verified result"
            )

    print("REFERENCE CHECK: PASS")

    # --------------------------------------------------
    # POOLED WITHIN-SPECIMEN PAIRWISE RESULTS
    # --------------------------------------------------

    print()
    print("=" * 88)
    print("POOLED WITHIN-SPECIMEN REPOSITIONING RESULTS")
    print("=" * 88)

    for estimator in ESTIMATORS:
        pooled = []

        specimen_p95 = []

        total_valid = 0

        for specimen in SPECIMENS:
            values = [
                x[1]
                for x in all_results[specimen][estimator]
            ]

            total_valid += len(values)

            if len(values) >= 2:
                diffs = pairwise_differences(values)
                pooled.extend(diffs.tolist())

                specimen_p95.append(
                    (
                        specimen,
                        float(
                            np.percentile(
                                diffs,
                                95,
                            )
                        ),
                    )
                )

        pooled = np.asarray(
            pooled,
            dtype=float,
        )

        if not len(pooled):
            continue

        pooled_p95 = float(
            np.percentile(
                pooled,
                95,
            )
        )

        pooled_max = float(np.max(pooled))
        pooled_median = float(np.median(pooled))
        pooled_mean = float(np.mean(pooled))

        worst_specimen, worst_p95 = max(
            specimen_p95,
            key=lambda x: x[1],
        )

        best_specimen, best_p95 = min(
            specimen_p95,
            key=lambda x: x[1],
        )

        print()
        print(estimator.upper())
        print(
            f"  Measurement availability: "
            f"{total_valid}/50 "
            f"({100.0 * total_valid / 50:.3f}%)"
        )
        print(
            f"  Within-specimen pairs:     "
            f"{len(pooled)}"
        )
        print(
            f"  Pooled mean pairwise:      "
            f"{pooled_mean:.9f} in"
        )
        print(
            f"  Pooled median pairwise:    "
            f"{pooled_median:.9f} in"
        )
        print(
            f"  Pooled P95 pairwise:       "
            f"{pooled_p95:.9f} in"
        )
        print(
            f"  Pooled maximum pairwise:   "
            f"{pooled_max:.9f} in"
        )
        print(
            f"  Best specimen P95:         "
            f"{best_specimen} "
            f"({best_p95:.9f} in)"
        )
        print(
            f"  Worst specimen P95:        "
            f"{worst_specimen} "
            f"({worst_p95:.9f} in)"
        )

        summary_rows.append(
            {
                "scope": "pooled",
                "specimen": "ALL",
                "estimator": estimator,
                "valid_n": total_valid,
                "mean_oal_in": "",
                "min_oal_in": "",
                "max_oal_in": "",
                "range_in": "",
                "sample_sd_in": "",
                "pairwise_n": len(pooled),
                "pairwise_p95_in": pooled_p95,
                "pairwise_max_in": pooled_max,
            }
        )

    # --------------------------------------------------
    # WRITE DERIVED OUTPUTS
    # --------------------------------------------------

    with SUMMARY_CSV.open("w", newline="") as f:
        fieldnames = [
            "scope",
            "specimen",
            "estimator",
            "valid_n",
            "mean_oal_in",
            "min_oal_in",
            "max_oal_in",
            "range_in",
            "sample_sd_in",
            "pairwise_n",
            "pairwise_p95_in",
            "pairwise_max_in",
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(summary_rows)

    with PAIRWISE_CSV.open("w", newline="") as f:
        fieldnames = [
            "specimen",
            "estimator",
            "abs_pairwise_difference_in",
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(pairwise_rows)

    print()
    print("=" * 88)
    print("ANALYSIS COMPLETE")
    print("=" * 88)
    print(f"Summary:  {SUMMARY_CSV}")
    print(f"Pairwise: {PAIRWISE_CSV}")


if __name__ == "__main__":
    main()
