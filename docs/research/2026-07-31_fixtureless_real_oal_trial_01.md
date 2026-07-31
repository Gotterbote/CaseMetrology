# Fixtureless Real-Image OAL Trial 01

## Status

Exploratory real-image detection result. Not yet an accepted dimensional
metrology result.

## Date

2026-07-31

## Hardware Configuration

- Compute platform: NVIDIA Jetson Orin Nano
- Camera resolution: 1456 x 1088
- Reported frame rate: 44.00 fps
- Illumination: backlight
- Lexan locator: retained in its established position
- Gauge block: removed
- V-block fixture: not used
- Test part: straight-wall unheaded case
- Part placement: on its side at a diagonal orientation
- Camera, lighting, and Lexan locator remained unchanged between blank and
  occupied captures.

## Source Images

- Blank reference:
  `data/oal_real/2026-07-31_trial_01/01_blank_lexan_reference.png`
- Part image:
  `data/oal_real/2026-07-31_trial_01/02_case_position_01.png`

## Source Image SHA-256

- Blank reference:
  `58831293d9f579a14be34483ae4ace2aad311a95e62579f763041e7a06a6ebcd`
- Part image:
  `2b49cfa2bb3192f7aac49d5cbb03ea3517f08812bab11a475c62451d835f13c3`

## Preliminary Segmentation Result

- Otsu threshold: 107.000
- Darkening mean: 13.367506
- Darkening maximum: 237
- Detected foreground pixels: 92,796
- Connected foreground components: 1
- Largest component bounding box:
  - x: 519
  - y: 345
  - width: 470 px
  - height: 493 px

## Exploratory OAL Detection Result

- Largest component pixels: 92,796
- PCA projected length: 523.802576 px
- Minimum-area rectangle long side: 523.795593 px
- Absolute difference between methods: 0.006983 px
- Detected axis angle: -47.305051 degrees
- Endpoint 1: (576.657, 785.296)
- Endpoint 2: (931.845, 400.315)

## Visual Diagnostic Review

The generated overlay was reviewed visually.

The review confirmed:

- the measurement line followed the case longitudinal axis;
- one endpoint marker contacted each physical end;
- neither endpoint marker incorrectly selected a sidewall corner;
- the complete case silhouette was retained;
- the Lexan locator was excluded from the foreground mask;
- no large segmentation holes or unrelated objects were present.

Visual diagnostic outcome: **Pass**

## Interpretation

The fixtureless configuration successfully isolated and measured the projected
pixel length of one real case image. The close agreement between the PCA
projected length and the minimum-area rectangle long side supports internal
geometric consistency for this image.

This result does not yet establish:

- dimensional accuracy in inches;
- calibration validity;
- repeatability across repeated placements;
- reproducibility;
- robustness across image locations and orientations;
- suitability for production inspection.

## Design Implication

Fixtureless top-down imaging appears viable for further testing. A V-block
should be introduced only if later trials demonstrate unacceptable rolling,
movement, or measurement-plane variation.

## Next Step

Capture the same part at multiple positions and orientations without changing
the camera, lighting, or Lexan locator. Evaluate detection success, pixel-length
variation, and endpoint placement before applying dimensional calibration.
