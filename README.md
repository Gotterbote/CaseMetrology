# CaseMetrology

Research platform for the Kansas State University M.S. thesis **Engineering Evaluation of an Embedded Computer-Vision System for Static Dimensional Screening of Cartridge-Case Overall Length** by Timmy D. Bell.

The formal study evaluates cartridge-case overall length (OAL) under static, single-operator conditions. It combines a backlit IMX296 global-shutter camera and 16 mm lens, a Jetson Orin Nano, calibrated dimensional conversion, controlled specimen presentation, and an independent manual reference process. The October 2026 committee manuscript was distributed separately and is authoritative for the final research narrative. The advisor-review manuscript retained in this repository is an earlier snapshot.

> **Status:** V1–V3 formal evaluation complete. This is a graduate research prototype. The evidence does not validate autonomous production inspection, unconditional final acceptance, moving-part measurement, or production throughput.

## Formal result

The study used a frozen cohort of 60 cases selected from 235 source cases, with three randomized, independent placements per prospective configuration. Five development specimens were excluded from the formal cohort. Specimen means (n = 60) are the primary unit for agreement with the accepted three-round manual reference. The 180 pooled within-specimen pairwise differences describe repositioning; they are related observations, not 180 independent specimens.

| Measure | Original V1 | Final V3 |
| --- | ---: | ---: |
| Valid measurement availability | 180/180 | 180/180 |
| Mean signed bias | +0.001613 in | −0.000435 in |
| RMSE | 0.002205 in | 0.001794 in |
| P95 absolute specimen error | 0.003960 in | 0.003170 in |
| P95 pairwise repositioning difference | 0.004831 in | 0.000633 in |
| Quantitative criteria met | 1 of 6 | 5 of 6 |
| Unguarded false passes / false fails | 1 / 8 | 1 / 3 |

The V1-to-V3 P95 repositioning difference fell by approximately 86.9% at the **system level**. The full sequence changed both estimation and presentation, so the reduction cannot be assigned entirely to one component. V3 missed the P95 absolute-error target of 0.0030 in by 0.000170 in. Its remaining false pass prevents an unconditional acceptance claim under the nominal 0.9900–1.0100 in interval.

A post-validation guard-band analysis explored secondary review near the specification limits. Candidate margins were selected and evaluated on the same enriched cohort; they are not validated production rules or estimates of future false-pass probability.

## Start with the evidence

The [thesis defense evidence guide](docs/research/THESIS_DEFENSE_START_HERE.md) maps the prospective V3 plan, pre-acquisition freeze, calibration and reference records, raw images, formal observations, analysis scripts, results, and interpretation boundaries.

Key records:

- [V3 formal validation plan](docs/research/v3_formal_validation/V3_FORMAL_VALIDATION_PLAN.md)
- [V3 final freeze evidence](docs/research/v3_formal_validation/V3_FINAL_FREEZE_EVIDENCE.md) and [measurement-system manifest](docs/research/v3_formal_validation/V3_MEASUREMENT_SYSTEM_MANIFEST.sha256)
- [V3 formal images and observations](data/oal_validation/v3_formal/)
- [V1–V3 engineering progression](docs/research/2026-09-17_v1_v2_v3_engineering_progression.md)
- [V3 results and exploratory guard-band record](docs/research/2026-09-17_v3_formal_performance_and_guard_band_analysis.md)

## Measurement architecture

The system uses a static backlit side view of the case on a clear measurement plane. The original V1 and V2 formal phases used a PCA silhouette-extrema estimator. V3 used the frozen Endface-Hybrid estimator with controlled seating and roll orientation. Spatial and directional calibration converts accepted pixel endpoint separation to inches. Acquisition controls, blank images, specimen IDs, randomized order, and file integrity records support traceability.

The V3 formal capture was **capture-only**: the primary estimator was not run or displayed during acquisition. The frozen estimators were applied after all 180 scheduled images had been collected.

## Scope and limitations

The work evaluates one operator and one static optical configuration on an intentionally enriched cohort. It does not estimate production yield. The manual comparator has finite uncertainty. The source of residual V3 absolute disagreement was not uniquely identified. The V2 Endface-Hybrid analysis is retrospective, and the guard-band analysis is post hoc.

Future experiments can compare a suitable telecentric lens under the existing presentation procedure, then test keyed mechanical seating under the same lens. Each configuration needs its own calibration and prospective evaluation. Production handling, multiple operators, motion, throughput, and long-term robustness require separate studies.

## Repository map

- `docs/research/`: protocols, freezes, decisions, formal summaries, and thesis support
- `data/oal_validation/`: cohort, manual reference, formal CV observations, and images
- `scripts/` and `src/`: acquisition, estimation, calibration, audit, and analysis code
- `tests/`: software tests for measurement and supporting components

Earlier development notes remain in the repository for historical traceability. [README_V3_FORMAL_SUPPORT.md](README_V3_FORMAL_SUPPORT.md) is a historical pre-acquisition setup note.

## Researcher

Timmy Bell  
M.S. Integrated Systems Design and Dynamics  
Kansas State University, College of Technology and Aviation, Salina
