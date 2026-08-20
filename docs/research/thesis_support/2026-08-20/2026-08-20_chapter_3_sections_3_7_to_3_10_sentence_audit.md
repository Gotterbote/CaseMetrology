# Chapter 3 Sentence-Level Evidence Audit — Sections 3.7–3.10

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Scope:** K-State M.S. Integrated Systems Design & Dynamics thesis — cartridge-case OAL only
**Status:** Working audited draft; formal validation has not begun; repository commit deferred by researcher.

## Tag legend

- `[REPO]` — supported by CaseMetrology repository evidence.
- `[LITERATURE]` — general scientific/statistical concept requiring outside citation.
- `[STANDARD]` — supported by recognized metrology/engineering guidance.
- `[MANUFACTURER]` — supported by official manufacturer documentation.
- `[CERTIFICATE]` — supported by an actual calibration certificate.
- `[CERTIFICATE-PENDING]` — cannot be finalized until the formal reference-instrument certificate is reviewed.
- `[FORMAL-DATA-PENDING]` — procedure may be stated prospectively, but numerical study content does not yet exist.
- `[GUARDRAIL]` — wording needed to prevent an unsupported or post-hoc claim.

---

# A. Annotated evidence-audit version

## 3.7 Prevalidation Engineering and Method Freeze

`[REPO]` CaseMetrology development activities were conducted before formal validation and included segmentation development, estimator comparison, calibration characterization, integrated-pipeline verification, and measurement-assurance checks.

`[REPO]` These prevalidation activities were used to select and freeze the measurement method, but their numerical results are not treated as formal validation evidence.

`[REPO]` The development history is intentionally preserved rather than rewritten to show only the final successful method.

`[REPO]` In particular, the geometry-based estimator was temporarily selected during the August 7, 2026 development stage and was later superseded by the PCA/extreme-mask estimator following the August 13 physical-unit comparison.

`[REPO]` PCA/extreme-mask was frozen as the primary OAL estimator on August 13, 2026, before collection of any formal validation measurements.

`[REPO]` The five specimens used in the physical-unit prevalidation comparison—121, 146, 178, 187, and 197—are excluded from the formal validation sample.

`[REPO]` The frozen validation method includes the segmentation sequence and parameters, estimator logic, spatial/directional calibration mapping, quality gates, physical-unit conversion, and failure-status behavior.

`[REPO]` Any post-freeze change capable of altering dimensional output requires explicit documentation and disposition under the validation change-control procedure.

`[REPO] [GUARDRAIL]` Once formal validation begins, observed validation outcomes cannot be used to retune segmentation, calibration, endpoint logic, acceptance criteria, or the prespecified statistical analysis.

`[LITERATURE]` Prospective experimental planning and randomization are standard design principles used to reduce ambiguity between planned methodology and data-dependent decisions.
**Recommended support:** NIST/SEMATECH e-Handbook of Statistical Methods, experimental-design sections.

### Audit disposition for Section 3.7

**Supported now:** development/validation separation, freeze date, excluded specimens, change control, preserved chronology.
**External citation:** optional but useful for the general principle of prospective experimental design.
**Formal-data dependency:** none.

---

## 3.8 Specimen Population and Screening

`[REPO]` The available study population consists of 235 cartridge cases that were previously laser etched with unique integer identifiers from 1 through 235.

`[REPO]` The existing laser-etched identifier is used as the specimen `part_id`; no second labeling system is introduced for the formal study.

`[REPO]` The population was intentionally retained as a mixed-dimensional population rather than restricted to specimens clustered near nominal OAL.

`[REPO]` Some members of the population were intentionally produced short or long during earlier preparation, and those specimens are not automatically excluded merely because their dimensions are away from nominal.

`[REPO] [GUARDRAIL]` The five previously used prevalidation specimens—121, 146, 178, 187, and 197—are excluded from eligibility for the formal validation sample because they were used during method selection.

`[REPO]` Before formal sample selection, the remaining eligible population is screened once using the designated manual screening process so that its dimensional distribution can be characterized for stratification.

`[REPO]` Screening measurements are population-characterization data only; they do not become the three-replicate formal manual reference value for a selected specimen.

`[REPO]` Screening records preserve the specimen identifier, reading, date, time, operator, caliper identity, session identity, reference-check information, screening class, selection status, and notes required by the prospective screening workflow.

`[REPO]` Screening sessions include pre- and post-session reference checks against the certified gauge block under the formal measurement-assurance procedure.

`[CERTIFICATE-PENDING]` Final numerical acceptance limits governing screening-session reference checks remain dependent on review of the calibrated manual-reference instrument certificate.

`[FORMAL-DATA-PENDING]` The completed screening distribution, counts within dimensional regions, and any resulting final stratum boundaries cannot be reported until screening is actually performed.

### Audit disposition for Section 3.8

**Supported now:** population size, ID system, eligibility rules, screening purpose and schema.
**Pending:** completed screening distribution and certificate-derived session limits.
**Important wording:** screening is not formal reference measurement and should not be merged with the formal three-replicate dataset.

---

## 3.9 Formal Validation Sample Selection

`[REPO]` The formal validation sample will contain 60 unique specimens selected from the eligible screened population.

`[REPO]` Selection occurs after screening and uses a stratified random procedure so that the formal sample represents the observed OAL distribution more deliberately than an unrestricted convenience sample.

`[LITERATURE]` Stratified random sampling is a recognized probability-sampling approach in which a population is partitioned into defined subgroups and random selection is then performed within those groups.
**Recommended source:** a standard sampling text such as Cochran, *Sampling Techniques*, or a modern equivalent.
**Status:** exact citation still to finalize.

`[REPO] [GUARDRAIL]` The actual CaseMetrology strata are defined from the screened study population and are not to be altered after the formal sample is drawn in response to validation outcomes.

`[REPO]` Intentionally short and long eligible specimens remain in the sampling frame; their inclusion is governed by the same prospective stratification and random-selection procedure rather than discretionary hand selection.

`[REPO]` The five prevalidation specimens are removed from the eligible sampling frame before formal selection.

`[REPO]` The selection process is intended to be reproducible by preserving the screened population input, eligibility rules, stratification logic, randomization procedure, and final selected identifiers.

`[FORMAL-DATA-PENDING]` Exact stratum boundaries, eligible counts per stratum, sample allocation per stratum, and the final 60 specimen identifiers must remain blank until screening and formal sample selection are completed.

`[GUARDRAIL]` Chapter 3 may describe the selection algorithm prospectively, but it must not report a final sample composition that does not yet exist.

### Audit disposition for Section 3.9

**Supported now:** n=60 target, stratified-random design, exclusions, prospective selection rules.
**Pending:** final strata, allocation, and selected IDs.
**External citation:** one sampling reference recommended if explaining why stratification is used.

---

## 3.10 Manual Reference Measurement Method

`[REPO] [MANUFACTURER]` Formal manual reference measurements are planned using Mitutoyo digital caliper model 500-197-30 / CD-8"ASX, serial number B23090910.

`[MANUFACTURER]` Mitutoyo documentation identifies model 500-197-30 as a 0–8 in (0–200 mm) digital caliper with 0.0005-in (0.01-mm) resolution.
**Manufacturer source:** Mitutoyo official catalog/product literature.

`[GUARDRAIL]` Manufacturer catalog accuracy specifications describe the product model and must not be substituted for the actual calibration status, error, or uncertainty of serial B23090910 during this study.

`[CERTIFICATE-PENDING]` Formal use of serial B23090910 as the reference instrument remains conditional on review and acceptance of its calibration certificate.

`[CERTIFICATE-PENDING]` The certificate review must establish, as applicable, the calibration laboratory and traceability information, certificate number, calibration date, as-found/as-left condition, reported error or correction near the approximately 1-in measurement region, and reported uncertainty.

`[STANDARD]` Metrological traceability should be described according to the VIM as a property of a measurement result related to a reference through a documented unbroken calibration chain in which each calibration contributes to measurement uncertainty.
**Source:** JCGM 200:2012, VIM 2.41.

`[REPO]` Before and after each formal manual measurement session, five reference readings are obtained from the certified 1-in gauge block with full removal and repositioning between readings.

`[CERTIFICATE]` The gauge-block assigned central length used for these checks is 1.0000024 in, as reported by certificate T26A06624.

`[REPO]` Session acceptance is determined prospectively from reference-check error, within-check range/repeatability, and pre-to-post drift criteria defined by the formal measurement-assurance protocol.

`[CERTIFICATE-PENDING]` The final numerical values of `E_limit`, `R_limit`, and `D_limit` cannot be finalized until the manual-reference calibration certificate has been reviewed and its uncertainty/performance information incorporated into the session-assurance rationale.

`[REPO]` For each selected validation specimen, three formal manual reference readings are obtained.

`[REPO]` The specimen is fully removed and repositioned between each replicate reading so that the replicate series includes the positioning variation inherent in the specified manual measurement procedure.

`[REPO]` Formal manual run order is randomized prospectively and is independent of the computer-vision acquisition order.

`[REPO]` The preserved manual run-order seed is `2026081901`.

`[LITERATURE]` NIST describes randomization as determining experimental run sequence randomly and identifies replication as repeated execution under the specified experimental design; these concepts support prospective run-order control and repeated observations.
**Recommended source:** NIST/SEMATECH e-Handbook of Statistical Methods.

`[STANDARD]` Under the VIM, measurement repeatability is measurement precision under repeatability conditions, whereas measurement reproducibility refers to precision under reproducibility conditions.
**Source:** JCGM 200:2012, VIM 2.21 and 2.25.

`[REPO] [STANDARD]` Because the CaseMetrology formal manual study uses one operator, it can characterize within-operator repeated-measurement behavior under the stated procedure but does not estimate between-operator reproducibility.

`[GUARDRAIL]` The formal manual result should be called a **reference measurement** or **manual reference value**, not “true OAL” or an error-free ground truth.

`[STANDARD]` Measurement uncertainty is a property of the measurement result and must be considered when interpreting the reference measurement and any conformity decision near a specification limit.
**Recommended sources:** JCGM 100:2008 and JCGM 106:2012.

`[CERTIFICATE-PENDING]` The final treatment of any calibration correction, reference uncertainty, or near-specification guard band remains prospective and certificate-dependent.

`[REPO]` Formal manual observations are preserved as raw replicate readings; any specimen-level reference mean is derived from those preserved readings rather than replacing them.

### Audit disposition for Section 3.10

**Supported now:** instrument identity, planned three replicates, full repositioning, manual run-order seed, five pre/post standard checks, single-operator design.
**Manufacturer support:** model range and display resolution.
**Certificate pending:** actual calibrated performance, traceability-chain details, error/correction, uncertainty, and final session limits.
**Standards support:** VIM/GUM/JCGM 106.
**Critical guardrail:** do not call the manual reference an error-free truth.

---

# B. Clean thesis-ready version

## 3.7 Prevalidation Engineering and Method Freeze

Development and prevalidation activities were completed before formal validation and included segmentation development, estimator comparison, spatial calibration characterization, integrated-pipeline verification, and measurement-assurance checks. These activities were used to select and freeze the measurement method; their numerical outcomes are not treated as formal validation results.

The development record was intentionally preserved under version control. PCA/extreme-mask initially served as the development baseline, a geometry-based estimator was temporarily selected during the August 7, 2026 development stage, and subsequent physical-unit comparison favored PCA/extreme-mask for aggregate dimensional agreement. PCA/extreme-mask was therefore selected and frozen as the primary formal-validation estimator on August 13, 2026. Specimens 121, 146, 178, 187, and 197, which were used during that comparison, are excluded from the formal validation sample.

The frozen method includes the segmentation sequence and parameters, endpoint and axis logic, spatial/directional calibration mapping, quality gates, physical-unit conversion, and formal failure-status behavior. Any subsequent change capable of affecting dimensional output is subject to explicit validation change control. Once formal validation begins, validation outcomes cannot be used to retune the measurement method, acceptance criteria, or prespecified primary statistical analysis. This prospective separation between method development and validation is consistent with established principles of preplanned experimental design [NIST/SEMATECH DOE SOURCE].

---

## 3.8 Specimen Population and Screening

The available study population consists of 235 cartridge cases previously laser etched with unique integer identifiers from 1 through 235. The existing laser-etched identifier is used directly as the specimen `part_id`, avoiding the introduction of a second identification system. The population contains specimens spanning the available OAL range, including specimens intentionally prepared shorter or longer than nominal during earlier study preparation.

The five specimens previously used during estimator prevalidation—121, 146, 178, 187, and 197—are excluded from eligibility for formal validation. All other eligible specimens remain in the screening population regardless of whether they appear nominal, short, or long.

Before formal sample selection, the eligible population is screened using the designated manual screening process to characterize its dimensional distribution for stratification. Screening measurements are population-characterization measurements only and are not substituted for the three-replicate formal manual reference measurements subsequently obtained from selected validation specimens.

The screening record preserves specimen identity, screening reading, date, time, operator, caliper identity, session identity, reference-check information, screening classification, selection status, and explanatory notes. Screening sessions are bracketed by reference checks against the certified 1-in gauge block under the prospective measurement-assurance procedure. Final numerical session-acceptance limits remain dependent on review of the calibrated manual-reference instrument certificate.

Because screening has not yet been completed, the final population distribution and resulting stratum boundaries are not reported at this stage.

---

## 3.9 Formal Validation Sample Selection

The formal validation sample will contain 60 unique specimens selected from the eligible screened population. Selection will occur after screening using a stratified random procedure intended to preserve representation across the observed OAL distribution rather than relying on convenience or discretionary specimen selection. Stratified random sampling partitions a population into defined subgroups and applies random selection within those groups [SAMPLING SOURCE].

The CaseMetrology strata will be established from the completed screening dataset before the formal sample is drawn. Intentionally short and long eligible specimens remain within the sampling frame and are subject to the same prospective stratification and random-selection process as other eligible specimens. The five specimens used during prevalidation are removed from the eligible sampling frame before selection.

The selection process will preserve the screened population input, eligibility rules, stratification logic, random-selection procedure, and final selected identifiers so that the sample draw can be reproduced and audited. Exact stratum boundaries, counts, allocation, and the identities of the 60 selected specimens will be reported only after population screening and formal selection have been completed.

---

## 3.10 Manual Reference Measurement Method

Formal manual reference measurements are planned using a Mitutoyo digital caliper, model 500-197-30 / CD-8"ASX, serial number B23090910. Mitutoyo manufacturer documentation identifies this model as having a 0–8 in (0–200 mm) measuring range and 0.0005-in (0.01-mm) resolution [MITUTOYO SOURCE]. Manufacturer specifications are used only to describe the instrument model; the calibrated performance of the actual study instrument will be established from its calibration certificate.

Formal use of serial B23090910 as the reference instrument is conditional on review and acceptance of that certificate. The review will document the calibration laboratory and traceability information, certificate identification, applicable calibration date and condition, reported error or correction near the study's measurement region, and reported measurement uncertainty. Metrological traceability is treated in accordance with the International Vocabulary of Metrology, which relates a measurement result to a reference through a documented unbroken calibration chain in which the calibrations contribute to measurement uncertainty [JCGM 200:2012].

Before and after each formal manual measurement session, five readings of the certified gauge block are obtained with full removal and repositioning between readings. The gauge block has a certified central length of 1.0000024 in under certificate T26A06624. Session acceptance is prospectively based on reference error, within-check spread, and pre-to-post drift criteria. Final numerical limits for these checks will be established only after the manual-reference calibration certificate has been reviewed.

Each selected validation specimen is measured manually three times. The specimen is fully removed and repositioned between replicate readings so that the repeated-measurement series includes positioning variation inherent in the stated manual procedure. Formal manual run order is randomized independently of computer-vision acquisition order using the preserved manual randomization seed `2026081901`. Randomization and replication are established experimental-design principles used to control run-order effects and characterize repeated-observation behavior [NIST/SEMATECH DOE SOURCE].

The formal manual study is conducted by a single operator. Accordingly, the repeated manual measurements characterize within-operator behavior under the specified measurement conditions; they do not estimate between-operator measurement reproducibility. This distinction follows the VIM separation of measurement repeatability from measurement reproducibility [JCGM 200:2012].

The manual process is treated as the study's reference measurement process rather than as an error-free determination of “true” OAL. Its calibration status, resolution, repeatability, and measurement uncertainty remain relevant to interpretation of agreement with the computer-vision method. The final treatment of calibration correction, reference uncertainty, and any near-specification decision rule remains dependent on certificate review and will follow the applicable GUM and conformity-assessment framework [JCGM 100:2008; JCGM 106:2012].

Raw manual replicate readings are preserved individually. Any specimen-level manual reference mean used in the agreement analysis is derived from those preserved observations rather than replacing the underlying measurements.

---

# C. Verified source-placement record for this block

## NIST/SEMATECH Engineering Statistics Handbook

**Authoritative source:** National Institute of Standards and Technology.

Useful sections:
- Experimental design overview.
- Completely randomized designs.
- DOE terminology for randomization and replication.

**Use in Sections 3.7 and 3.10**
- Prospective experimental planning.
- Randomized run order.
- Replication rationale.

**Important qualification**
CaseMetrology is not being represented as a classical factorial DOE. NIST is used only for general experimental-design principles that are applicable to the prospective study structure.

---

## JCGM 200:2012 — VIM

Useful entries:
- 2.21 measurement repeatability.
- 2.25 measurement reproducibility.
- 2.41 metrological traceability.

**Use in Section 3.10**
- Single-operator repeatability/reproducibility distinction.
- Traceability terminology.

---

## JCGM 100:2008 — GUM

**Use in Section 3.10**
- Measurement uncertainty framing.
- Avoidance of treating the manual reference as error-free truth.

---

## JCGM 106:2012

**Use in Section 3.10**
- Framework for uncertainty in conformity assessment and eventual near-limit decision logic.

**Important qualification**
JCGM 106 does not determine the project's numerical session limits or guard bands. Those remain certificate- and protocol-dependent.

---

## Mitutoyo 500-197-30

Official Mitutoyo documentation supports:
- model 500-197-30 / CD-8"ASX;
- measuring range 0–8 in / 0–200 mm;
- resolution 0.0005 in / 0.01 mm.

**Use in Section 3.10**
Model description only.

**Do not use manufacturer catalog accuracy as a substitute for the calibration certificate of serial B23090910.**

---

# D. Remaining open items after Sections 3.7–3.10

1. Complete formal screening of the eligible specimen population.
2. Establish final stratum boundaries from the completed screening data.
3. Execute and preserve the formal 60-specimen selection.
4. Receive and review the calibration certificate for caliper serial B23090910.
5. Finalize `E_limit`, `R_limit`, and `D_limit`.
6. Finalize any calibration correction and near-specification reference decision rule.
7. Select the final sampling-method citation if Chapter 3 includes a general explanation of stratified random sampling.
8. Keep the three formal manual readings distinct from the earlier screening reading.
9. Do not claim between-operator reproducibility from the single-operator study.
10. Do not begin formal reference measurements until the reference-instrument certificate gate is satisfied.
