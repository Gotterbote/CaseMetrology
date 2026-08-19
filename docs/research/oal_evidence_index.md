---
title: OAL Research Evidence Index
project: CaseMetrology
researcher: Timmy Bell
status: Living index
last_updated: 2026-08-19
---

# OAL Research Evidence Index

## Status definitions

- **Accepted baseline:** controlled development or prevalidation result accepted as an official baseline within its stated scope.
- **Accepted calibration characterization:** accepted calibration evidence supporting the frozen dimensional-conversion method within its documented range and limitations.
- **Exploratory method:** implemented candidate method evaluated during development but not selected as the final formal-validation method.
- **Exploratory evidence:** quantitative development evidence used to compare or diagnose candidate methods.
- **Exploratory visual evidence:** diagnostic image or overlay evidence used for method development and interpretation.
- **Research synthesis:** document integrating multiple experimental or analytical results into a research-level interpretation.
- **Research interpretation:** documented interpretation of experimental, visual, or algorithmic evidence.
- **Procedural:** reproducibility, validity, or process-control evidence rather than a dimensional result.
- **Governance/traceability:** living research-control record preserving methodological decisions and their rationale.
- **Certified reference:** external dimensional-standard evidence supporting calibration or traceability.
- **Prevalidation:** engineering or measurement evidence intentionally collected before formal validation and excluded from primary formal-validation evidence where applicable.
- **Frozen method/configuration:** accepted configuration or method state intended to remain unchanged during formal validation.
- **Corrective governance:** documented prospective correction to methodology or interpretation made before formal validation while preserving historical evidence.
- **Verification:** evidence that integrated implementation behavior agrees with the intended frozen method or workflow.
- **Prospective protocol:** methodology, analysis, failure handling, or acceptance rules defined before the corresponding formal data are collected.
- **Supporting infrastructure:** system component supporting persistence, monitoring, or engineering use without altering the dimensional computation.
- **Superseded historical method:** historically valid method decision later replaced by a documented subsequent decision.
- **Superseded/invalid:** output not used for current scientific interpretation because it was superseded or invalidated for a documented reason.

## Evidence table

| Evidence ID | Description | Classification | Primary location | Repository provenance | Notes |
|---|---|---|---|---|---|
| OAL-E001 | Trial 03 static PCA repeatability, 10 captures | Accepted baseline | `data/oal_real/2026-07-31_trial_03_static/` | `0aa6464` | SD `0.050349452 px`; range `0.166581476 px` |
| OAL-E002 | Trial 03 research narrative | Accepted baseline | `docs/research/2026-07-31_fixtureless_real_oal_trial_03_static.md` | Present by `cb3bf01` | Defines static trial context and limitations |
| OAL-E003 | Trial 05 controlled-orientation PCA result, 17 accepted captures | Accepted baseline | `data/oal_real/2026-07-31_trial_05_controlled_orientation/` | `cb3bf01` | Group-median range `1.752720470 px`; 90° anomaly retained/flagged |
| OAL-E004 | Trial 05 research narrative | Accepted baseline | `docs/research/2026-07-31_fixtureless_real_oal_trial_05_controlled_orientation.md` | `cb3bf01` | Placement control and visual review record |
| OAL-E005 | Binary-geometry estimator implementation | Exploratory method | `src/measurement/topdown_oal_geometry.py` | `8bb3a9f` | PCA initialization; Huber-fitted sidewalls and end faces |
| OAL-E006 | Valid binary-estimator comparison code | Procedural | `scripts/compare_oal_estimators.py` | `1ee63b0` | Handles empty groups and disables fixture gate for accepted masks |
| OAL-E007 | Binary-geometry comparison results | Exploratory evidence | `data/oal_real/2026-07-31_geometry_estimator_comparison/` | `e690127` | Static SD improved; orientation range worsened |
| OAL-E008 | Binary-geometry contact sheets and overlays | Exploratory visual evidence | Same as OAL-E007 | `e690127` | No widespread gross fit failure observed |
| OAL-E009 | Grayscale subpixel estimator implementation | Exploratory method | `src/measurement/topdown_oal_subpixel.py` | `4dca7b1` | Maximum-gradient edge at subpixel profile spacing |
| OAL-E010 | Grayscale subpixel comparison summary and CSV | Exploratory evidence | `data/oal_real/2026-07-31_subpixel_estimator_comparison/` | Evidence commit `d67fe69`; analysis source commit `4dca7b1e39c5ed67c008eef430d9bc64eb2a4f50` | 27 rows; zero failed triplets; 27 flagged captures |
| OAL-E011 | Grayscale subpixel contact sheets and overlays | Exploratory visual evidence | Same as OAL-E010 | `d67fe69` | 70°/90° behavior supports inconsistent edge-feature selection |
| OAL-E012 | Consolidated estimator development summary | Research synthesis | `docs/research/2026-07-31_fixtureless_oal_estimator_development_summary.md` | `34784e0` | Integrates methods, statistics, limitations, and decisions |
| OAL-E013 | Binary-geometry estimator review | Research interpretation | `docs/research/2026-07-31_binary_geometry_oal_estimator_review.md` | `34784e0` | Candidate classified exploratory |
| OAL-E014 | Grayscale subpixel estimator review | Research interpretation | `docs/research/2026-07-31_grayscale_subpixel_oal_estimator_review.md` | `34784e0` | Candidate classified exploratory |
| OAL-E015 | Human visual review record | Research interpretation | `docs/research/2026-07-31_oal_estimator_visual_review_record.md` | `34784e0` | Records overlay checklist, observations, and limitations |
| OAL-E016 | Method decision log | Governance/traceability | `docs/research/oal_method_decision_log.md` | Originating commit `34784e0`; living document | Records why methods were retained, rejected, superseded, or frozen |

| OAL-E017 | Certified Mitutoyo Grade 0 gauge block, ID 253568, certificate T26A06624 | Certified reference | `docs/calibration_gauge_block_certificate_2026-01-21.txt` | `9866746` | Certified central length `1.0000024 in`; expanded uncertainty `2.4 microinches` for lengths up to 4 in |
| OAL-E018 | Physical camera, lens, backlight, Lexan, and optical-geometry baseline | Frozen method/configuration | `docs/physical_configuration_baseline_2026-07-30.md` | `0803f24` | Documents Arducam B0499, CS2316ZM02 16 mm CS lens, 8.625-in lens-front distance, locked acquisition controls, and fixture construction |
| OAL-E019 | Geometry-estimator primary selection/freeze at 2026-08-07 development stage | Superseded historical method | `docs/research/2026-08-07_primary_oal_estimator_selection_and_freeze_record.md` | `5d77dc6` | Valid historical decision; later superseded by PCA selection after additional prevalidation comparison |
| OAL-E020 | Subpixel Version 2 diagnostic review and disposition | Exploratory evidence | `docs/research/2026-08-07_subpixel_v2_diagnostic_review_and_disposition.md` | `e8abd23` | Candidate did not justify replacing the retained measurement approach |
| OAL-E021 | Formal spatial/directional OAL calibration characterization | Accepted calibration characterization | `docs/research/2026-08-07_formal_oal_calibration_analysis_and_disposition.md` | `300c696` | A-D spatial planes; E principal-direction and oblique holdouts; original oblique interpretation later superseded only for angle convention |
| OAL-E022 | Five-case prevalidation estimator checkpoint | Prevalidation | `docs/research/2026-08-13_prevalidation_oal_estimator_checkpoint.md` | `6e68cc5` | Five development specimens used for estimator comparison; excluded from formal validation sample |
| OAL-E023 | PCA/extreme-mask primary estimator selection and freeze | Frozen method/configuration | `docs/research/2026-08-13_oal_pca_estimator_selection_and_freeze.md` | `8db408f` | Final primary OAL pixel-length estimator selected before formal validation |
| OAL-E024 | Prevalidation measurement-assurance postcheck | Prevalidation | `docs/research/2026-08-13_prevalidation_measurement_assurance_postcheck.md` | `0173d10` | Same-session manual and optical checks; no gross reference or scale failure identified |
| OAL-E025 | Calibration angle-convention correction | Corrective governance | `docs/research/2026-08-13_oal_calibration_angle_convention_correction.md` | `8fffefe` | Preserves A-D planes and PCA estimator; corrects historical gauge-block orientation mapping before formal validation |
| OAL-E026 | Corrected PCA physical-unit production-pipeline verification | Verification | `docs/research/2026-08-13_pca_production_pipeline_verification.md` | `cc10723` | Frozen segmentation, PCA estimator, corrected calibration mapping, and physical-unit conversion verified together |
| OAL-E027 | Integrated one-command live OAL workflow verification | Verification | `docs/research/2026-08-14_live_integrated_oal_cycle_verification.md` | `c42476b` | Demonstrates integrated acquisition, measurement, artifact persistence, and supporting workflow |
| OAL-E028 | Formal OAL validation protocol amendment | Prospective protocol | `docs/research/2026-08-15_formal_oal_validation_protocol_amendment.md` | `a1a49f9` | Records frozen PCA estimator, calibration integration, and formal-validation protections |
| OAL-E029 | Formal OAL validation master protocol | Prospective protocol | `docs/research/2026-08-19_formal_oal_validation_master_protocol.md` | `bce7f19` | Prospective formal validation design, failure rules, data controls, and acceptance requirements |
| OAL-E030 | Formal OAL statistical analysis plan | Prospective protocol | `docs/research/2026-08-19_formal_oal_statistical_analysis_plan.md` | `bce7f19` | Defines experimental unit, bias, MAE, RMSE, empirical P95, availability, repeatability, agreement, and classification analyses |
| OAL-E031 | Formal caliper calibration-certificate review control | Prospective protocol | `docs/research/2026-08-19_formal_oal_calibration_certificate_review_template.md` | `650dce4` | Formal reference measurement remains on hold until required certificate evidence is reviewed |
| OAL-E032 | Read-only office engineering dashboard integration | Supporting infrastructure | `docs/research/2026-08-19_office_engineering_dashboard_integration.md` | `78677cb` | Supporting visualization and persistence layer; does not alter dimensional computation |
| OAL-E033 | Optical configuration continuity verification | Frozen method/configuration | `docs/research/2026-08-19_optical_configuration_continuity_verification.md` | `ea52b7c` | Confirms evidence supporting continued use of documented CS2316ZM02 16 mm CS-mount lens; no 25 mm installation found |

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
| PCA was the provisional comparator as of 2026-07-31 | OAL-E012, OAL-E016 |
| Geometry was temporarily selected during the 2026-08-07 development stage | OAL-E019 |
| PCA/extreme-mask was selected and frozen as the primary OAL estimator on 2026-08-13 | OAL-E022, OAL-E023 |
| The certified calibration reference is `1.0000024 in` | OAL-E017 |
| Effective image scale varies with image position and measurement direction | OAL-E021 |
| The calibration angle convention was corrected prospectively without refitting the spatial planes | OAL-E025 |
| The corrected PCA physical-unit measurement path was verified before formal validation | OAL-E026 |
| Formal validation methodology and primary statistical analysis were frozen prospectively | OAL-E028, OAL-E029, OAL-E030 |
| The supported validation optical configuration uses the documented CS2316ZM02 16 mm CS-mount lens | OAL-E018, OAL-E033 |
| A physically consistent normalized-crossing estimator was identified as the next development direction on 2026-07-31; subsequent development did not select that approach for formal validation | OAL-E012, OAL-E014, OAL-E016, OAL-E020, OAL-E023 |

## Maintenance instructions

1. Add one evidence row for each new controlled trial, estimator comparison, or formal visual review.
2. Record both the generating source commit and the evidence commit.
3. Do not label exploratory evidence as accepted without a documented decision entry.
4. Preserve invalid-run records when they affect reproducibility or interpretation.
5. Verify the originating commit for Trial 03 during the next repository-history review and replace the provisional snapshot reference.
