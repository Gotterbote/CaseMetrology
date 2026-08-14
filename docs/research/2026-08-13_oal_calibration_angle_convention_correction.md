# OAL Calibration Angle-Convention Correction

**Project:** CaseMetrology
**Date:** 2026-08-13
**Research phase:** Prevalidation calibration-to-estimator integration review
**Formal validation status:** Not started

## 1. Purpose

A read-only audit of the formal OAL calibration implementation and records
identified an angle-convention mismatch between the gauge-block calibration
analyzer and the cartridge-case PCA OAL estimator.

The issue was identified before formal validation began.

This correction does not modify the underlying accepted A-D calibration data,
the fitted spatial calibration planes, the segmentation algorithm, or the
frozen PCA/extreme-mask pixel-length estimator.

## 2. Source of the Convention Difference

The orientation-independent gauge-block analyzer computes the rectangular
reference's long axis and its perpendicular short axis.

The certified dimensional span is measured along the short axis.

However, the analyzer field `orientation_degrees` reports the angle of the
gauge block's long axis.

Therefore, calibration conditions historically labeled by gauge-block
long-axis orientation correspond to dimensional measurement directions rotated
90 degrees from those labels.

In practical terms:

- gauge-block long axis near 0 degrees -> certified short dimension measured
  approximately vertically;
- gauge-block long axis near 90 degrees -> certified short dimension measured
  approximately horizontally.

The cartridge-case PCA estimator reports the direction of the OAL measurement
itself, not an axis perpendicular to the measured dimension.

## 3. Frozen Spatial Calibration Planes

The previously fitted calibration planes remain unchanged:

`PPI_0(x,y) = 516.907045 + 0.00843326411*x + 0.000817091863*y`

`PPI_90(x,y) = 518.408825 + 0.00322556849*x + 0.00442714650*y`

The labels `PPI_0` and `PPI_90` are retained for historical traceability to the
gauge-block acquisition conditions.

They shall not be re-fit using prevalidation or holdout data.

## 4. Correct Mapping for Cartridge-Case OAL

For a cartridge-case OAL direction `theta`, where `theta` is the PCA
pixel-length estimator's measured OAL angle, the effective image scale shall
be resolved as:

`effective_ppi = sqrt((PPI_90*cos(theta))^2 + (PPI_0*sin(theta))^2)`

This gives the expected principal-direction limits:

- horizontal cartridge-case OAL (`theta = 0 deg`) -> `PPI_90`
- vertical cartridge-case OAL (`theta = 90 deg`) -> `PPI_0`

The previously used exploratory mapping:

`effective_ppi = sqrt((PPI_0*cos(theta))^2 + (PPI_90*sin(theta))^2)`

is superseded for cartridge-case OAL physical-unit conversion.

## 5. Spatial Coordinate Convention

The calibration planes were fit and evaluated using measured component
centroids.

The OAL segmentation implementation likewise reports the centroid of the
largest segmented case component as:

`centroid_xy = (mean foreground x, mean foreground y)`

Therefore, the segmented case-component centroid shall provide `(x,y)` to the
spatial calibration planes.

No alternate spatial coordinate is introduced by this correction.

## 6. Corrected Five-Case Prevalidation Results

The five prevalidation specimens were re-evaluated without changing
segmentation, PCA pixel length, geometry pixel length, calibration
coefficients, or manual measurements.

Only the calibration angle-to-principal-direction mapping was corrected.

Specimens:

`187, 121, 178, 146, 197`

### Geometry estimator

- Mean bias: `-0.0030850 in`
- MAE: `0.0030850 in`
- RMSE: `0.0035832 in`
- Maximum absolute error: `0.0060090 in`
- Closer than PCA: `1/5`

### PCA/extreme-mask estimator

- Mean bias: `+0.0007934 in`
- MAE: `0.0015322 in`
- RMSE: `0.0018564 in`
- Maximum absolute error: `0.0035146 in`
- Closer than geometry: `4/5`

The estimator-selection conclusion is unchanged.

PCA/extreme-mask remains the selected primary OAL pixel-length estimator.

The five specimens remain prevalidation/development specimens and remain
excluded from the formal 60-case validation sample.

## 7. Corrected Oblique Holdout Interpretation

The original formal calibration record reported the independent oblique
holdout using:

- mean centroid: `(805.737, 642.145) px`
- reported gauge-block long-axis angle: `11.361394 deg`
- observed PPI: `523.649096602`

Using the cartridge-case-style direct-angle mapping produced an expected PPI
of approximately:

`524.212139811`

That interpretation did not account for the fact that the gauge-block analyzer
measures the certified dimension perpendicular to the reported long axis.

Using the corrected dimensional-direction mapping produces:

- corrected expected PPI: `523.865254503`
- observed PPI: `523.649096602`
- observed-minus-expected residual: `-0.216157901 PPI`
- equivalent dimensional residual: approximately `-0.000412622 in`

Thus, the corrected angle convention improves rather than degrades the
independent oblique-holdout interpretation.

The underlying holdout measurement is unchanged.

## 8. Historical Evidence Preservation

The following earlier records are retained unchanged as historical evidence:

- `docs/research/2026-08-07_formal_oal_calibration_analysis_and_disposition.md`
- `data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_comparison.csv`
- `data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_summary.txt`
- `docs/research/2026-08-13_prevalidation_oal_estimator_checkpoint.md`
- `docs/research/2026-08-13_oal_pca_estimator_selection_and_freeze.md`

Their original calculations document the state of knowledge before the
angle-convention audit.

They shall not be silently rewritten.

Where derived physical-unit values conflict with this correction, this document
supersedes the earlier angle-to-calibration mapping.

## 9. Estimator Freeze Status

The PCA/extreme-mask pixel-length estimator selected and frozen on 2026-08-13
remains frozen.

No PCA endpoint, segmentation, threshold, morphology, component-selection,
orientation, or pixel-length behavior is changed by this correction.

This correction applies only to the conversion of the selected PCA result from
pixels to physical units.

## 10. Implementation Requirement

The formal raw-image OAL measurement path shall implement:

1. frozen case segmentation;
2. segmented component centroid `(x,y)`;
3. frozen PCA/extreme-mask pixel-length estimator;
4. PCA OAL angle `theta`;
5. evaluation of the unchanged `PPI_0(x,y)` and `PPI_90(x,y)` planes;
6. corrected effective-PPI mapping:

   `sqrt((PPI_90*cos(theta))^2 + (PPI_0*sin(theta))^2)`

7. physical OAL:

   `OAL_in = PCA_length_px / effective_ppi`

The implementation shall be tested prospectively before formal validation
begins.

## 11. Disposition

**CALIBRATION ANGLE-CONVENTION ISSUE: IDENTIFIED AND CORRECTED**

**A-D CALIBRATION DATA: UNCHANGED**

**SPATIAL CALIBRATION COEFFICIENTS: UNCHANGED**

**PCA PIXEL-LENGTH ESTIMATOR: UNCHANGED AND REMAINS FROZEN**

**PCA ESTIMATOR SELECTION: UNCHANGED**

**FORMAL VALIDATION: REMAINS ON HOLD**

The next activity is implementation and testing of the corrected
calibration-to-PCA physical-unit measurement path before formal validation.
