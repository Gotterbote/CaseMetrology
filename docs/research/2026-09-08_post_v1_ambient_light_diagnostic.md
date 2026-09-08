# Post-V1 Ambient-Light Diagnostic

Date: 2026-09-08

## Purpose

Determine whether changes in ambient room lighting measurably affect the CaseMetrology image state or calculated OAL when specimen position is held fixed.

This is a post-V1 engineering diagnostic only.

Formal V1 validation remains complete, immutable, and the primary thesis validation result. No V1 measurements, results, calibration values, estimator settings, thresholds, or software parameters will be modified based on this diagnostic.

## Diagnostic specimen

Specimen 121.

This specimen was previously segregated from the formal 60-specimen validation set during prevalidation and is not part of the retained formal V1 sample.

## System configuration

The V1 camera, lens, backlight, fixture, Lexan surface, measurement plane, software, calibration, and OAL estimator shall remain unchanged.

The backlight shall remain continuously energized.

The ceiling fan motor shall remain OFF.

## Lighting conditions

A  = window blocked, ceiling light OFF
B  = window exposed, ceiling light OFF
C  = window blocked, ceiling light ON
A2 = window blocked, ceiling light OFF again

An opaque window covering shall be used for the blocked condition.

## Phase 1: Blank images

No specimen present.

Acquire:

- A: 5 blank images
- B: 5 blank images
- C: 5 blank images
- A2: 5 blank images

Wait approximately 30 seconds after changing each lighting condition before acquisition.

Total blank images: 20.

## Phase 2: Fixed specimen

Return to condition A.

Place specimen 121 once in normal OAL orientation.

After initial placement, the specimen shall not be touched, lifted, translated, rotated, or reseated until all fixed-specimen acquisitions are complete.

Acquire:

- A: 10 specimen images
- B: 10 specimen images
- C: 10 specimen images
- A2: 10 specimen images

Wait approximately 30 seconds after changing each lighting condition before acquisition.

Total fixed-specimen images: 40.

## Primary comparisons

Blank-image intensity:
A versus B versus C versus A2.

Fixed-specimen OAL:
A versus B versus C versus A2.

The A-to-A2 comparison will be used to assess whether the system returned to its initial controlled-light condition.

## Interpretation

Observed changes will be treated as post-validation diagnostic evidence.

A reproducible lighting-associated change in OAL with the specimen physically unmoved would demonstrate that ambient-light state can affect the measurement pipeline.

Such a result would not by itself establish that ambient daylight caused the V1 validation errors.

Failure to observe an effect during weak daylight conditions will not be interpreted as proof that the sunny-day V1 conditions could not have affected the system.

## Stop conditions

Stop acquisition if:

- the camera or fixture is bumped;
- camera controls change unexpectedly;
- the specimen moves during the fixed-specimen phase;
- the window-blocked condition cannot adequately block exterior daylight;
- the measurement system configuration changes.

Invalid images shall be retained and documented rather than silently replaced.
