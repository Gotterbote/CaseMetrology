# Formal OAL Calibration Analysis and Disposition

**Date:** 2026-08-07
**Project:** CaseMetrology
**Purpose:** Formal calibration characterization supporting fixtureless computer-vision overall-length (OAL) validation.

## 1. Calibration Objective

The purpose of this experiment was to characterize conversion from image-space
measurements to physical dimensions at the actual OAL measurement plane.

The calibration study was designed to determine whether a single global
pixels-per-inch (PPI) value was sufficient or whether effective image scale
varied with image position and measurement direction.

This calibration work supports the primary thesis objective of evaluating
computer-vision OAL metrology relative to manual dimensional inspection. It is
not intended as a standalone optical-calibration study.

## 2. Physical Reference

Certified gauge-block reference dimension:

- Nominal/reference dimension used: 1.0000024 in
- Gauge block: Mitutoyo Grade 0
- The certified short dimension of the rectangular gauge block was used as the
  dimensional reference.
- The permanent clear Lexan measurement/locator surface remained installed
  throughout the formal calibration experiment.

## 3. Calibration Analyzer

Orientation-independent gauge-block analysis:

- Source:
  `src/calibration/oriented_gauge_block.py`
- Git commit:
  `ee173852d98ec20c16bf9e64a3b163c131173537`
- Analyzer SHA256:
  `987ef699c5d1abec52200ada7508ad994977b51a5d1c37b57ee3e3bc20b04b56`

The analyzer measures the certified short dimension using orientation-aware
gauge-block geometry and edge refinement.

## 4. Acquisition Provenance

All accepted formal calibration and holdout sessions were acquired at the same
committed software state:

- Git commit:
  `ee173852d98ec20c16bf9e64a3b163c131173537`
- Git working tree dirty: False

Camera acquisition conditions were invariant across all accepted sessions:

- Device: `/dev/case-metrology-camera`
- Resolution: 1456 x 1088
- Pixel format: YUYV
- Frame rate: 44 fps
- Warmup frames: 20
- Brightness: 0
- Contrast: 10
- Saturation: 0
- Automatic white balance: 0
- Gain: 100
- White-balance temperature: 2498
- Auto exposure control value: 1
- Exposure time absolute: 5

For every accepted session, the camera controls recorded before acquisition,
after acquisition, and as expected controls agreed.

## 5. Coordinate-Controlled Calibration Design

A coordinate-controlled 2 x 2 spatial calibration grid was collected using
two principal gauge-block orientations.

Approximate calibration locations:

| Position | Target X (px) | Target Y (px) |
|---|---:|---:|
| A | 750 | 600 |
| B | 750 | 700 |
| C | 850 | 600 |
| D | 850 | 700 |

Three images were acquired at each position/orientation combination.

An independent holdout location E near the center of the grid was not used to
fit the spatial calibration models.

Approximate E target:

- X = 804 px
- Y = 651 px

Five repeated images were acquired for each E holdout condition.

## 6. Accepted Calibration Sessions

### Position A

0-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_a_000_20260807_163033`

- Mean centroid: (753.181, 596.371) px
- Mean PPI: 523.728895305
- PPI SD: 0.009208398
- PPI range: 0.016641827

90-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_a_090_20260807_163450`

- Mean centroid: (753.780, 601.488) px
- Mean PPI: 523.459985755
- PPI SD: 0.021142870
- PPI range: 0.038846272

### Position B

0-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_b_000_20260807_163854`

- Mean centroid: (753.913, 706.993) px
- Mean PPI: 523.860622494
- PPI SD: 0.001349903
- PPI range: 0.002677309

90-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_b_090_20260807_164208`

- Mean centroid: (750.356, 704.153) px
- Mean PPI: 523.988899389
- PPI SD: 0.014909396
- PPI range: 0.029792508

### Position C

0-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_c_000_20260807_164547`

- Mean centroid: (856.467, 596.373) px
- Mean PPI: 524.635595844
- PPI SD: 0.017136548
- PPI range: 0.029800547

Accepted 90-degree retake:

`raw_images/oal_calibration_formal/formal_oal_calibration_c_090_retake_20260807_165646`

- Mean centroid: (855.659, 600.005) px
- Mean PPI: 523.868900491
- PPI SD: 0.008743300
- PPI range: 0.016008825

The initial C/90 session was retained for provenance but superseded because its
centroid did not match the C/0 location as tightly as desired. The retake used
the measured C/0 centroid as the positioning target.

### Position D

0-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_d_000_20260807_165951`

- Mean centroid: (853.175, 699.881) px
- Mean PPI: 524.654775732
- PPI SD: 0.005770546
- PPI range: 0.011392849

90-degree session:

`raw_images/oal_calibration_formal/formal_oal_calibration_d_090_20260807_170159`

- Mean centroid: (854.002, 700.990) px
- Mean PPI: 524.223797936
- PPI SD: 0.010289987
- PPI range: 0.018685874

## 7. Principal-Direction Calibration Results

The accepted A-D results demonstrate that effective scale varies with both
image position and gauge-block orientation.

| Position | 0 deg PPI | 90 deg PPI | 90 deg - 0 deg |
|---|---:|---:|---:|
| A | 523.728895 | 523.459986 | -0.268910 |
| B | 523.860622 | 523.988899 | +0.128277 |
| C | 524.635596 | 523.868900 | -0.766695 |
| D | 524.654776 | 524.223798 | -0.430978 |

These observations reject the assumption that one global scalar PPI fully
describes the usable measurement region.

They also show that the orientation effect is not a constant offset because
the magnitude and sign vary with image position.

## 8. Spatial Calibration Models

Separate first-order spatial planes were fit using only the A-D calibration
data.

For the 0-degree gauge-block condition:

`PPI_0(x,y) = 516.907045 + 0.00843326411*x + 0.000817091863*y`

For the 90-degree gauge-block condition:

`PPI_90(x,y) = 518.408825 + 0.00322556849*x + 0.00442714650*y`

The models are empirical calibration descriptions over the tested region only
and should not be extrapolated beyond the validated measurement area.

## 9. Independent Holdout E

Position E was withheld from calibration-model fitting.

### E / 0 degrees

Session:

`raw_images/oal_calibration_formal/formal_oal_calibration_e_000_holdout_20260807_171113`

Results:

- Mean centroid: (802.885, 647.184) px
- Mean measured PPI: 523.948557937
- PPI SD: 0.004777908
- PPI range: 0.011656626
- A-D model prediction at measured centroid: 524.206794635 PPI
- PPI residual, measured minus predicted: -0.258236698 PPI
- Equivalent dimensional residual over the certified approximately 1-inch
  reference: approximately -0.000493 in

### E / 90 degrees

Session:

`raw_images/oal_calibration_formal/formal_oal_calibration_e_090_holdout_20260807_171837`

Results:

- Mean centroid: (803.974, 645.506) px
- Mean measured PPI: 523.757494803
- PPI SD: 0.005241046
- PPI range: 0.012068046
- A-D model prediction at measured centroid: 523.859848277 PPI
- PPI residual, measured minus predicted: -0.102353474 PPI
- Equivalent dimensional residual over the certified approximately 1-inch
  reference: approximately -0.000195 in

Both principal-orientation holdouts were therefore within 0.0005 in of the
A-D model prediction over the approximately 1-inch certified reference.

## 10. Independent Oblique Holdout

The permanent fixture and available field of view prevented the certified
rectangular gauge block from being positioned at large oblique angles such as
20 or 45 degrees at the desired measurement location.

Approximately 10 degrees was physically achievable without removing the
fixture or clipping the reference.

The final oblique holdout session was:

`raw_images/oal_calibration_formal/formal_oal_calibration_e_010_holdout_20260807_173514`

Results:

- Mean centroid: (805.737, 642.145) px
- Mean reported long-axis angle: 11.361394 degrees
- Angle SD: 0.001829 degrees
- Mean measured PPI: 523.649096602
- PPI SD: 0.011170129
- PPI range: 0.030705456

Using the A-D principal-direction spatial models and resolving the calibrated
image scale for the measured oblique orientation produced an expected
effective PPI of approximately:

524.212139 PPI

Observed minus expected:

-0.563043 PPI

The equivalent dimensional residual over the approximately 1-inch reference
was approximately:

-0.001074 in

The oblique holdout therefore revealed a small residual orientation-dependent
error not fully represented by the two first-order principal-direction spatial
models.

## 11. Superseded and Excluded Sessions

The following sessions are retained for complete provenance but are not used
to fit or validate the final calibration characterization.

### Earlier subjective-position sessions

- `formal_oal_calibration_center_000_static_20260807_160240`
- `formal_oal_calibration_center_090_static_20260807_160422`
- `formal_oal_calibration_down_000_static_20260807_161744`
- `formal_oal_calibration_down_090_static_retake_20260807_162211`

These sessions were superseded after centroid analysis demonstrated that
subjective "center" and "down" placement did not provide matched image
coordinates between orientations.

### Accidental capture

- `formal_oal_calibration_down_090_static_20260807_161909`

This acquisition occurred before the intended physical repositioning/rotation
was performed and is excluded from analysis.

### Initial C / 90-degree capture

- `formal_oal_calibration_c_090_20260807_165052`

This session met the original target-window criterion but was superseded by a
tighter coordinate-matched retake after spatial scale variation became
apparent.

No raw data were deleted.

## 12. Interpretation

The formal calibration experiment produced four primary findings.

1. Calibration measurement repeatability was high under locked acquisition
   conditions.

2. Effective PPI varies measurably across the usable image region.

3. Effective PPI also varies with measurement direction, and the directional
   difference itself varies spatially.

4. A simple position-aware principal-direction model predicted independent
   0-degree and 90-degree holdouts to substantially better than 0.001 in over
   the approximately 1-inch reference, but the approximately 11-degree
   oblique holdout retained an approximately 0.00107-in dimensional residual.

Accordingly, the system should not be represented as having demonstrated
universal sub-0.001-inch calibration accuracy at arbitrary orientation.

The observed calibration error remains small relative to the approximately
+/-0.010-in OAL tolerance relevant to the present thesis application.

## 13. Calibration Disposition

Calibration data collection is complete for the thesis OAL validation phase.

Disposition:

- A-D are accepted as calibration-development/model data.
- E/0 and E/90 are accepted as independent principal-direction holdouts.
- E/~11.36 degrees is accepted as an independent oblique-orientation holdout.
- The permanent fixture remains part of the measurement system.
- The physical inability to place the certified rectangular reference at
  larger oblique angles is recorded as a calibration limitation.
- No additional calibration tuning will be performed against the holdout data.
- The frozen OAL geometry estimator will not be modified based on these
  calibration results.
- Subsequent end-to-end accuracy evaluation will be performed using actual
  case specimens and the independent manual reference measurement system.

The calibration characterization is considered sufficient to proceed with
the planned thesis OAL validation study while explicitly retaining the
observed spatial and orientation-dependent calibration uncertainty as a study
limitation.
