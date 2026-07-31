# Top-Down OAL Measurement Baseline

## Status

Exploratory software verification. This is not an accepted physical metrology result.

## Date

2026-07-31

## Execution Environment

- Platform: NVIDIA Jetson Orin Nano
- Python: 3.12.3
- pytest: 7.4.4

## Measurement Configuration

The implementation models a top-down view of:

- an unheaded, straight-wall case lying on its side,
- a wider V-notch fixture crossing the case body,
- both physical case endpoints remaining visible,
- the fixture and case rotating together,
- longitudinal movement of the case within the fixture.

## Algorithm Baseline

The exploratory implementation:

1. Extracts the largest connected silhouette.
2. Rejects significant additional objects.
3. Estimates the assembly orientation with PCA.
4. Generates a transverse-width profile.
5. Detects the wider fixture region.
6. Uses exposed case pixels to refine the longitudinal axis.
7. Projects the merged silhouette onto the refined axis.
8. Measures between the two projected axial extremes.

## Test Results

### Top-Down Geometry Tests

- Tests passed: 2
- Tests failed: 0

### OAL Measurement Tests

- Tests passed: 5
- Tests failed: 0

The measurement tests included:

- 0-degree orientation,
- 45-degree orientation,
- 90-degree orientation,
- 35-degree orientation with a negative fixture offset,
- 35-degree orientation with a positive fixture offset.

### Full Project Test Suite

- Tests passed: 7
- Tests failed: 0

## Interpretation

The software produced consistent synthetic OAL results under the tested
orientations and fixture offsets. The full project test suite completed without
regressions.

These results verify software behavior under controlled synthetic geometry only.

They do not establish:

- dimensional accuracy on physical cases,
- camera calibration accuracy,
- real-image segmentation performance,
- repeatability or reproducibility,
- fixture stability,
- robustness to lens distortion, lighting variation, blur, or contamination.

## Next Validation Step

Create diagnostic overlays showing:

- the detected merged silhouette,
- the initial and refined longitudinal axes,
- the detected fixture-width region,
- the two projected case endpoints,
- the calculated OAL in pixels.

After diagnostic review, the algorithm will be evaluated on real images captured
with the Jetson Orin Nano and compared with manual reference measurements.
