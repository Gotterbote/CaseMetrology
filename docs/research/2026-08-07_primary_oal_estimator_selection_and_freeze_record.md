# Primary OAL Estimator Selection and Freeze Record

**Date:** 2026-08-07  
**Project:** CaseMetrology  
**Measurement:** Fixtureless top-down overall length (OAL)  
**Selected method:** Robust geometry estimator using fitted sidewalls and fitted end faces  

## 1. Purpose

This record formally selects and freezes the geometry-based OAL estimator as the primary computer-vision measurement method for thesis calibration and validation.

The estimator is being frozen before formal validation so that the validation dataset is not used to iteratively tune the measurement algorithm. Any subsequent change to the frozen estimator must be documented and must trigger a determination of whether previously collected validation results remain valid.

## 2. Selected Implementation

Primary estimator source file:

`src/measurement/topdown_oal_geometry.py`

Source-file provenance:

- Commit introducing the geometry estimator: `8bb3a9f` — `Add geometry-based fixtureless OAL estimator`
- SHA-256 of frozen source file:

`d80aa30e1f7702833b03444af3cb80c6f3b87d1019704026a6750bc3aee44b3b`

The estimator determines OAL from robustly fitted sidewalls and fitted physical end faces rather than from PCA-axis extreme mask pixels.

## 3. Verification Before Freeze

Before selection, the repository test suite was executed:

- Tests passed: **45**
- Tests failed: **0**

The geometry comparison was then reproduced on the existing 27 accepted development masks:

- Source masks: **27**
- Geometry estimator failures: **0**
- Geometry diagnostic flags: **27**

The diagnostic flags were residual-quality warnings rather than estimator execution failures.

## 4. Static Repeatability Evidence

For `trial_03_static`, the geometry estimator produced:

- Count: **10**
- Mean: **521.484317 px**
- Median: **521.486602 px**
- Standard deviation: **0.025910 px**
- Minimum: **521.437588 px**
- Maximum: **521.516659 px**
- Range: **0.079071 px**

The prior PCA/extreme-mask baseline produced:

- Standard deviation: **0.050349 px**
- Range: **0.166581 px**

The geometry estimator therefore reduced the static standard deviation by approximately 48.5% and reduced the static range by approximately 52.5% relative to the PCA/extreme-mask development baseline.

## 5. Controlled-Orientation Evidence

For `trial_05_controlled_orientation`, the geometry estimator successfully processed all 17 accepted masks.

Orientation-group medians were:

| Orientation group | PCA baseline median (px) | Geometry median (px) | Geometry minus baseline (px) |
|---|---:|---:|---:|
| angle_000_controlled | 523.069154 | 520.811662 | -2.257492 |
| angle_020_controlled | 522.776435 | 520.585730 | -2.190705 |
| angle_040_controlled | 522.782483 | 520.443237 | -2.339246 |
| angle_070_controlled | 521.612035 | 519.358508 | -2.253527 |
| angle_090_controlled_retake | 523.364755 | 521.608281 | -1.756475 |

Range among orientation-group medians:

- PCA baseline: **1.752720 px**
- Geometry estimator: **2.249772 px**

Using the preliminary scale of approximately 523.066855 px/in, the geometry orientation-group median range corresponds to approximately **0.00430 in**.

The geometry-minus-baseline offset remained relatively stable from 0° through 70° and diverged most strongly in the 90° group. The controlled-orientation result is therefore treated as a known orientation-sensitivity characteristic to be evaluated during formal validation rather than tuned away using the development dataset.

## 6. Diagnostic Residual Flags

All 27 development captures produced a sidewall residual diagnostic flag:

- `minimum_sidewall_high_residual`: **24**
- `maximum_sidewall_high_residual`: **3**

The residual flag threshold in the estimator is:

- Sidewall RMS > **1.5 px**

These flags are retained as diagnostic warnings and are not treated as automatic measurement failures.

This interpretation is supported by the static trial, where minimum-sidewall RMS values were approximately 3.2 px while OAL repeatability remained strong at 0.025910 px standard deviation.

## 7. Comparison With Alternative Estimators

### PCA/extreme-mask baseline

Advantages:

- Simple implementation
- No failures on the development masks
- Lower orientation-group median range than the geometry estimator in the controlled-orientation development trial

Limitations:

- Static standard deviation approximately twice that of the geometry estimator
- Relies on extreme mask pixels, making endpoint estimation more sensitive to local mask irregularities

### Subpixel Version 1

Disposition:

- Exploratory only
- All completed results were quality-flagged
- Not selected for primary OAL measurement

### Subpixel Version 2

Disposition:

- Exploratory only
- 7 failures among 27 accepted image/mask pairs
- Strong sidewall asymmetry in mask anchoring and grayscale contrast
- Not selected for primary OAL measurement

The Version 2 closeout is documented separately in:

`docs/research/2026-08-07_subpixel_v2_diagnostic_review_and_disposition.md`

## 8. Selection Rationale

The geometry estimator is selected because it provides the best balance of:

- strong static repeatability,
- zero execution failures across the development dataset,
- physically interpretable fitted end faces,
- simpler behavior than the grayscale subpixel refinements,
- compatibility with the existing accepted-mask workflow,
- and readiness for calibration and validation.

The geometry estimator is not being selected because it is assumed to be orientation invariant. Controlled-orientation testing identified measurable orientation sensitivity. That behavior is explicitly retained as a known limitation for formal validation.

## 9. Freeze Decision

**The geometry estimator is frozen as the primary OAL estimator for the thesis validation phase.**

The frozen implementation is identified by:

- File: `src/measurement/topdown_oal_geometry.py`
- Originating estimator commit: `8bb3a9f`
- SHA-256:

`d80aa30e1f7702833b03444af3cb80c6f3b87d1019704026a6750bc3aee44b3b`

No algorithmic parameter tuning, geometry-model changes, residual-threshold tuning, or endpoint-estimation changes should be made during formal validation without change control.

## 10. Change-Control Rule

If the frozen estimator is modified after validation data collection begins:

1. Record the reason for the change.
2. Record the exact code diff and new Git commit.
3. Generate a new SHA-256 for the estimator source.
4. Re-run the automated test suite.
5. Re-run the development comparison dataset.
6. Determine whether previously collected calibration and validation results remain comparable.
7. If measurement behavior changes materially, repeat affected validation measurements.

Changes to reporting, plotting, file organization, or non-measurement user-interface code do not automatically invalidate validation, provided the frozen measurement function and its inputs remain unchanged.

## 11. Next Research Phase

With estimator development frozen, the OAL work proceeds to:

1. Confirm the calibration method and pixel-to-inch scale.
2. Establish calibration traceability and session checks.
3. Complete manual reference measurements using the defined caliper procedure.
4. Execute the randomized OAL validation sample plan.
5. Measure the same specimens with the frozen computer-vision estimator.
6. Compare computer-vision measurements against manual reference measurements.
7. Quantify bias, agreement, repeatability, reproducibility, and orientation effects.
8. Determine whether the system meets the thesis OAL measurement objective.

## 12. Research Interpretation

The estimator-development phase demonstrated that increasing algorithmic sophistication did not automatically improve the measurement system. The geometry estimator improved static repeatability substantially relative to the PCA/extreme-mask baseline, while grayscale subpixel refinement introduced optical and anchoring sensitivity that was not justified for the current thesis scope.

The selected geometry method therefore represents an evidence-based engineering tradeoff between precision, robustness, interpretability, and validation readiness.
