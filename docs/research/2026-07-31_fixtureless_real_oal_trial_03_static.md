# Fixtureless Real-Image OAL Trial 03 — Static Repeatability

## Status

Accepted exploratory static-repeatability baseline. This is not yet an accepted
dimensional-accuracy result.

## Date

2026-07-31

## Objective

Estimate capture and segmentation variation while holding part position,
orientation, seating, camera configuration, lighting, and locator position
constant.

## Configuration

- Platform: NVIDIA Jetson Orin Nano
- Camera resolution: 1456 x 1088
- Reported frame rate: 44.00 fps
- Illumination: backlight
- Lexan locator retained
- V-block not used
- Same straight-wall unheaded case used throughout
- Case remained untouched during all 10 captures
- Trial 02 blank reference was reused because camera, lighting, and locator
  configuration remained unchanged

## Source Evidence

- Blank-reference images: 1
- Static case captures: 10
- Source-manifest entries: 11

## Numerical Results

- Cycles analyzed: 10
- Mean PCA length: 523.620541 px
- Sample standard deviation: 0.050349 px
- Minimum PCA length: 523.544327 px
- Maximum PCA length: 523.710908 px
- Range: 0.166581 px
- Coefficient of variation: 0.009616%
- Mean Otsu threshold: 107.400000
- Otsu threshold range: 1.000000
- Mean component area: 89,906.300 px
- Component-area range: 184 px

## Visual Diagnostic Review

All 10 overlays were reviewed.

The review confirmed:

- the measurement axis remained centered along the case;
- one endpoint marker contacted each physical end;
- endpoint placement was visually consistent across all captures;
- no marker incorrectly selected a sidewall corner;
- no visible rolling or movement occurred;
- the Lexan locator was excluded from the measured silhouette;
- the case remained clear of the image boundaries.

Visual diagnostic result: **10 of 10 passed**

## Interpretation

The fixtureless imaging and segmentation pipeline demonstrated excellent
frame-to-frame stability when the part remained stationary.

Compared with the Trial 02 repositioning sequence, Trial 03 produced
substantially lower variation. This indicates that ordinary capture and
thresholding noise accounts for only a small portion of the repositioning
variation observed in Trial 02.

Trial 03 does not establish dimensional accuracy, calibration validity,
repositioning repeatability, or reproducibility.

## Next Experiment

Separate image-location effects from orientation effects through controlled
experiments in which only one factor is changed at a time.
