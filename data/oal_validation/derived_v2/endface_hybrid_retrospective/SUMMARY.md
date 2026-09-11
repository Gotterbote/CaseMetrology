# V2 Endface-Hybrid Retrospective Evaluation

**Exploratory retrospective analysis only. Formal V1/V2 results remain unchanged.**

- Estimator freeze commit: `dbc4920`
- Frozen estimator SHA-256: `3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af`
- Run Git HEAD: `dbc4920a1a9173d6e4c29fd44d0d9d765225a743`
- Maximum PCA reproduction difference: 0.000000000000 in

## Availability

- Hybrid valid observations: 180/180
- Hybrid availability: 100.000%
- Complete 3-round specimens: 60/60

## Primary comparison

| Metric | Recorded V2 PCA | Frozen endface hybrid |
|---|---:|---:|
| Mean bias (CV-manual) | 0.000277 in | -0.000505 in |
| MAE | 0.001191 in | 0.001257 in |
| RMSE | 0.001538 in | 0.001601 in |
| P95 absolute error | 0.003065 in | 0.003109 in |
| Maximum absolute error | 0.004290 in | 0.003842 in |
| P95 repositioning | 0.003994 in | 0.003021 in |
| Maximum repositioning | 0.005199 in | 0.004557 in |

## Classification

- Recorded V2 false passes: 1
- Recorded V2 false fails: 5
- Hybrid false passes: 0
- Hybrid false fails: 5

## Ten largest hybrid specimen ranges

- Part 48: range 0.004557 in
- Part 106: range 0.004205 in
- Part 70: range 0.003938 in
- Part 75: range 0.003818 in
- Part 189: range 0.003452 in
- Part 118: range 0.003279 in
- Part 194: range 0.003256 in
- Part 221: range 0.003021 in
- Part 127: range 0.003014 in
- Part 51: range 0.003004 in

## Ten largest hybrid absolute errors

- Part 14: abs error 0.003842 in; bias -0.003842 in
- Part 85: abs error 0.003250 in; bias -0.003250 in
- Part 9: abs error 0.003115 in; bias -0.003115 in
- Part 230: abs error 0.003109 in; bias +0.003109 in
- Part 100: abs error 0.003044 in; bias +0.003044 in
- Part 75: abs error 0.002829 in; bias -0.002829 in
- Part 40: abs error 0.002774 in; bias -0.002774 in
- Part 172: abs error 0.002473 in; bias +0.002473 in
- Part 215: abs error 0.002466 in; bias -0.002466 in
- Part 51: abs error 0.002321 in; bias -0.002321 in

## Interpretation guardrail

The estimator architecture and numerical parameters were frozen before this retrospective V2 analysis. These results may support a decision about prospective V3 validation, but they are not an independent prospective validation and must not be used to retune this frozen estimator version.
