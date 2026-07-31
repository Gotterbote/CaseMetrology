# Fixtureless Real-Image OAL Trial 02

## Status

Exploratory 10-cycle repositioning result. Not yet an accepted dimensional
metrology or repeatability result.

## Date

2026-07-31

## Configuration

- Platform: NVIDIA Jetson Orin Nano
- Camera resolution: 1456 x 1088
- Reported frame rate: 44.00 fps
- Illumination: backlight
- Lexan locator retained
- Gauge block removed
- V-block not used
- Same straight-wall unheaded case used for all cycles
- Case position and angle varied between cycles
- Both case endpoints remained visible
- Camera and lighting remained unchanged

## Source Evidence

- Blank references: 1
- Repositioned case captures: 10
- Session metadata files: 1
- Source-evidence manifest entries: 12

## Detection Results

- Cycles analyzed: 10
- Successful measurements: 10
- Failed measurements: 0
- Border-contact failures: 0

## Pixel-Length Results

- Mean PCA length: 522.745150 px
- Sample standard deviation: 1.339887 px
- Minimum PCA length: 520.283151 px
- Maximum PCA length: 524.234310 px
- Range: 3.951159 px
- Coefficient of variation: 0.256317%

## Independent Geometric Comparison

- Mean minimum-area-rectangle length: 522.599188 px
- Mean absolute PCA/rectangle difference: 0.212080 px
- Maximum absolute PCA/rectangle difference: 0.541964 px

## Visual Diagnostic Review

All 10 diagnostic overlays were reviewed.

Visual review confirmed:

- the measurement line followed the case longitudinal axis;
- one endpoint marker contacted each physical end;
- no endpoint marker incorrectly selected a sidewall corner;
- the Lexan locator was excluded from the measured silhouette;
- the full case silhouette was retained;
- no case contacted the image boundary.

Visual detection outcome: **10 of 10 passed**

## Focused Endpoint Comparison

Cycles 01, 04, 06, and 09 were compared at a common pixel scale.

Observed normalized mask widths:

- Cycle 01: 521 px
- Cycle 04: 526 px
- Cycle 06: 521 px
- Cycle 09: 523 px

The masks remained visually complete, but Cycle 04 retained a larger
longitudinal foreground extent than the shorter cycles.

## Interpretation

Fixtureless imaging produced reliable case isolation and visually correct
endpoint placement in all 10 cycles.

The observed 3.951-pixel range cannot yet be attributed to one factor because
case angle and image location were changed together. Possible contributors
include segmentation-boundary variation, position-dependent image scale, lens
distortion, orientation effects, and small seating or rolling differences.

Trial 02 is therefore classified as a successful exploratory detection trial,
not an accepted repeatability result.

## Next Experiment

Capture 10 consecutive images without touching or repositioning the case. This
static sequence will estimate capture and segmentation variation independently
of placement, orientation, and seating effects.
