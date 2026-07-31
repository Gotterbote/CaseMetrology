# Top-Down OAL Synthetic Geometry Baseline

## Status

Approved exploratory geometry model. Not a physical metrology result.

## Date

2026-07-31

## Physical Configuration Represented

- Camera views the measurement surface from directly above.
- The case lies on its side in a V-notch fixture.
- The case is unheaded, straight-walled, and has no taper or neck.
- The fixture crosses the middle portion of the case.
- Both physical case endpoints remain visible.
- The fixture and case may rotate together within the image.
- The case may shift longitudinally because the fixture has no stops.

## Synthetic Verification

- Tests collected: 2
- Tests passed: 2
- Tests failed: 0
- Execution time: 0.18 seconds
- Python: 3.10.10

## Functions Verified

- The synthetic scene and binary mask are generated successfully.
- The fixture region is wider than the exposed case regions.
- The complete case-and-fixture assembly can be rotated as one object.

## Visual Review

The generated vertical and rotated previews were reviewed by the system designer
and judged to represent the intended physical arrangement accurately.

## Research Classification

This is an exploratory software-development baseline. It documents the approved
geometry used to develop and test orientation-independent OAL detection.

It does not establish:

- physical measurement accuracy,
- camera calibration accuracy,
- real-image segmentation performance,
- repeatability,
- reproducibility,
- fixture dimensional stability.

## Next Development Step

Develop the OAL measurement pipeline using the merged case-and-fixture
silhouette. The method will identify the wider fixture region, fit the exposed
straight case edges, establish the case longitudinal axis, and measure between
the two visible case endpoints.
