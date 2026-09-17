# Chapter 4 Results Evidence Audit

Date: 2026-09-17

## Audit conclusion

`CaseMetrology_Chapter3_Source_002f4e4.zip` contains sufficient preserved evidence to rebuild Chapter 4. It includes the frozen protocols and criteria, V1 and V2 formal derived tables, the retrospective V2 Endface-Hybrid outputs, post-V1 and controlled-presentation diagnostic results, all 180 V3 observation rows, per-image V3 estimator-result records, the accepted manual-reference summary, the V3 validation plan, and the exploratory guard-band record.

The package does not contain a machine-readable V3 specimen-level statistics file analogous to the V1 and V2 `formal_validation_statistics.json` files, and it does not contain a dedicated script that reproduces the V3 specimen-level agreement and guard-band tables from the preserved observation tables. The underlying V3 data needed for those calculations are present. Raw V3 images are not needed to reproduce Chapter 4 statistics because the processed observation table and per-image estimator diagnostics are included; raw-image reprocessing would require the full repository dataset.

## Authoritative result sources

| Evidence block | Primary source |
|---|---|
| V1 prospective PCA | `data/oal_validation/derived/formal_validation_statistics.json`; associated CSV tables |
| V2 prospective PCA | `data/oal_validation/derived_v2/formal_validation_statistics.json`; associated CSV tables |
| V2 retrospective Endface-Hybrid | `data/oal_validation/derived_v2/endface_hybrid_retrospective/statistics.json`; specimen and observation CSV tables |
| V3 prospective Endface-Hybrid | `data/oal_validation/v3_formal/v3_cv_observations.csv`; `data/oal_validation/derived/manual_reference_summary.csv`; `docs/research/v3_formal_validation/V3_FORMAL_VALIDATION_PLAN.md` |
| Guard-band analysis | V3 specimen means derived from the two V3 source tables; `docs/research/2026-09-17_v3_formal_performance_and_guard_band_analysis.md` |
| Diagnostic and development results | Preserved summaries and CSV tables under `data/oal_validation/post_v1_diagnostics/` |

## V3 calculation correction

The V3 narrative summaries report MAE, RMSE, and P95 absolute error across the 180 individual CV observations. That basis is inconsistent with the frozen statistical plan and Chapter 3, which define the unique specimen as the primary agreement unit. The six prospective targets apply to the 60 specimen errors

\[
e_i=\bar{C}_i-\bar{M}_i.
\]

Recalculation from the preserved V3 observation table and frozen manual-reference summary gives:

| Specimen-level V3 endpoint | Correct value |
|---|---:|
| Bias | -0.000435 in |
| MAE | 0.001517 in |
| RMSE | 0.001794 in |
| Nearest-rank P95 absolute error | 0.003170 in |
| Maximum absolute error | 0.003913 in |

Availability remains an attempt-level result (180/180), and P95 repositioning remains the nearest-rank result from 180 pooled pairwise differences (0.000633 in).

The V3 plan contains six quantitative criteria. V3 met availability, absolute-bias, RMSE, maximum-absolute-error, and P95-repositioning criteria. It did not meet the P95 absolute-error criterion. V3 therefore met five of six quantitative criteria. The separate zero-false-pass preference was not met because one unguarded false pass was observed.

## Drafting controls

- Keep all reported dimensional results within the OAL-only thesis scope.
- Identify V1 PCA and V2 PCA as prospective results.
- Identify V2 Endface-Hybrid as retrospective and do not treat it as a prospective validation.
- Identify V3 Endface-Hybrid as the prospective result of the frozen estimator and controlled-presentation configuration.
- Keep the guard-band analysis explicitly exploratory and post hoc.
- Report Chapter 4 results descriptively; reserve causal interpretation and industrial recommendations for Chapter 5.
