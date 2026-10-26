# Thesis Defense Evidence Guide

This guide maps the repository evidence for Timmy Bell's October 2026 M.S. thesis on **static cartridge-case overall-length measurement**. The committee manuscript was distributed separately and is the authoritative final narrative. The advisor-review PDF committed in September is an earlier manuscript snapshot.

## Research sequence

1. V1 prospectively tested the original PCA system and met one of six quantitative criteria.
2. Diagnostics and excluded development specimens informed fixture and estimator changes.
3. V2 prospectively evaluated the revised fixture with PCA. The later Endface-Hybrid analysis of preserved V2 images was retrospective.
4. V3 froze its estimator, presentation procedure, cohort, and analysis plan before formal acquisition. All 180 images were collected before estimator results were processed.
5. Guard-band analysis followed V3 and remains exploratory.

The 60-specimen cohort was intentionally enriched near the 0.9900–1.0100 in limits and reused for paired engineering comparisons. Each prospective phase had three independently randomized placements per specimen. The 60 specimen means are the primary agreement units. Pooled pairwise repositioning differences are descriptive related values.

## Evidence map

| Purpose | Record |
| --- | --- |
| Cohort and reference process | [Formal specimens](../../data/oal_validation/formal_validation_specimens.csv), [manual observations](../../data/oal_validation/manual_reference_observations.csv), and [reference summary](../../data/oal_validation/derived/manual_reference_summary.csv) |
| V1–V3 chronology | [Engineering progression](2026-09-17_v1_v2_v3_engineering_progression.md) |
| V3 prospective design and targets | [Formal validation plan](v3_formal_validation/V3_FORMAL_VALIDATION_PLAN.md) |
| Pre-acquisition freeze and source identity | [Freeze evidence](v3_formal_validation/V3_FINAL_FREEZE_EVIDENCE.md) and [SHA-256 manifest](v3_formal_validation/V3_MEASUREMENT_SYSTEM_MANIFEST.sha256) |
| V3 run order and observation results | [Run-order CSV](../../data/oal_validation/v3_formal/v3_cv_run_orders.csv) and [observation CSV](../../data/oal_validation/v3_formal/v3_cv_observations.csv) |
| Formal source images and session blanks | [V3 raw images](../../data/oal_validation/v3_formal/raw/) |
| Acquisition and processing | [V3 capture](../../scripts/run_v3_formal_capture.py), [post-acquisition processing](../../scripts/analyze_v3_formal_images.py), and [frozen Endface-Hybrid implementation](../../scripts/evaluate_oal_endface_hybrid_dev.py) |
| Results and decision analysis | [V3 performance and exploratory guard band](2026-09-17_v3_formal_performance_and_guard_band_analysis.md) |
| Software checks | [Tests](../../tests/) |

The [formal V3 plan](v3_formal_validation/V3_FORMAL_VALIDATION_PLAN.md) identifies the prospective criteria and exclusions. The [freeze record](v3_formal_validation/V3_FINAL_FREEZE_EVIDENCE.md) records the estimator hash and capture-only procedure. The raw directory contains the 180 formal case images and three session blank references.

## Principal result

| Endpoint | V3 observed | Retained target |
| --- | ---: | ---: |
| Availability | 180/180 | ≥99% |
| Absolute mean bias | 0.000435 in | ≤0.0010 in |
| RMSE | 0.001794 in | ≤0.0020 in |
| P95 absolute specimen error | 0.003170 in | ≤0.0030 in |
| Maximum absolute specimen error | 0.003913 in | ≤0.0040 in |
| P95 pairwise repositioning difference | 0.000633 in | ≤0.0020 in |

V3 met five of six quantitative criteria. Mean signed bias was −0.000435 in. The unguarded specimen-level classification produced one false pass and three false fails. Relative to V1, P95 repositioning was approximately 86.9% lower at the system level. Absolute disagreement with the manual reference remained larger than the repositioning difference.

## Interpretation boundaries

- The full V1-to-V3 change includes both estimator and presentation changes. The total improvement is not a causal estimate for one component.
- The same enriched cohort supported the post hoc guard-band analysis. The observed zero-false-pass margins are not validated production rules.
- One operator and static presentation were evaluated. Production yield, multiple-operator reproducibility, moving-part measurement, throughput, and long-term robustness were not established.
- Reference means have finite uncertainty, and the physical source of residual absolute disagreement remains unresolved.
