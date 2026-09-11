# Endface-Hybrid OAL Estimator — Retrospective V2 Evaluation

Date: 2026-09-11

## Status

This analysis is retrospective and exploratory.

Formal V1 and V2 results remain unchanged.

The endface-hybrid estimator architecture and numerical parameters were frozen
before this analysis at commit:

    dbc4920

Frozen estimator SHA-256:

    3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af

Retrospective evaluation script SHA-256:

    4e501647ab09575cc853e448c9d569da9d6a6719d29c90551f178ca1188c95a3

No estimator parameter was changed after viewing the V2 retrospective results.

## Data-integrity check

All 180 formal V2 raw images were regenerated through the frozen V2 PCA
pipeline before interpretation of the hybrid results.

Maximum regenerated-versus-recorded PCA OAL difference:

    0.000000000000 in

Result:

    PASS

## Endface-hybrid availability

Valid observations:

    180 / 180

Availability:

    100.000%

Complete three-round specimens:

    60 / 60

## Retrospective comparison

| Metric | Recorded V2 PCA | Frozen Endface Hybrid |
|---|---:|---:|
| P95 repositioning | 0.003994 in | 0.003021 in |
| Mean bias (CV - manual) | +0.000277 in | -0.000505 in |
| RMSE | 0.001538 in | 0.001601 in |
| P95 absolute error | 0.003065 in | 0.003109 in |
| Maximum absolute error | 0.004290 in | 0.003842 in |
| Availability | 100.000% | 100.000% |

Hybrid classification results:

- False passes: 0
- False fails: 5

## Primary interpretation

The frozen endface-hybrid estimator reduced P95 repositioning error from
0.003994 in to 0.003021 in, an improvement of approximately 24.4%, while
maintaining 100% availability.

However, the estimator did not achieve the development objective of
P95 repositioning <= 0.002 in.

The mixed accuracy results, together with development evidence showing very
high fixed-position stability but substantially larger independent-placement
variation, indicate that endpoint localization explains only part of the V2
repositioning error.

The remaining investigation should therefore focus on the specimen-level
residual/repositioning pattern rather than additional endpoint-parameter
tuning.

## Methodological guardrail

These retrospective V2 results must not be used to retune this frozen version
of the endface-hybrid estimator.

Any subsequent software-development hypothesis must have an independently
defensible physical or geometric basis and must be developed using non-formal
development data before prospective validation.
