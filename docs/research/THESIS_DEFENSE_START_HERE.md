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

The estimator source retains its development-era filename and header. The V3 freeze manifest identifies its exact SHA-256, and the post-acquisition analysis driver imports that frozen source. The name does not imply that formal V3 observations were used to tune it.

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

## Offline reproduction

For a smaller download, use `git clone --depth 1 https://github.com/Gotterbote/CaseMetrology.git` and record `git rev-parse HEAD`. A shallow clone omits earlier history; use a full clone when investigating historical commits. Run commands from the repository root.

### Recompute summary statistics without image processing

```bash
python3 scripts/summarize_v3_formal_results.py
```

This standard-library-only command reads the preserved V3 observations and accepted manual specimen means, validates cohort/round coverage, and prints JSON to standard output. It does not write files. The output includes input SHA-256 hashes. Optional `--output PATH` creates a new JSON file and refuses to replace an existing file or write inside the research checkout.

Agreement uses 60 specimen means; repositioning uses 180 related within-specimen absolute pairwise differences. P95 uses nearest rank. Compare unrounded calculations to six-decimal published values with an absolute tolerance of 0.0000005 inch; classification counts must match exactly. This recomputes statistics from saved measurements, not measurements from images or an independent validation of the manual reference.

### Reprocess preserved images in a disposable checkout

The recorded environment is Python 3.12.3, OpenCV 4.6.0, and NumPy 1.26.4. Other analysis scripts import SciPy (the July inventory records 1.11.4). The [Jetson environment record](../jetson_software_environment_2026-07-24.txt) and [Python inventory](../python_environment_manifest_2026-07-24.txt) document the original machine. The inventory contains distribution-specific packages and is not a portable pip requirements file. `requirements-dev.txt` lists development tools, not runtime dependencies. A clean installation on another platform has not been verified.

In a disposable checkout with compatible dependencies:

```bash
sha256sum -c docs/research/v3_formal_validation/V3_MEASUREMENT_SYSTEM_MANIFEST.sha256
python3 scripts/analyze_v3_formal_images.py
python3 scripts/summarize_v3_formal_results.py
```

The image processor reads the 180 formal images, session blanks, and frozen estimator/calibration sources. It **replaces** `data/oal_validation/v3_formal/v3_cv_observations.csv` and writes timestamped JSON under `data/oal_validation/v3_formal/diagnostics/`. Review `git diff` in that disposable checkout; do not commit regenerated evidence over the preserved records. The summarizer then calculates specimen-level statistics from the resulting CSV.

## Retained development backup

`scripts/analyze_fixture_rocking_generalization.py.pre_parser_fix` is retained as a development backup. It is not a formal V3 entry point; use the evidence map above. No research evidence was removed during documentation cleanup.
