# V1-V2-V3 Engineering Progression

Date: 2026-09-17

## Purpose

This record summarizes the engineering progression from V1 through V3 and preserves the interpretation needed for the thesis manuscript and defense.

The central purpose is to distinguish improvement in part-presentation repeatability from improvement in absolute measurement accuracy.

## Validation Basis

### V1

V1 was the original formal OAL validation configuration using the PCA estimator.

The formal results established the baseline magnitude of placement-dependent variability and absolute measurement error.

### V2

V2 introduced fixture changes intended to improve physical presentation and stability.

The PCA estimator remained the formal V2 estimator.

The Endface-Hybrid estimator was subsequently applied retrospectively to the already-acquired V2 images. Therefore, V2 Endface-Hybrid results are useful comparative evidence but are not a prospective validation of that estimator.

### V3

V3 introduced controlled part presentation, including controlled roll orientation and improved resistance to presentation movement.

The Endface-Hybrid estimator was frozen before the V3 formal acquisition and was processed only after all 180 formal images had been acquired.

V3 therefore provides the prospective formal validation of the frozen Endface-Hybrid estimator under the controlled-presentation configuration.

## Performance Comparison

| Metric | V1 PCA | V2 PCA | V2 Endface-Hybrid | V3 Endface-Hybrid |
|---|---:|---:|---:|---:|
| Validation basis | Formal | Formal | Retrospective | Formal prospective |
| Availability | 100% | 100% | 100% | 100% |
| Bias (in) | +0.001613 | +0.000277 | -0.000505 | -0.000435 |
| RMSE (in) | 0.002205 | 0.001538 | 0.001601 | 0.001804 |
| P95 absolute error (in) | 0.003960 | 0.003065 | 0.003109 | 0.003267 |
| P95 repositioning (in) | 0.004831 | 0.003994 | 0.003021 | 0.000633 |

## Repositioning Improvement

The strongest V3 improvement occurred in placement-to-placement repeatability.

Observed P95 repositioning:

- V1 PCA: 0.004831 in
- V2 PCA: 0.003994 in
- V2 Endface-Hybrid: 0.003021 in
- V3 Endface-Hybrid: 0.000633 in

Relative reduction in P95 repositioning:

- V1 PCA to V2 PCA: approximately 17.3%
- V1 PCA to V2 Endface-Hybrid: approximately 37.5%
- V1 PCA to V3 Endface-Hybrid: approximately 86.9%
- V2 Endface-Hybrid to V3 Endface-Hybrid: approximately 79.0%

The reduction from 0.004831 in in V1 to 0.000633 in in V3 is evidence that controlled part presentation substantially reduced the dominant placement-dependent component observed in the original configuration.

## Absolute Accuracy

Absolute accuracy did not improve in proportion to repeatability.

P95 absolute error changed as follows:

- V1 PCA: 0.003960 in
- V2 PCA: 0.003065 in
- V2 Endface-Hybrid: 0.003109 in
- V3 Endface-Hybrid: 0.003267 in

V3 therefore achieved a large improvement in repositioning repeatability while retaining an absolute-error magnitude near 0.003 in.

The V3 P95 absolute error was slightly larger than the V2 PCA and retrospective V2 Endface-Hybrid values despite the large improvement in repositioning performance.

## Engineering Interpretation

The results demonstrate that repeatability and absolute accuracy were distinct limitations of the prototype.

Earlier configurations contained a substantial placement-dependent error component.

The controlled-presentation V3 configuration greatly reduced that component, as demonstrated by the decrease in P95 repositioning to 0.000633 in.

However, the remaining absolute error did not decrease proportionally.

This indicates that once presentation instability was reduced, other components of the measurement chain became comparatively more important.

The formal data establish the existence of a residual absolute-error floor but do not, by themselves, uniquely identify its source.

Potential contributors discussed in the thesis should therefore be described as possible mechanisms rather than proven causes unless separately supported by experimental evidence.

Examples may include:

- optical and silhouette-edge measurement limitations,
- dimensional variation in the physical case end geometry,
- spatial calibration effects,
- image-resolution limitations,
- and uncertainty in the manual reference measurement.

## Formal Target Interpretation

V3 results relative to the predeclared performance targets were:

| Criterion | V3 result | Target | Outcome |
|---|---:|---:|---|
| Availability | 100% | >= 99% | MET |
| Absolute bias | 0.000435 in | <= 0.001 in | MET |
| RMSE | 0.001804 in | <= 0.002 in | MET |
| P95 absolute error | 0.003267 in | <= 0.003 in | NOT MET |
| P95 repositioning | 0.000633 in | <= 0.002 in | MET |
| False-pass objective | 1 observed | 0 preferred | NOT MET |

V3 therefore met four of the five quantitative measurement-performance thresholds but did not meet the P95 absolute-error threshold.

The zero-false-pass preference was also not met under the unguarded specification decision rule.

## Thesis Interpretation

The results do not support a claim that the prototype is interchangeable with precision contact metrology across the full specification interval.

They do support a more limited industrial-inspection interpretation.

The system demonstrated:

- complete measurement availability in the formal V3 cohort,
- low systematic bias,
- RMSE below the stated 0.002 in target,
- substantially improved part-presentation repeatability,
- and a residual absolute-error level that can be accounted for through guarded decision logic.

The V3 and guard-band findings therefore support evaluation of the system as a dimensional screening device rather than as a direct replacement for precision reference measurement.

## Defense-Relevant Conclusion

A central finding of the study is not simply that the prototype became "more accurate."

The stronger and more defensible conclusion is:

1. V1 revealed that uncontrolled presentation was a major source of measurement variability.
2. V2 fixture changes reduced some of that variability.
3. V3 controlled presentation reduced P95 repositioning by approximately 86.9% relative to V1.
4. Absolute error did not decrease proportionally.
5. Therefore, presentation repeatability and absolute metrological accuracy were experimentally shown to be separate engineering limitations.
6. The resulting system is better characterized as a stable dimensional screening platform than as a replacement for precision contact metrology.

## Important Comparison Limitation

The V2 Endface-Hybrid results were generated retrospectively from previously acquired V2 images.

They should not be described as an independent prospective formal validation of the Endface-Hybrid estimator.

The V3 study is the prospective formal evaluation in which the Endface-Hybrid estimator was frozen before formal image acquisition and the formal images remained blinded from estimator-result interpretation until acquisition was complete.
