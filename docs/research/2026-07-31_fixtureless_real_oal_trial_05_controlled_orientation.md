# Fixtureless Real-Image OAL Trial 05 — Controlled Orientation

## Status

Accepted exploratory controlled-orientation result.

This trial identifies an orientation-dependent bias in the current
PCA-plus-extreme-projection estimator. It is not an accepted dimensional-
accuracy result.

## Date

2026-07-31

## Objective

Evaluate the effect of case orientation on measured pixel length while
controlling image location with a predefined centroid target.

## Configuration

- Platform: NVIDIA Jetson Orin Nano
- Camera resolution: 1456 x 1088
- Reported frame rate: 44.00 fps
- Illumination: backlight
- Lexan locator retained
- V-block not used
- Same straight-wall unheaded case used throughout
- Fresh blank reference captured for Trial 05
- Three measurement captures initially collected for each orientation
- Five additional accepted captures retained for the settled 90-degree retake

## Centroid Placement Control

The target centroid was derived from the accepted Trial 03 static position.

- Target X: 757.444 px
- Target Y: 648.175 px
- Acceptance tolerance: plus or minus 5 px in X and Y

A placement-check script was created at:

`scripts/check_oal_centroid.py`

The script:

1. subtracts the blank reference;
2. segments the largest foreground component;
3. calculates the case centroid;
4. compares the centroid with the target;
5. reports pass or fail;
6. reports the required movement direction;
7. saves a diagnostic mask and overlay.

## Accepted Initial Placements

### Near-horizontal group

- Accepted centroid: (757.403, 644.150) px
- Delta X: -0.041 px
- Delta Y: -4.025 px
- Placement result: Pass

### Approximately 16-degree group

- Accepted centroid: (758.740, 647.534) px
- Delta X: +1.296 px
- Delta Y: -0.641 px
- Placement result: Pass

### Approximately 33-degree group

- Accepted centroid: (757.108, 645.300) px
- Delta X: -0.336 px
- Delta Y: -2.875 px
- Placement result: Pass

### Approximately 58-degree group

- Accepted centroid: (759.792, 647.964) px
- Delta X: +2.348 px
- Delta Y: -0.211 px
- Placement result: Pass

### Original approximately 90-degree placement

The provisional placement check passed, but all three subsequent measurement
captures shifted approximately 7 px left and failed the centroid requirement.

Original measurement-capture deltas:

- Capture 01: (-7.016, +1.563) px
- Capture 02: (-7.020, +1.545) px
- Capture 03: (-7.061, +1.605) px

The original images were retained as failed placement-control evidence and were
excluded from the revised controlled-orientation comparison.

## Settled 90-Degree Retake

The case was repositioned, allowed to settle, and checked twice before
measurement.

### Settled check 1

- Centroid: (761.167, 646.738) px
- Delta: (+3.723, -1.437) px
- Result: Pass

### Settled check 2

- Centroid: (761.064, 646.712) px
- Delta: (+3.620, -1.463) px
- Result: Pass

Movement between the two checks was approximately:

- X: 0.103 px
- Y: 0.026 px

Five retake images were then captured. All five passed the centroid requirement.

## Revised Accepted-Capture Analysis

- Accepted-placement captures analyzed: 17
- Centroid-tolerance passes: 17 of 17
- Border-contact failures: 0
- Diagnostic segmentation flags: 1

The segmentation-flag threshold was defined as five times the independent
Trial 03 static standard deviation:

- Trial 03 static standard deviation: 0.050349 px
- Diagnostic threshold: 0.251745 px

This threshold was used as a diagnostic rule, not as justification for deleting
or concealing observations.

## Orientation-Group Results

### Near-horizontal group

- Mean detected angle: 3.467319 degrees
- Mean length: 523.070423 px
- Median length: 523.069154 px
- Sample standard deviation: 0.032855 px
- Range: 0.065674 px
- Diagnostic flags: 0

### Approximately 16-degree group

- Mean detected angle: 15.650805 degrees
- Mean length: 522.778558 px
- Median length: 522.776435 px
- Sample standard deviation: 0.004222 px
- Range: 0.007601 px
- Diagnostic flags: 0

### Approximately 33-degree group

- Mean detected angle: 32.617937 degrees
- Mean length: 522.802673 px
- Median length: 522.782483 px
- Sample standard deviation: 0.039256 px
- Range: 0.070294 px
- Diagnostic flags: 0

### Approximately 58-degree group

- Mean detected angle: 57.823983 degrees
- Mean length: 521.629784 px
- Median length: 521.612035 px
- Sample standard deviation: 0.038778 px
- Range: 0.071202 px
- Diagnostic flags: 0

### Approximately 89-degree settled retake

- Mean detected angle: 89.128907 degrees
- Five-capture mean length: 523.451640 px
- Median length: 523.364755 px
- Five-capture sample standard deviation: 0.187519 px
- Five-capture range: 0.423245 px
- Diagnostic flags: 1
- Mean of four unflagged captures: 523.367832 px

## Segmentation Flag

The second settled 90-degree retake measured:

- OAL: 523.786876 px
- Deviation from group median: approximately 0.422 px

The other four captures clustered near 523.365 px.

Visual review showed no gross movement, axis failure, border contact, or
incorrect endpoint selection. The difference was therefore classified as a
transient endpoint-segmentation anomaly.

The flagged image and its results were retained in the evidence package.

## Primary Robust Orientation Comparison

Orientation-group medians were used for the primary exploratory comparison.

- Minimum group median: 521.612035 px
- Maximum group median: 523.364755 px
- Range of group medians: 1.752720 px
- Approximate range relative to measured length: 0.335 percent

## Visual Diagnostic Review

All 17 accepted-centroid overlays were reviewed.

The review confirmed:

- the measurement axis followed the case longitudinal axis;
- both endpoint markers contacted the physical ends;
- no endpoint marker selected a sidewall corner;
- the complete case silhouette was retained;
- the Lexan locator was excluded;
- no case contacted an image boundary;
- the flagged 90-degree capture showed no gross geometric failure.

Visual diagnostic result: 17 of 17 passed.

## Interpretation

Trial 05 successfully controlled image location and demonstrated that the
current PCA-plus-extreme-mask-pixel estimator produces systematic
orientation-dependent variation.

The 1.752720-pixel range among orientation-group medians is substantially larger
than the 0.050349-pixel static standard deviation measured during Trial 03.
Ordinary frame-to-frame capture noise therefore cannot explain the observed
orientation effect.

The likely contributors include:

- pixel-grid quantization;
- orientation-dependent endpoint segmentation;
- dependence on the most extreme projected mask pixels;
- small boundary changes having different projected effects at different
  orientations.

The finding does not show that fixtureless imaging is unsuitable. It shows that
the current endpoint estimator requires refinement before dimensional
calibration and accuracy testing.

## Next Development Step

Replace the extreme-mask-pixel estimator with a geometry-based method:

1. fit the two straight case sidewalls;
2. derive the longitudinal center axis from the fitted sidewalls;
3. fit a line to each physical end face;
4. calculate axial distance between the fitted end-face lines;
5. use robust fitting to prevent isolated boundary pixels from controlling the
   result.

The revised estimator should be tested first against existing Trial 03 and
Trial 05 images. No additional physical captures are required for the initial
algorithm comparison.
