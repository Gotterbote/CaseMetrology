# V3 Formal Performance and Guard-Band Analysis

Date: 2026-09-17

## Purpose

This record documents the formal V3 Endface-Hybrid performance results and the exploratory guard-band analysis used to evaluate industrial screening feasibility.

The intent is to preserve the analysis basis for the thesis manuscript and defense. This record does not modify the frozen estimator, formal images, or formal observations.

## Data Sources

- Formal V3 CV observations:
  `data/oal_validation/v3_formal/v3_cv_observations.csv`
- Manual reference summary:
  `data/oal_validation/derived/manual_reference_summary.csv`
- Frozen V3 primary estimator:
  `scripts/evaluate_oal_endface_hybrid_dev.py`
- Frozen Endface-Hybrid SHA-256:
  `3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af`

Formal V3 observations:
- 60 specimens
- 3 placements per specimen
- 180 total CV observations
- 180/180 valid Endface-Hybrid results

## Formal Decision Limits

The existing study decision limits were retained:

- LSL = 0.9900 in
- USL = 1.0100 in

Specimen-level classification uses the mean of the three CV observations and the corresponding manual-reference specimen mean.

## Formal V3 Performance

| Metric | V3 Endface-Hybrid |
|---|---:|
| Availability | 180/180 = 100.000% |
| Bias | -0.000435 in |
| MAE | 0.001517 in |
| RMSE | 0.001794 in |
| P95 absolute error | 0.003170 in |
| Maximum absolute error | 0.003913 in |
| P95 repositioning | 0.000633 in |
| False passes | 1 |
| False fails | 3 |

Observed false-pass specimen:
- 143

Observed false-fail specimens:
- 9
- 151
- 194

## Repositioning Definition

The V3 repositioning metric uses the same pooled pairwise approach as the existing V1/V2 analysis.

For each specimen, the three formal placements generate three absolute pairwise differences. Across 60 specimens this produces 180 pairwise repositioning differences.

The reported P95 repositioning value uses the frozen nearest-rank convention:
- rank 171 of 180

V3 P95 repositioning:
- 0.000633 in

## Comparison With Earlier Validation Stages

| Metric | V1 PCA | V2 PCA | V2 Endface-Hybrid | V3 Endface-Hybrid |
|---|---:|---:|---:|---:|
| Availability | 100% | 100% | 100% | 100% |
| Bias (in) | +0.001613 | +0.000277 | -0.000505 | -0.000435 |
| RMSE (in) | 0.002205 | 0.001538 | 0.001601 | 0.001794 |
| P95 absolute error (in) | 0.003960 | 0.003065 | 0.003109 | 0.003170 |
| P95 repositioning (in) | 0.004831 | 0.003994 | 0.003021 | 0.000633 |

The dominant V3 improvement was repositioning performance.

Relative reduction in P95 repositioning:
- V1 to V3: approximately 86.9%
- V2 Endface-Hybrid to V3: approximately 79%

The V1-to-V3 system progression substantially reduced placement-dependent measurement variability. Controlled presentation was an important V3 design change, but the 86.9% improvement is a system-level result and is not attributed solely to that change.

Absolute accuracy did not improve proportionally. V3 P95 absolute error remained approximately 0.0032 in.

This supports separating two performance characteristics:
1. repeatability / presentation sensitivity, and
2. residual absolute measurement error.

## Guard-Band Method

An exploratory symmetric guard band, g, was applied to the original specification limits.

Automatic acceptance interval:

`LSL + g <= CV specimen mean <= USL - g`

Measurements near the specification limits are withheld from automatic acceptance and routed to review.

This analysis evaluates whether guarded decision logic can reduce observed false-pass risk without claiming that the CV system replaces precision reference metrology.

## Guard-Band Results

| Guard band | Automatic-accept interval | Auto-accepted | Review-zone count | Observed false passes | Conforming not automatically accepted |
|---:|---:|---:|---:|---:|---:|
| 0.0000 in | 0.9900-1.0100 | 43/60 | 0 | 1 | 3 |
| 0.0005 in | 0.9905-1.0095 | 39/60 | 4 | 1 | 7 |
| 0.0010 in | 0.9910-1.0090 | 34/60 | 9 | 0 | 11 |
| 0.0015 in | 0.9915-1.0085 | 31/60 | 12 | 0 | 14 |
| 0.0020 in | 0.9920-1.0080 | 30/60 | 13 | 0 | 15 |
| 0.0025 in | 0.9925-1.0075 | 27/60 | 16 | 0 | 18 |
| 0.0030 in | 0.9930-1.0070 | 24/60 | 19 | 0 | 21 |
| 0.0035 in | 0.9935-1.0065 | 22/60 | 21 | 0 | 23 |
| 0.0040 in | 0.9940-1.0060 | 21/60 | 22 | 0 | 24 |

## Smallest Observed Zero-False-Pass Guard

The smallest retrospectively observed guard band that eliminated false passes in this validation cohort was:

- Guard band: 0.0006 in
- Automatic-accept interval: 0.9906-1.0094 in
- Automatically accepted: 38/60
- Review-zone specimens: 5
- Observed false passes: 0
- Conforming specimens not automatically accepted: 7

Review-zone specimen IDs:
- 35
- 58
- 104
- 143
- 221

Specimen 143, which produced the unguarded V3 false pass, is moved out of automatic acceptance by the 0.0006 in guard band.

## Interpretation

The 0.0006 in value is a retrospective cohort result and must not be represented as a validated production guard band.

A 0.0010 in symmetric guard band provides a simpler engineering example for thesis discussion:

- Automatic-accept interval: 0.9910-1.0090 in
- 34/60 specimens automatically accepted
- 0 observed false passes
- 9 specimens in the near-limit review zone
- 11 conforming specimens not automatically accepted

These counts describe the intentionally stratified 60-specimen validation cohort and must not be interpreted as production yield estimates.

## Thesis-Relevant Finding

V3 demonstrated substantially improved system repeatability, with P95 repositioning reduced to 0.000633 in. This improvement is interpreted as a system-level V1-to-V3 result rather than as an effect attributable solely to controlled part presentation.

Residual absolute measurement error remained materially larger than the repositioning error, with P95 absolute error of 0.003170 in.

Accordingly, the formal results do not support treating the prototype as a direct substitute for precision reference metrology across the full specification interval.

The results do support evaluating the system as an industrial dimensional screening tool in which:

- measurements comfortably inside specification may be automatically accepted,
- near-limit measurements are referred for secondary inspection, and
- measurements outside specification are rejected or investigated.

The guard-band analysis provides exploratory evidence that such an architecture can reduce observed false-pass risk while retaining useful automatic inspection capability.

## Limitation

The guard-band analysis was performed retrospectively using the same validation cohort from which performance was evaluated.

It demonstrates feasibility and decision-behavior tradeoffs but does not independently validate a production guard-band rule.

