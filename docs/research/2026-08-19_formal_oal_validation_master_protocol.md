# CaseMetrology Formal OAL Validation Master Protocol and Stop/Go Checklist

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Primary researcher/operator:** Timmy D. Bell
**Planned validation sample:** 60 specimens
**Status:** Prospective master protocol; formal validation measurements have not begun

## 1. Purpose

This document serves as the controlling index and pre-measurement stop/go checklist for the CaseMetrology formal OAL validation study.

Formal validation shall not begin until all required pre-measurement items are complete and the study is declared `GO`.

## 2. Study Objective

Evaluate agreement and repeatability of the frozen CaseMetrology CV OAL measurement system relative to a calibrated manual reference method.

The formal study shall not be used to tune, recalibrate, optimize, or select the measurement system under test.

## 3. Study Scope

The current formal validation study is limited to:

**Cartridge-case overall length (OAL).**

Other case dimensions remain outside the current thesis validation scope.

## 4. Measurement System Under Test

Formal validation shall use the frozen CaseMetrology configuration including:

- camera;
- lens;
- camera-to-measurement-plane geometry;
- fixture;
- backlight;
- blank-image procedure;
- segmentation pipeline;
- PCA/extreme-mask OAL estimator;
- calibration planes;
- quality gates;
- software revision;
- acquisition workflow.

The formal configuration shall be identified by Git commit before data collection.

## 5. Reference Measurement System

Designated reference instrument:

- Mitutoyo CD-8"ASX
- Code 500-197-30
- Serial B23090910
- Resolution 0.0005 in

Each validation specimen shall receive three independent formal manual measurements.

Screening measurements shall not be part of the formal reference value.

## 6. Designated Operator

All formal validation work shall be performed by:

**Timmy D. Bell**

This includes manual measurements, check-standard observations, environmental observations, specimen identification, CV placement/acquisition, and protocol documentation.

The study is a single-operator validation study.

## 7. Validation Population and Sample

The available population consists of 235 uniquely laser-etched specimens.

The existing etched integer shall be used as `part_id`.

The final validation sample shall contain 60 specimens selected using the frozen stratified-random-sampling procedure.

## 8. Measurement Structure

### Manual reference

3 rounds × 60 specimens = 180 planned observations.

### Computer vision

3 rounds × 60 specimens = 180 planned system attempts.

Every observation requires complete removal and independent repositioning.

## 9. Measurement Order

Manual and CV order shall be generated independently.

Prospective seeds:

- manual: `2026081901`
- CV: `2026081902`

Run-order files shall be frozen before their respective phases begin.

## 10. Measurement Phase Order

1. Complete formal manual reference measurements.
2. Complete formal CV acquisition.
3. Audit the data.
4. Join datasets and run the frozen statistical analysis.

Manual-reference results shall not influence CV acquisition.

## 11. Manual Measurement Requirements

For each scheduled manual observation:

1. verify `part_id`;
2. measure once;
3. record display exactly;
4. completely remove specimen;
5. proceed to next randomized specimen.

No retake because a value appears unexpected.

## 12. Reference-Standard Session Checks

Each formal manual session requires:

- five independent pre-session check-standard measurements;
- five independent post-session measurements.

Final numerical limits remain pending certificate review.

Failed pre-check = `NO-GO`.

Failed post-check = `HOLD_FOR_REVIEW`.

## 13. Environmental Requirements

Use practical control:

- consistent indoor location;
- reasonable thermal equilibration;
- start/end room-temperature records;
- check-standard surface temperature for manual sessions;
- calibrated temperature-monitoring equipment;
- documentation of substantial abnormalities.

Continuous environmental logging is not required.

## 14. CV Acquisition Requirements

For each CV run position:

1. verify specimen;
2. independently place;
3. perform one acquisition attempt;
4. record outcome;
5. remove specimen;
6. continue.

Pipeline failure counts as a formal system attempt and is not automatically repeated.

## 15. Observation Classifications

Use:

- `VALID`
- `SYSTEM_FAILURE`
- `PROTOCOL_INVALID`
- `HOLD_FOR_REVIEW`

## 16. Replacement Rule

Only a `PROTOCOL_INVALID` observation may receive an authorized replacement.

A `SYSTEM_FAILURE` shall not receive an automatic replacement.

## 17. Raw Data Preservation

Formal raw evidence includes:

- manual readings;
- reference-standard readings;
- environmental observations;
- raw CV images;
- masks/diagnostics;
- run-order records;
- session records;
- failures;
- protocol deviations.

Raw observations shall not be silently deleted or overwritten.

## 18. Derived Data

Derived data include specimen means, SDs, ranges, bias, errors, RMSE, limits of agreement, classification metrics, repeatability statistics, figures, and tables.

Derived data shall be generated programmatically.

## 19. Primary Statistical Unit

The primary unit for agreement is the unique specimen.

Planned maximum:

\[
n=60
\]

Triplicate measurements shall not be treated as 180 independent specimens.

## 20. Primary Performance Targets

| Metric | Target |
|---|---:|
| CV measurement availability | ≥99% |
| 95th-percentile repositioning difference | ≤0.002 in |
| Absolute mean bias | ≤0.001 in |
| RMSE | ≤0.002 in |
| 95th-percentile absolute error | ≤0.003 in |
| Maximum absolute specimen error | ≤0.004 in |
| False passes | Zero preferred |

## 21. Validation Failure Is an Acceptable Research Result

Failure to satisfy one or more targets shall be reported and shall not trigger retrospective retuning, specimen removal, threshold changes, or relaxed criteria.

## 22. Required Repository Documentation

The formal validation documentation set includes:

1. `2026-08-19_formal_oal_measurement_order_randomization_protocol.md`
2. `2026-08-19_formal_oal_manual_reference_measurement_protocol.md`
3. `2026-08-19_formal_oal_reference_standard_session_acceptance_protocol.md`
4. `2026-08-19_formal_oal_environmental_temperature_protocol.md`
5. `2026-08-19_formal_oal_cv_acquisition_protocol.md`
6. `2026-08-19_formal_oal_validation_dataset_schema.md`
7. `2026-08-19_formal_oal_protocol_deviation_data_disposition_policy.md`
8. `2026-08-19_formal_oal_statistical_analysis_plan.md`
9. `2026-08-19_formal_oal_validation_master_protocol.md`

## 23. Required Supporting Scripts

Before formal collection/analysis, the repository should contain:

- validation sample-selection script;
- manual run-order generator;
- CV run-order generator;
- validation-data audit script;
- formal statistical-analysis script.

## 24. Required Formal Data Files

Maintain at minimum:

- frozen specimen-selection file;
- manual run-order file;
- CV run-order file;
- raw manual observations;
- manual-session records;
- raw reference-standard checks;
- environmental observations;
- raw CV observation manifest;
- protocol-deviation log;
- derived analysis outputs.

## 25. Certificate Review Requirements

Before formal validation:

### Caliper

- certificate matches B23090910;
- calibration status accepted;
- indication error reviewed;
- uncertainty reviewed;
- approximately 1-in performance reviewed;
- adjustment status documented.

### Check standard

- identity established;
- certified dimension confirmed;
- certificate status reviewed;
- uncertainty reviewed;
- reference temperature reviewed.

### Temperature instrument

- identity established;
- calibration certificate reviewed;
- uncertainty recorded;
- limitations documented.

## 26. Pending Certificate-Dependent Items

Before formal measurements, finalize:

- manual-session mean-error limit;
- manual-session range limit;
- pre/post drift limit;
- calibration-correction treatment;
- manual-reference uncertainty;
- treatment near specification limits;
- any required guard band.

## 27. Formal Pre-Measurement Stop/Go Checklist

### A. Reference Instrument

- [ ] Mitutoyo B23090910 returned from accredited calibration.
- [ ] Calibration certificate received.
- [ ] Serial number verified.
- [ ] Calibration status accepted.
- [ ] As-found/as-left results reviewed.
- [ ] Calibration uncertainty reviewed.
- [ ] Approximately 1-in calibration performance reviewed.
- [ ] Calibration-correction policy frozen.

### B. Check Standard

- [ ] Physical identity verified.
- [ ] Certificate obtained.
- [ ] Certified dimension confirmed.
- [ ] Certificate number recorded.
- [ ] Measurement uncertainty recorded.
- [ ] Calibration status accepted.
- [ ] Reference-temperature information recorded.

### C. Temperature Monitoring

- [ ] Digi-Sense thermometer received.
- [ ] Thermometer identity recorded.
- [ ] Calibration certificate reviewed.
- [ ] Type-T surface probe available.
- [ ] Temperature-record procedure verified.

### D. Session Acceptance Rules

- [ ] `E_limit` established.
- [ ] `R_limit` established.
- [ ] `D_limit` established.
- [ ] Technical basis documented.
- [ ] Session PASS/HOLD rules frozen.

### E. Specimen Screening and Selection

- [ ] Screening population record complete.
- [ ] All 235 specimen IDs accounted for.
- [ ] Screening classifications complete.
- [ ] Sampling strata finalized.
- [ ] Stratum allocations finalized.
- [ ] Previously excluded/prevalidation specimens identified.
- [ ] 60-specimen sample selected programmatically.
- [ ] Selection seed recorded.
- [ ] Selection script committed.
- [ ] Frozen specimen-selection CSV created.
- [ ] Specimen-selection file audited.

### F. Randomization

- [ ] Manual randomization script finalized.
- [ ] CV randomization script finalized.
- [ ] Manual seed confirmed.
- [ ] CV seed confirmed.
- [ ] Manual run order generated.
- [ ] CV run order generated.
- [ ] Every selected specimen appears exactly once per round.
- [ ] Three manual rounds verified.
- [ ] Three CV rounds verified.
- [ ] Run-order files frozen.

### G. Manual Data System

- [ ] Manual-observation CSV/template created.
- [ ] Manual-session CSV/template created.
- [ ] Reference-check CSV/template created.
- [ ] Data-entry fields verified.
- [ ] Previous manual results hidden where practical.
- [ ] Manual session-ID convention finalized.

### H. CV Measurement System

- [ ] Physical fixture configuration verified.
- [ ] Camera identity verified.
- [ ] Camera position verified.
- [ ] Backlight verified.
- [ ] Blank/reference procedure verified.
- [ ] Frozen segmentation verified.
- [ ] Frozen PCA/extreme-mask estimator verified.
- [ ] Frozen calibration planes verified.
- [ ] Quality gates verified.
- [ ] Production acquisition workflow verified.
- [ ] Formal validation Git commit recorded.
- [ ] Repository clean at freeze point.

### I. CV Data Storage

- [ ] Formal raw-image directory created.
- [ ] Naming convention finalized.
- [ ] CV observation manifest created.
- [ ] Mask/diagnostic storage verified.
- [ ] File-path fields verified.
- [ ] Adequate storage available.

### J. Environmental Records

- [ ] Environmental observation CSV/template created.
- [ ] Start/end temperature fields verified.
- [ ] Check-standard surface-temperature fields verified.
- [ ] Environmental abnormality field verified.

### K. Deviation Controls

- [ ] Protocol-deviation log created.
- [ ] Status vocabulary frozen.
- [ ] Replacement rules frozen.
- [ ] Data-disposition categories frozen.
- [ ] Deviation-ID convention finalized.

### L. Statistical Analysis

- [ ] Statistical Analysis Plan committed.
- [ ] Primary metrics frozen.
- [ ] Acceptance thresholds frozen.
- [ ] 95th-percentile definition frozen.
- [ ] Availability denominator frozen.
- [ ] Missing-CV rules frozen.
- [ ] Outlier policy frozen.
- [ ] Classification rules frozen.
- [ ] Certificate-dependent uncertainty decisions completed.

### M. Automated Audit

- [ ] Validation-data audit script created.
- [ ] Frozen-sample checks implemented.
- [ ] Run-order checks implemented.
- [ ] Session linkage checks implemented.
- [ ] Failure classification checks implemented.
- [ ] Replacement linkage checks implemented.
- [ ] Raw-file existence checks implemented.
- [ ] Audit tested on mock/nonformal data.

### N. Research Record

- [ ] All formal protocols committed.
- [ ] Calibration reviews committed.
- [ ] Randomization scripts committed.
- [ ] Run-order files committed/frozen.
- [ ] Formal validation directory structure created.
- [ ] Git status clean.
- [ ] Pre-measurement Git commit recorded.
- [ ] Repository backup/snapshot created.

## 28. Stop Conditions

Formal validation remains `NO-GO` if any critical item remains unresolved, including unaccepted reference calibration, undefined session acceptance limits, unfrozen sample/run orders, unfrozen measurement system, incomplete data-storage structure, unfrozen SAP, unresolved material prevalidation issues, or inability to establish the tested configuration.

## 29. GO Declaration

Formal specimen measurements may begin only when all critical checklist items are satisfied.

The research record should then contain a dated declaration:

**CaseMetrology Formal OAL Validation Status: GO**

identifying date, operator, frozen Git commit, sample file, manual/CV run-order files, calibration certificates, session acceptance criteria, SAP revision, and any noncritical remaining administrative items.

## 30. Formal Validation Start Point

The formal study begins when the first scheduled specimen receives its first formal manual-reference measurement under the frozen protocol.

## 31. Final Principle

The objective is not to ensure that CaseMetrology passes validation.

The objective is to ensure that the resulting conclusion—favorable, conditional, or unfavorable—is supported by a prospectively defined, reproducible, and auditable experimental process.
