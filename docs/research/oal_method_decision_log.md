---
title: OAL Method Decision Log
project: CaseMetrology
researcher: Timmy Bell
status: Living document
last_updated: 2026-08-19
---

# OAL Method Decision Log

This file records major research and implementation decisions. It is not a chronological terminal log. Each entry identifies the decision, evidence basis, alternatives, limitations, and status.

---

## OAL-D001 — Preserve the PCA estimator as an unchanged comparator

- **Date:** 2026-07-31
- **Decision:** Develop candidate estimators in separate modules and leave `src/measurement/topdown_oal.py` unchanged.
- **Rationale:** A stable comparator is required to attribute differences to endpoint estimation rather than simultaneous changes to segmentation or public interfaces.
- **Alternatives considered:** Replace the existing function in place.
- **Evidence:** Trial 03 and Trial 05 baseline results at repository snapshot `cb3bf01`.
- **Status:** Active.

## OAL-D002 — Reuse accepted masks and images before collecting new data

- **Date:** 2026-07-31
- **Decision:** Evaluate new estimators on the existing 10 Trial 03 and 17 Trial 05 records before additional physical acquisition.
- **Rationale:** Paired reuse isolates estimator behavior, avoids introducing reacquisition variability, and conserves research effort.
- **Limitations:** Reuse cannot establish generalizability to new cases, positions, or imaging conditions.
- **Status:** Completed for binary geometry and first grayscale subpixel estimator.

## OAL-D003 — Disable the fixture-width gate for accepted-mask endpoint comparisons

- **Date:** 2026-07-31
- **Decision:** Set `minimum_fixture_width_ratio = 0.0` only in comparison scripts processing previously accepted masks.
- **Rationale:** Object/fixture acceptance had already occurred; retaining the gate caused all 27 records to fail before estimator evaluation and confounded the intended endpoint-only comparison.
- **Safeguard:** The production/default estimator parameter remains unchanged.
- **Status:** Active for accepted-mask retrospective comparisons only.

## OAL-D004 — Retain the 90° sensitivity candidate

- **Date:** 2026-07-31
- **Decision:** Retain the algorithmically identified 90° sensitivity capture in primary statistics and report it rather than automatically excluding it.
- **Rationale:** Excluding a difficult capture after observing its effect would bias the comparison.
- **Evidence:** Binary comparison identified `capture_02_mask` as the largest absolute deviation from the 90° median.
- **Status:** Active.

## OAL-D005 — Classify binary geometry as exploratory

- **Date:** 2026-07-31
- **Decision:** Do not replace the PCA baseline with the binary-geometry estimator.
- **Evidence:** Static SD improved 48.54%, but Trial 05 orientation-group median range increased 28.36% from `1.752720470 px` to `2.249772382 px`.
- **Visual evidence:** No widespread gross fit failure; likely orientation-dependent rasterization remained.
- **Status:** Final for estimator version represented by commit `8bb3a9f` and comparison evidence commit `e690127`.

## OAL-D006 — Investigate grayscale subpixel localization

- **Date:** 2026-07-31
- **Decision:** Develop a grayscale edge estimator initialized from accepted-mask geometry.
- **Rationale:** Binary line fitting remained sensitive to integer-grid boundaries.
- **Implementation:** Commit `4dca7b1`.
- **Status:** Completed for maximum-gradient version.

## OAL-D007 — Classify maximum-gradient subpixel geometry as exploratory

- **Date:** 2026-07-31
- **Decision:** Do not replace the PCA baseline with the first grayscale subpixel estimator.
- **Evidence:** Trial 05 orientation-group median range increased 64.75% to `2.887565849 px`; Trial 05 SD increased 69.54%.
- **Visual evidence:** The strongest local gradient did not consistently represent the same physical edge across orientation, especially at 70° and 90°.
- **Status:** Final for the version represented by commit `4dca7b1`.

## OAL-D008 — Retain PCA as the provisional working baseline

- **Date:** 2026-07-31
- **Decision:** Continue using PCA plus extreme mask pixels as the comparator, not as a declared final metrology solution.
- **Rationale:** It produced the smallest range among Trial 05 orientation-group medians of the three evaluated methods.
- **Limitation:** It still exhibits `1.752720470 px` orientation dependence and has not been validated for absolute accuracy.
- **Status:** Superseded on 2026-08-13 by OAL-D013. Retained as a valid historical development decision.

## OAL-D009 — Define the next edge physically, not only numerically

- **Date:** 2026-07-31
- **Decision:** Develop a mask-anchored, polarity-aware normalized intensity-crossing estimator.
- **Required behavior:** Use local interior/exterior plateaus, a consistent crossing criterion, and rejection of ambiguous multi-transition profiles.
- **Rationale:** Subpixel resolution without a consistent edge definition increased orientation bias.
- **Status:** Completed and subsequently dispositioned through later subpixel development; the candidate did not replace the final primary estimator. See OAL-D012 and OAL-D013.

## OAL-D010 — Defer additional physical acquisition

- **Date:** 2026-07-31
- **Decision:** Do not collect new OAL images until the next estimator has been compared on the existing 27 records.
- **Rationale:** The current unresolved issue is algorithmic edge definition; additional data would not isolate that cause.
- **Status:** Superseded after the planned estimator evaluation was completed; subsequent physical and prevalidation acquisition proceeded under later documented protocols.

## OAL-D011 — Temporarily select and freeze the geometry estimator

- **Date:** 2026-08-07
- **Decision:** Select the binary-geometry estimator as the primary OAL candidate at the then-current development stage and freeze that implementation for the next validation-preparation activities.
- **Rationale:** The geometry estimator substantially improved static repeatability relative to the PCA/extreme-mask development baseline and provided a physically motivated endpoint model.
- **Evidence:** `docs/research/2026-08-07_primary_oal_estimator_selection_and_freeze_record.md`, repository provenance `5d77dc6`.
- **Limitation:** This decision preceded later five-case physical-unit prevalidation comparison against manual measurements.
- **Status:** Superseded on 2026-08-13 by OAL-D013. Retained as a valid historical decision.

## OAL-D012 — Do not advance Subpixel Version 2 as the primary method

- **Date:** 2026-08-07
- **Decision:** Retain Subpixel Version 2 as diagnostic/exploratory rather than replacing the primary OAL candidate.
- **Rationale:** Diagnostic review identified optical and anchoring sensitivity that did not justify additional parameter tuning or advancement for the current thesis validation.
- **Evidence:** `docs/research/2026-08-07_subpixel_v2_diagnostic_review_and_disposition.md`, repository provenance `e8abd23`.
- **Status:** Final for the evaluated Subpixel Version 2 implementation.

## OAL-D013 — Select and freeze PCA/extreme-mask as the formal-validation estimator

- **Date:** 2026-08-13
- **Decision:** Select `src/measurement/topdown_oal.py` PCA/extreme-mask as the primary OAL pixel-length estimator for formal validation.
- **Rationale:** Five-case prevalidation comparison showed more favorable aggregate dimensional agreement for PCA/extreme-mask than for the geometry estimator. The five specimens remain development specimens and are excluded from the formal validation sample.
- **Evidence:** `docs/research/2026-08-13_prevalidation_oal_estimator_checkpoint.md` (`6e68cc5`) and `docs/research/2026-08-13_oal_pca_estimator_selection_and_freeze.md` (`8db408f`).
- **Supersedes:** OAL-D008 as a provisional-only designation and OAL-D011 as the temporary geometry selection.
- **Status:** Active and frozen for formal validation.

## OAL-D014 — Correct the calibration angle convention without refitting the calibration planes

- **Date:** 2026-08-13
- **Decision:** Correct the mapping between historical gauge-block orientation labels and the cartridge-case OAL measurement direction while leaving the accepted A-D spatial calibration planes unchanged.
- **Rationale:** The gauge-block analyzer reports the long-axis orientation while measuring the certified short dimension perpendicular to that axis; the PCA estimator reports the OAL measurement direction itself.
- **Implementation rule:** `effective_ppi = sqrt((PPI_90*cos(theta))^2 + (PPI_0*sin(theta))^2)`.
- **Evidence:** `docs/research/2026-08-13_oal_calibration_angle_convention_correction.md`, repository provenance `8fffefe`.
- **Safeguard:** No calibration refit, segmentation change, endpoint change, or PCA pixel-length change was made.
- **Status:** Active and frozen for formal validation.

## OAL-D015 — Accept the corrected PCA physical-unit pipeline after prospective verification

- **Date:** 2026-08-13
- **Decision:** Use the integrated segmentation → PCA pixel length → centroid/direction-aware calibration → inch conversion path for formal-validation preparation.
- **Rationale:** The corrected calibration-to-PCA implementation reproduced the independently calculated corrected results for the five prevalidation specimens without modifying the frozen PCA estimator.
- **Evidence:** `docs/research/2026-08-13_pca_production_pipeline_verification.md`, repository provenance `cc10723`.
- **Status:** Active.

## OAL-D016 — Preserve system failures as formal performance outcomes

- **Date:** 2026-08-15
- **Decision:** Distinguish `SYSTEM_FAILURE` from `PROTOCOL_INVALID`; do not automatically reacquire or replace a system failure.
- **Rationale:** Repeating failed acquisitions until a valid result appears would bias measurement-availability estimates and conceal operational failure behavior.
- **Evidence:** `docs/research/2026-08-15_formal_oal_validation_protocol_amendment.md`, repository provenance `a1a49f9`, with later formalization in the master protocol.
- **Status:** Active for formal validation.

## OAL-D017 — Freeze the prospective formal-validation protocol and statistical analysis plan

- **Date:** 2026-08-19
- **Decision:** Establish the formal validation design, data-disposition rules, experimental unit, agreement metrics, failure treatment, and primary acceptance criteria before formal validation data are collected.
- **Rationale:** Prospective control reduces post hoc methodological changes and protects the independence of the validation conclusions.
- **Evidence:** `docs/research/2026-08-19_formal_oal_validation_master_protocol.md` and `docs/research/2026-08-19_formal_oal_statistical_analysis_plan.md`, repository provenance `bce7f19`.
- **Status:** Active. Formal validation remains on hold pending required reference-calibration evidence and study preconditions.

## OAL-D018 — Keep network transport and dashboard functions outside the dimensional computation

- **Date:** 2026-08-19
- **Decision:** Treat office transfer, persistent indexing, and the engineering dashboard as supporting infrastructure only.
- **Rationale:** Network or dashboard availability must not influence an OAL value already computed and preserved locally on the Jetson.
- **Evidence:** `docs/research/2026-08-19_office_engineering_dashboard_integration.md`, repository provenance `78677cb`.
- **Status:** Active.

## OAL-D019 — Use the documented 16 mm CS-mount optical configuration for thesis and validation records

- **Date:** 2026-08-19
- **Decision:** Treat the Arducam HQ Lens CS2316ZM02, 16 mm effective focal length, CS mount as the supported optical configuration. Do not use the unsupported 25 mm recollection as thesis evidence.
- **Rationale:** The 2026-07-30 physical baseline documents CS2316ZM02/16 mm; repository history contains no 25 mm installation; direct visual inspection on 2026-08-19 was consistent with the documented lens and did not disturb the optical setup.
- **Evidence:** `docs/physical_configuration_baseline_2026-07-30.md` (`0803f24`) and `docs/research/2026-08-19_optical_configuration_continuity_verification.md` (`ea52b7c`).
- **Status:** Active and verified.
