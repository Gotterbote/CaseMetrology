# OAL PCA Estimator Selection and Freeze

**Project:** CaseMetrology
**Date:** 2026-08-13
**Research phase:** Prevalidation method selection
**Repository state at decision:** `25ef3e14dcbfc5984af13bbf5c92a263d50814d6`
**Short commit:** `25ef3e1`
**Formal validation status:** Not started

## 1. Decision

The PCA/extreme-mask OAL estimator implemented in:

`src/measurement/topdown_oal.py`

is selected as the primary pixel-length estimator for the forthcoming formal
OAL validation study.

The geometry estimator implemented in:

`src/measurement/topdown_oal_geometry.py`

is discontinued as the primary measurement estimator.

The geometry implementation is retained for diagnostic, historical, and
development-reproducibility purposes.

This decision selects the estimator to be tested during formal validation.
It does not claim that PCA/extreme-mask has already been validated.

## 2. Scope of Freeze

This record freezes:

- the identity of the primary OAL pixel-length estimator;
- the PCA/extreme-mask implementation state;
- the segmentation implementation state used by that estimator;
- the prohibition against tuning the selected estimator using the five
  prevalidation specimens.

This record does not yet declare the complete physical-unit measurement system
ready for formal validation.

Formal validation remains on hold until the remaining reference-method and
calibration-integration prerequisites are reviewed and prospectively closed.

## 3. Evidence Sequence

The estimator decision was made only after the following prevalidation
evidence had been generated and preserved.

### 3.1 Five-case estimator checkpoint

Document:

`docs/research/2026-08-13_prevalidation_oal_estimator_checkpoint.md`

Comparison data:

`data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_comparison.csv`

Summary:

`data/oal_validation/prevalidation/2026-08-13_estimator_checkpoint/five_case_estimator_summary.txt`

Specimens:

`187, 121, 178, 146, 197`

Five-case results:

#### Geometry

- mean bias relative to manual comparison: `-0.0036041 in`
- MAE: `0.0036041 in`
- RMSE: `0.0040385 in`
- maximum absolute error: `0.0060271 in`
- closer than PCA: `1/5`
- signed discrepancy negative for all five specimens

#### PCA/extreme-mask

- mean bias relative to manual comparison: `+0.0002724 in`
- MAE: `0.0015365 in`
- RMSE: `0.0017680 in`
- maximum absolute error: `0.0030635 in`
- closer than geometry: `4/5`

Mean PCA-minus-geometry pixel-length difference:

`2.029675 px`

No estimator or calibration parameter was tuned during the checkpoint.

### 3.2 Same-session measurement-assurance postcheck

Document:

`docs/research/2026-08-13_prevalidation_measurement_assurance_postcheck.md`

After the five-case checkpoint, the 1-inch dimensional reference was measured
five times using Mitutoyo caliper serial `B23090910`.

Displayed readings:

`1.0000, 1.0000, 1.0000, 1.0000, 1.0000 in`

Mean:

`1.0000000 in`

Displayed range:

`0.0000000 in`

The absence of an instrument-specific current calibration certificate remains
a limitation. These readings are measurement-assurance evidence rather than
formal certified ground truth.

A same-session optical reference check was also performed.

The first optical attempt was invalid for interpretation because the gauge
block was presented with the 1.375-inch dimension vertical while the analyzer
assumes the certified 1.0000024-inch dimension is vertical.

That invalid attempt was retained in the evidence trail.

After correcting the block orientation without changing the camera or
calibration implementation, the gauge-block diagnostic produced:

- fitted center span: `523.147633 px`
- preliminary scale: `523.146377 px/in`
- analyzer status: `PRELIMINARY SUBPIXEL DIAGNOSTIC`

The postcheck provided no evidence of a gross same-session manual-reference or
optical-scale failure sufficient to explain the geometry estimator's observed
systematic negative discrepancy.

The gauge-block postcheck is not an independent validation because the gauge
block participates in the calibration lineage.

## 4. Selection Rationale

The primary goal of estimator selection is to choose, before formal validation,
the measurement algorithm that has the strongest combined evidence for
repeatability, orientation behavior, measurement availability, and physically
reasonable dimensional performance.

Earlier development work demonstrated that the geometry estimator could
provide strong static repeatability.

However, repeatability alone is not sufficient if the estimator produces a
systematic dimensional discrepancy on physical specimens.

The five-case prevalidation checkpoint showed that the geometry estimator was
below the manual comparison mean for every specimen and had substantially
larger aggregate error than PCA/extreme-mask.

The PCA/extreme-mask estimator was closer to the manual comparison on four of
five cases and exhibited substantially smaller mean bias and mean absolute
error.

The same-session manual and optical reference checks did not identify a gross
measurement-system problem that would reasonably account for the geometry
estimator's systematic negative discrepancy.

Therefore, PCA/extreme-mask is selected as the stronger estimator candidate
for formal validation.

## 5. No Post-Hoc Correction

The approximately `2.03 px` mean separation between PCA and geometry shall not
be converted into an additive correction.

No correction factor, regression correction, endpoint offset, threshold
adjustment, morphology change, calibration shift, or estimator parameter shall
be derived from the five prevalidation specimens for use in formal validation.

The five specimens were used for estimator selection only.

## 6. Development-Validation Separation

The following permanently laser-etched case IDs are designated
prevalidation/development specimens for estimator-selection purposes:

`187, 121, 178, 146, 197`

They shall not be eligible for selection into the formal 60-case validation
sample.

They may remain in the 235-case screening population for population
characterization.

## 7. Frozen Implementation Identity

### Selected primary estimator

Path:

`src/measurement/topdown_oal.py`

SHA-256:

`d00e7b872f45505658ffef6cb2d75cdae4d443940e7ef121c431f1df843805b3`

### Segmentation implementation

Path:

`src/image_processing/oal_segmentation.py`

SHA-256:

`41a9578a44cecdcb036f53ac253d7d00fc6fd4b214866a1f9f5eea39f30c3f37`

### Geometry estimator retained for historical/diagnostic comparison

Path:

`src/measurement/topdown_oal_geometry.py`

SHA-256:

`d80aa30e1f7702833b03444af3cb80c6f3b87d1019704026a6750bc3aee44b3b`

### Supporting evidence identities

Five-case comparison CSV SHA-256:

`9903c600df3194f658028a5b9fed48d465486f34e8e41c898d9a62b3bab1cafb`

Five-case summary SHA-256:

`1ce88f591ba627bf3d95e2b2cea4f406de619e1855dfab34c352968a7339cd8a`

Estimator checkpoint document SHA-256:

`4346385cd7120fe4aca8c5931ff032b158017dc5301089673509518ceed52f6d`

Measurement-assurance postcheck document SHA-256:

`2f1c650880adbb39c4d99c1c75ca578e5c5d05a8555e13c76b2a219c5c934c89`

Repository commit at estimator-selection decision:

`25ef3e14dcbfc5984af13bbf5c92a263d50814d6`

## 8. Change Control

After this freeze record is committed, any change affecting the following
requires prospective documentation before formal validation measurements are
collected:

- PCA/extreme-mask endpoint definition;
- segmentation algorithm;
- thresholding;
- morphology;
- largest-component selection;
- estimator orientation calculation;
- PCA/extreme measurement logic;
- estimator failure or acceptance logic;
- calibration equations used with the selected estimator;
- camera geometry;
- fixture configuration affecting measurement;
- primary estimator identity.

No such change shall be introduced silently.

If a required change is identified before formal validation begins, it shall be
documented as a prospective amendment and the affected implementation shall be
re-frozen before validation.

## 9. Formal Validation Boundary

No formal 60-case validation measurement has been collected as part of this
estimator-selection activity.

The next research task is not additional estimator-development specimen
collection.

Before formal validation begins, the project shall:

1. verify the exact calibration-to-PCA integration used to convert the frozen
   PCA pixel length into physical units;
2. resolve and document the formal manual reference-method status;
3. freeze the remaining formal validation measurement-system prerequisites;
4. confirm the formal validation protocol and stop/go criteria.

Only after those prerequisites are closed shall formal validation data
collection begin.

## 10. Disposition

**PRIMARY OAL PIXEL-LENGTH ESTIMATOR: PCA/EXTREME-MASK**

**ESTIMATOR SELECTION: FROZEN**

**GEOMETRY ESTIMATOR PRIMARY ROLE: DISCONTINUED**

**FIVE PREVALIDATION SPECIMENS: EXCLUDED FROM FORMAL VALIDATION SAMPLE**

**FORMAL OAL VALIDATION: HOLD PENDING REMAINING PREREQUISITES**
