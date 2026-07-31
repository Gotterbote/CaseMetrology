# Top-Down OAL Diagnostic Overlay Baseline

## Status

Exploratory software diagnostic verification. This is not an accepted physical metrology result.

## Date

2026-07-31

## Execution Environment

- Platform: NVIDIA Jetson Orin Nano
- Python: 3.12.3
- pytest: 7.4.4

## Scope

This checkpoint adds a monochrome diagnostic overlay for the top-down OAL
measurement workflow.

The overlay is intended to support visual verification of:

- the merged case-and-fixture silhouette,
- the measured case axis,
- the two endpoint markers,
- the reported OAL in pixels,
- the detected axis angle.

## Diagnostic Result

A synthetic overlay was generated and visually reviewed.

Observed diagnostic output:

- Passed: True
- Measured OAL: 360.954 px
- Detected angle: -34.992 degrees
- Fixture width ratio: 2.900

## Visual Review Outcome

The overlay was visually judged acceptable.

Confirmed:

- the merged silhouette looked physically correct,
- the measurement line followed the case longitudinal axis,
- the endpoint markers touched the two physical case ends,
- the overlay remained monochrome,
- the overlay was suitable for diagnostic review.

## Automated Verification

### Overlay tests
- Tests passed: 2
- Tests failed: 0

### Full project suite
- Tests passed: 9
- Tests failed: 0

## Interpretation

This result supports that the exploratory diagnostic overlay correctly renders
the current synthetic measurement result and that the added overlay code does
not introduce regressions into the current software baseline.

These results do not establish:

- physical dimensional accuracy,
- performance on real captured images,
- repeatability,
- reproducibility,
- calibration validity.

## Next Step

Apply the diagnostic overlay to real Jetson-captured images and evaluate whether
the detected axis and endpoints remain visually correct on actual fixture data.
