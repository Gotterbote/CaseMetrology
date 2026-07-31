---
title: Binary-Geometry Fixtureless OAL Estimator Review
project: CaseMetrology
researcher: Timmy Bell
date: 2026-07-31
status: Completed exploratory review
research_classification: Exploratory; not accepted as final estimator
---

# Binary-Geometry Fixtureless OAL Estimator Review

## 1. Objective

Evaluate whether fitting the physical case sidewalls and end faces to an accepted binary silhouette improves fixtureless top-down OAL repeatability and orientation invariance relative to the existing PCA-plus-extreme-mask-pixel estimator.

## 2. Rationale

The baseline estimator measures the distance between the minimum and maximum mask projections along a PCA-derived axis. A single isolated or rasterized endpoint pixel can therefore alter the measured length. The geometry candidate was designed to replace these extreme pixels with robustly fitted physical lines.

## 3. Implementation

Primary implementation:

- `src/measurement/topdown_oal_geometry.py`
- `src/diagnostics/topdown_oal_geometry_overlay.py`
- `scripts/compare_oal_estimators.py`
- `tests/test_topdown_oal_geometry.py`

Algorithm sequence:

1. Select the largest accepted connected component.
2. Use PCA only as an initial local coordinate system.
3. Construct axial width profiles from the binary mask.
4. Select straight case-wall regions while excluding wider fixture and end-transition regions.
5. Fit opposite sidewalls with deterministic Huber iteratively reweighted least squares.
6. Derive the longitudinal center axis from the fitted sidewalls.
7. Select central transverse portions of the minimum and maximum end faces.
8. Fit both end lines robustly.
9. Intersect each end line with the center axis.
10. Report axial intersection distance as OAL and retain residual, inlier, angle, and diagnostic information.

The existing PCA estimator was left unchanged and served as the comparator.

## 4. Software validation and provenance

- Initial geometry-specific synthetic tests: 8 passed.
- Full test suite after integration and comparison correction: 17 passed.
- Geometry implementation commit: `8bb3a9f`
- Valid accepted-mask comparison code commit: `1ee63b0`
- Exploratory comparison evidence commit: `e690127`

No source image, accepted mask, or prior trial result was overwritten.

## 5. Data and comparison design

- Trial 03: 10 static captures.
- Trial 05: 17 controlled-orientation captures.
- Same accepted masks used for baseline and candidate.
- No resegmentation and no new physical acquisition.
- Fixture-width validation gate disabled for the comparison because object acceptance was already established.
- Valid run began from clean Git status at commit `1ee63b0`.
- Output: `data/oal_real/2026-07-31_geometry_estimator_comparison/`

## 6. Results

### 6.1 Trial 03 static condition

| Statistic | PCA baseline (px) | Binary geometry (px) | Candidate change |
|---|---:|---:|---:|
| Mean | 523.620541427 | 521.484317165 | −2.136224262 px |
| Median | 523.634306987 | 521.486601736 | −2.147705251 px |
| Sample SD | 0.050349452 | 0.025909506 | 48.54% reduction |
| Range | 0.166581476 | 0.079070832 | 52.53% reduction |

The candidate produced substantially lower repeated-capture variation under the static condition.

### 6.2 Trial 05 controlled orientation

| Statistic | PCA baseline (px) | Binary geometry (px) | Candidate change |
|---|---:|---:|---:|
| Mean | 522.829559788 | 520.684302365 | −2.145257423 px |
| Median | 522.847915488 | 520.597564662 | −2.250350826 px |
| Sample SD | 0.641592996 | 0.779168884 | 21.44% increase |
| Full range | 2.183819347 | 2.273582168 | 4.11% increase |
| Range among orientation-group medians | 1.752720470 | 2.249772382 | 28.36% increase |

### 6.3 Orientation-group medians

| Orientation | PCA (px) | Binary geometry (px) | Geometry minus PCA (px) |
|---|---:|---:|---:|
| 0° | 523.069153912 | 520.811661820 | −2.257492092 |
| 20° | 522.776434595 | 520.585730039 | −2.190704556 |
| 40° | 522.782483310 | 520.443237463 | −2.339245847 |
| 70° | 521.612035008 | 519.358508326 | −2.253526682 |
| 90° retake | 523.364755478 | 521.608280708 | −1.756474770 |

The candidate was consistently shorter than the extreme-pixel baseline, which is expected when fitted end lines do not extend to isolated corner pixels. However, the offset was not constant across orientation; the 90° group differed materially from the other groups.

## 7. Diagnostic and visual review

Generated evidence:

- `oal_estimator_comparison_results.csv`
- `oal_estimator_comparison_summary.txt`
- `trial_03_static_comparison_contact_sheet.png`
- `trial_05_controlled_orientation_comparison_contact_sheet.png`
- per-capture overlays
- `sha256_manifest.txt`

Observations:

1. Trial 03 sidewall, end-line, and center-axis overlays appeared stable across all ten captures.
2. Trial 05 fits were generally plausible rather than catastrophically misplaced.
3. The 70° group showed the largest visible separation between the original PCA axis and fitted-geometry axis.
4. The algorithmically selected 90° sensitivity candidate was `capture_02_mask`; it was retained in all primary statistics.
5. Aggregate output recorded `geometry_flagged_capture_count = 27`. The flag thresholds were therefore not selective enough for acceptance/rejection decisions.

## 8. Interpretation

The estimator achieved its narrow goal of reducing static endpoint noise, supporting the proposition that extreme mask pixels contribute to repeated-capture variation. It did not achieve the broader goal of orientation invariance.

The most defensible interpretation is that robust line fitting reduces local endpoint sensitivity but still fits a rasterized binary boundary. Diagonal orientations generate staircase structure and orientation-dependent boundary location. Consequently, a line can be repeatable within an orientation while remaining biased between orientations.

The shorter absolute pixel length is not, by itself, evidence of error or improvement. No calibrated absolute ground truth was used in this comparison.

## 9. Decision

**Status: Exploratory; not accepted as the final OAL estimator.**

The PCA estimator remains the provisional working baseline because its Trial 05 orientation-group median range was smaller.

The binary-geometry result should be retained as a controlled negative result demonstrating that improved static repeatability does not necessarily improve orientation invariance.

## 10. Limitations

- Binary masks provide integer-grid boundaries.
- The test used one case and one imaging configuration.
- Trial 05 group sizes were small and unequal.
- No absolute OAL ground truth or uncertainty budget was evaluated.
- The diagnostic flag thresholds were not validated.
- Contact-sheet review may hide subpixel-scale fitting differences.

## 11. Follow-on action

The binary geometry was used as initialization for a grayscale subpixel estimator. Because that first subpixel method also failed to improve orientation invariance, the next revision must define one consistent physical intensity crossing rather than selecting the strongest local gradient.
