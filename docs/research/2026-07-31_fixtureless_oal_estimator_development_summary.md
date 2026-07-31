---
title: Fixtureless OAL Estimator Development Summary
project: CaseMetrology
researcher: Timmy Bell
date: 2026-07-31
status: Living research summary
research_classification: Mixed accepted baseline and exploratory algorithm development
---

# Fixtureless OAL Estimator Development Summary

## 1. Purpose

This document consolidates the fixtureless top-down overall-length (OAL) estimator work performed after repository commit `cb3bf01`. It records the research question, experimental controls, software changes, numerical outcomes, visual-diagnostic findings, invalid intermediate runs, methodological decisions, limitations, and next planned work.

The purpose of this work was not merely to produce a lower numerical variance. The objective was to determine whether a measurement estimator based on fitted physical geometry could reduce orientation-dependent OAL error while preserving or improving static repeatability.

## 2. Research questions

**RQ1 — Static repeatability:** When the case and imaging conditions remain unchanged, does the candidate estimator reduce capture-to-capture OAL variation relative to the existing PCA-plus-extreme-mask-pixel estimator?

**RQ2 — Orientation invariance:** When case centroid is controlled and orientation changes, does the candidate estimator reduce the range among orientation-group median OAL values?

**RQ3 — Physical consistency:** Do fitted sidewalls and end faces correspond visually to the intended physical case boundaries, and do diagnostic residuals provide credible evidence of fit quality?

## 3. Working hypotheses

- **H1:** Replacing extreme mask pixels with fitted end faces will reduce sensitivity to isolated endpoint pixels and improve static repeatability.
- **H2:** Deriving the longitudinal axis from fitted straight sidewalls will reduce orientation-dependent OAL variation.
- **H3:** Grayscale subpixel edge localization will reduce rasterization bias remaining in binary-mask geometry.

These hypotheses were evaluated descriptively using existing real images. No formal inferential hypothesis test was performed.

## 4. Existing evidence used

### 4.1 Trial 03 — static condition

- Data directory: `data/oal_real/2026-07-31_trial_03_static/`
- Captures: 10
- Condition: case remained static across repeated captures
- Existing PCA-estimator standard deviation: `0.050349452 px`
- Existing PCA-estimator range: `0.166581476 px`

### 4.2 Trial 05 — controlled orientation

- Data directory: `data/oal_real/2026-07-31_trial_05_controlled_orientation/`
- Accepted captures: 17
- Orientation groups: 0°, 20°, 40°, 70°, and 90°
- Group sizes: 3, 3, 3, 3, and 5 captures, respectively
- Placement control: accepted case centroid within ±5 pixels of the target
- Existing PCA-estimator range among orientation-group medians: `1.752720470 px`
- A transient 90° endpoint-segmentation anomaly was retained and flagged in the Trial 05 record rather than silently discarded. The estimator comparisons retained all accepted captures and did not automatically exclude the designated 90° sensitivity candidate.

## 5. Comparative design and controls

The comparison was paired by capture. Each estimator processed the same previously accepted object mask; the grayscale estimator additionally used the corresponding original source image.

Controls applied:

1. No new physical data were collected.
2. Accepted Trial 03 and Trial 05 masks were reused without resegmentation.
3. The fixture-width validation gate was disabled only for these endpoint-estimator comparisons because object acceptance had already occurred upstream.
4. All estimators were evaluated on the same 27 accepted capture records.
5. The repository was clean before each valid analysis run, and the source Git commit was written into the generated summary.
6. Failed and flagged captures were retained in generated records; no favorable-case filtering was permitted.

This design isolates estimator behavior from segmentation and physical reacquisition variability. It does not establish absolute dimensional accuracy because no independent calibrated OAL ground-truth value was introduced in these comparisons.

## 6. Estimators evaluated

### 6.1 Baseline: PCA plus extreme mask pixels

Implementation: `src/measurement/topdown_oal.py`

The baseline identifies the largest connected component, uses PCA to establish a longitudinal axis, refines that axis from exposed case pixels, and defines OAL as the distance between the minimum and maximum mask projections along the refined axis.

Status: **Working baseline**. It is not considered fully orientation invariant, but it remained the best-performing method among the three evaluated methods for Trial 05 orientation-group median range.

### 6.2 Binary geometry estimator

Implementation: `src/measurement/topdown_oal_geometry.py`

Method:

1. Use PCA only to initialize a local coordinate frame.
2. Extract opposite case sidewall profiles from the accepted binary mask.
3. Fit sidewalls using deterministic Huber iteratively reweighted least squares.
4. Derive a center axis from the fitted sidewalls.
5. Fit both physical end faces from central boundary regions.
6. Intersect the fitted end lines with the center axis.
7. Calculate OAL as the axial distance between those intersections.

Relevant commits:

- `8bb3a9f` — Add geometry-based fixtureless OAL estimator
- `1ee63b0` — Fix accepted-mask OAL estimator comparison
- `e690127` — Document exploratory geometry OAL comparison

Status: **Exploratory; not accepted as the final estimator.**

### 6.3 Grayscale subpixel geometry estimator

Implementation: `src/measurement/topdown_oal_subpixel.py`

Method:

1. Initialize from accepted-mask binary geometry.
2. Sample grayscale profiles normal to candidate sidewalls and end faces.
3. Search ±5 pixels around each seed point at 0.20-pixel profile spacing.
4. Smooth each profile with a 0.65-pixel Gaussian scale.
5. Select the largest absolute local gradient satisfying minimum contrast and gradient thresholds.
6. Refine the gradient peak by local quadratic interpolation.
7. Robustly fit sidewall and end-face lines to the resulting subpixel points.
8. Calculate axial distance between the fitted subpixel end lines.

Relevant commit:

- `4dca7b1` — Add grayscale subpixel fixtureless OAL estimator

Status: **Exploratory; not accepted as the final estimator.**

## 7. Numerical results

All standard deviations below are sample standard deviations as generated by Python `statistics.stdev`.

### 7.1 Trial 03 static results

| Estimator | n | Mean (px) | Median (px) | SD (px) | Range (px) |
|---|---:|---:|---:|---:|---:|
| PCA/extreme pixels | 10 | 523.620541427 | 523.634306987 | 0.050349452 | 0.166581476 |
| Binary geometry | 10 | 521.484317165 | 521.486601736 | 0.025909506 | 0.079070832 |
| Grayscale subpixel | 10 | 524.368289779 | 524.361210078 | 0.048944639 | 0.167674518 |

Relative to the baseline:

- Binary geometry reduced static SD by **48.54%** and static range by **52.53%**.
- Grayscale subpixel reduced static SD by **2.79%**, while static range increased by **0.66%**.

### 7.2 Trial 05 controlled-orientation results

| Estimator | n | Mean (px) | Median (px) | SD (px) | Full range (px) | Range among orientation-group medians (px) |
|---|---:|---:|---:|---:|---:|---:|
| PCA/extreme pixels | 17 | 522.829559788 | 522.847915488 | 0.641592996 | 2.183819347 | 1.752720470 |
| Binary geometry | 17 | 520.684302365 | 520.597564662 | 0.779168884 | 2.273582168 | 2.249772382 |
| Grayscale subpixel | 17 | 523.047813948 | 522.697188013 | 1.087746685 | 2.983334128 | 2.887565849 |

Relative to the baseline:

- Binary geometry increased Trial 05 SD by **21.44%** and increased the orientation-group median range by **28.36%**.
- Grayscale subpixel increased Trial 05 SD by **69.54%** and increased the orientation-group median range by **64.75%**.

### 7.3 Orientation-group medians

| Orientation group | PCA (px) | Binary geometry (px) | Grayscale subpixel (px) |
|---|---:|---:|---:|
| 0° | 523.069153912 | 520.811661820 | 522.820548002 |
| 20° | 522.776434595 | 520.585730039 | 522.460664933 |
| 40° | 522.782483310 | 520.443237463 | 522.695701897 |
| 70° | 521.612035008 | 519.358508326 | 521.703440701 |
| 90° retake | 523.364755478 | 521.608280708 | 524.591006550 |

The grayscale candidate exhibited a pronounced positive 90° shift and a lower 70° result, producing the largest orientation-dependent spread of the three methods.

## 8. Visual diagnostic review

The detailed review is recorded in `docs/research/2026-07-31_oal_estimator_visual_review_record.md`.

Summary:

- Trial 03 overlays for both fitted-geometry methods showed stable sidewalls, end lines, and center axes without an obvious gross fit failure.
- Trial 05 binary-geometry overlays were generally plausible, although the 70° group showed the largest visible separation between the original PCA axis and fitted-geometry axis.
- Trial 05 subpixel overlays were visually plausible at contact-sheet scale, but the selected grayscale boundary appeared to shift among different portions of the optical edge-spread profile across orientation.
- The source images contain a physical silhouette boundary, a backlight transition, gray haloing, and case-surface reflections. Selecting the largest absolute gradient does not guarantee selection of the same physical edge at every orientation.

## 9. Invalid and superseded intermediate analysis runs

The following runs are procedural records and must not be treated as research results:

1. **Aborted binary comparison:** the summary attempted to calculate a median for an empty orientation group and raised `statistics.StatisticsError`. Partial output was incomplete.
2. **Invalid 27-failure comparison:** the accepted-mask comparison incorrectly retained the fixture-width validation gate, causing all 27 records to fail before endpoint estimation. The output was deleted and regenerated after the gate was explicitly disabled for this comparison scope.
3. **Formatting-hook interruption:** one attempted comparison-script commit was blocked by Black formatting. The estimator tests passed, but the code change was not committed until formatting was corrected.

These events did not alter source images or accepted masks. Valid comparisons were rerun from clean repository states after correction.

## 10. Interpretation

### 10.1 Hypothesis outcomes

- **H1 supported for binary geometry:** fitted end geometry substantially improved static repeatability.
- **H2 not supported:** binary sidewall/end-line fitting increased orientation dependence.
- **H3 not supported in its first implementation:** maximum-gradient subpixel localization further increased orientation dependence.

### 10.2 Current scientific interpretation

The data indicate that isolated extreme pixels contribute to static variation, but they are not the sole cause of orientation-dependent error. Binary fitted geometry remains affected by rasterized boundary structure. The first grayscale subpixel method did not solve this issue because it selected the strongest local gradient without enforcing a common physical edge definition. At different orientations, the strongest gradient can correspond to different lobes of the optical transition, halo, or reflection pattern.

The results demonstrate a distinction central to metrology: increased numerical precision or subpixel resolution does not establish improved measurement accuracy or invariance unless the measured feature is physically and operationally defined consistently.

## 11. Current decision

The PCA-plus-extreme-mask-pixel estimator remains the **provisional working baseline** because it produced the smallest Trial 05 range among orientation-group medians (`1.752720470 px`).

Neither candidate is accepted as the final OAL estimator:

- Binary geometry: **Exploratory**
- Maximum-gradient grayscale subpixel geometry: **Exploratory**

This decision does not imply that the PCA estimator is adequate for final deployment. It is the comparator retained while a more physically constrained edge method is developed.

## 12. Limitations

1. The comparisons assess repeatability and orientation sensitivity in pixels, not absolute dimensional accuracy.
2. Trial 03 contains only 10 repeated captures of one static condition.
3. Trial 05 contains 17 captures across five orientation groups with unequal group sizes.
4. Repeated captures are not statistically independent physical specimens.
5. No inferential model was fitted; results are descriptive.
6. The same case, imaging plane, optics, and backlight environment limit generalizability.
7. Visual review was primarily contact-sheet based; individual full-resolution overlays should be rechecked before final thesis figures are selected.
8. Diagnostic thresholds flagged all 27 candidate measurements and therefore were not selective enough for automated acceptance decisions.
9. Lens distortion, image-plane scale variation, camera non-orthogonality, and fixture/part height effects have not yet been isolated in this estimator comparison.

## 13. Next planned method

Develop a **mask-anchored, polarity-aware normalized intensity-crossing estimator**:

1. Anchor each profile to the accepted-mask boundary.
2. determine case-interior and illuminated-background directions.
3. Estimate local interior and exterior intensity plateaus.
4. Normalize the profile between those plateaus.
5. Locate a consistent physical crossing, initially the 50% intensity transition.
6. Reject profiles with insufficient contrast, multiple transitions, inconsistent polarity, or excessive distance from the mask boundary.
7. Fit sidewalls and end faces from the accepted crossing points.
8. Compare against the same 27 records before collecting new physical data.

If orientation dependence persists after a consistent edge definition is enforced, the investigation should advance to image-plane scale mapping, lens-distortion correction, and camera-to-measurement-plane alignment.

## 14. Thesis-use guidance

The candidate comparisons are suitable for a methodology-development or limitations section because they document controlled negative results and show why the final method was selected. They must not be presented as proof of dimensional accuracy. Any thesis claim should distinguish:

- static repeatability,
- orientation invariance,
- agreement with manual or calibrated ground truth,
- and absolute measurement uncertainty.

## 15. Related records

- `docs/research/2026-07-31_binary_geometry_oal_estimator_review.md`
- `docs/research/2026-07-31_grayscale_subpixel_oal_estimator_review.md`
- `docs/research/2026-07-31_oal_estimator_visual_review_record.md`
- `docs/research/oal_method_decision_log.md`
- `docs/research/oal_evidence_index.md`
