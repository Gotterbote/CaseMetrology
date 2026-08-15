# Formal OAL Computer-Vision Replicate and Failure Protocol

**Project:** CaseMetrology
**Date:** 2026-08-15
**Research phase:** Pre-formal-validation protocol control
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Formal validation status:** Not started

## 1. Purpose

This document prospectively defines the computer-vision replicate,
repositioning, failure, and retry rules for the formal OAL validation study.

These rules are established before formal validation measurements are
collected and shall not be changed in response to observed validation results.

## 2. Formal computer-vision replicate count

Each of the 60 formal-validation specimens shall receive exactly three planned
computer-vision acquisition attempts.

The planned formal study therefore contains:

`60 specimens x 3 CV attempts = 180 planned CV acquisition attempts`

Each acquisition attempt is an independent physical presentation of the
specimen.

## 3. Repositioning requirement

Before every formal CV acquisition attempt:

1. the specimen shall be completely removed from the measurement fixture;
2. the specimen shall then be repositioned according to the established
   measurement procedure; and
3. a new source image shall be acquired.

Repeated processing of a previously acquired image does not constitute an
independent formal replicate.

## 4. Measurement identity

Each formal CV acquisition attempt shall receive its own unique
`measurement_id`.

The research `part_id` identifies the specimen.

`measurement_id` identifies the individual measurement attempt.

Multiple measurements of the same specimen shall therefore remain separate
records.

## 5. Measurement-system failure

A planned acquisition that completes normally but fails within the frozen
measurement pipeline is a formal measurement-system outcome.

Examples include:

- segmentation failure;
- PCA estimator failure;
- failure of a required measurement-quality condition.

Such an attempt:

- remains part of the formal study record;
- contributes to measurement-success/failure statistics;
- shall not be deleted;
- shall not be silently replaced by another acquisition; and
- shall not be converted manually into a dimensional value.

## 6. Protocol-invalid observation

An observation may be declared protocol-invalid only when a documented event
prevents the intended measurement procedure from having been performed.

Examples may include:

- incorrect specimen identification discovered before or during acquisition;
- operator abort before completion of the intended acquisition;
- camera disconnection or verified hardware malfunction;
- corrupted or missing source-image file;
- verified acquisition outside the frozen camera configuration;
- documented fixture disturbance requiring measurement-system review.

A protocol-invalid observation is distinct from a measurement-system failure.

The original record and reason for invalidation shall be retained.

A replacement acquisition may be performed only for a documented
protocol-invalid observation.

## 7. No performance-based retries

Additional acquisitions shall not be performed because:

- the reported OAL appears unfavorable;
- the result differs substantially from the manual reference;
- the result is statistically unusual;
- the result is near a specification limit; or
- the operator believes another acquisition would produce a better result.

A validly executed measurement-system failure shall not be retried merely to
obtain a successful dimensional result.

## 8. Measurement success rate

The primary CV attempt-level measurement success rate shall be calculated as:

`valid CV measurements / validly executed formal CV measurement attempts`

The study is designed to obtain 180 validly executed formal CV measurement
attempts: three for each of 60 specimens.

A protocol-invalid acquisition does not count as one of those 180 measurement
attempts because the intended measurement procedure was not completed. The
invalid record shall nevertheless be retained in the audit trail. Its
authorized replacement becomes the corresponding formal measurement attempt.

A measurement-system failure occurring during a validly executed formal
attempt does count in the denominator and shall not be replaced.

Failure reasons shall be summarized separately.

## 9. Specimen-level formal CV result

For the primary specimen-level agreement analysis, a formal CV specimen mean
shall require three valid independent CV measurements.

For a specimen with three valid measurements:

`CV_mean_i = (CV_i1 + CV_i2 + CV_i3) / 3`

If fewer than three valid CV measurements are produced from the three planned
validly executed attempts, the specimen shall remain in the formal study as a
measurement-system failure outcome but shall not receive a three-replicate
primary CV mean.

No additional performance-based acquisition shall be collected to force the
specimen to achieve three valid measurements.

## 10. Relationship to manual reference measurements

The formal manual reference procedure separately requires three independent
manual readings with complete specimen removal and repositioning between
readings.

The specimen-level manual reference mean and specimen-level CV mean therefore
represent separate independently replicated measurement procedures.

## 11. Development-validation separation

Formal CV replicate data shall not be used to:

- modify the frozen segmentation algorithm;
- modify the PCA/extreme-mask estimator;
- change calibration coefficients or equations;
- introduce a post-hoc correction;
- change retry rules;
- change the required replicate count; or
- exclude a specimen because of unfavorable measurement performance.

## 12. Disposition

**FORMAL CV REPLICATES PER SPECIMEN: 3**

**COMPLETE REMOVAL AND REPOSITIONING BETWEEN REPLICATES: REQUIRED**

**NEW SOURCE IMAGE FOR EVERY REPLICATE: REQUIRED**

**MEASUREMENT-SYSTEM FAILURE: RETAINED AND NOT REPLACED**

**PROTOCOL-INVALID OBSERVATION: DOCUMENTED REPLACEMENT PERMITTED**

**PERFORMANCE-BASED RETRY: PROHIBITED**

**PRIMARY SPECIMEN-LEVEL CV MEAN: REQUIRES 3/3 VALID CV MEASUREMENTS**

**FORMAL VALIDATION: REMAINS ON HOLD**
