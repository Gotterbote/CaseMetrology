# Formal OAL Validation Protocol Amendment

**Project:** CaseMetrology  
**Date:** 2026-08-15  
**Research phase:** Pre-formal-validation protocol control  
**Measurement characteristic:** Cartridge-case overall length (OAL)  
**Formal validation status:** Not started  
**Amends:** `docs/research/2026-08-09_formal_oal_validation_screening_protocol.md`

## 1. Purpose

This document prospectively amends the formal OAL validation screening protocol
dated 2026-08-09.

The original protocol is retained unchanged as historical prospective evidence.

Since that protocol was written, additional prevalidation work prospectively
resolved the primary OAL estimator, corrected the calibration angle convention,
integrated the selected estimator with the frozen spatial calibration model,
and verified the resulting production measurement path.

No formal 60-case validation measurements have been collected.

Where this amendment conflicts with the 2026-08-09 protocol, this amendment
controls subsequent formal-validation activity.

## 2. Calibration characterization versus final measurement-system identity

The 2026-08-09 screening protocol identified commit `300c696` as the
calibration freeze commit.

That commit remains the accepted formal calibration-characterization record.
It is not retrospectively altered or replaced.

Subsequent prospective prevalidation work established the final OAL
measurement path as follows:

- `300c696` — document formal OAL calibration characterization;
- `8db408f` — select and freeze the PCA/extreme-mask OAL estimator;
- `8fffefe` — correct the calibration angle convention;
- `5e904cf` — integrate PCA OAL with the frozen spatial/directional calibration;
- `cc10723` — document production-pipeline integration verification.

The final measurement path used for formal validation is therefore not defined
by `300c696` alone.

## 3. Frozen primary OAL measurement path

The primary formal-validation measurement chain is:

1. frozen blank-reference segmentation;
2. segmented largest-component centroid `(x,y)`;
3. frozen PCA/extreme-mask OAL pixel-length estimator;
4. PCA OAL measurement direction;
5. frozen spatial calibration planes;
6. corrected directional calibration mapping;
7. effective pixels-per-inch calculation;
8. calibrated OAL in inches.

The selected primary pixel-length estimator is implemented in:

`src/measurement/topdown_oal.py`

The frozen segmentation implementation is:

`src/image_processing/oal_segmentation.py`

The spatial/directional calibration implementation is:

`src/calibration/oal_spatial_calibration.py`

The integrated calibrated raw-image measurement path is:

`src/measurement/topdown_oal_pipeline.py`

No estimator, segmentation, threshold, morphology, endpoint, calibration,
or physical-unit conversion parameter shall be tuned using formal validation
results.

## 4. Development-specimen exclusion

The following laser-etched specimen IDs were used during estimator-selection
prevalidation:

`187, 121, 178, 146, 197`

These specimens remain eligible for inclusion in population screening and
population-distribution characterization.

They are permanently ineligible for selection into the formal 60-case
validation sample.

They shall not be used to derive any formal validation acceptance threshold,
bias correction, regression correction, endpoint correction, calibration
adjustment, or estimator parameter.

## 5. Terminology

Subsequent research records and thesis text shall use the terms:

- `manual reference measurement`;
- `manual reference method`; or
- `reference measurement system`

rather than treating the manual caliper result as error-free `ground truth`.

The manual reference method has finite resolution, repeatability, calibration
status, and measurement uncertainty that must be considered when interpreting
agreement with the computer-vision system.

Historical records containing the phrase `ground truth` are retained unchanged
as part of the research chronology.

## 6. Screening authorization remains unchanged

Population screening remains authorized under the 2026-08-09 protocol.

Screening measurements are used only for:

- characterization of the 235-case population;
- determination of dimensional coverage;
- definition of final sampling strata;
- stratified random selection of the formal validation sample.

Screening measurements are not formal manual reference measurements.

No screening value shall be included in the formal manual reference mean.

## 7. Formal manual reference measurements

The existing protocol requirement remains in force:

- each selected formal-validation specimen shall receive at least three
  independent manual reference readings;
- the specimen shall be completely removed and repositioned between readings;
- the formal reference mean shall be calculated only from those formal
  reference readings.

Formal manual reference measurements remain unauthorized until the designated
reference caliper calibration documentation has been received, reviewed, and
accepted for the study.

## 8. Remaining prerequisites before formal validation

The following items must be prospectively resolved and documented before
official formal-validation measurements begin:

1. review and disposition of the manual reference caliper calibration
   certificate;
2. completion and audit of the 235-case screening population;
3. final validation-stratum boundaries;
4. sample allocation among strata and reproducible random selection of the
   60-case formal validation sample;
5. treatment of intentionally short and intentionally long specimens within
   the sampling framework;
6. formal computer-vision replicate count;
7. specimen removal/repositioning procedure for computer-vision replicates;
8. formal measurement-order and randomization procedure;
9. screening-session and formal-session reference-check acceptance criteria;
10. environmental and temperature-monitoring procedure;
11. predefined measurement-failure, review, exclusion, and protocol-deviation
    rules;
12. final statistical analysis plan and engineering acceptance criteria;
13. complete formal-validation stop/go review.

## 9. Development-validation separation

The following activities remain prohibited once formal validation begins
unless a prospectively documented system change and appropriate revalidation
are performed:

- estimator tuning;
- segmentation tuning;
- threshold adjustment;
- morphology adjustment;
- endpoint correction;
- calibration refitting using case-validation data;
- additive or multiplicative bias correction derived from validation results;
- exclusion of specimens because their computer-vision results are
  unfavorable;
- post-hoc alteration of sampling strata based on computer-vision performance.

Formal validation data are intended to evaluate the frozen measurement system,
not to continue development of that system.

## 10. Historical evidence preservation

Earlier prevalidation records shall not be silently rewritten to reflect later
knowledge.

Where a later prospective correction or amendment supersedes an earlier
interpretation, both records shall be retained and their chronological
relationship documented.

This includes the calibration angle-convention correction and the later
PCA/extreme-mask estimator selection.

## 11. Current disposition

**2026-08-09 SCREENING PROTOCOL: RETAINED AND AMENDED**

**PCA/EXTREME-MASK ESTIMATOR: FROZEN**

**SEGMENTATION IMPLEMENTATION: FROZEN**

**SPATIAL/DIRECTIONAL CALIBRATION: FROZEN**

**CALIBRATED PRODUCTION PIPELINE: PREVALIDATION INTEGRATION VERIFIED**

**PREVALIDATION CASES 187, 121, 178, 146, 197: EXCLUDED FROM FORMAL SAMPLE**

**POPULATION SCREENING: AUTHORIZED**

**FORMAL MANUAL REFERENCE MEASUREMENT: HOLD**

**FORMAL COMPUTER-VISION VALIDATION: HOLD**

Formal validation may begin only after the remaining prerequisites and the
formal stop/go gate have been prospectively closed.
