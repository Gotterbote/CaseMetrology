# Mitutoyo Caliper Calibration Intake and Evidence Plan

**Project:** CaseMetrology  
**Instrument:** Mitutoyo Digimatic Caliper  
**Model:** CD-8"ASX  
**Code number:** 500-197-30  
**Serial number:** B23090910  
**Resolution:** 0.0005 inch / 0.01 mm  
**Planned calibration date:** 2026-08-03  
**Document date:** 2026-07-31  
**Status:** Prospective instrument-control record

## 1. Purpose

This document defines the information and evidence to obtain when the
Mitutoyo caliper is submitted for calibration. The calibration result will
determine whether the instrument may serve as the official physical
comparison reference for the current 1.000 ±0.010-inch OAL validation phase.

The caliper must not be described as currently calibrated until the returned
certificate has been reviewed and accepted.

## 2. Information to provide to the calibration laboratory

- Manufacturer: Mitutoyo
- Model: CD-8"ASX
- Code number: 500-197-30
- Serial number: B23090910
- Range: 0-8 inch / 0-200 mm
- Resolution: 0.0005 inch / 0.01 mm
- Intended use: comparison-reference measurement near 1.000 inch
- Study tolerance: 1.000 ±0.010 inch
- Requested emphasis: measurement error and uncertainty near 1.000 inch

## 3. Requested calibration evidence

Request a calibration certificate containing, when available:

- calibration-laboratory name and address;
- accreditation status and accreditation number;
- certificate number;
- calibration date;
- recommended due date;
- environmental conditions;
- traceability statement;
- reference standards used;
- as-found results;
- as-left results;
- any adjustment or repair performed;
- measurement points across the range;
- a measurement point near 1.000 inch;
- stated expanded uncertainty and coverage factor;
- pass/fail disposition;
- technician or authorized-signatory identification.

## 4. Intake checks before submission

Before handing over the instrument:

1. Verify that the serial number is B23090910.
2. Photograph the full instrument.
3. Photograph the serial/model markings.
4. Record visible damage, jaw condition, and battery/display condition.
5. Do not adjust, repair, or alter the caliper before calibration.
6. Ask the laboratory to preserve and report the as-found condition.
7. Confirm whether the laboratory will clean or adjust the instrument.
8. Obtain a service receipt or intake number.

## 5. Required questions for the laboratory

- Is the calibration traceable to national or international standards?
- Is the laboratory accredited for caliper calibration?
- Will the certificate include measurement uncertainty?
- Will as-found and as-left values both be reported?
- Will a point near 1.000 inch be included?
- Will any adjustment be performed without prior authorization?
- What calibration interval or due date is recommended?

## 6. Evidence handling after return

After the caliper returns:

1. Scan or photograph every certificate page clearly.
2. Preserve the original certificate.
3. Record the certificate number, calibration date, and due date.
4. Record as-found and as-left error near 1.000 inch.
5. Record stated uncertainty and coverage factor.
6. Record whether adjustment or repair occurred.
7. Calculate a SHA-256 hash for each digital certificate image or PDF.
8. Store the certificate under a dedicated instrument-calibration evidence
   directory.
9. Update `config/pca_oal_validation_plan.json`.
10. Update the OAL method decision log and evidence index.
11. Do not authorize official validation until the certificate has been
    reviewed.

## 7. Acceptance review for the current OAL phase

The certificate will be reviewed to determine whether the caliper is suitable
for the current 0.020-inch total tolerance.

The review will consider:

- as-found error near 1.000 inch;
- as-left error near 1.000 inch;
- stated measurement uncertainty;
- observed resolution;
- calibration-laboratory traceability;
- calibration interval;
- whether adjustment changed the instrument response.

The final suitability decision will be documented rather than inferred from
a generic pass label alone.

## 8. Effect of calibration outcome

### Pass with acceptable uncertainty

The caliper may be authorized as the physical comparison reference for the
current OAL validation phase.

### Pass but uncertainty is too large

The caliper may remain useful for development or screening, but a stronger
reference instrument will be required for official validation.

### As-found out of tolerance but adjusted and passed as-left

Measurements taken before adjustment will not be treated as validated
reference values. Official measurements may begin only after return and
verification.

### Fail or indeterminate result

Official validation remains on hold until another suitable reference
instrument is obtained.

## 9. Research status

No official validation measurements have been collected under a currently
reviewed calibration certificate at the time this plan is written.
