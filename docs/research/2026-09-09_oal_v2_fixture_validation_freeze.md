# OAL V2 Formal Validation — Revised Fixture Freeze

## Purpose

This record prospectively freezes the configuration and execution basis for the second formal OAL computer-vision validation study (V2).

V1 formal validation is complete and immutable at Git tag:

`v1-oal-formal-validation-final`

V2 is intended to evaluate whether mechanically registered specimen placement reduces the placement-dependent measurement variability observed during V1.

## Intentional V2 System Change

The sole intentional system change from V1 is specimen mechanical registration.

The revised fixture consists of:

- Fixture 1: 90-degree mouth stop plate constrained by the fixture frame rails.
- Fixture 2: rebuilt U-shaped lateral locator.
- Base Lexan: unchanged and retained as the specimen support and measurement plane.

Fixture 2 was shortened approximately 0.505 in on the left side and its groove was rebuilt narrower, then hand-fit until specimens rested on the base Lexan and moved freely without binding.

No additional fixture development or adjustment is planned after this freeze unless a documented pre-run verification demonstrates that the system cannot be operated as frozen.

## Frozen Imaging and Measurement System

The following remain unchanged from V1:

- Arducam USB 3.0 IMX296 global-shutter camera.
- 16 mm lens used during V1.
- Camera mounting and imaging geometry.
- Backlight configuration.
- Base Lexan measurement plane.
- Frozen camera controls.
- Frozen calibration.
- Frozen segmentation pipeline.
- Frozen PCA/extreme-mask OAL estimator.
- Frozen measurement software and analysis definitions.

No post-hoc estimator, calibration, segmentation, exposure, or measurement tuning will be performed using V2 formal results.

## Specimen Population

The same 60 retained formal-validation specimens used during V1 will be used during V2.

The accepted V1 manual-reference measurements remain the reference measurements for V2. Manual measurements will not be repeated solely because the fixture changed.

Development specimens and post-V1 diagnostic observations are not part of the V2 formal dataset.

## Formal Acquisition Structure

V2 will consist of:

- 60 retained formal-validation specimens.
- 3 independent CV placements per specimen.
- 180 formal V2 CV observations total.
- Separate randomized specimen order for each of the three rounds.

For each formal observation, the specimen will be fully removed from the fixture and independently reseated before image acquisition.

A placement is acceptable when the specimen:

1. rests on the base Lexan,
2. is seated against the Fixture 1 mouth stop, and
3. occupies its natural mechanically constrained position within Fixture 2 without obstruction or binding.

A specimen will not be reseated or remeasured because the reported OAL value appears unexpected.

Obvious acquisition or physical-placement failures may be marked invalid, but the original attempt will be preserved in the study record.

## Analysis Basis

V2 will be evaluated using the same core analysis definitions used for V1, including:

- CV availability,
- mean bias,
- 95% confidence interval for bias,
- median signed error,
- mean absolute error,
- RMSE,
- P95 absolute error,
- maximum absolute error,
- false-pass and false-fail classifications,
- specimen-level repeatability,
- independent-placement P95 pairwise OAL difference.

A paired V1-versus-V2 comparison will also be performed using the same retained 60 specimens.

Post-V1 development results justify proceeding with the revised fixture but do not establish V2 acceptance thresholds.

## Freeze Statement

Effective with this record, the revised mechanical fixture and the inherited V1 imaging, calibration, estimator, and software configuration are frozen for formal V2 validation.

Any required departure from this configuration must occur before formal V2 acquisition or be documented as a protocol deviation.

No formal V2 specimen image has been intentionally collected under this freeze at the time of its creation.
