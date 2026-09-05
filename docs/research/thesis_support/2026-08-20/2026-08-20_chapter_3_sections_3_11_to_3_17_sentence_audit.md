# Chapter 3 Sentence-Level Evidence Audit — Sections 3.11–3.17

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Scope:** K-State M.S. Integrated Systems Design & Dynamics thesis — cartridge-case OAL only
**Status:** Working audited draft; formal validation has not begun; repository commit deferred by researcher.

## Tag legend

- `[REPO]` — supported by CaseMetrology repository evidence.
- `[LITERATURE]` — general scientific/statistical concept requiring outside citation.
- `[STANDARD]` — supported by recognized metrology/engineering guidance.
- `[MANUFACTURER]` — supported by official manufacturer information.
- `[CERTIFICATE-PENDING]` — depends on formal calibration-certificate evidence.
- `[FORMAL-DATA-PENDING]` — no formal result may be stated yet.
- `[GUARDRAIL]` — prevents unsupported, post-hoc, or overly broad interpretation.

---

# A. Annotated evidence-audit version

## 3.11 Computer-Vision Validation Measurement Method

`[REPO]` Formal computer-vision validation will use the frozen PCA/extreme-mask OAL measurement pipeline after completion of the manual reference measurement phase.

`[REPO]` The formal design contains 60 unique validation specimens and three planned computer-vision acquisition attempts per specimen, yielding 180 planned CV acquisition opportunities.

`[REPO]` The specimen is fully removed and repositioned between each CV replicate so that the repeated acquisitions incorporate specimen-placement variation under the documented fixture procedure.

`[REPO]` Formal CV acquisition order is randomized independently of the manual reference-measurement order.

`[REPO]` The preserved CV run-order seed is `2026081902`.

`[REPO]` Each formal CV attempt is assigned one of three prospective statuses: `VALID`, `SYSTEM_FAILURE`, or `PROTOCOL_INVALID`.

`[REPO]` A `SYSTEM_FAILURE` represents a genuine failure of the system to produce a valid measurement under an otherwise valid formal attempt and remains part of formal system-performance accounting.

`[REPO] [GUARDRAIL]` A system failure is not automatically repeated merely to obtain a successful value because doing so would remove evidence of measurement-system availability.

`[REPO]` A `PROTOCOL_INVALID` attempt represents an acquisition invalidated by documented procedural nonconformance rather than measurement-system performance.

`[REPO]` A protocol-invalid event may receive a documented appended replacement attempt when permitted by the prospective deviation procedure; the original invalid record remains preserved.

`[REPO]` No computer-vision value is imputed for a system failure.

`[REPO]` At least two valid CV replicates are required to compute the primary specimen-level CV mean used in agreement analysis.

`[REPO]` A specimen with fewer than two valid CV measurements remains in failure/availability reporting but is excluded from the primary specimen-level agreement analysis.

`[GUARDRAIL]` Formal validation must not be described as containing 180 independent experimental units. The primary experimental unit for agreement analysis is the unique specimen, n = 60.

### Audit disposition for Section 3.11

**Supported now:** 60 × 3 design, independent CV order, seed, failure statuses, replacement rule, no imputation, two-valid-replicate rule.
**Formal-data dependency:** actual status counts and measurements.
**Critical guardrail:** preserve system failures rather than “cleaning” them from the study.

---

## 3.12 Randomization and Replication

`[REPO]` Manual and computer-vision measurements use independently randomized run orders to reduce systematic coupling between specimen sequence and measurement method.

`[REPO]` The manual run-order seed is `2026081901`, and the CV run-order seed is `2026081902`.

`[REPO]` Each method acquires three repeated measurements per selected specimen with full removal and repositioning between replicates.

`[LITERATURE]` NIST describes randomization as determining experimental run sequence randomly and replication as repeating the experimental condition; these principles support control of run-order effects and characterization of repeated-measurement behavior.
**Source:** NIST/SEMATECH Engineering Statistics Handbook.

`[REPO]` The three repeated measurements are used to characterize repeated-measurement behavior and to construct a specimen-level mean for the primary between-method agreement analysis.

`[GUARDRAIL]` Replicates from one specimen are not treated as though they were measurements from three independent specimens.

`[REPO]` The formal statistical analysis therefore uses 60 unique specimen-level pairs as the primary agreement dataset when sufficient valid CV replicates exist.

### Audit disposition for Section 3.12

**Supported now:** independent seeds, three repeats, full repositioning, specimen as experimental unit.
**External support:** NIST DOE terminology/principles.
**Formal-data dependency:** actual completed run orders and any deviations.

---

## 3.13 Environmental and Measurement-Assurance Controls

`[REPO]` Formal measurement sessions include environmental observation and reference-standard checks intended to document measurement conditions and identify material changes during data collection.

`[REPO]` The planned environmental instrumentation includes a Digi-Sense WD-20250-91 thermocouple thermometer and Digi-Sense WD-08519-54 Type-T self-adhesive surface probes.

`[CERTIFICATE-PENDING]` Formal claims that those environmental measurements are calibrated or metrologically traceable require review of the instrument/probe calibration documentation applicable to the study.

`[REPO] [GUARDRAIL]` Earlier approximate temperature observations obtained with non-traceable equipment are prevalidation observations and are not substituted for formal calibrated environmental evidence.

`[STANDARD]` Environmental conditions are properly treated as potential influence quantities when they can affect the measured quantity or the measurement result.
**Recommended source:** JCGM 200:2012 and JCGM 100:2008.

`[REPO]` The current formal method records environmental measurements but does not apply an automatic temperature correction to cartridge-case OAL or the CV result.

`[GUARDRAIL]` Any later thermal correction would constitute a methodological change and cannot be introduced after formal results are inspected unless it is handled as a documented protocol amendment with appropriate study disposition.

`[REPO]` Manual measurement sessions are bracketed by five pre-session and five post-session readings of the certified 1-in gauge block.

`[REPO]` These checks provide session-level evidence for reference error, within-check spread, and pre-to-post drift.

`[CERTIFICATE-PENDING]` Numerical acceptance thresholds for the manual measurement-assurance checks remain dependent on review of the calibrated manual-reference instrument certificate.

`[FORMAL-DATA-PENDING]` Actual formal temperatures, pre/post check results, session acceptability, and any associated deviations cannot be reported until data collection occurs.

### Audit disposition for Section 3.13

**Supported now:** prospective environmental and assurance procedure.
**Certificate pending:** environmental traceability and final manual-reference session limits.
**Formal-data pending:** actual temperatures/check outcomes.
**Guardrail:** do not retroactively thermal-correct formal data without a prospective basis.

---

## 3.14 Data Integrity, Traceability, and Protocol Deviations

`[REPO]` Formal study records preserve raw observations separately from derived summaries.

`[REPO]` Manual replicate readings, CV attempt-level records, status codes, identifiers, timestamps, and applicable acquisition artifacts are retained so that specimen-level statistics can be regenerated from the underlying evidence.

`[REPO]` Research-relevant software, protocols, calibration records, methodological decisions, and corrections are preserved under version control.

`[REPO]` The OAL evidence index and method decision log provide a claim-to-evidence and chronology layer over the underlying repository artifacts.

`[REPO]` Where artifact manifests or transport records use SHA-256 hashes, those hashes provide an integrity check that the compared or transferred artifact has not changed.

`[REPO] [GUARDRAIL]` Formal observations are not deleted solely because they are statistically inconvenient or appear to be outliers.

`[REPO]` A questionable observation is retained and dispositioned according to the prospective status/deviation framework.

`[REPO]` Material protocol deviations are documented, assessed for their effect on study validity, and retained in the research record.

`[REPO] [GUARDRAIL]` A protocol correction or methodological clarification cannot silently rewrite the historical record; the original evidence and the subsequent correction are both retained.

### Audit disposition for Section 3.14

**Supported now:** repository/version-control governance, raw/derived separation, failure preservation, deviation policy.
**External citation:** not necessary for the specific project procedure.
**Formal-data dependency:** actual deviation log entries.

---

## 3.15 Statistical Analysis

`[REPO]` The primary unit of between-method agreement analysis is the unique validation specimen.

`[REPO]` For each specimen with sufficient valid CV replicates, the formal analysis compares the specimen-level CV mean with the corresponding specimen-level manual reference mean.

`[REPO]` Signed specimen error is defined as

\[
e_i = \bar{x}_{CV,i} - \bar{x}_{REF,i}.
\]

`[REPO]` Positive error therefore represents a CV value greater than the manual reference value; negative error represents a CV value less than the manual reference value.

`[REPO]` The prespecified primary summary measures include mean bias, mean absolute error (MAE), root mean squared error (RMSE), empirical 95th percentile of absolute specimen error, and maximum absolute specimen error.

`[REPO]` The empirical P95 is calculated using the project's prespecified nearest-rank convention.

`[REPO]` With 60 specimen-level observations, the prespecified nearest-rank P95 corresponds to the 57th ordered absolute error when all 60 specimens are evaluable.

`[REPO]` Repositioning repeatability is assessed separately from between-method agreement using absolute differences among replicate measurements under the frozen repeated-measurement procedure.

`[STANDARD]` The term repeatability should be used consistently with the VIM definition of measurement precision under repeatability conditions.
**Source:** JCGM 200:2012.

`[REPO]` Error is also examined against measurement magnitude and against the final screening-defined strata to identify evidence of magnitude-dependent or stratum-dependent behavior.

`[LITERATURE]` Agreement between measurement methods is evaluated using a Bland–Altman-style difference-versus-magnitude analysis rather than relying on correlation as a measure of agreement. Bland and Altman specifically warned that correlation can be misleading when the research question is agreement between measurement methods.
**Primary source:** Bland and Altman (1986).

`[REPO]` Correlation, if reported, is therefore supplementary and cannot substitute for the prespecified error and agreement metrics.

`[REPO]` Classification performance is assessed relative to the project OAL specification limits of 0.990 in and 1.010 in.

`[STANDARD]` Classification near a specification limit must be interpreted in the context of reference-measurement uncertainty and the prospective decision rule.
**Source:** JCGM 106:2012.

`[REPO]` CV availability is defined prospectively as

\[
Availability =
\frac{N_{\mathrm{VALID}}}
{N_{\mathrm{VALID}} + N_{\mathrm{SYSTEM\_FAILURE}}}.
\]

`[REPO]` `PROTOCOL_INVALID` attempts are not counted as system failures because they represent invalid procedure rather than system performance; their original records and any permitted replacement attempts remain documented.

`[GUARDRAIL]` No outlier is removed from the primary analysis solely because its inclusion worsens bias, RMSE, P95 error, limits of agreement, or classification performance.

`[FORMAL-DATA-PENDING]` Numerical values for every formal metric remain unwritten until the prospective dataset is collected and the frozen analysis is executed.

### Audit disposition for Section 3.15

**Supported now:** formulas/metrics, experimental unit, nearest-rank rule, availability definition, agreement framework, classification approach.
**External support:** Bland–Altman; VIM; JCGM 106.
**Formal-data pending:** all numerical results.

---

## 3.16 Validation Acceptance Criteria

`[REPO]` The primary validation acceptance criteria were defined before formal validation data collection and are not to be revised after observing formal outcomes.

`[REPO]` Formal CV availability must be at least 99%.

`[REPO]` The prespecified P95 absolute repositioning difference must not exceed 0.002 in.

`[REPO]` The absolute mean specimen-level bias must not exceed 0.001 in.

`[REPO]` Specimen-level RMSE must not exceed 0.002 in.

`[REPO]` The empirical P95 absolute specimen error must not exceed 0.003 in.

`[REPO]` Maximum absolute specimen error must not exceed 0.004 in.

`[REPO]` With 180 planned CV acquisition opportunities, 179 valid attempts out of 180 corresponds to approximately 99.44% availability and satisfies the 99% threshold, whereas 178 of 180 corresponds to approximately 98.89% and does not.

`[REPO]` Zero false-pass classifications are preferred.

`[REPO] [STANDARD]` A confirmed false pass is treated as a material outcome because it represents acceptance by the CV method where the applicable reference decision indicates nonconformance. JCGM 106 identifies false acceptance as a distinct conformity-assessment risk and describes guarded decision rules as one means of reducing that risk.
**Source:** JCGM 106:2012.

`[CERTIFICATE-PENDING]` The final determination of a reference pass/fail classification for specimens sufficiently near a specification limit remains dependent on the manual-reference calibration certificate and the prospectively established uncertainty/decision rule.

`[REPO]` Unresolved material protocol deviations prevent an unconditional validation conclusion even if numerical performance thresholds are otherwise satisfied.

`[GUARDRAIL]` The acceptance thresholds are CaseMetrology project criteria. They must not be represented as numerical limits supplied by Bland–Altman, JCGM, ASME, Mitutoyo, Arducam, or another external source unless a direct source specifically establishes such a limit.

### Audit disposition for Section 3.16

**Supported now:** all project-specific thresholds and prospective nature.
**Standard context:** JCGM 106 for false-acceptance/conformity risk.
**Certificate pending:** final near-limit reference decision rule.
**Formal-data pending:** pass/fail outcome of the validation itself.

---

## 3.17 Methodological Limitations

`[REPO]` The validation study is limited to cartridge-case overall length and does not validate rim geometry, pocket dimensions, concentricity, or other dimensional characteristics.

`[REPO]` The study evaluates a static, backlit, fixture-based measurement configuration and does not directly establish performance on a conveyor, moving production line, robotic handling system, or other dynamic acquisition environment.

`[REPO]` Validation applies to the documented camera, 16 mm CS-mount lens, measurement-plane geometry, illumination, fixture, software, segmentation, estimator, and calibration configuration used during the formal study.

`[GUARDRAIL]` A materially changed optical, mechanical, lighting, calibration, or software configuration should not automatically inherit the validation conclusion without an appropriate verification or revalidation assessment.

`[REPO] [STANDARD]` The manual comparator is a reference measurement process rather than an error-free “true” value; its resolution, repeatability, calibration status, and uncertainty limit the interpretation of measured agreement.
**Sources:** JCGM 100:2008 and JCGM 200:2012.

`[REPO] [STANDARD]` The study uses one manual operator and therefore does not estimate between-operator reproducibility.
**Source:** JCGM 200:2012, repeatability/reproducibility terminology.

`[REPO]` The formal agreement analysis is based on 60 unique specimens, which provides a finite empirical characterization of the selected population rather than proof of worst-case performance for every possible cartridge case.

`[GUARDRAIL]` The empirical P95 and maximum observed error characterize the formal sample and must not be described as universal physical bounds.

`[REPO]` The selected population contains intentionally short and long examples, but the degree to which the final 60-specimen sample represents every future manufacturing distribution will remain limited by the screened source population and prospective sampling design.

`[REPO]` The study is designed to determine whether the frozen CaseMetrology system satisfies the prespecified OAL validation criteria under the documented conditions; broader claims must be reserved for future work.

### Audit disposition for Section 3.17

**Supported now:** scope, static-system limitation, configuration-specific validity, single-operator limitation, finite-sample limitation.
**External support:** GUM/VIM terminology.
**Future work:** other dimensions, dynamic production, broader operators/configurations/populations.

---

# B. Clean thesis-ready version

## 3.11 Computer-Vision Validation Measurement Method

Formal computer-vision validation will use the frozen PCA/extreme-mask OAL pipeline after completion of the manual reference measurement phase. The formal design includes 60 unique specimens with three planned CV acquisition attempts per specimen, yielding 180 planned acquisition opportunities. Each specimen is fully removed and repositioned between replicate acquisitions so that the repeated measurements include positioning variation under the documented fixture procedure.

The CV run order is randomized independently of the manual reference-measurement order using the preserved seed `2026081902`. Each formal CV attempt is assigned one of three prospective statuses: `VALID`, `SYSTEM_FAILURE`, or `PROTOCOL_INVALID`. A system failure represents a genuine failure of the system to produce a valid result during an otherwise valid attempt and remains part of formal system-performance accounting. It is not automatically repeated merely to replace an unsuccessful result. A protocol-invalid attempt represents a documented procedural nonconformance rather than measurement-system performance; when permitted by the prospective deviation procedure, such an attempt may receive a documented replacement while the original invalid record remains preserved.

No CV result is imputed for a system failure. At least two valid CV replicates are required for calculation of the specimen-level CV mean used in the primary agreement analysis. Specimens with fewer than two valid CV replicates remain represented in availability and failure reporting but are excluded from the primary specimen-level agreement analysis. The experimental unit for the primary between-method analysis is the unique specimen rather than the individual replicate acquisition.

---

## 3.12 Randomization and Replication

Manual and computer-vision measurements use independently randomized run orders. The manual sequence uses seed `2026081901`, whereas the CV sequence uses seed `2026081902`. Each method obtains three repeated measurements per selected specimen with full removal and repositioning between replicates.

Randomization and replication are established experimental-design principles that support control of run-order effects and characterization of repeated-observation behavior [NIST/SEMATECH ENGINEERING STATISTICS HANDBOOK]. Within the present study, the replicate measurements are used to characterize repeated-measurement behavior and to construct specimen-level means for the primary agreement analysis. Replicates obtained from one specimen are not treated as independent specimens; the principal agreement dataset contains at most 60 unique specimen-level pairs.

---

## 3.13 Environmental and Measurement-Assurance Controls

Formal measurement sessions include environmental observation and reference-standard checks to document measurement conditions and identify material changes during data collection. The planned environmental instrumentation consists of a Digi-Sense WD-20250-91 thermocouple thermometer and WD-08519-54 Type-T self-adhesive surface probes. Formal claims of calibrated or metrologically traceable environmental measurement will be made only after the applicable calibration documentation has been reviewed.

Environmental conditions are treated as potential influence quantities when they can affect the measurement result [JCGM 100:2008; JCGM 200:2012]. The formal protocol records temperature observations but does not apply an automatic thermal correction to the cartridge-case or CV measurement. Earlier approximate temperature observations obtained during prevalidation are not substituted for formal calibrated environmental evidence.

Manual reference sessions are bracketed by five pre-session and five post-session readings of the certified 1-in gauge block. These checks are used to assess reference error, within-check spread, and pre-to-post drift. Final numerical acceptance limits for those checks remain dependent on review of the calibrated manual-reference instrument certificate. Formal temperature observations, session-check results, and any associated deviations will be reported only after data collection.

---

## 3.14 Data Integrity, Traceability, and Protocol Deviations

Formal study records preserve raw observations separately from derived summaries. Manual replicate readings, CV attempt-level records, status codes, specimen identifiers, timestamps, and applicable acquisition artifacts are retained so that specimen-level results can be regenerated from the underlying evidence.

Research-relevant software, protocols, calibration records, methodological decisions, and corrections are preserved under version control. The OAL evidence index and method decision log provide an additional claim-to-evidence and chronology layer over the underlying artifacts. Where SHA-256 manifests or transport records are used, they provide integrity checks for preserved or transferred artifacts.

Formal observations are not deleted solely because they are statistically inconvenient or appear to be outliers. Questionable observations are retained and dispositioned using the prospective failure/deviation framework. Material protocol deviations are documented and assessed for their effect on study validity. Methodological corrections preserve both the original evidence and the later correction rather than silently rewriting the research history.

---

## 3.15 Statistical Analysis

The primary unit of between-method agreement analysis is the unique validation specimen. For each specimen with sufficient valid CV replicates, the specimen-level CV mean is compared with the corresponding specimen-level manual reference mean. Signed error is defined as

\[
e_i = \bar{x}_{CV,i} - \bar{x}_{REF,i},
\]

such that positive values indicate CV measurements greater than the reference value and negative values indicate CV measurements less than the reference value.

The prespecified primary statistical summaries include mean bias, mean absolute error, root mean squared error, empirical 95th percentile of absolute specimen error, and maximum absolute specimen error. The empirical P95 is calculated using the prespecified nearest-rank convention; with 60 evaluable specimen-level observations, the 57th ordered absolute error represents the nearest-rank P95.

Repeated-measurement behavior is examined separately from between-method agreement using absolute differences among replicate measurements. The term repeatability is used consistently with the International Vocabulary of Metrology [JCGM 200:2012]. Error is also examined as a function of measurement magnitude and the final screening-defined strata.

Agreement between the two measurement methods is further examined using a Bland–Altman-style difference-versus-magnitude analysis. Bland and Altman showed that correlation can be misleading when the scientific question concerns agreement between measurement methods [BLAND AND ALTMAN 1986]. Correlation, if included, is therefore supplementary and does not replace the prespecified error and agreement metrics.

Classification performance is evaluated relative to the project OAL specification limits of 0.990 in and 1.010 in. Interpretation of classifications near a specification limit will incorporate the applicable reference-measurement uncertainty and prospective decision rule [JCGM 106:2012].

Computer-vision availability is defined as

\[
Availability =
\frac{N_{\mathrm{VALID}}}
{N_{\mathrm{VALID}} + N_{\mathrm{SYSTEM\_FAILURE}}}.
\]

Protocol-invalid attempts are not counted as system failures because they represent invalid procedure rather than system performance; however, the original invalid records and any permitted replacements remain documented. No observation is removed solely because its inclusion worsens the statistical performance metrics. Numerical results will be reported only after collection and analysis of the formal prospective dataset.

---

## 3.16 Validation Acceptance Criteria

The primary validation acceptance criteria were defined before formal validation data collection and will not be revised after formal results are observed. The frozen criteria require:

- CV availability of at least 99%;
- P95 absolute repositioning difference no greater than 0.002 in;
- absolute mean specimen-level bias no greater than 0.001 in;
- specimen-level RMSE no greater than 0.002 in;
- empirical P95 absolute specimen error no greater than 0.003 in; and
- maximum absolute specimen error no greater than 0.004 in.

With 180 planned CV acquisition opportunities, 179 valid attempts correspond to approximately 99.44% availability and satisfy the 99% requirement, whereas 178 valid attempts correspond to approximately 98.89% and do not.

Zero false-pass classifications are preferred. False acceptance is a recognized conformity-assessment risk, and guarded decision rules may be used to reduce that risk when appropriate [JCGM 106:2012]. The final reference classification of a specimen sufficiently near a specification limit remains dependent on the calibrated manual-reference instrument certificate and the prospectively established uncertainty/decision rule.

Unresolved material protocol deviations prevent an unconditional validation conclusion even when numerical performance thresholds are otherwise met. The numerical acceptance criteria above are CaseMetrology-specific prospective criteria and are not attributed to external standards or manufacturer specifications.

---

## 3.17 Methodological Limitations

The formal study is limited to cartridge-case overall length. It does not validate rim geometry, primer-pocket dimensions, concentricity, or other dimensional characteristics. The study evaluates a static, backlit, fixture-based measurement configuration and does not directly establish performance for conveyor-based, robotic, or otherwise dynamic production acquisition.

The validation conclusion applies to the documented camera, 16 mm CS-mount lens, measurement-plane geometry, illumination, fixture, software, segmentation, estimator, and calibration configuration used during the formal study. A materially changed optical, mechanical, lighting, calibration, or software configuration should not automatically inherit the validation conclusion without an appropriate verification or revalidation assessment.

The manual comparator is a reference measurement process rather than an error-free value. Its resolution, repeatability, calibration status, and measurement uncertainty limit the interpretation of agreement [JCGM 100:2008; JCGM 200:2012]. Because the manual study is performed by one operator, the study does not estimate between-operator reproducibility.

The formal agreement analysis contains 60 unique specimens and therefore provides a finite empirical characterization of the selected study population rather than proof of worst-case performance for every possible cartridge case. The empirical P95 and maximum observed error describe the formal sample and are not interpreted as universal physical bounds. Although the sampling population includes intentionally short and long specimens, generalization to future manufacturing populations remains constrained by the source population, sampling design, and documented study configuration.

The formal study is therefore designed to determine whether the frozen CaseMetrology OAL system satisfies its prespecified validation criteria under the documented conditions. Broader dimensional, operational, and production-line claims are reserved for future research.

---

# C. Verified source-placement record

## Bland and Altman (1986)

J. M. Bland and D. G. Altman.
“Statistical Methods for Assessing Agreement Between Two Methods of Clinical Measurement.”
*The Lancet*, 1986; 1(8476):307–310.
PMID: 2868172.
DOI: `10.1016/S0140-6736(86)90837-8`.

**Use:** Section 3.15.

**Reason:** The original article specifically identifies correlation as misleading for measurement-method agreement and presents an alternative difference-based graphical approach.

---

## JCGM 200:2012 — VIM

**Use:** Sections 3.13, 3.15, and 3.17.

Relevant concepts:
- measurement repeatability;
- measurement reproducibility;
- measurement uncertainty;
- influence quantity;
- metrological traceability.

---

## JCGM 106:2012

**Use:** Sections 3.15 and 3.16.

Relevant concepts:
- conformity assessment;
- false acceptance;
- false rejection;
- acceptance intervals;
- guarded acceptance / guard bands.

**Important qualification:** JCGM 106 supplies conformity-assessment concepts, not the CaseMetrology numerical acceptance thresholds.

---

## NIST/SEMATECH Engineering Statistics Handbook

**Use:** Section 3.12 and optionally Section 3.7.

Relevant concepts:
- prospective experimental planning;
- randomized run sequence;
- replication.

**Important qualification:** CaseMetrology is not being represented as a classical factorial DOE.

---

# D. Chapter 3 unresolved evidence after completion of Sections 3.4–3.17

## External-source cleanup
1. Verify one image-processing source for Gaussian smoothing, morphology, and connected components.
2. Select a final sampling reference if the thesis explains stratified sampling theoretically.
3. Confirm final thesis/reference formatting style against current K-State ETDR requirements.

## Certificate dependencies
4. Receive and review calibration certificate for manual reference caliper serial B24254849.
5. Finalize any certificate-derived correction.
6. Finalize `E_limit`, `R_limit`, and `D_limit`.
7. Finalize the near-specification reference decision rule.
8. Review environmental thermometer/probe calibration documentation before claiming traceable formal temperature measurements.

## Formal-data dependencies
9. Complete screening.
10. Freeze final stratum boundaries.
11. Select and preserve the formal 60-specimen sample.
12. Complete formal manual reference measurements.
13. Complete formal CV validation acquisitions.
14. Execute the frozen statistical analysis.
15. Write Chapter 4 only from the formal dataset.
16. Write Chapter 5 conclusions only after formal results exist.

## Existing-thesis consistency checks
17. Ensure every `PPI_90` equation uses Y coefficient `0.00442714650`.
18. Ensure the corrected angle convention is used throughout.
19. Ensure optical configuration is 16 mm CS2316ZM02.
20. Use “reference measurement” rather than “true OAL” or unqualified “ground truth.”
21. Do not claim between-operator reproducibility.
22. Keep prevalidation numerical evidence out of formal-validation results.
23. Keep non-OAL dimensional work outside the current thesis validation scope.
