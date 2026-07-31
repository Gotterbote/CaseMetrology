# Fixtureless Real-Image OAL Trial 04 — Orientation and Location Robustness

## Status

Accepted exploratory robustness trial. This was not a pure controlled-orientation
experiment because image location changed between orientation groups.

## Date

2026-07-31

## Objective

Evaluate fixtureless OAL detection across substantially different case
orientations while attempting to keep the case near the same general image
region.

## Configuration

- Platform: NVIDIA Jetson Orin Nano
- Camera resolution: 1456 x 1088
- Illumination: backlight
- Lexan locator retained
- V-block not used
- Same straight-wall unheaded case used throughout
- Five nominal orientation groups
- Three consecutive captures per orientation
- Total captures: 15
- Trial 02 blank reference reused because camera, lighting, and locator
  configuration remained unchanged

## Detected Orientation Groups

- Nominal 0 degrees: mean detected angle 0.788980 degrees
- Nominal 30 degrees: mean detected angle 39.398820 degrees
- Nominal 45 degrees: mean detected angle 68.977472 degrees
- Nominal 60 degrees: mean detected angle 60.665440 degrees
- Nominal 90 degrees: mean detected angle 87.928074 degrees

The detected angles, rather than the nominal labels, should be used for
technical interpretation.

## Detection Results

- Captures analyzed: 15
- Successful measurements: 15
- Failed measurements: 0
- Border-contact failures: 0
- Visual diagnostic passes: 15 of 15

## Within-Group Results

### Angle 0 Group

- Mean length: 523.010104 px
- Sample standard deviation: 0.015802 px
- Range: 0.027559 px

### Nominal Angle 30 Group

- Mean length: 523.852839 px
- Sample standard deviation: 0.051278 px
- Range: 0.102309 px

### Nominal Angle 45 Group

- Mean length: 523.577018 px
- Sample standard deviation: 0.040232 px
- Range: 0.069925 px

### Nominal Angle 60 Group

- Mean length: 523.005468 px
- Sample standard deviation: 0.033027 px
- Range: 0.062439 px

### Nominal Angle 90 Group

- Mean length: 523.356092 px
- Sample standard deviation: 0.043419 px
- Range: 0.077899 px

## Across-Group Results

- Overall mean length: 523.360304 px
- Overall sample standard deviation: 0.341145 px
- Overall minimum: 522.980470 px
- Overall maximum: 523.906047 px
- Overall range: 0.925577 px
- Range of orientation-group means: 0.847371 px
- Mean absolute PCA/minimum-area-rectangle difference: 0.089691 px
- Maximum absolute PCA/minimum-area-rectangle difference: 0.213563 px

## Centroid-Location Analysis

Mean group centroids:

- Angle 0: (816.301, 680.483) px
- Nominal angle 30: (772.183, 718.593) px
- Nominal angle 45: (754.074, 641.576) px
- Nominal angle 60: (739.612, 598.993) px
- Nominal angle 90: (773.380, 627.163) px

Observed group-centroid ranges:

- X range: 76.690 px
- Y range: 119.599 px

The location change was too large to treat this as an orientation-only
experiment.

## Visual Diagnostic Review

All 15 overlays were reviewed.

The review confirmed:

- the measurement axis followed the case longitudinal axis;
- both endpoint markers contacted the physical ends;
- no endpoint marker selected a sidewall corner;
- the full silhouette was retained;
- the Lexan locator was excluded;
- no case contacted the image boundary.

Visual diagnostic result: **15 of 15 passed**

## Interpretation

The algorithm demonstrated reliable detection across substantial changes in
both orientation and image location. Within each fixed placement, measurement
variation remained low.

However, the observed differences between orientation-group means cannot be
attributed to orientation alone because case centroid location also changed.
Potential contributors include orientation, lens distortion, position-dependent
pixel scale, endpoint segmentation, and minor seating differences.

This trial is therefore classified as an exploratory orientation-and-location
robustness result.

## Next Experiment

Conduct a controlled-orientation trial using a fixed center target. Require the
detected case centroid to remain within approximately plus or minus 5 pixels of
the target in both image axes before accepting each orientation.
