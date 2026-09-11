# Endface-Hybrid V2 Scale Decomposition

**Diagnostic only. No estimator parameters are changed.**

## Pairwise P95 repositioning

- Actual hybrid: 0.003021 in
- Pixel-length component with specimen calibration scale held fixed: 0.003062 in
- Calibration-scale component with specimen pixel length held fixed: 0.000094 in

## Maximum pairwise repositioning

- Actual hybrid: 0.004557 in
- Pixel-length component: 0.004489 in
- Calibration-scale component: 0.000107 in

## Within-specimen centered correlations with actual hybrid OAL

- Pixel length Pearson: 0.9991
- Pixel length Spearman: 0.9983
- Effective PPI Pearson: 0.0277
- Effective PPI Spearman: 0.0285
- Geometry angle Pearson: -0.1239
- Geometry angle Spearman: -0.1671

## Interpretation

If the pixel-only P95 remains close to the actual hybrid P95 while the scale-only P95 is small, the remaining repositioning error is primarily present in the observed image geometry before inch conversion. If the scale-only component is substantial, spatial-calibration selection is materially contributing to placement sensitivity.
