#!/usr/bin/env python3
"""Recompute V3 descriptive results from preserved CSVs without changing inputs."""

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import statistics


REPO = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def finite(value):
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("Non-finite measurement")
    return number


def p95(values):
    return sorted(values)[math.ceil(0.95 * len(values)) - 1]


def summarize(root):
    paths = [root / "data/oal_validation/v3_formal/v3_cv_observations.csv",
             root / "data/oal_validation/derived/manual_reference_summary.csv"]
    observations, references = map(read_csv, paths)
    if len(observations) != 180 or len(references) != 60:
        raise ValueError("Expected 180 CV observations and 60 manual references")
    manual = {}
    for row in references:
        key = int(row["part_id"])
        if key in manual or row["reference_status"] != "ACCEPTED" or int(row["manual_n_valid"]) != 3:
            raise ValueError("Duplicate or unaccepted manual reference")
        manual[key] = finite(row["manual_mean_in"])
    groups = {}
    positions = set()
    for row in observations:
        key = int(row["specimen_id"])
        round_id, sequence = int(row["round"]), int(row["sequence"])
        position = (round_id, sequence)
        if round_id not in {1, 2, 3} or not 1 <= sequence <= 60 or position in positions:
            raise ValueError("Invalid or duplicate scheduled position")
        positions.add(position)
        if row["validity"] != "VALID":
            raise ValueError("Expected completed all-valid V3 dataset")
        group = groups.setdefault(key, {})
        if round_id in group:
            raise ValueError("Duplicate specimen round")
        group[round_id] = finite(row["endface_hybrid_in"])
    if set(groups) != set(manual) or any(set(g) != {1, 2, 3} for g in groups.values()):
        raise ValueError("CV/manual cohort or round coverage mismatch")
    errors, pairwise, false_passes, false_fails = [], [], [], []
    for key, group in sorted(groups.items()):
        values = list(group.values())
        mean = statistics.mean(values)
        errors.append(mean - manual[key])
        pairwise.extend(abs(a - b) for a, b in itertools.combinations(values, 2))
        cv_pass = 0.9900 <= mean <= 1.0100
        manual_pass = 0.9900 <= manual[key] <= 1.0100
        if cv_pass and not manual_pass:
            false_passes.append(key)
        if manual_pass and not cv_pass:
            false_fails.append(key)
    return {
        "input_sha256": {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        "specimens": len(groups), "valid_observations": len(observations),
        "availability": 1.0, "pairwise_differences": len(pairwise),
        "percentile_method": "nearest rank; related pairwise differences are descriptive",
        "bias_in": statistics.mean(errors),
        "mae_in": statistics.mean(map(abs, errors)),
        "rmse_in": math.sqrt(statistics.mean(e * e for e in errors)),
        "p95_absolute_error_in": p95(list(map(abs, errors))),
        "maximum_absolute_error_in": max(map(abs, errors)),
        "p95_pairwise_repositioning_in": p95(pairwise),
        "false_pass_specimens": false_passes, "false_fail_specimens": false_fails,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Create a new JSON file outside the repository")
    args = parser.parse_args()
    try:
        result = summarize(REPO)
        text = json.dumps(result, indent=2) + "\n"
        if args.output:
            output = args.output.resolve()
            if output.is_relative_to(REPO):
                raise ValueError("Output must be outside the repository")
            with output.open("x", encoding="utf-8") as stream:
                stream.write(text)
        else:
            print(text, end="")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"STOP: {error}\n")


if __name__ == "__main__":
    main()
