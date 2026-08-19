# CaseMetrology Formal OAL Protocol-Deviation and Data-Disposition Policy

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Designated operator:** Timmy D. Bell
**Status:** Prospective policy; formal validation measurements have not begun

## 1. Purpose

This policy defines how deviations, abnormalities, invalid observations, measurement-system failures, and questionable sessions shall be documented and dispositioned.

## 2. General Principle

All formal validation attempts and associated records shall be retained unless preservation is technically impossible.

An observation shall not be deleted, replaced, repeated, or excluded merely because:

- its value appears unusual;
- it disagrees with another measurement;
- it is outside specification;
- it increases calculated error;
- it changes a statistical conclusion;
- it appears to be an outlier;
- it causes CV performance to look worse.

Unexpected results remain study data unless independent evidence shows the prescribed measurement was not validly executed.

## 3. Event Categories

### `VALID`

Measurement performed according to protocol and legitimate result obtained.

### `SYSTEM_FAILURE`

The intended CV attempt occurred, but the frozen system failed to return an accepted measurement.

### `PROTOCOL_INVALID`

The intended measurement was not correctly performed because of an external procedural event.

### Session-level deviation

A condition potentially affects multiple observations.

### Administrative deviation

A documentation issue with no plausible measurement effect.

## 4. Deviation Identification

Recommended format:

`DEV-YYYYMMDD-NNN`

Example:

`DEV-20260912-001`

## 5. Immediate Response to a Deviation

When a potentially significant deviation is identified:

1. stop affected activity when continuing could compromise more data;
2. preserve measurements already obtained;
3. record the event promptly;
4. identify affected specimens/observations/sessions;
5. do not delete or overwrite raw data;
6. do not repeat unless protocol authorizes replacement;
7. investigate;
8. document final disposition.

## 6. Required Deviation Record

Preserve at minimum:

- `deviation_id`;
- date/time identified;
- operator;
- modality;
- `session_id`;
- `part_id`, when applicable;
- affected observation IDs/run positions;
- deviation category;
- factual description;
- detection method;
- immediate action;
- potential data impact;
- corrective action;
- replacement authorization;
- review status;
- final disposition;
- technical basis;
- disposition date;
- notes.

## 7. Replacement Measurements

Replacement is permitted only when the original observation is `PROTOCOL_INVALID`.

The original record shall remain preserved.

The replacement shall receive a new ID, reference the original, and be appended according to the applicable round protocol.

## 8. Events That Do Not Authorize Replacement

No replacement solely because:

- manual reading is unexpected;
- manual readings disagree;
- CV result appears inaccurate;
- CV and manual disagree;
- specimen appears as an outlier;
- CV pipeline failure occurs;
- result worsens statistics;
- specimen is out of specification;
- another result might be more favorable.

## 9. Treatment of CV System Failures

`SYSTEM_FAILURE` is a performance result and remains part of the formal study.

The statistical plan shall report dimensional performance among valid measurements separately from measurement availability/failure rate.

## 10. Manual Measurement Abnormalities

An unusual but properly executed manual reading remains valid.

Invalidation requires independent evidence of procedural error.

## 11. Failed Pre-Session Reference Check

A failed pre-session check means formal specimen measurement shall not begin.

The failed check remains in the record.

## 12. Failed Post-Session Reference Check

If pre-check passed but post-check fails:

1. retain all specimen measurements;
2. classify session `HOLD_FOR_REVIEW`;
3. suspend additional formal manual measurement;
4. investigate;
5. review environmental/reference-check evidence;
6. document findings;
7. assign final disposition.

## 13. Session Disposition Categories

Use:

- `PASS`
- `HOLD_FOR_REVIEW`
- `ACCEPT_WITH_DEVIATION`
- `REJECTED`

## 14. Data-Disposition Categories

Use:

- `INCLUDE_PRIMARY`
- `INCLUDE_WITH_DEVIATION`
- `SYSTEM_FAILURE`
- `PROTOCOL_INVALID_REPLACED`
- `PROTOCOL_INVALID_NO_REPLACEMENT`
- `EXCLUDE_DOCUMENTED`
- `PENDING_REVIEW`

## 15. Criteria for Excluding Data

Exclusion from primary dimensional agreement analysis requires a documented reason independent of the resulting error, such as:

- wrong measurement system;
- incorrect calibration configuration;
- unresolvable specimen identity;
- irretrievably corrupted source file from external failure;
- rejected formal session;
- other specific violation demonstrating the observation is not representative of the frozen procedure.

Excluded observations remain visible in the research record.

## 16. Outliers

Statistical outlier status alone shall not justify exclusion.

Investigate identity, source integrity, diagnostics, session status, and documented deviations. Retain the observation if no independent reason for invalidation exists.

## 17. Specimen Damage

If a specimen is damaged after selection:

1. stop further measurement of that specimen;
2. document the condition;
3. identify prior measurements;
4. determine whether earlier data remain unaffected;
5. do not automatically substitute another specimen;
6. document sampling implications.

## 18. Hardware or Software Changes

Material CV changes include camera, lens, geometry, fixture, backlight, segmentation, calibration, estimator, quality gates, or measurement-affecting software changes.

Such changes require formal review and shall not be silently pooled with previous data.

## 19. Corrections to Recorded Data

A factual transcription/metadata error may be corrected only when the correct value is independently recoverable.

Preserve original value, corrected value, reason, evidence, date, operator, and correction/deviation identifier.

## 20. No Silent Data Cleaning

Prohibited:

- deleting rows without documentation;
- overwriting failed observations;
- replacing results with averages;
- removing inconvenient specimens;
- dropping CV failures from attempt counts;
- altering run-order files after measurement;
- converting failures to unexplained missing values;
- filtering solely to improve agreement;
- changing acceptance criteria after results are seen.

## 21. Review Responsibility

Timmy D. Bell is the designated operator and primary researcher and shall document deviations and proposed dispositions.

Material deviations capable of affecting scientific interpretation should be brought to the thesis advisor or committee as appropriate before final analysis/reporting.

## 22. Relationship to Statistical Analysis

The statistical plan shall define which disposition categories enter primary analysis, how system failures are reported, treatment of incomplete triplicates, and any sensitivity analyses.

## 23. Reporting in the Thesis

Material deviations affecting formal validation shall be reported transparently.

## 24. Protocol Lock

After formal data collection begins:

- definitions of `SYSTEM_FAILURE` and `PROTOCOL_INVALID` shall not be weakened;
- replacement rules shall not be expanded;
- exclusion criteria shall not be broadened based on observed results;
- material changes shall be documented explicitly.
