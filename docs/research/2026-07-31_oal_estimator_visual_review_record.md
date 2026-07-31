---
title: OAL Estimator Visual Diagnostic Review Record
project: CaseMetrology
researcher: Timmy Bell
date: 2026-07-31
status: Completed exploratory visual review
review_scope: Contact sheets and selected enlarged regions
---

# OAL Estimator Visual Diagnostic Review Record

## 1. Purpose

Document the human visual review of fitted sidewalls, center axes, end lines, and endpoints for the binary-geometry and grayscale-subpixel fixtureless OAL estimators. Numerical range alone was not used as an acceptance criterion.

## 2. Evidence reviewed

### Binary geometry

- `data/oal_real/2026-07-31_geometry_estimator_comparison/trial_03_static_comparison_contact_sheet.png`
- `data/oal_real/2026-07-31_geometry_estimator_comparison/trial_05_controlled_orientation_comparison_contact_sheet.png`
- selected enlarged Trial 05 regions, including the 70° group

### Grayscale subpixel

- `data/oal_real/2026-07-31_subpixel_estimator_comparison/trial_03_static_subpixel_comparison_contact_sheet.png`
- `data/oal_real/2026-07-31_subpixel_estimator_comparison/trial_05_controlled_orientation_subpixel_comparison_contact_sheet.png`
- selected enlarged 70° and 90° regions

## 3. Review checklist

Each overlay was evaluated for the following:

1. Sidewall lines follow the long straight case walls.
2. Sidewall fits exclude the wider fixture or end-transition regions.
3. Center axis passes through the central body of the case.
4. End lines correspond to the intended physical end faces.
5. End lines are not visibly pulled toward rounded corners, halo, or reflections.
6. Axis/end-line intersections remain on the intended silhouette boundaries.
7. Fit behavior remains qualitatively consistent across orientation.
8. Diagnostic flags correspond to visible fit degradation.

## 4. Binary-geometry observations

### Trial 03

- The cyan sidewall fits were visually stable across all ten captures.
- The magenta end lines remained on the two physical ends.
- The green center axis remained centered.
- No gross fit failure or abrupt capture-to-capture line movement was apparent.
- Visual stability was consistent with the reduced static SD and range.

### Trial 05

- Fits at 0°, 20°, 40°, and 90° were generally plausible.
- The 70° group showed the largest visible separation between the PCA axis and the fitted-geometry axis.
- The 90° sensitivity candidate did not show a catastrophic line-fit failure.
- Sidewall and end-line placement remained plausible even where the numerical result was orientation biased.
- The fact that all 27 captures were flagged was not supported by 27 visually obvious failures; diagnostic thresholds were therefore not selective.

### Binary-geometry visual conclusion

The visual evidence does not indicate widespread gross line-placement failure. The remaining between-orientation variation is more consistent with fitting an orientation-dependent rasterized boundary than with a single obvious fitting defect.

## 5. Grayscale-subpixel observations

### Trial 03

- Sidewall, center-axis, and end-line placement appeared stable across all ten static captures.
- No gross subpixel fit failure was visible.
- The overlays were compatible with static repeatability approximately equal to the PCA baseline.

### Trial 05

- Center axes generally remained centered across orientation.
- At contact-sheet scale, sidewalls and end lines appeared plausible.
- Enlarged 70° and 90° regions showed that the grayscale edge transition was broad and contained more than one candidate feature.
- The case silhouette was surrounded by a combination of physical edge, backlight transition, gray halo, and reflective structure.
- The maximum-gradient edge could therefore shift from one transition lobe to another with orientation.
- The 90° group’s positive numerical bias was compatible with selection of an outer transition relative to other groups.
- The 70° group remained lower, indicating that the selected edge definition was not invariant.
- All 27 captures were flagged, but not all showed visible gross failure; diagnostic criteria require redesign.

### Grayscale-subpixel visual conclusion

The primary visual concern is not gross axis placement. It is inconsistent physical edge definition. The maximum absolute gradient is not guaranteed to represent the same case boundary at each orientation.

## 6. Acceptance decision

| Estimator | Visual fit plausibility | Numerical orientation performance | Decision |
|---|---|---|---|
| Binary geometry | Generally plausible | Worse than PCA | Exploratory only |
| Maximum-gradient subpixel | Generally plausible but edge feature inconsistent | Worst of three methods | Exploratory only |

Neither candidate is accepted as the final estimator.

## 7. Review limitations

- Contact sheets downsample each overlay and may hide small residual errors.
- The visual review was qualitative and not blinded.
- No independent annotation of true physical edge locations was available.
- A future acceptance review should include full-resolution per-capture inspection, profile plots, and defined numerical quality criteria.

## 8. Re-review trigger

Repeat visual review whenever any of the following changes:

- edge-selection rule,
- profile search radius or smoothing,
- sidewall/end-face point selection,
- distortion correction,
- spatial calibration,
- camera or lighting configuration,
- or accepted-mask generation.
