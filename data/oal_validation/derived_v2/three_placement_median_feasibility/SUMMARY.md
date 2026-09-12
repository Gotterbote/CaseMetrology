# Three-Placement Median Protocol — Retrospective Feasibility

**Exploratory feasibility analysis only. This does not revise formal V2 and does not prospectively validate a multi-placement protocol.**

## Critical limitation

The V2 dataset contains one three-placement group per specimen. It can therefore evaluate the accuracy and classification behavior of a median-of-three reported value, but it cannot estimate repeatability of the complete median-of-three protocol. Prospective repeatability requires multiple independent three-placement groups per specimen.

## Integrity baseline

- PCA mean-of-three bias: +0.000277 in
- PCA mean-of-three RMSE: 0.001538 in
- Hybrid mean-of-three bias: -0.000505 in
- Hybrid mean-of-three RMSE: 0.001601 in

These reproduce the previously preserved specimen-level mean results within the script's integrity tolerance.

## PCA: mean-of-three versus median-of-three

| Metric | Mean of 3 | Median of 3 |
|---|---:|---:|
| Bias | +0.000277 in | +0.000265 in |
| MAE | 0.001191 in | 0.001274 in |
| RMSE | 0.001538 in | 0.001599 in |
| P95 absolute error | 0.003065 in | 0.003513 in |
| Maximum absolute error | 0.004290 in | 0.004068 in |
| False passes | 1 | 1 |
| False fails | 5 | 6 |

- PCA median had smaller absolute error on 29/60 specimens.
- PCA mean had smaller absolute error on 31/60 specimens.
- Equal absolute error: 0/60 specimens.

## Endface hybrid: mean-of-three versus median-of-three

| Metric | Mean of 3 | Median of 3 |
|---|---:|---:|
| Bias | -0.000505 in | -0.000556 in |
| MAE | 0.001257 in | 0.001285 in |
| RMSE | 0.001601 in | 0.001673 in |
| P95 absolute error | 0.003109 in | 0.003099 in |
| Maximum absolute error | 0.003842 in | 0.004173 in |
| False passes | 0 | 0 |
| False fails | 5 | 4 |

- Hybrid median had smaller absolute error on 28/60 specimens.
- Hybrid mean had smaller absolute error on 32/60 specimens.
- Equal absolute error: 0/60 specimens.

## Interpretation guardrail

A favorable median-of-three accuracy result would justify considering a prospectively frozen multi-placement measurement protocol. It would not convert the original V2 single-placement repeatability criterion into a pass. A new protocol would require prospective validation, including repeatability of repeated independent three-placement groups.
