# CaseMetrology Formal OAL Validation Dataset Schema

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Designated operator:** Timmy D. Bell
**Status:** Prospective schema; formal validation measurements have not begun

## 1. Purpose

This document defines the data structure for the formal OAL validation study before formal measurements are collected.

The schema is intended to preserve raw observations, maintain traceability, keep manual and CV acquisition independent, distinguish system failures from protocol-invalid events, support reproducible analysis, and prevent retrospective dataset restructuring.

## 2. Data-Architecture Principle

Use separate source files for:

1. frozen validation-specimen identity;
2. manual run order;
3. CV run order;
4. raw manual-reference observations;
5. manual-session reference checks;
6. environmental observations;
7. raw CV observations;
8. protocol deviations;
9. certificate reviews;
10. derived statistical datasets.

Raw files shall remain authoritative. Derived files shall be programmatically regenerated.

## 3. Primary Specimen Identifier

The primary research specimen identifier is:

`part_id`

For this study, `part_id` equals the integer physically laser etched onto the specimen.

## 4. Recommended Files

### Frozen validation sample

`data/oal_validation/formal_validation_specimens.csv`

Required fields:

- `part_id`
- `laser_etched_id_verified`
- `screening_reading_in`
- `screening_class`
- `selection_stratum`
- `selected_for_validation`
- `selection_seed`
- `selection_order`
- `selection_timestamp`
- `selection_script_commit`
- `notes`

### Manual run order

`data/oal_validation/manual_run_order.csv`

Required fields:

- `manual_run_id`
- `manual_round`
- `planned_sequence`
- `part_id`
- `selection_stratum`
- `randomization_seed`
- `run_order_generated_at`
- `run_order_script_commit`
- `completion_status`
- `session_id`
- `notes`

### CV run order

`data/oal_validation/cv_run_order.csv`

Required fields:

- `cv_run_id`
- `cv_round`
- `planned_sequence`
- `part_id`
- `selection_stratum`
- `randomization_seed`
- `run_order_generated_at`
- `run_order_script_commit`
- `completion_status`
- `session_id`
- `notes`

### Raw manual observations

`data/oal_validation/manual_reference_observations.csv`

Required fields:

- `manual_observation_id`
- `manual_run_id`
- `part_id`
- `manual_round`
- `planned_sequence`
- `session_id`
- `laser_etched_id_verified`
- `reading_in`
- `measurement_date`
- `measurement_time`
- `operator`
- `caliper_manufacturer`
- `caliper_model`
- `caliper_code`
- `caliper_serial`
- `measurement_valid`
- `protocol_invalid`
- `invalidation_reason`
- `replacement_for_observation_id`
- `notes`

### Manual sessions

`data/oal_validation/manual_sessions.csv`

Required fields:

- `session_id`
- `manual_round`
- `session_date`
- `operator`
- `caliper_serial`
- `caliper_certificate_id`
- `check_standard_id`
- `check_standard_certificate_id`
- `check_standard_certified_in`
- `session_start_time`
- `session_end_time`
- `pre_check_status`
- `post_check_status`
- `session_status`
- `review_required`
- `deviation_id`
- `notes`

### Reference-check observations

`data/oal_validation/manual_reference_checks.csv`

Required fields:

- `reference_check_id`
- `session_id`
- `check_position`
- `repeat_number`
- `check_standard_id`
- `certified_value_in`
- `observed_value_in`
- `check_timestamp`
- `operator`
- `valid`
- `notes`

### Environmental observations

`data/oal_validation/environmental_observations.csv`

Required fields:

- `environment_observation_id`
- `session_id`
- `measurement_modality`
- `observation_position`
- `observation_timestamp`
- `room_temperature`
- `room_temperature_unit`
- `check_standard_surface_temperature`
- `surface_temperature_unit`
- `temperature_instrument_id`
- `temperature_probe_id`
- `environment_abnormality`
- `review_required`
- `notes`

### Raw CV observations

`data/oal_validation/cv_observations.csv`

Required fields:

- `cv_observation_id`
- `cv_run_id`
- `part_id`
- `cv_round`
- `planned_sequence`
- `session_id`
- `laser_etched_id_verified`
- `acquisition_date`
- `acquisition_time`
- `operator`
- `software_commit`
- `camera_id`
- `measurement_status`
- `oal_in`
- `effective_ppi`
- `quality_gate_status`
- `failure_class`
- `protocol_invalid`
- `invalidation_reason`
- `replacement_for_observation_id`
- `raw_image_path`
- `mask_path`
- `diagnostic_path`
- `notes`

## 5. CV Measurement Status Vocabulary

Use only:

- `VALID`
- `SYSTEM_FAILURE`
- `PROTOCOL_INVALID`

## 6. Protocol-Deviation Log

Recommended file:

`data/oal_validation/protocol_deviations.csv`

Required fields:

- `deviation_id`
- `deviation_date`
- `session_id`
- `measurement_modality`
- `part_id`
- `observation_id`
- `deviation_type`
- `description`
- `immediate_action`
- `data_affected`
- `review_status`
- `disposition`
- `decision_basis`
- `operator`
- `notes`

## 7. Certificate Review Records

Recommended files:

- `docs/research/calibration/caliper_certificate_review.md`
- `docs/research/calibration/check_standard_certificate_review.md`
- `docs/research/calibration/temperature_instrument_certificate_review.md`

## 8. Derived Manual Reference Dataset

Recommended:

`data/oal_validation/derived/manual_reference_summary.csv`

Suggested fields:

- `part_id`
- `manual_1_in`
- `manual_2_in`
- `manual_3_in`
- `manual_mean_in`
- `manual_sd_in`
- `manual_range_in`
- `manual_n_valid`
- `reference_status`

## 9. Derived CV Dataset

Recommended:

`data/oal_validation/derived/cv_summary.csv`

Suggested fields:

- `part_id`
- `cv_1_in`
- `cv_2_in`
- `cv_3_in`
- `cv_mean_in`
- `cv_sd_in`
- `cv_range_in`
- `cv_n_valid`
- `cv_n_system_failures`
- `cv_complete`

## 10. Joined Analysis Dataset

Recommended:

`data/oal_validation/derived/oal_validation_analysis.csv`

Suggested fields:

- `part_id`
- `selection_stratum`
- `manual_mean_in`
- `manual_sd_in`
- `cv_mean_in`
- `cv_sd_in`
- `difference_in`
- `absolute_error_in`
- `percent_error`
- `cv_n_valid`
- `cv_failure_count`
- `analysis_included`
- `exclusion_reason`

This file shall be generated programmatically and shall not be manually populated.

## 11. Missing Values

Use empty fields for legitimate absence and explicit status fields explaining why.

Do not use numeric sentinels such as `0`, `999`, or `-1` for missing dimensional values.

## 12. Date/Time Format

Recommended:

- date: `YYYY-MM-DD`
- time: `HH:MM:SS`
- combined timestamp: ISO 8601 local time with UTC offset

## 13. Units

Use inches as the primary dimensional study unit.

Where practical, encode units in field names such as `reading_in`, `oal_in`, `manual_mean_in`.

## 14. File Integrity

Preserve formal raw-data files after each completed session.

Where practical, generate SHA-256 manifests for raw CSVs, images, masks, diagnostics, run orders, and key protocol records.

## 15. Recommended Repository Structure

```text
CaseMetrology/
├── data/
│   └── oal_validation/
│       ├── formal_validation_specimens.csv
│       ├── manual_run_order.csv
│       ├── cv_run_order.csv
│       ├── manual_reference_observations.csv
│       ├── manual_reference_checks.csv
│       ├── manual_sessions.csv
│       ├── environmental_observations.csv
│       ├── cv_observations.csv
│       ├── protocol_deviations.csv
│       ├── derived/
│       │   ├── manual_reference_summary.csv
│       │   ├── cv_summary.csv
│       │   └── oal_validation_analysis.csv
│       └── manifests/
│           └── formal_validation_sha256.txt
├── docs/
│   └── research/
│       └── ...
└── scripts/
    ├── generate_oal_validation_sample.py
    ├── generate_oal_manual_run_order.py
    ├── generate_oal_cv_run_order.py
    ├── audit_oal_validation_data.py
    └── analyze_oal_validation.py
```

## 16. Automated Audit Requirements

Before analysis, an automated audit should verify at minimum:

- exactly 60 frozen validation specimens;
- valid/unique `part_id` values;
- 60 planned observations per manual round;
- 60 planned observations per CV round;
- every selected specimen appears once per round;
- required session reference checks exist;
- every valid observation links to a known session;
- all CV failures are classified;
- replacements link to invalid originals;
- expected raw files exist;
- software commits are recorded;
- dimensional fields parse correctly;
- no unauthorized specimen enters the formal dataset.

The audit shall fail loudly rather than silently repair inconsistent records.

## 17. Separation of Raw and Derived Evidence

Raw evidence includes individual readings, check-standard observations, environmental observations, raw images, masks, failures, run orders, and deviations.

Derived evidence includes means, SDs, ranges, bias, errors, limits of agreement, regression results, figures, and summary tables.

Derived evidence shall always be reproducible from preserved raw evidence and version-controlled analysis code.

## 18. Protocol Lock

Before formal measurement, freeze:

1. final filenames;
2. column names;
3. status vocabulary;
4. identifier formats;
5. timestamp format;
6. unit conventions;
7. directory structure;
8. randomization output format;
9. validation audit rules.
