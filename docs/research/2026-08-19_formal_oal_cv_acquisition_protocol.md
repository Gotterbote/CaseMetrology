# CaseMetrology Formal OAL Computer-Vision Acquisition Protocol

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Measurement modality:** Computer vision
**Designated operator:** Timmy D. Bell
**Status:** Prospective protocol; formal validation measurements have not begun

## 1. Purpose

This protocol defines the procedure for obtaining formal CV OAL measurements during CaseMetrology validation.

## 2. Frozen Measurement System

Formal validation shall use the frozen CaseMetrology OAL configuration established before validation.

The primary estimator is the PCA/extreme-mask method in:

`src/measurement/topdown_oal.py`

The frozen segmentation pipeline in:

`src/image_processing/oal_segmentation.py`

uses:

1. grayscale inputs;
2. blank-image subtraction;
3. 5×5 Gaussian blur;
4. Otsu thresholding;
5. 3×3 morphological opening/closing;
6. largest connected component;
7. established quality gates.

The previously frozen calibration planes and effective-PPI calculation shall remain unchanged.

## 3. Formal CV Dataset Independence

Formal CV acquisition shall occur after completion of formal manual-reference measurements.

During CV acquisition, the operator shall not consult:

- formal manual readings or means;
- screening measurements;
- specimen stratum;
- CV-versus-manual errors.

## 4. Measurement-Round Structure

The 60 specimens shall be measured in three independently randomized CV rounds.

Each specimen appears once per round.

Total planned attempts:

\[
60\times3=180
\]

Every observation shall include complete removal and independent repositioning.

## 5. Randomized Run Order

The operator shall follow the frozen CV run-order file.

The sequence shall not be changed based on convenience, suspected specimen dimension, or observed results.

If a session stops, resume at the next uncompleted run-order position without reshuffling.

## 6. Pre-Session Preparation

Before formal CV acquisition:

1. verify designated camera and computing platform;
2. verify frozen software revision;
3. verify no uncommitted measurement-system changes;
4. verify camera/fixture geometry;
5. verify blank/reference configuration;
6. verify backlight and acquisition function;
7. record `session_id`;
8. record software Git commit;
9. record required environmental information.

No code, calibration value, or image-processing parameter shall be adjusted during a formal session.

## 7. Specimen Identification

For each scheduled observation:

1. locate the scheduled specimen;
2. read the laser-etched ID;
3. verify it matches `part_id`;
4. record verification;
5. do not proceed if identity is uncertain.

## 8. Specimen Placement

For every observation:

1. completely remove the specimen before placement;
2. place it in the established OAL fixture;
3. position it according to the frozen physical procedure;
4. ensure normal resting position;
5. do not manipulate it to force a numerical result;
6. initiate one acquisition;
7. completely remove it afterward.

The fixture shall remain installed in the validated configuration.

## 9. One Planned Attempt per Run-Order Position

Each scheduled position permits **one formal acquisition attempt**.

The operator shall not repeat an acquisition because:

- OAL appears incorrect;
- result differs from another reading;
- result is outside specification;
- result differs from expectation;
- segmentation appears imperfect after seeing the result;
- manual disagreement is suspected.

A surprising result is data.

## 10. Valid CV Measurement

Classify an attempt `VALID` when the frozen pipeline completes normally and returns an accepted OAL.

Retain, where produced:

- raw image;
- blank/reference linkage;
- mask;
- centroid/geometric metadata;
- effective calibration;
- OAL;
- quality flags;
- timestamp;
- specimen ID;
- round;
- sequence;
- session;
- software revision.

## 11. Measurement-System Failure

If the frozen pipeline rejects the observation or fails to return accepted OAL due to segmentation, quality-gate, detection, mask, geometry, endpoint, or other internal measurement-pipeline conditions, classify:

`SYSTEM_FAILURE`

The event counts as the scheduled formal system attempt and shall not automatically be repeated.

## 12. Protocol-Invalid CV Events

Classify `PROTOCOL_INVALID` when an external procedural event prevents the intended acquisition.

Examples:

- wrong specimen;
- wrong ID/run-order position;
- camera disconnect before acquisition;
- external storage failure;
- specimen moved before completion;
- acquisition triggered before proper placement;
- lighting unintentionally disabled;
- wrong software configuration.

An unexpected OAL value or pipeline rejection is not protocol-invalid merely because it is unfavorable.

## 13. Replacement of Protocol-Invalid Observations

When legitimately protocol-invalid:

1. preserve the original record;
2. document reason;
3. retain files when available;
4. append one authorized replacement to the end of the applicable CV round;
5. link the replacement to the original.

System failures do not qualify for automatic replacement.

## 14. Operator Blinding to CV Output

Where practical, the acquisition interface shall prevent numerical OAL output from influencing reacquisition decisions.

If OAL is displayed, the operator shall not use it as justification for a retake.

## 15. Session Interruptions

If interrupted:

- completed observations remain;
- run order remains frozen;
- resume at next uncompleted position;
- create a new session ID when required;
- document relevant interruptions.

## 16. Hardware or Software Abnormality

If a hardware/software abnormality could affect validity:

1. stop formal acquisition;
2. preserve completed data;
3. document the condition;
4. identify last known valid position;
5. investigate;
6. document corrective action;
7. determine whether acquisition can resume under the same frozen configuration.

Material changes to algorithm, calibration, fixture, camera geometry, or segmentation require formal review.

## 17. Required CV Observation Record

Each attempt shall preserve at minimum:

- `cv_observation_id`;
- `cv_run_id`;
- `part_id`;
- `cv_round`;
- `planned_sequence`;
- `session_id`;
- ID verification status;
- date/time;
- operator;
- software commit;
- camera ID;
- `measurement_status`;
- `oal_in`, when available;
- `effective_ppi`;
- quality-gate status;
- failure classification;
- protocol-invalid status/reason;
- replacement linkage;
- raw image path;
- mask/diagnostic paths;
- notes.

## 18. Data Preservation

No formal CV observation shall be silently deleted, replaced, rerun, filtered, or excluded based on agreement with the manual reference.

All unsuccessful system attempts shall remain in the research record.

## 19. End-of-Session Record

Record:

- session end date/time;
- final completed run-order position;
- valid measurement count;
- system-failure count;
- protocol-invalid count;
- replacement count;
- required environmental information;
- abnormalities;
- operator notes.

## 20. Protocol Lock

Before first formal CV acquisition, freeze and document:

1. formal software Git commit;
2. camera identity;
3. camera/fixture physical configuration;
4. segmentation pipeline;
5. primary estimator;
6. calibration equations;
7. acquisition wrapper;
8. blank/reference procedure;
9. formal CV run order;
10. storage paths/naming;
11. final CV dataset schema.
