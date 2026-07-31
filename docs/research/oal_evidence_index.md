---
title: Fixtureless OAL Research Evidence Index
project: CaseMetrology
researcher: Timmy Bell
status: Living index
last_updated: 2026-07-31
---

# Fixtureless OAL Research Evidence Index

## Status definitions

- **Accepted:** official controlled result suitable for use as a baseline or thesis result within its stated scope.
- **Exploratory:** informative algorithm-development evidence; not the accepted final measurement method.
- **Pending commit:** generated and reviewed but not yet stored in a repository commit.
- **Procedural:** reproducibility or validity record, not a measurement result.
- **Superseded/invalid:** output excluded from scientific interpretation for a documented reason.

## Evidence table

| Evidence ID | Description | Classification | Primary location | Repository provenance | Notes |
|---|---|---|---|---|---|
| OAL-E001 | Trial 03 static PCA repeatability, 10 captures | Accepted baseline | `data/oal_real/2026-07-31_trial_03_static/` | Present in repository snapshot `cb3bf01`; originating commit to verify | SD `0.050349452 px`; range `0.166581476 px` |
| OAL-E002 | Trial 03 research narrative | Accepted baseline | `docs/research/2026-07-31_fixtureless_real_oal_trial_03_static.md` | Present by `cb3bf01` | Defines static trial context and limitations |
| OAL-E003 | Trial 05 controlled-orientation PCA result, 17 accepted captures | Accepted baseline | `data/oal_real/2026-07-31_trial_05_controlled_orientation/` | `cb3bf01` | Group-median range `1.752720470 px`; 90° anomaly retained/flagged |
| OAL-E004 | Trial 05 research narrative | Accepted baseline | `docs/research/2026-07-31_fixtureless_real_oal_trial_05_controlled_orientation.md` | `cb3bf01` | Placement control and visual review record |
| OAL-E005 | Binary-geometry estimator implementation | Exploratory method | `src/measurement/topdown_oal_geometry.py` | `8bb3a9f` | PCA initialization; Huber-fitted sidewalls and end faces |
| OAL-E006 | Valid binary-estimator comparison code | Procedural | `scripts/compare_oal_estimators.py` | `1ee63b0` | Handles empty groups and disables fixture gate for accepted masks |
| OAL-E007 | Binary-geometry comparison results | Exploratory evidence | `data/oal_real/2026-07-31_geometry_estimator_comparison/` | `e690127` | Static SD improved; orientation range worsened |
| OAL-E008 | Binary-geometry contact sheets and overlays | Exploratory visual evidence | Same as OAL-E007 | `e690127` | No widespread gross fit failure observed |
| OAL-E009 | Grayscale subpixel estimator implementation | Exploratory method | `src/measurement/topdown_oal_subpixel.py` | `4dca7b1` | Maximum-gradient edge at subpixel profile spacing |
| OAL-E010 | Grayscale subpixel comparison summary and CSV | Exploratory evidence | `data/oal_real/2026-07-31_subpixel_estimator_comparison/` | Pending commit at time of documentation; analysis source commit `4dca7b1e39c5ed67c008eef430d9bc64eb2a4f50` | 27 rows; zero failed triplets; 27 flagged captures |
| OAL-E011 | Grayscale subpixel contact sheets and overlays | Exploratory visual evidence | Same as OAL-E010 | Pending commit at time of documentation | 70°/90° behavior supports inconsistent edge-feature selection |
| OAL-E012 | Consolidated estimator development summary | Research synthesis | `docs/research/2026-07-31_fixtureless_oal_estimator_development_summary.md` | Pending documentation commit | Integrates methods, statistics, limitations, and decisions |
| OAL-E013 | Binary-geometry estimator review | Research interpretation | `docs/research/2026-07-31_binary_geometry_oal_estimator_review.md` | Pending documentation commit | Candidate classified exploratory |
| OAL-E014 | Grayscale subpixel estimator review | Research interpretation | `docs/research/2026-07-31_grayscale_subpixel_oal_estimator_review.md` | Pending documentation commit | Candidate classified exploratory |
| OAL-E015 | Human visual review record | Research interpretation | `docs/research/2026-07-31_oal_estimator_visual_review_record.md` | Pending documentation commit | Records overlay checklist, observations, and limitations |
| OAL-E016 | Method decision log | Governance/traceability | `docs/research/oal_method_decision_log.md` | Pending documentation commit | Records why methods were retained, rejected, or planned |

## Invalid or superseded outputs

| Record ID | Event | Classification | Disposition |
|---|---|---|---|
| OAL-X001 | Binary comparison aborted with `StatisticsError: no median for empty data` | Invalid procedural run | Partial output not interpreted |
| OAL-X002 | Binary comparison reported 27 failures because accepted-mask analysis retained fixture-width gate | Invalid procedural run | Deleted and regenerated after comparison-scope correction |
| OAL-X003 | Commit attempt blocked by Black formatting hook | Procedural interruption | Formatting corrected; tests and valid analysis rerun |

## Claim-to-evidence map

| Research claim | Supporting evidence |
|---|---|
| PCA static SD is `0.050349452 px` | OAL-E001, OAL-E002 |
| PCA Trial 05 orientation-group median range is `1.752720470 px` | OAL-E003, OAL-E004 |
| Binary geometry improves static repeatability | OAL-E007, OAL-E013 |
| Binary geometry does not improve orientation invariance | OAL-E007, OAL-E008, OAL-E013 |
| Maximum-gradient subpixel localization does not improve orientation invariance | OAL-E010, OAL-E011, OAL-E014 |
| A visually plausible overlay can still represent an inconsistent physical edge | OAL-E011, OAL-E014, OAL-E015 |
| PCA remains the provisional comparator | OAL-E012, OAL-E016 |
| Next estimator must use a physically consistent normalized crossing | OAL-E012, OAL-E014, OAL-E016 |

## Maintenance instructions

1. Add one evidence row for each new controlled trial, estimator comparison, or formal visual review.
2. Record both the generating source commit and the evidence commit.
3. Do not label exploratory evidence as accepted without a documented decision entry.
4. Preserve invalid-run records when they affect reproducibility or interpretation.
5. Verify the originating commit for Trial 03 during the next repository-history review and replace the provisional snapshot reference.
