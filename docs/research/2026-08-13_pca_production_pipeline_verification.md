# PCA Production Pipeline Verification

**Project:** CaseMetrology
**Date:** 2026-08-13
**Research phase:** Prevalidation measurement-system integration
**Repository commit:** `5e904cf3b7e27bd15c94eddca110807a59efd7ae`
**Formal validation status:** Not started

## 1. Purpose

The newly integrated PCA OAL physical-unit production pipeline was verified
using the five previously acquired prevalidation specimens.

No new specimen images or manual measurements were collected for this
verification.

The objective was to confirm that the committed production path reproduces
the independently calculated corrected calibration-to-PCA results established
before implementation.

## 2. Production Measurement Chain

The verified production path is:

1. frozen blank-reference case segmentation;
2. segmented component centroid `(x,y)`;
3. frozen PCA/extreme-mask OAL pixel-length estimator;
4. PCA OAL measurement angle;
5. unchanged A-D spatial calibration planes;
6. corrected calibration angle mapping;
7. effective pixels-per-inch calculation;
8. calibrated OAL in inches.

## 3. Verification Specimens

The following prevalidation/development specimens were used:

`187, 121, 178, 146, 197`

These specimens remain excluded from the formal 60-case validation sample.

## 4. Verification Result

All five saved images passed through the committed production pipeline.

Production results matched the independently calculated corrected
prevalidation results within a tolerance of `0.0000001 in`.

Cases passing:

`5/5`

Maximum absolute numerical difference:

`0.000000041 in`

Overall result:

`PASS`

Detailed data:

`data/oal_validation/prevalidation/2026-08-13_pca_pipeline_verification/five_case_production_pipeline_verification.csv`

Summary:

`data/oal_validation/prevalidation/2026-08-13_pca_pipeline_verification/five_case_production_pipeline_verification_summary.txt`

## 5. Automated Regression Testing

Immediately before commit `5e904cf`, the pipeline-specific test suite passed:

`11 passed`

The complete repository test suite passed:

`67 passed`

Repository pre-commit checks also passed:

- Ruff lint check
- Black formatting check
- Python syntax check

## 6. Frozen Implementation Identity

PCA/extreme-mask estimator:

`src/measurement/topdown_oal.py`

SHA-256:

`d00e7b872f45505658ffef6cb2d75cdae4d443940e7ef121c431f1df843805b3`

Segmentation:

`src/image_processing/oal_segmentation.py`

SHA-256:

`41a9578a44cecdcb036f53ac253d7d00fc6fd4b214866a1f9f5eea39f30c3f37`

Spatial/directional calibration integration:

`src/calibration/oal_spatial_calibration.py`

SHA-256:

`677376b0d89434e5e1c627f32a65365d02981260ab08d3e1b00d6b16c475ec4b`

Production raw-image pipeline:

`src/measurement/topdown_oal_pipeline.py`

SHA-256:

`06aa9effde9b1945c2c20c83de807a801cbd1a4d7547dcdadf8a9dc5f1e034a4`

## 7. Interpretation

The production pipeline reproduces the independently derived corrected
calibration-to-PCA calculations on all five prevalidation cases.

The verification demonstrates implementation consistency and regression
integrity.

It is not formal measurement-system validation and does not convert the five
development specimens into formal validation data.

## 8. Disposition

**PCA PRODUCTION PIPELINE INTEGRATION VERIFICATION: PASS**

**REAL-IMAGE REPRODUCTION: 5/5 PASS**

**FULL AUTOMATED TEST SUITE: 67/67 PASS**

**FROZEN PCA ESTIMATOR: UNCHANGED**

**FROZEN SEGMENTATION: UNCHANGED**

**FORMAL VALIDATION: REMAINS ON HOLD**

Estimator development and calibration-to-PCA integration are considered
closed unless new evidence requires a prospectively documented change.

The remaining work before formal validation concerns the formal reference
method, measurement-region controls, and final validation stop/go criteria.
