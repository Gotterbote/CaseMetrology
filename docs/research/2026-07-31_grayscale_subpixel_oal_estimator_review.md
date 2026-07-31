---
title: Grayscale Subpixel Fixtureless OAL Estimator Review
project: CaseMetrology
researcher: Timmy Bell
date: 2026-07-31
status: Completed exploratory review; evidence commit pending at time of preparation
research_classification: Exploratory; not accepted as final estimator
---

# Grayscale Subpixel Fixtureless OAL Estimator Review

## 1. Objective

Determine whether fitting case sidewalls and end faces to subpixel grayscale edge locations reduces the orientation dependence observed when geometry is fitted to integer-valued binary-mask boundaries.

## 2. Rationale

The binary-geometry estimator reduced static variation but increased the range among Trial 05 orientation-group medians. The initial interpretation was that mask rasterization and diagonal pixel staircasing could bias fitted lines. The grayscale candidate therefore searched the original image for subpixel edge locations while using accepted masks only for object association and geometric initialization.

## 3. Implementation

Primary implementation:

- `src/measurement/topdown_oal_subpixel.py`
- `src/diagnostics/topdown_oal_subpixel_overlay.py`
- `scripts/compare_oal_subpixel_estimators.py`
- `tests/test_topdown_oal_subpixel.py`

Default profile parameters:

| Parameter | Value |
|---|---:|
| Search radius | ±5.0 px |
| Profile step | 0.20 px |
| Gaussian profile sigma | 0.65 px |
| Minimum contrast | 12 intensity units |
| Minimum gradient | 3 intensity units/px |
| Sidewall samples | 72 per segment |
| End-face samples | 41 per end |
| Minimum accepted-profile fraction | 0.65 |
| End-face transverse fraction | 0.30 |

Algorithm sequence:

1. Convert the original source image to grayscale.
2. Initialize sidewall, end-face, and axis geometry from the accepted binary mask.
3. Sample bilinearly interpolated profiles normal to each candidate edge.
4. Smooth each profile.
5. Identify the largest absolute gradient within the search interval.
6. Refine the gradient peak by quadratic interpolation.
7. Reject profiles below contrast or gradient thresholds.
8. Robustly fit subpixel sidewall and end-face points.
9. Calculate OAL from the two end-line intersections with the fitted center axis.

## 4. Software validation and provenance

- Full repository test suite after installation: 29 passed.
- Ruff lint checks: passed.
- Implementation commit: `4dca7b1` — Add grayscale subpixel fixtureless OAL estimator.
- The valid comparison began from clean Git status at full commit `4dca7b1e39c5ed67c008eef430d9bc64eb2a4f50`.
- At the time this review document was prepared, the generated comparison directory remained uncommitted and should be committed with this documentation after researcher review.

## 5. Data and comparison design

- 27 accepted image/mask pairs: 10 Trial 03 and 17 Trial 05.
- Original grayscale source images used.
- Accepted masks reused without resegmentation.
- Baseline, binary geometry, and subpixel methods compared on the same capture records.
- Fixture-width validation gate disabled for the endpoint-only comparison.
- No new physical data collected.
- Output directory: `data/oal_real/2026-07-31_subpixel_estimator_comparison/`

## 6. Results

### 6.1 Trial 03 static condition

| Statistic | PCA baseline (px) | Binary geometry (px) | Grayscale subpixel (px) |
|---|---:|---:|---:|
| Mean | 523.620541427 | 521.484317165 | 524.368289779 |
| Median | 523.634306987 | 521.486601736 | 524.361210078 |
| Sample SD | 0.050349452 | 0.025909506 | 0.048944639 |
| Range | 0.166581476 | 0.079070832 | 0.167674518 |

Relative to PCA, the subpixel candidate reduced sample SD by only **2.79%**, while range increased by **0.66%**. Static performance was therefore approximately equivalent to the PCA baseline and worse than binary geometry.

### 6.2 Trial 05 controlled orientation

| Statistic | PCA baseline (px) | Binary geometry (px) | Grayscale subpixel (px) |
|---|---:|---:|---:|
| Mean | 522.829559788 | 520.684302365 | 523.047813948 |
| Median | 522.847915488 | 520.597564662 | 522.697188013 |
| Sample SD | 0.641592996 | 0.779168884 | 1.087746685 |
| Full range | 2.183819347 | 2.273582168 | 2.983334128 |
| Range among orientation-group medians | 1.752720470 | 2.249772382 | 2.887565849 |

Relative to PCA, the subpixel candidate increased sample SD by **69.54%** and increased the range among orientation-group medians by **64.75%**.

### 6.3 Orientation-group medians

| Orientation | PCA (px) | Binary geometry (px) | Grayscale subpixel (px) | Subpixel minus PCA (px) |
|---|---:|---:|---:|---:|
| 0° | 523.069153912 | 520.811661820 | 522.820548002 | −0.248605910 |
| 20° | 522.776434595 | 520.585730039 | 522.460664933 | −0.315769662 |
| 40° | 522.782483310 | 520.443237463 | 522.695701897 | −0.086781413 |
| 70° | 521.612035008 | 519.358508326 | 521.703440701 | +0.091405693 |
| 90° retake | 523.364755478 | 521.608280708 | 524.591006550 | +1.226251072 |

The 90° group exhibited a pronounced positive bias relative to the other orientations and relative to its PCA result.

## 7. Diagnostic and visual review

Generated evidence:

- `oal_subpixel_estimator_comparison_results.csv`
- `oal_subpixel_estimator_comparison_summary.txt`
- `trial_03_static_subpixel_comparison_contact_sheet.png`
- `trial_05_controlled_orientation_subpixel_comparison_contact_sheet.png`
- per-capture overlays
- SHA-256 manifest

Aggregate result:

- Failed triplets: 0
- Subpixel-flagged captures: 27

Visual observations:

1. Trial 03 center axes, sidewalls, and end lines appeared stable across repeated captures.
2. Trial 05 center-axis estimates were generally centered, making gross axis failure an unlikely sole explanation.
3. At 70° and 90°, fitted lines remained visually plausible at contact-sheet scale but appeared to follow different portions of the broad dark-to-light transition.
4. The source image contains more than one candidate edge feature: physical silhouette boundary, backlight transition, gray halo, and case-surface reflections.
5. The maximum-absolute-gradient rule can select different gradient lobes at different orientations while still producing a visually plausible overlay.
6. Because every candidate measurement carried a diagnostic flag, the present thresholds do not provide a selective automated quality gate.

## 8. Interpretation

The results do not support the hypothesis that generic maximum-gradient subpixel localization removes orientation dependence. The dominant issue is not simply integer-pixel quantization.

The estimator lacks an operational definition of which grayscale transition represents the physical measurement edge. Searching for the strongest local gradient allows the selected feature to change with orientation, illumination distribution, edge spread, halo, and reflection. Consequently, increased numerical resolution amplified an inconsistent feature definition rather than improving measurement validity.

This is a research-relevant negative result: **subpixel precision is not equivalent to metrological accuracy**.

## 9. Decision

**Status: Exploratory; not accepted as the final OAL estimator.**

The PCA-plus-extreme-mask-pixel method remains the provisional comparator because it retained the smallest Trial 05 orientation-group median range.

The generated subpixel evidence should be preserved and cited as algorithm-development evidence, but it should not be reported as an accepted final measurement method.

## 10. Limitations

- The method selected maximum gradient magnitude without explicit edge polarity.
- The search was not anchored to a normalized physical crossing between local interior and exterior plateaus.
- Multiple transitions within the ±5-pixel window were not explicitly rejected.
- The comparison used one case and one imaging setup.
- No calibrated absolute ground truth was available.
- Group sizes were small and unequal.
- All 27 captures were flagged, indicating that diagnostic thresholds require redesign rather than simple relaxation.

## 11. Required next revision

Develop a mask-anchored, polarity-aware normalized intensity-crossing estimator:

1. Locate the accepted-mask boundary nearest each seed.
2. Determine case-interior and illuminated-background directions.
3. Estimate robust local intensity plateaus on both sides.
4. Normalize the local edge-spread profile.
5. Measure a consistent crossing, initially 50% of the local contrast.
6. Reject inadequate contrast, multiple crossings, incorrect polarity, excessive boundary displacement, and unstable local profiles.
7. Retain profile-level diagnostics and per-line residuals.
8. Evaluate on the same 27 capture records before new physical acquisition.

If the revised edge definition does not reduce orientation dependence, the next controlled study should examine spatial calibration, lens distortion, telecentricity/perspective, and camera-to-object-plane alignment.
