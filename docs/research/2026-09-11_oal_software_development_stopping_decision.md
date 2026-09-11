# OAL Software-Only Development Stopping Decision

Date: 2026-09-11

## Scope

This record documents the decision to stop further software-only OAL estimator
development using the final fixed hardware and fixture configuration.

Formal V1 and V2 results remain unchanged.

## Background

The formal V2 PCA estimator produced:

- Availability: 100%
- P95 repositioning: 0.003994 in
- Mean bias: +0.000277 in
- RMSE: 0.001538 in
- P95 absolute error: 0.003065 in
- Maximum absolute error: 0.004290 in

The original software-development objective was to determine whether estimator
improvement alone could reduce P95 repositioning to approximately 0.002 in or
better without modifying the final hardware or fixture.

## Frozen endface-hybrid result

A geometry-axis / subpixel-endface estimator was developed using non-formal
development data and frozen before retrospective V2 evaluation.

Retrospective V2 results:

- Availability: 180/180 = 100%
- P95 repositioning: 0.003021 in
- Mean bias: -0.000505 in
- RMSE: 0.001601 in
- P95 absolute error: 0.003109 in
- Maximum absolute error: 0.003842 in
- False passes: 0
- False fails: 5

The hybrid therefore reduced P95 repositioning by approximately 24.4% relative
to formal V2 PCA while preserving 100% availability, but it did not achieve
the <=0.002-in development objective.

## Residual-error evidence

Residual diagnostics showed:

- 147/180 hybrid pairwise repositioning differences <=0.002 in
- 40/60 specimens had a three-round hybrid range <=0.002 in
- 10/60 specimens had a hybrid range >0.003 in
- PCA-versus-hybrid specimen-range Pearson correlation: 0.8755
- PCA-versus-hybrid centered-placement Pearson correlation: 0.9068

The strong agreement between two different endpoint estimators indicates a
substantial shared placement/image-geometry component.

## Pixel/calibration decomposition

The hybrid measurement was decomposed into observed pixel-length and
calibration-scale contributions.

Results:

- Actual hybrid P95: 0.003021 in
- Pixel-length-only P95: 0.003062 in
- Calibration-only P95: 0.000094 in
- Actual versus pixel-length Pearson correlation: 0.9991
- Actual versus effective-PPI Pearson correlation: 0.0277
- Actual versus in-plane-angle Pearson correlation: -0.1239

The remaining repositioning variation is therefore overwhelmingly present in
the observed projected pixel geometry rather than the inch-conversion
calibration.

## Independent pose-observability test

Independent image cues were evaluated without fitting an OAL correction.

Development data showed potentially strong relationships for some cues,
particularly fixture-relative centroid Y.

However, those relationships did not generalize to the formal V2 population.

Formal V2 correlations included:

- centroid_y_px: Pearson +0.0925; Spearman +0.1057
- body_width_gradient_norm: Pearson -0.1590; Spearman -0.1538
- in_plane_tilt_deg: Pearson -0.1239; Spearman -0.1671
- endface_sharpness_log_ratio: Pearson -0.1186; Spearman -0.0945
- body_width_ratio_mouth_to_base: Pearson -0.0985; Spearman -0.1206
- endface_skew_difference: Pearson -0.0607; Spearman -0.0628
- case_width_px: Pearson +0.0427; Spearman +0.0495
- centroid_x_px: Pearson +0.0231; Spearman +0.0211

No independent observable pose cue demonstrated a sufficiently strong,
generalizable relationship to justify development of a pose-compensation
correction.

## Decision

Further estimator-only tuning is stopped.

The available evidence indicates that:

1. Endpoint-localization improvements can reduce, but not eliminate,
   repositioning variation.
2. Spatial calibration is not a material source of the remaining error.
3. The dominant residual is present in the projected image geometry.
4. No independently observable pose variable has been identified that
   generalizes sufficiently to support a defensible software correction.
5. Additional outcome-driven fitting to the formal V2 dataset would compromise
   methodological integrity.

A prospective V3 formal validation using another software-only estimator is
therefore not justified under the current hardware/fixture constraints and
the <=0.002-in P95 repeatability objective.

## Thesis interpretation

The post-V2 estimator-development work should be reported as diagnostic and
exploratory evidence.

The formal V2 validation remains the primary validation result.

The software-development investigation demonstrates both measurable
improvement and an empirical performance limit associated with
placement-dependent projected geometry in the current single-view system.

Future work may investigate additional physical pose constraint, telecentric
optics, additional camera views, or other methods capable of independently
observing or eliminating out-of-plane placement variation.
