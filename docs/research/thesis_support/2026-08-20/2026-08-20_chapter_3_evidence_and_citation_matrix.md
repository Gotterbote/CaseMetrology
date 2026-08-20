---
title: Chapter 3 Evidence and Citation Matrix
project: CaseMetrology
researcher: Timmy D. Bell
status: Working thesis-support matrix
date: 2026-08-20
scope: K-State M.S. Integrated Systems Design & Dynamics thesis — OAL only
---

# Chapter 3 Evidence and Citation Matrix

## Purpose

This matrix separates five kinds of support for Chapter 3:

1. **Repository evidence** — CaseMetrology records, code, data, protocols, certificates, and Git provenance.
2. **External scholarly citation** — peer-reviewed or authoritative technical literature supporting general scientific or statistical concepts.
3. **Manufacturer/standards citation** — authoritative source for hardware specifications or recognized metrology standards.
4. **Pending evidence** — information that cannot be finalized until a certificate, formal dataset, or physical study condition exists.
5. **Original method statement** — a CaseMetrology-specific design choice that should be supported by the repository rather than presented as a general literature claim.

Repository evidence demonstrates what was actually done. External literature supports general principles. One should not be substituted for the other.

## Evidence-status vocabulary

- **SUPPORTED NOW** — repository evidence is sufficient for the project-specific statement.
- **EXTERNAL CITATION REQUIRED** — a general scientific/statistical/metrology statement should carry an external source.
- **MANUFACTURER/STANDARD SOURCE** — use an authoritative product datasheet or standard for a specification/general standard claim.
- **CERTIFICATE PENDING** — do not finalize the claim until the applicable calibration certificate is reviewed.
- **FORMAL DATA PENDING** — methodology may be written prospectively, but results cannot be claimed yet.
- **PHYSICAL/CONFIGURATION VERIFIED** — physical configuration has a documented evidence chain.
- **NO EXTERNAL CITATION NEEDED** — thesis is describing the study's own procedure or implementation.
- **THESIS CORRECTION REQUIRED** — prior draft language must be reconciled to the evidence before submission.

## Chapter 3 matrix

| Section | Claim / content to support | Repository evidence | External source need | Recommended external source | Current disposition / action |
|---|---|---|---|---|---|
| **3.1 Research Methodology Overview** | Study is an engineering validation of a frozen CV OAL method against an independent manual reference process | `2026-08-19_formal_oal_validation_master_protocol.md`; `2026-08-19_formal_oal_statistical_analysis_plan.md`; OAL-E029/E030 | General experimental-design principles benefit from citation | Montgomery, *Design and Analysis of Experiments* | **SUPPORTED NOW** for project design; add one DOE source if discussing prospective control/randomization as a general methodology |
| **3.1** | Development/prevalidation observations are not formal validation results | Master protocol; estimator freeze records; evidence index; decision log | No external citation needed for this project rule | None | **SUPPORTED NOW** |
| **3.2 CaseMetrology System Architecture** | Jetson performs image acquisition and OAL computation; office systems provide persistence/monitoring without changing the result | architecture document; workflow/transport/receiver source; OAL-E032 | No external citation needed for architecture as built | None | **SUPPORTED NOW** |
| **3.3.1 Embedded Computing Platform** | NVIDIA Jetson Orin Nano Super Developer Kit used for system execution | runtime/system records; research preflight; hardware records | Manufacturer source recommended if hardware specifications are stated | NVIDIA official Jetson Orin Nano Super Developer Kit documentation | **SUPPORTED NOW** for identity/runtime |
| **3.3.1** | aarch64 L4T R39 rev 2.0; 15 W mode; Python 3.12.3; OpenCV 4.6.0; NumPy 1.26.4 | verified runtime/environment records | No external source required for observed installed versions | Optional software citations only if required by thesis style | **SUPPORTED NOW** |
| **3.3.2 Camera and Optical Configuration** | Arducam B0499 / IMX296 global-shutter camera; 1456×1088 acquisition; 44 fps acquisition configuration | camera-control baseline; physical configuration baseline; acquisition metadata | Manufacturer source recommended for sensor/global-shutter/product specifications | Arducam B0499 IMX296 official datasheet | **SUPPORTED NOW** |
| **3.3.2** | Lens is Arducam HQ Lens CS2316ZM02, 16 mm effective focal length, CS mount | physical configuration baseline; optical continuity verification; OAL-E018/E033; `ea52b7c` | Manufacturer source optional if quoting lens design specifications | Arducam manufacturer record | **PHYSICAL/CONFIGURATION VERIFIED**; do not use unsupported 25 mm recollection |
| **3.3.2** | Lens-front-to-measurement-plane distance = 8.625 in | physical configuration baseline | No external citation needed | None | **SUPPORTED NOW** |
| **3.3.3 Backlighting and Specimen Arrangement** | VALIKIY 24 V, 36 W backlight; Lexan working surface 0.250 in nominal; locator 0.125 in nominal | physical configuration baseline | No external source needed for observed configuration | Manufacturer source only if broader product claims are made | **SUPPORTED NOW** |
| **3.3.3** | Exact external dimensions of installed Lexan locator | baseline explicitly states dimensions were not recorded | Not a citation issue | None | **DO NOT INVENT** |
| **3.3.4 Software Environment and Configuration Control** | Git preserves research-relevant software/configuration history | Git repository; evidence index; decision log | No external citation needed for what the study did | None | **SUPPORTED NOW** |
| **3.3.5 Networked Data Persistence and Engineering Monitoring** | Local Jetson artifacts authoritative; durable outbox; SHA-256 verification; idempotent receiver; read-only dashboard | transport/receiver code; tests; dashboard integration record; OAL-E032 | No external citation required for implemented architecture | None | **SUPPORTED NOW** |
| **3.4 Image Acquisition and Segmentation** | Blank subtraction → 5×5 Gaussian blur → Otsu threshold → 3×3 opening/closing → largest connected component | `src/image_processing/oal_segmentation.py`; formal CV acquisition protocol; OAL-E026 | Otsu concept should be cited; morphology/Gaussian operations benefit from standard image-processing source | Otsu (1979); Gonzalez & Woods or equivalent | **SUPPORTED NOW + EXTERNAL CITATION REQUIRED** |
| **3.4** | Otsu thresholding automatically selects a gray-level threshold from histogram class separation | implementation uses Otsu | Scholarly citation required | Otsu, 1979, DOI 10.1109/TSMC.1979.4310076 | **CITE** |
| **3.4** | Morphological opening/closing and connected-component filtering suppress small artifacts / isolate primary object | source code demonstrates operations | Citation recommended if explanatory language goes beyond listing operations | Standard digital-image-processing text | **CITE** |
| **3.5 Overall-Length Measurement Algorithm** | PCA establishes/refines specimen longitudinal measurement direction | `src/measurement/topdown_oal.py`; development records; OAL-E023 | PCA conceptual description requires citation | Jolliffe & Cadima (2016), DOI 10.1098/rsta.2015.0202 | **SUPPORTED NOW + CITE PCA CONCEPT** |
| **3.5** | OAL pixel length is defined from extreme accepted-mask projections along refined PCA axis | estimator implementation and freeze record | Exact endpoint definition is project method | None | **SUPPORTED NOW** |
| **3.5** | Geometry and subpixel alternatives were explored but not selected for formal validation | OAL-E005–E015, E019/E020/E022/E023; decision log | No external citation needed | None | **SUPPORTED NOW** |
| **3.5** | Geometry estimator temporarily selected Aug. 7 and later superseded by PCA Aug. 13 | OAL-E019; OAL-E022/E023; OAL-D011/D013 | No external citation needed | None | **SUPPORTED NOW** |
| **3.6 Spatial Calibration Method** | Certified gauge-block central length = 1.0000024 in | certificate T26A06624; OAL-E017 | Certificate is primary evidence | Certificate; ASME B89.1.9 for context | **SUPPORTED NOW** |
| **3.6** | Gauge-block certificate basis is ASME B89.1.9-2002 | certificate transcription | Cite the version actually named by the certificate | ASME B89.1.9-2002 | **SUPPORTED NOW** |
| **3.6** | Current general gauge-block standard is ASME B89.1.9-2023 | external contextual fact | Standard source needed only if current practice is discussed | ASME B89.1.9-2023 | Optional contextual citation |
| **3.6** | PPI varies with position and measurement direction; separate first-order planes were fit | formal calibration characterization; OAL-E021 | No external citation required for observed project result | General calibration source optional | **SUPPORTED NOW** |
| **3.6** | Frozen calibration equations | calibration record and implementation | No external citation required | None | **SUPPORTED NOW** |
| **3.6** | Correct `PPI_90` Y coefficient is `0.00442714650` | calibration record, correction record, source | No external citation | None | **THESIS CORRECTION REQUIRED** if any draft still contains `0.000436889756` |
| **3.6** | Effective PPI = sqrt((PPI_90 cosθ)^2 + (PPI_0 sinθ)^2) | angle-convention correction; implementation; OAL-E025/E026 | No external citation required for project mapping | None | **SUPPORTED NOW** |
| **3.6** | Corrected oblique holdout residual ≈ -0.000412622 in | Aug. 13 correction record | No external citation | None | **SUPPORTED NOW** |
| **3.6** | Calibration uncertainty/measurement-model terminology | certificate plus formal calibration records | Authoritative metrology citation recommended | JCGM 100:2008; JCGM 200:2012 | **CITE** |
| **3.7 Prevalidation Engineering and Method Freeze** | Development and formal validation separated; validation-set retuning prohibited | master protocol; decision log; estimator freeze | General DOE citation helpful | Montgomery or equivalent | **SUPPORTED NOW** |
| **3.7.1** | Prevalidation specimens 121, 146, 178, 187, 197 excluded from formal validation sample | estimator checkpoint/freeze records | No external citation | None | **SUPPORTED NOW** |
| **3.7.2–3.7.3** | Measurement-affecting changes prohibited once formal validation begins | formal protocols; deviation policy | No external citation required | None | **SUPPORTED NOW** |
| **3.8 Specimen Population and Screening** | Population contains 235 laser-etched specimens with IDs 1–235 | screening schema/data and protocols | No external citation | None | **SUPPORTED NOW** |
| **3.8** | Screening characterizes population before selection and is not part of formal reference mean | screening/master protocols | No external citation | None | **SUPPORTED NOW** |
| **3.8.2** | Completed screening distribution | no formal readings yet | Not an external-citation issue | None | **FORMAL DATA PENDING** |
| **3.9 Formal Validation Sample Selection** | Planned n=60 stratified random sample | master protocol/sample design | General sampling rationale can be cited | Cochran, *Sampling Techniques*, or accepted sampling text | **SUPPORTED PROSPECTIVELY** |
| **3.9** | Exact strata boundaries and allocation | depend on completed screening distribution | No external citation | None | **FORMAL DATA PENDING** |
| **3.9** | Intentionally short/long specimens not automatically excluded | formal sampling/protocol decision | No external citation | None | **SUPPORTED PROSPECTIVELY** |
| **3.9** | Reproducible programmatic selection with documented seed/ranking | selection infrastructure/protocol | No external citation required | None | **SUPPORTED PROSPECTIVELY** |
| **3.10 Manual Reference Measurement Method** | Mitutoyo 500-197-30 / CD-8"ASX, 0–8 in, 0.0005-in resolution | study records | Manufacturer citation recommended | Mitutoyo official product information | **SUPPORTED for identity/resolution**; actual calibrated performance must come from certificate |
| **3.10** | Serial B23090910 and formal calibration status | project protocol/template | Actual certificate required | Incoming accredited certificate | **CERTIFICATE PENDING** |
| **3.10** | Five pre + five post check-standard readings with removal/repositioning | formal manual/session protocols | No external citation | None | **SUPPORTED PROSPECTIVELY** |
| **3.10** | Check-standard assigned value 1.0000024 in | gauge-block certificate | Certificate primary; VIM/GUM useful terminology | T26A06624; JCGM 200/JCGM 100 | **SUPPORTED NOW** |
| **3.10** | Final `E_limit`, `R_limit`, `D_limit`, and any certificate-derived correction/decision rule | certificate review protocol | GUM/JCGM 106 relevant | JCGM 100; JCGM 106 | **CERTIFICATE PENDING** |
| **3.10.4** | Repeatability versus reproducibility terminology; single-operator limitation | design/protocol | Authoritative terminology citation recommended | JCGM 200:2012; optionally ISO 5725 | **CITE** |
| **3.11 Computer-Vision Validation Measurement Method** | 60 specimens × 3 planned attempts = 180 CV opportunities; full removal/repositioning | formal CV protocol/master protocol | No external citation | None | **SUPPORTED PROSPECTIVELY** |
| **3.11** | `VALID`, `SYSTEM_FAILURE`, `PROTOCOL_INVALID`; system failure not automatically replaced | CV/failure/deviation protocols; OAL-D016 | No external citation | None | **SUPPORTED PROSPECTIVELY** |
| **3.11** | At least two valid CV replicates required for specimen-level agreement; no imputation | SAP/master protocol | No external citation required | None | **SUPPORTED PROSPECTIVELY** |
| **3.12 Randomization and Replication** | Independent manual/CV run orders; three rounds; full repositioning | run-order protocol; seeds | General randomization/replication rationale should be cited | Montgomery or equivalent DOE text | **SUPPORTED NOW + CITE GENERAL PRINCIPLE** |
| **3.12** | Manual seed 2026081901; CV seed 2026081902 | randomization protocol | No external citation | None | **SUPPORTED NOW** |
| **3.12.3** | Experimental unit is specimen (n=60), not 180 replicate observations | SAP | General experimental-unit concept benefits from citation | DOE/statistics reference | **SUPPORTED NOW + CITE GENERAL PRINCIPLE** |
| **3.13 Environmental and Measurement-Assurance Controls** | Environmental observations recorded; no automatic thermal correction currently planned | environmental protocol | GUM/VIM appropriate for uncertainty/environmental influence language | JCGM 100; JCGM 200 | **SUPPORTED PROSPECTIVELY + CITE** |
| **3.13** | Calibrated Digi-Sense thermometer/probe traceability | equipment/protocol | Actual certificate required | Instrument certificate | **CERTIFICATE PENDING** before calling formal readings traceable |
| **3.13.1** | Pre/post reference checks support session assurance | session acceptance protocol | General terminology may cite VIM/GUM | JCGM 200/JCGM 100 | **SUPPORTED PROSPECTIVELY** |
| **3.14 Data Integrity, Traceability, and Protocol Deviations** | Raw observations separate from derived data; deviations explicit; no outlier deletion solely for convenience | dataset schema; deviation policy; master protocol | No external citation required for project governance | Optional research-data-integrity source | **SUPPORTED NOW** |
| **3.14** | SHA-256 used for artifact integrity in applicable workflows | manifests; transport code; research records | No external citation necessary for project use | Optional cryptographic standard only if discussing SHA-256 properties | **SUPPORTED NOW** |
| **3.15 Statistical Analysis** | Signed error, MAE, RMSE, empirical nearest-rank P95, max error | frozen SAP | Formulas can be stated as prespecified analysis; external stats source optional | Standard statistics text if desired | **SUPPORTED NOW** |
| **3.15.1** | Mean bias and confidence interval | SAP | General statistical source advisable if CI details are explained | Standard statistics text | **CITE IF NEEDED** |
| **3.15.5** | Bland–Altman-style agreement; correlation is not evidence of agreement | SAP | Primary scholarly citation required | Bland & Altman (1986), DOI 10.1016/S0140-6736(86)90837-8 | **CITE** |
| **3.15.6** | Availability = VALID / (VALID + SYSTEM_FAILURE) | SAP; project-defined metric | No external citation | None | **SUPPORTED NOW** |
| **3.15.7** | Repositioning repeatability using pairwise absolute differences; pairs not independent specimens | SAP | Repeatability terminology source recommended | JCGM 200; optionally ISO 5725 | **SUPPORTED NOW + CITE TERMINOLOGY** |
| **3.15.9** | False-pass/false-fail classification; near-limit rule should account for reference uncertainty | SAP | Conformity-assessment source strongly recommended | JCGM 106:2012 | **CITE**; final project rule remains certificate-dependent |
| **3.15.10** | High correlation can coexist with poor method agreement | SAP | Bland–Altman primary source | Bland & Altman (1986) | **CITE** |
| **3.16 Validation Acceptance Criteria** | ≥99% availability; P95 repositioning ≤0.002 in; abs bias ≤0.001 in; RMSE ≤0.002 in; P95 abs error ≤0.003 in; max abs error ≤0.004 in | prospective master protocol/SAP; OAL-E029/E030 | Thresholds are project-specific; do not attribute them to literature unless directly supported | JCGM 106 only for general conformity context | **SUPPORTED NOW as prospectively frozen project criteria** |
| **3.16.7** | Zero false passes preferred; confirmed false pass blocks unconditional acceptance absent predefined rule | SAP/master protocol | JCGM 106 supports decision-rule context | JCGM 106:2012 | **SUPPORTED NOW + CITE GENERAL CONTEXT** |
| **3.16.8** | Unresolved material deviations prevent unconditional validation conclusion | deviation/master protocol | No external citation | None | **SUPPORTED NOW** |
| **3.17 Methodological Limitations** | Single operator means study does not estimate between-operator reproducibility | protocol/design | VIM/ISO terminology supports distinction | JCGM 200; optionally ISO 5725 | **SUPPORTED NOW + CITE TERMINOLOGY** |
| **3.17** | Manual reference is not error-free truth; it has uncertainty, resolution, repeatability, calibration limitations | reference framework | Strong metrology citation required | JCGM 100; JCGM 200 | **CITE** |
| **3.17** | Static fixture limits generalization to conveyors/dynamic production | study design | No external citation | None | **SUPPORTED NOW** |
| **3.17** | Validation applies only to documented optical/fixture/software configuration | freeze/configuration records | No external citation | None | **SUPPORTED NOW** |
| **3.17** | Thesis validates OAL only; other case dimensions remain future work | scope records/master protocol | No external citation | None | **SUPPORTED NOW** |
| **3.17** | Finite n=60 and empirical P95/max error do not establish universal worst-case performance | SAP/design | General statistical citation useful | Standard statistical inference text | **CITE GENERAL LIMITATION if stated formally** |

## Priority external references

### Tier 1 — should almost certainly appear in the thesis

- **Otsu thresholding:** Nobuyuki Otsu. “A Threshold Selection Method from Gray-Level Histograms.” *IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), 62–66, 1979. DOI: 10.1109/TSMC.1979.4310076.
- **Principal component analysis:** Ian T. Jolliffe and Jorge Cadima. “Principal component analysis: a review and recent developments.” *Philosophical Transactions of the Royal Society A*, 374(2065), 20150202, 2016. DOI: 10.1098/rsta.2015.0202.
- **Measurement agreement:** J. Martin Bland and Douglas G. Altman. “Statistical Methods for Assessing Agreement Between Two Methods of Clinical Measurement.” *The Lancet*, 327(8476), 307–310, 1986. DOI: 10.1016/S0140-6736(86)90837-8.
- **Measurement uncertainty:** JCGM 100:2008, *Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM)*. DOI: 10.59161/JCGM100-2008E.
- **Metrology vocabulary:** JCGM 200:2012, *International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM)*.
- **Conformity assessment / decision rules:** JCGM 106:2012, *Evaluation of measurement data — The role of measurement uncertainty in conformity assessment*. DOI: 10.59161/JCGM106-2012.

### Tier 2 — authoritative standards/manufacturer support

- **Gauge blocks:** ASME B89.1.9-2002 is the version explicitly named by certificate T26A06624. ASME B89.1.9-2023 is the current revision and should only be used for current general context, not as though it were the certificate basis.
- **Measurement-method precision terminology:** ISO 5725-2:2019 may be cited selectively for repeatability/reproducibility terminology and precision principles. Do not imply that the single-operator CaseMetrology study is an ISO 5725 interlaboratory study.
- **Jetson platform:** NVIDIA official Jetson Orin Nano Super Developer Kit documentation for manufacturer specifications only.
- **Camera:** Arducam official B0499 IMX296 Global Shutter USB3.0 camera datasheet.
- **Manual reference caliper:** Mitutoyo official product information for 500-197-30 / CD-8"ASX for model, range, and display resolution only. Actual calibrated performance must come from the study instrument certificate.

## Claims that should NOT rely primarily on outside literature

Use repository evidence for:

- exact camera controls;
- 8.625-in optical distance;
- installed 16 mm lens identity;
- segmentation parameter values;
- exact PCA/extreme-mask endpoint implementation;
- fitted spatial calibration equations;
- corrected angle convention;
- five excluded prevalidation specimens;
- formal randomization seeds;
- 235-specimen population;
- final 60-specimen sample and strata;
- formal failure statuses;
- project-specific acceptance thresholds;
- network/outbox/dashboard architecture;
- Git freeze state;
- final formal results.

## Claims that remain blocked

### Calibration/reference system
- Caliper calibration certificate number and laboratory details.
- As-found/as-left condition.
- Calibration uncertainty near 1 in.
- Any required correction.
- Final `E_limit`, `R_limit`, and `D_limit`.
- Final near-specification decision rule.

### Environmental system
- Formal thermometer/probe certificate details and traceability statement.
- Formal session temperature observations.

### Formal specimen study
- Completed 235-case screening distribution.
- Final stratum boundaries.
- Final allocation of 60 specimens.
- Final validation sample IDs.
- Formal manual reference measurements.
- Formal CV measurements.
- Bias, MAE, RMSE, P95, limits of agreement, availability, classification errors, and final validation conclusion.

## Citation-placement guidance

1. Cite general concepts at first substantive use, not after every sentence.
2. Use repository evidence for project-specific statements.
3. Use manufacturer sources for hardware specifications, not for validation claims.
4. Use standards/guides for metrology definitions, uncertainty, and conformity-assessment principles.
5. Do not call the manual reference “true OAL.” Prefer “manual reference value” or “reference measurement.”
6. Do not cite ASME B89.1.9-2023 as though it were the basis of certificate T26A06624; the certificate explicitly identifies B89.1.9-2002.
7. Do not use prevalidation numerical results in Chapter 4 as formal validation results.
8. Do not change acceptance criteria after formal results are observed.
9. Before committee submission, every substantive Chapter 3 claim should map to repository evidence, an external authoritative citation, a certificate, or an explicit pending status.

## Recommended next audit

After citations are collected, perform a sentence-level Chapter 3 pass using:

- `[REPO]`
- `[LITERATURE]`
- `[STANDARD]`
- `[MANUFACTURER]`
- `[CERTIFICATE]`
- `[PENDING]`

No substantive technical sentence should remain unsupported or ambiguously sourced.
