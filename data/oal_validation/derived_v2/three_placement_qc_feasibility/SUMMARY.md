# Three-Placement Repeatability-QC Feasibility

**Exploratory diagnostic only. No QC threshold is selected or validated by this analysis.**

## Continuous association: spread versus absolute error

- PCA Pearson: +0.1227
- PCA Spearman: +0.2588
- Hybrid Pearson: +0.1621
- Hybrid Spearman: +0.2233

A strong positive association would support using internal three-placement spread as an accuracy-risk signal. Weak association would indicate that good internal agreement does not reliably imply accuracy relative to the manual reference.

## Predeclared spread thresholds — endface hybrid

| Spread limit | Accept | Availability | Accepted MAE | Accepted RMSE | Accepted P95 abs | Accepted max abs | FP | FF |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0010 in | 23/60 | 38.3% | 0.001019 | 0.001402 | 0.003109 | 0.003115 | 0 | 2 |
| 0.0015 in | 37/60 | 61.7% | 0.001100 | 0.001506 | 0.003115 | 0.003842 | 0 | 4 |
| 0.0020 in | 40/60 | 66.7% | 0.001136 | 0.001541 | 0.003109 | 0.003842 | 0 | 4 |
| 0.0025 in | 45/60 | 75.0% | 0.001172 | 0.001550 | 0.003109 | 0.003842 | 0 | 4 |
| 0.0030 in | 50/60 | 83.3% | 0.001214 | 0.001583 | 0.003115 | 0.003842 | 0 | 4 |

## Predeclared spread thresholds — PCA

| Spread limit | Accept | Availability | Accepted MAE | Accepted RMSE | Accepted P95 abs | Accepted max abs | FP | FF |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0010 in | 14/60 | 23.3% | 0.000882 | 0.001200 | 0.002917 | 0.002917 | 0 | 2 |
| 0.0015 in | 23/60 | 38.3% | 0.000832 | 0.001118 | 0.002438 | 0.002917 | 0 | 3 |
| 0.0020 in | 34/60 | 56.7% | 0.001118 | 0.001542 | 0.003534 | 0.004290 | 1 | 5 |
| 0.0025 in | 39/60 | 65.0% | 0.001163 | 0.001569 | 0.003534 | 0.004290 | 1 | 5 |
| 0.0030 in | 44/60 | 73.3% | 0.001152 | 0.001536 | 0.003164 | 0.004290 | 1 | 5 |

## Interpretation guardrail

These cutoffs are descriptive feasibility checks only. V2 must not be used to select an optimized acceptance threshold and then claim that threshold as validated. A practical QC/retry protocol would need a threshold defined from independent development evidence and then prospectively validated, including availability, retry burden, accuracy, classification, and repeatability of the complete procedure.
