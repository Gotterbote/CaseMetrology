#!/usr/bin/env python3
"""Generate thesis-ready figures for CaseMetrology Formal OAL Validation V1.

V1 acquisition condition:
- independent specimen removal and replacement;
- free placement within the camera viewing window;
- no dedicated measurement-positioning fixture;
- consistent gross base-to-mouth vertical orientation;
- exact position and small angular variation otherwise unconstrained.

Figures are generated only from the preserved formal V1 derived results.
No raw measurements or statistical results are modified.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


LSL_IN = 0.9900
USL_IN = 1.0100

STRATUM_ORDER = (
    "below_lsl",
    "near_lsl_in_spec",
    "central_nominal",
    "near_usl_in_spec",
    "above_usl",
)

STRATUM_LABELS = (
    "Below LSL",
    "Near LSL",
    "Central",
    "Near USL",
    "Above USL",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_inputs(root: Path):
    required = (
        "oal_validation_analysis.csv",
        "manual_reference_summary.csv",
        "cv_summary.csv",
        "formal_validation_statistics.json",
    )

    for name in required:
        if not (root / name).is_file():
            fail(f"Missing required V1 result file: {root / name}")

    analysis = read_csv(root / "oal_validation_analysis.csv")
    manual = read_csv(root / "manual_reference_summary.csv")
    cv = read_csv(root / "cv_summary.csv")

    with (root / "formal_validation_statistics.json").open(
        encoding="utf-8"
    ) as handle:
        summary = json.load(handle)

    if len(analysis) != 60:
        fail(
            "Expected 60 specimen-level analysis rows; "
            f"found {len(analysis)}"
        )

    if len(manual) != 60:
        fail(
            "Expected 60 manual specimen summaries; "
            f"found {len(manual)}"
        )

    if len(cv) != 60:
        fail(
            "Expected 60 CV specimen summaries; "
            f"found {len(cv)}"
        )

    return analysis, manual, cv, summary


def save_figure(fig, output_dir: Path, stem: str) -> None:
    fig.tight_layout()

    fig.savefig(
        output_dir / f"{stem}.png",
        dpi=300,
        bbox_inches="tight",
    )

    fig.savefig(
        output_dir / f"{stem}.pdf",
        bbox_inches="tight",
    )

    plt.close(fig)


def make_cv_vs_manual(analysis, summary, output_dir):
    manual = np.array(
        [float(r["manual_mean_in"]) for r in analysis]
    )
    cv = np.array(
        [float(r["cv_mean_in"]) for r in analysis]
    )

    regression = summary["regression"]

    lower = min(manual.min(), cv.min()) - 0.002
    upper = max(manual.max(), cv.max()) + 0.002

    xline = np.linspace(lower, upper, 200)

    fig, ax = plt.subplots(figsize=(7.5, 6.0))

    ax.scatter(manual, cv)

    ax.plot(
        xline,
        xline,
        linestyle="--",
        label="1:1 identity",
    )

    ax.plot(
        xline,
        regression["intercept_in"]
        + regression["slope"] * xline,
        label="OLS fit",
    )

    ax.set_xlabel("Formal manual-reference mean OAL (in)")
    ax.set_ylabel("CV specimen mean OAL (in)")
    ax.set_title("CV OAL Versus Formal Manual Reference")
    ax.legend()

    ax.text(
        0.03,
        0.97,
        (
            f"Slope = {regression['slope']:.4f}\n"
            f"Intercept = {regression['intercept_in']:+.4f} in\n"
            f"$R^2$ = {regression['r_squared']:.4f}"
        ),
        transform=ax.transAxes,
        va="top",
    )

    save_figure(
        fig,
        output_dir,
        "figure_v1_cv_vs_manual",
    )


def make_signed_error(analysis, summary, output_dir):
    manual = np.array(
        [float(r["manual_mean_in"]) for r in analysis]
    )
    error = np.array(
        [float(r["difference_in"]) for r in analysis]
    )

    bias = summary["primary_agreement"]["bias_in"]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.scatter(manual, error)

    ax.axhline(
        0.0,
        linestyle="--",
        label="Zero error",
    )

    ax.axhline(
        bias,
        label=f"Mean bias = {bias:+.4f} in",
    )

    ax.axvline(
        LSL_IN,
        linestyle=":",
        label="Specification limits",
    )

    ax.axvline(
        USL_IN,
        linestyle=":",
    )

    ax.set_xlabel("Formal manual-reference mean OAL (in)")
    ax.set_ylabel("Signed error, CV − manual (in)")
    ax.set_title("Signed OAL Error Across the Validation Range")
    ax.legend()

    save_figure(
        fig,
        output_dir,
        "figure_v1_signed_error_vs_reference",
    )


def make_bland_altman(analysis, summary, output_dir):
    manual = np.array(
        [float(r["manual_mean_in"]) for r in analysis]
    )
    cv = np.array(
        [float(r["cv_mean_in"]) for r in analysis]
    )

    mean_pair = (manual + cv) / 2.0
    difference = cv - manual

    ba = summary["bland_altman"]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.scatter(mean_pair, difference)

    ax.axhline(
        ba["bias_in"],
        label=f"Bias = {ba['bias_in']:+.4f} in",
    )

    ax.axhline(
        ba["loa_lower_in"],
        linestyle="--",
        label=f"Lower LOA = {ba['loa_lower_in']:+.4f} in",
    )

    ax.axhline(
        ba["loa_upper_in"],
        linestyle="--",
        label=f"Upper LOA = {ba['loa_upper_in']:+.4f} in",
    )

    ax.set_xlabel("Mean of CV and manual OAL (in)")
    ax.set_ylabel("CV − manual difference (in)")
    ax.set_title("Bland–Altman Agreement")
    ax.legend()

    save_figure(
        fig,
        output_dir,
        "figure_v1_bland_altman",
    )


def make_absolute_error(analysis, summary, output_dir):
    absolute_error = np.array(
        [float(r["absolute_error_in"]) for r in analysis]
    )

    p95 = summary[
        "primary_agreement"
    ]["p95_absolute_error_in"]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.hist(
        absolute_error,
        bins="auto",
    )

    ax.axvline(
        0.003,
        linestyle="--",
        label="Prespecified P95 target = 0.003 in",
    )

    ax.axvline(
        p95,
        label=f"Observed P95 = {p95:.4f} in",
    )

    ax.set_xlabel("Absolute specimen-level error (in)")
    ax.set_ylabel("Specimen count")
    ax.set_title("Absolute Specimen-Level OAL Error")
    ax.legend()

    save_figure(
        fig,
        output_dir,
        "figure_v1_absolute_error_distribution",
    )


def make_placement_repeatability(cv, summary, output_dir):
    pairwise = []

    for r in cv:
        c1 = float(r["cv_1_in"])
        c2 = float(r["cv_2_in"])
        c3 = float(r["cv_3_in"])

        pairwise.extend(
            (
                abs(c1 - c2),
                abs(c1 - c3),
                abs(c2 - c3),
            )
        )

    if len(pairwise) != 180:
        fail(
            "Expected 180 independent-placement pairwise differences; "
            f"found {len(pairwise)}"
        )

    p95 = summary[
        "cv_repositioning_repeatability"
    ]["p95_pairwise_difference_in"]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.hist(
        pairwise,
        bins="auto",
    )

    ax.axvline(
        0.002,
        linestyle="--",
        label="Prespecified P95 target = 0.002 in",
    )

    ax.axvline(
        p95,
        label=f"Observed P95 = {p95:.4f} in",
    )

    ax.set_xlabel(
        "Absolute difference between independent placements (in)"
    )
    ax.set_ylabel("Pairwise comparison count")
    ax.set_title(
        "CV Repeatability Under Independent Free Placement"
    )
    ax.legend()

    save_figure(
        fig,
        output_dir,
        "figure_v1_independent_placement_repeatability",
    )


def make_repeatability_comparison(manual, cv, output_dir):
    manual_sd = [
        float(r["manual_sd_in"])
        for r in manual
    ]

    cv_sd = [
        float(r["cv_sd_in"])
        for r in cv
    ]

    fig, ax = plt.subplots(figsize=(6.5, 5.5))

    ax.boxplot(
        [manual_sd, cv_sd],
        labels=[
            "Manual reference",
            "CV free placement",
        ],
        showmeans=True,
    )

    ax.set_ylabel(
        "Within-specimen SD across three rounds (in)"
    )

    ax.set_title(
        "Manual and CV Within-Specimen Repeatability"
    )

    save_figure(
        fig,
        output_dir,
        "figure_v1_repeatability_comparison",
    )


def make_stratum_error(analysis, output_dir):
    grouped = []

    for stratum in STRATUM_ORDER:
        values = [
            float(r["difference_in"])
            for r in analysis
            if r["selection_stratum"] == stratum
        ]

        if not values:
            fail(f"No values found for stratum {stratum}")

        grouped.append(values)

    fig, ax = plt.subplots(figsize=(9.0, 5.5))

    ax.boxplot(
        grouped,
        labels=STRATUM_LABELS,
        showmeans=True,
    )

    ax.axhline(
        0.0,
        linestyle="--",
    )

    ax.set_xlabel("Frozen sampling stratum")
    ax.set_ylabel("Signed error, CV − manual (in)")
    ax.set_title("Signed OAL Error by Frozen Sampling Stratum")

    plt.setp(
        ax.get_xticklabels(),
        rotation=20,
        ha="right",
    )

    save_figure(
        fig,
        output_dir,
        "figure_v1_error_by_stratum",
    )


def make_confusion_matrix(summary, output_dir):
    cls = summary["classification"]

    matrix = np.array(
        [
            [
                cls["true_conforming"],
                cls["false_fails"],
            ],
            [
                cls["false_passes"],
                cls["true_nonconforming"],
            ],
        ]
    )

    fig, ax = plt.subplots(figsize=(6.8, 5.5))

    image = ax.imshow(matrix)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    ax.set_xticklabels(
        ["CV conforming", "CV nonconforming"]
    )

    ax.set_yticklabels(
        [
            "Reference conforming",
            "Reference nonconforming",
        ]
    )

    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                str(matrix[i, j]),
                ha="center",
                va="center",
            )

    ax.set_title(
        "Formal OAL Classification Confusion Matrix"
    )

    fig.colorbar(
        image,
        ax=ax,
        label="Specimen count",
    )

    save_figure(
        fig,
        output_dir,
        "figure_v1_classification_confusion_matrix",
    )


def make_qq(analysis, output_dir):
    error = np.array(
        [float(r["difference_in"]) for r in analysis]
    )

    (
        theoretical,
        ordered,
    ), (
        slope,
        intercept,
        _
    ) = stats.probplot(
        error,
        dist="norm",
        fit=True,
    )

    fig, ax = plt.subplots(figsize=(6.5, 5.5))

    ax.scatter(
        theoretical,
        ordered,
    )

    xline = np.linspace(
        min(theoretical),
        max(theoretical),
        100,
    )

    ax.plot(
        xline,
        slope * xline + intercept,
        linestyle="--",
    )

    ax.set_xlabel("Theoretical normal quantiles")
    ax.set_ylabel("Ordered signed errors (in)")
    ax.set_title(
        "Q–Q Assessment of Signed Specimen-Level Errors"
    )

    save_figure(
        fig,
        output_dir,
        "figure_v1_signed_error_qq",
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--root",
        type=Path,
        default=Path("data/oal_validation/derived"),
        help="directory containing preserved V1 derived results",
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="validate inputs without generating figures",
    )

    args = parser.parse_args()

    root = args.root.resolve()

    analysis, manual, cv, summary = load_inputs(root)

    if args.check:
        print("FIGURE INPUT CHECK PASS")
        print("60 formal V1 specimen-level rows verified.")
        print("60 manual specimen summaries verified.")
        print("60 CV specimen summaries verified.")
        print("No figures were created.")
        return 0

    output_dir = root / "figures"

    if output_dir.exists():
        fail(
            "Refusing to overwrite existing formal figure directory: "
            f"{output_dir}"
        )

    output_dir.mkdir()

    make_cv_vs_manual(
        analysis,
        summary,
        output_dir,
    )

    make_signed_error(
        analysis,
        summary,
        output_dir,
    )

    make_bland_altman(
        analysis,
        summary,
        output_dir,
    )

    make_absolute_error(
        analysis,
        summary,
        output_dir,
    )

    make_placement_repeatability(
        cv,
        summary,
        output_dir,
    )

    make_repeatability_comparison(
        manual,
        cv,
        output_dir,
    )

    make_stratum_error(
        analysis,
        output_dir,
    )

    make_confusion_matrix(
        summary,
        output_dir,
    )

    make_qq(
        analysis,
        output_dir,
    )

    print("FIGURE GENERATION PASS")
    print(f"Output directory: {output_dir}")
    print("Generated 9 PNG files and 9 PDF files.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"FIGURE GENERATION FAIL: {exc}")
        raise SystemExit(1)
