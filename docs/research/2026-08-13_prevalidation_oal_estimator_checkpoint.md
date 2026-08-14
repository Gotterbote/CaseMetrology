# Prevalidation OAL Estimator Checkpoint

**Project:** CaseMetrology
**Date:** 2026-08-13
**Research phase:** Prevalidation estimator review
**Starting repository commit:** `6148472`
**Formal validation status:** Not started

## 1. Purpose

A limited five-specimen prevalidation checkpoint was performed before formal
OAL validation to determine whether the frozen geometry estimator produced
physically reasonable calibrated measurements on newly acquired cartridge
cases.

This checkpoint was exploratory/prevalidation work and is not part of the
formal 60-specimen validation dataset.

No estimator or calibration parameter was tuned during data collection.

## 2. Specimens

The following permanently laser-etched case IDs were used:

- 187
- 121
- 178
- 146
- 197

Because these specimens were used to evaluate estimator suitability, they are
classified as development/prevalidation specimens and shall not be eligible
for selection into the formal 60-case validation sample.

They may still be included in population screening for characterization of the
available 235-case population.

## 3. Acquisition controls

All case images and the associated blank image were acquired on 2026-08-13
using the locked CaseMetrology camera configuration.

Repository state during acquisition:

`61484722f434e8baaf8a64084e0a4cb48f523a97`

The Git working tree was clean during acquisition.

The research preflight passed before image acquisition.

## 4. Estimators compared

Two previously implemented OAL estimators were compared without modification:

1. Frozen geometry estimator:
   `src/measurement/topdown_oal_geometry.py`

2. PCA/extreme-mask estimator:
   `src/measurement/topdown_oal.py`

Both estimators used the same accepted segmentation masks.

The frozen spatial/directional calibration equations were applied to each
estimator using that estimator's own measured orientation.

## 5. Manual comparison

After CV acquisition and estimator processing, each specimen received three
independent manual digital-caliper OAL measurements with complete removal and
repositioning between measurements.

The manual instrument was Mitutoyo caliper serial `B23090910`.

An instrument-specific current calibration certificate was not available at
the time of this checkpoint.

Therefore, these manual values are used only as prevalidation comparison
measurements and shall not be represented as certified or traceable formal
ground truth.

## 6. Results

Saved comparison data:

`data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_comparison.csv`

Saved summary:

`data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_summary.txt`

SHA-256:

- comparison CSV:
  `9903c600df3194f658028a5b9fed48d465486f34e8e41c898d9a62b3bab1cafb`
- summary TXT:
  `1ce88f591ba627bf3d95e2b2cea4f406de619e1855dfab34c352968a7339cd8a`

Five-case summary:

### Geometry estimator

- Mean bias: `-0.0036041 in`
- MAE: `0.0036041 in`
- RMSE: `0.0040385 in`
- Maximum absolute error: `0.0060271 in`
- Closer to manual comparison than PCA: `1/5`

The geometry result was below the manual comparison mean for all five cases.

### PCA/extreme estimator

- Mean bias: `+0.0002724 in`
- MAE: `0.0015365 in`
- RMSE: `0.0017680 in`
- Maximum absolute error: `0.0030635 in`
- Closer to manual comparison than geometry: `4/5`

### Estimator separation

Mean PCA-minus-geometry measured length:

`2.029675 px`

The observed estimator separation is consistent with earlier development
records showing that the geometry estimator returns systematically shorter
lengths than the PCA/extreme-mask estimator.

## 7. Research interpretation

The checkpoint does not establish formal measurement accuracy because the
manual comparison instrument had not yet received an instrument-specific
current calibration certificate.

However, the systematic negative discrepancy of the geometry estimator is
large enough that proceeding directly into formal validation with the
geometry estimator frozen as the primary method is not justified.

The purpose of prevalidation work is specifically to identify such
methodological problems before formal validation data are collected.

## 8. Disposition

**HOLD — FORMAL OAL VALIDATION**

The 2026-08-07 geometry-estimator freeze is reopened for estimator review.

No formal 60-case OAL validation measurements shall be collected until the
primary estimator decision is resolved and documented.

The five prevalidation cases shall not be used to tune a correction factor or
bias offset.

In particular, the approximately 2-pixel geometry/PCA difference shall not be
converted into an additive correction.

The next estimator decision shall compare the previously established
repeatability/robustness evidence with the new physical-case prevalidation
comparison evidence.

If the primary estimator changes, that decision shall be documented and frozen
before formal validation begins.

## 9. Development-validation separation

The five specimens used in this checkpoint are:

`187, 121, 178, 146, 197`

These IDs are permanently designated as prevalidation/development specimens
for estimator-selection purposes and are excluded from the formal validation
sample-selection pool.

No formal validation result existed when this checkpoint and disposition were
established.
