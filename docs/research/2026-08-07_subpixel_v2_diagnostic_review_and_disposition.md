# Subpixel OAL Version 2 Diagnostic Review and Disposition

**Date:** 2026-08-07  
**Project:** CaseMetrology  
**Research area:** Fixtureless top-down overall length (OAL) metrology  
**Method under review:** Mask-anchored grayscale subpixel estimator, Version 2  
**Repository checkpoint before diagnostic review:** `845fd06` — Add subpixel v2 diagnostic and disposition plan

## 1. Purpose

This record documents the final diagnostic review of the mask-anchored grayscale subpixel OAL estimator (Version 2) and the decision regarding whether it should continue as a candidate primary OAL measurement method for the thesis.

The purpose of this review was not to optimize the estimator through parameter tuning. The objective was to determine whether the previously observed Version 2 failures were caused by an obvious, localized implementation defect that justified a targeted correction, or whether the method introduced sufficient optical and algorithmic fragility that the existing binary geometry estimator should remain the primary OAL method.

## 2. Reproduced Development Baseline

The previously documented Version 2 comparison was rerun without changing estimator code or parameters.

Output directory:

`data/oal_real/2026-07-31_subpixel_v2_estimator_comparison/`

The rerun reproduced the prior development result exactly:

- Source image/mask pairs: **27**
- Version 2 failures: **7**
- Version 2 completed measurements: **20**
- Version 2 flagged captures: **20**

Primary result files:

- `oal_subpixel_v2_estimator_comparison_results.csv`
- `oal_subpixel_v2_profile_diagnostics.csv`
- `oal_subpixel_v2_estimator_comparison_summary.txt`
- `overlays/`

The exact reproduction confirmed that the observed failure behavior was deterministic under the current software and dataset rather than the result of environment drift or an intermittent execution condition.

## 3. Failure Localization

All seven Version 2 failures occurred in the static dataset:

`trial_03_static`

Failed captures:

- `cycle_01_mask`
- `cycle_02_mask`
- `cycle_03_mask`
- `cycle_05_mask`
- `cycle_06_mask`
- `cycle_09_mask`
- `cycle_10_mask`

Passing captures from the same static series:

- `cycle_04_mask`
- `cycle_07_mask`
- `cycle_08_mask`

Every failed capture returned the same estimator failure message:

> Insufficient accepted profiles on the minimum sidewall.

The relevant implementation criterion is:

`accepted minimum-sidewall profiles < minimum_sidewall_profile_count`

The configured minimum sidewall profile count was:

- `minimum_sidewall_profile_count = 25`

Each sidewall was sampled with 72 profiles.

## 4. Static Minimum-Sidewall Acceptance Results

| Capture | Accepted Profiles | Total Profiles | Acceptance Fraction | Result |
|---|---:|---:|---:|---|
| cycle_01_mask | 24 | 72 | 0.3333 | Fail |
| cycle_02_mask | 23 | 72 | 0.3194 | Fail |
| cycle_03_mask | 20 | 72 | 0.2778 | Fail |
| cycle_04_mask | 25 | 72 | 0.3472 | Pass |
| cycle_05_mask | 21 | 72 | 0.2917 | Fail |
| cycle_06_mask | 24 | 72 | 0.3333 | Fail |
| cycle_07_mask | 25 | 72 | 0.3472 | Pass |
| cycle_08_mask | 26 | 72 | 0.3611 | Pass |
| cycle_09_mask | 22 | 72 | 0.3056 | Fail |
| cycle_10_mask | 21 | 72 | 0.2917 | Fail |

The pass/fail threshold therefore divided a narrow range of static results. Two failed captures (`cycle_01_mask` and `cycle_06_mask`) missed the acceptance requirement by only one profile.

This behavior is important because the specimen remained stationary during this trial. A one-profile difference therefore changed the estimator state from failed to passed without any intended change in specimen geometry.

## 5. Rejection Mechanisms

For the minimum sidewall, the dominant rejection mechanisms were:

- `mask_anchor_not_found`: **31–34 profiles per capture**
- `low_contrast`: **15–19 profiles per capture**

The median minimum-sidewall contrast across the static captures remained close to the configured minimum local contrast criterion of 30.0. Observed median contrast values were approximately 31.84–33.36.

The Version 2 defaults relevant to this behavior were:

- `minimum_local_contrast = 30.0`
- `maximum_anchor_distance_pixels = 3.0`
- `minimum_sidewall_profile_count = 25`

Accepted minimum-sidewall anchor offsets extended to the configured search boundary:

- Minimum observed accepted offset: **-3.0 px**
- Maximum observed accepted offset: **+3.0 px**
- Median accepted offset: approximately **-1.31 px**

This indicates that some minimum-sidewall profiles were operating at the limit of the permitted mask-anchor search distance.

## 6. Sidewall Asymmetry

A direct comparison of the two sidewalls in `trial_03_static` showed a strong directional asymmetry.

### Minimum sidewall

- Profiles evaluated: **720**
- Profiles accepted: **231**
- Acceptance rate: **32.1%**
- Median grayscale contrast: **32.16**
- Median accepted mask-anchor offset: approximately **-1.31 px**
- Accepted offset range: **-3.0 to +3.0 px**

### Maximum sidewall

- Profiles evaluated: **720**
- Profiles accepted: **720**
- Acceptance rate: **100%**
- `mask_anchor_not_found`: **0**
- `low_contrast`: **0**
- Median grayscale contrast: **65.74**
- Median accepted mask-anchor offset: approximately **+0.47 px**
- Accepted offset range: approximately **-1.34 to +2.25 px**

The maximum sidewall therefore exhibited approximately twice the median grayscale contrast of the minimum sidewall while also achieving complete profile acceptance.

## 7. Normal-Direction Check

The median profile normals for the two sidewalls were:

- Minimum sidewall: approximately `(0.99768, -0.06805)`
- Maximum sidewall: approximately `(-0.99768, 0.06808)`

These vectors are effectively opposite as expected.

This result does not support an obvious normal-direction sign error or a gross error in the direction from which the two sidewalls are sampled.

## 8. Visual Diagnostic Review

The following overlays were reviewed directly:

Failed example:

`data/oal_real/2026-07-31_subpixel_v2_estimator_comparison/overlays/trial_03_static/static/cycle_01_mask_subpixel_v2_overlay.png`

Passing example:

`data/oal_real/2026-07-31_subpixel_v2_estimator_comparison/overlays/trial_03_static/static/cycle_04_mask_subpixel_v2_overlay.png`

The overlays did not show a gross geometric placement error on the minimum sidewall. The fitted sidewall location generally followed the physical boundary of the case.

However, the minimum sidewall showed a visibly softer and more irregular grayscale transition than the opposite side. Rejected-profile markers were concentrated along this weaker edge. The visual observation is consistent with the quantitative contrast and mask-anchor diagnostics.

The passing `cycle_04_mask` did not exhibit a fundamentally different physical edge. It passed because it produced exactly 25 accepted minimum-sidewall profiles, whereas the failed `cycle_01_mask` produced 24.

## 9. Failure Classification

The diagnostic evidence supports the following classifications.

### F1 — Insufficient local contrast

**Supported.**

The minimum sidewall had substantially lower grayscale contrast than the maximum sidewall. Numerous profiles were explicitly rejected as `low_contrast`, and the median minimum-sidewall contrast remained close to the configured minimum local contrast threshold.

### F4 — Mask-anchor limitation

**Supported.**

Between 31 and 34 minimum-sidewall profiles per static capture returned `mask_anchor_not_found`. Accepted anchor offsets reached the configured ±3.0 px search boundary, indicating that the permitted anchor search region was limiting profile availability on this side.

### F7 — Algorithmic rejection / threshold sensitivity

**Supported.**

The static specimen alternated between failed and passed estimator states based on accepted-profile counts that clustered around the hard threshold of 25. A change from 24 to 25 accepted profiles changed the estimator result despite no intended change in physical specimen geometry.

### Gross geometry or normal-direction failure

**Not supported by the reviewed evidence.**

The profile normals were correctly opposed, and visual overlay review did not reveal an obvious gross displacement of the minimum-sidewall geometry.

## 10. Interpretation

The Version 2 subpixel estimator is not globally defective. The maximum sidewall demonstrated complete profile acceptance and strong local contrast. The observed failures are localized primarily to one physical sidewall where the image exhibits weaker contrast and more difficult mask anchoring.

Correcting this behavior would likely require additional work involving one or more of the following:

- mask-anchor search strategy changes,
- anchor-distance parameter investigation,
- local-contrast criterion investigation,
- illumination or optical configuration changes,
- more sophisticated grayscale edge-profile modeling,
- and subsequent revalidation across all orientations and repeated captures.

Such work would expand the thesis from validation of a computer-vision metrology system into a substantial study of subpixel edge-detection optimization.

## 11. Disposition Decision

**Subpixel OAL Version 2 is retained as an exploratory research method but is not selected as the primary OAL estimator for the thesis.**

No further Version 2 parameter optimization or estimator redesign is planned within the current thesis scope unless later validation of the primary method reveals a measurement limitation that cannot be addressed by the geometry estimator.

The binary geometry estimator remains the primary OAL measurement candidate.

Previously established static geometry-estimator performance:

- Static standard deviation: **0.025910 px**
- Static range: **0.079071 px**
- Static mean: **521.484317 px**
- Static median: **521.486602 px**

The geometry estimator provides a simpler and more stable path into calibration and validation without the failure behavior observed in the subpixel method.

## 12. Thesis Significance

The subpixel investigation remains research-relevant even though the method was not adopted.

It demonstrates that:

1. A more sophisticated grayscale refinement method was implemented and evaluated rather than assumed to be superior.
2. The estimator exposed a directional optical/edge-quality asymmetry in the imaging system.
3. Failure behavior was investigated through profile-level diagnostics, quantitative comparison, implementation review, and visual overlay inspection.
4. The more complex method was rejected based on empirical evidence rather than software complexity alone.
5. The final estimator choice favors stability, traceability, and validation readiness.

A suitable thesis-level summary is:

> A mask-anchored grayscale subpixel refinement method was evaluated as a potential improvement over the binary geometry estimator. Although one sidewall demonstrated complete profile acceptance, the opposing side exhibited substantially reduced local contrast and frequent mask-anchor failures. In a static 10-frame evaluation, only 3 of 10 frames satisfied the minimum sidewall profile-count criterion despite unchanged specimen geometry. Because the simpler geometry estimator demonstrated stable repeatability without comparable failure behavior, subpixel refinement was not selected as the primary OAL estimator.

## 13. Next Research Phase

Following this disposition, the primary OAL development path is:

1. Freeze the current geometry estimator as the measurement candidate.
2. Establish or confirm pixel-to-inch calibration.
3. Complete manual reference measurements using the defined caliper procedure.
4. Execute the randomized OAL validation sample plan.
5. Compare computer-vision measurements against manual reference measurements.
6. Quantify bias, repeatability, agreement, and reproducibility.
7. Evaluate whether the computer-vision system satisfies the defined OAL measurement objective.
