# Chapter 3 Verified Source Dossier

**Project:** CaseMetrology
**Date:** 2026-08-20
**Purpose:** Verified external source set for Chapter 3 of the K-State M.S. thesis.
**Status:** Working bibliography/source-placement record. Repository commits intentionally deferred.

## 1. Source hierarchy

Use sources in this order:

1. Primary peer-reviewed article for named algorithms/statistical methods.
2. BIPM/JCGM documents for metrology terminology, uncertainty, traceability, validation, and conformity assessment.
3. Standards named by actual certificates when describing certificate basis.
4. Manufacturer documentation for vendor product specifications.
5. Repository evidence for what CaseMetrology actually did.

Do not use a manufacturer catalog specification as a substitute for the calibrated performance of the actual study instrument.

---

## 2. VERIFIED CORE SOURCES

### S-01 — Otsu thresholding

**Reference**

Nobuyuki Otsu. “A Threshold Selection Method from Gray-Level Histograms.”
*IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), 62–66, 1979.
DOI: `10.1109/TSMC.1979.4310076`

**Use in thesis**
- Section 3.4.
- Cite when first explaining why the segmentation pipeline uses Otsu thresholding.
- Repository evidence remains responsible for proving that CaseMetrology actually calls OpenCV Otsu thresholding.

**Do not use for**
- The 5×5 Gaussian kernel.
- The 3×3 morphology parameters.
- The decision to retain only the largest connected component.
Those are project implementation details or need separate image-processing literature.

---

### S-02 — Principal component analysis

**Reference**

Ian T. Jolliffe and Jorge Cadima. “Principal component analysis: a review and recent developments.”
*Philosophical Transactions of the Royal Society A*, 374(2065), 20150202, 2016.
DOI: `10.1098/rsta.2015.0202`

**Use in thesis**
- Section 3.5.
- Support the general explanation of PCA as a variance-based orthogonal transformation / principal-axis method.
- The specific CaseMetrology use of PCA to establish/refine the cartridge-case longitudinal axis remains a project-specific implementation claim.

---

### S-03 — Bland–Altman agreement

**Reference**

J. Martin Bland and Douglas G. Altman. “Statistical Methods for Assessing Agreement Between Two Methods of Clinical Measurement.”
*The Lancet*, 327(8476), 307–310, 1986.
DOI: `10.1016/S0140-6736(86)90837-8`

**Use in thesis**
- Section 3.15.5.
- Section 3.15.10.
- Support method-comparison plots based on paired difference versus paired mean.
- Support the statement that correlation is not an adequate measure of agreement between two measurement methods.

**Important framing**
The paper originates in clinical measurement, but the statistical method is applicable to paired measurement-method agreement. Do not imply the CaseMetrology study is clinical.

---

### S-04 — JCGM 100:2008 (GUM)

**Reference**

Joint Committee for Guides in Metrology.
*Evaluation of measurement data — Guide to the expression of uncertainty in measurement*.
JCGM 100:2008(E).
DOI: `10.59161/JCGM100-2008E`

**Use in thesis**
- Section 3.6: calibration/uncertainty framing.
- Section 3.10: reference-measurement uncertainty.
- Section 3.13: environmental/influence quantities where relevant.
- Section 3.17: limitation that the reference process is not error-free truth.

**Important framing**
Use the GUM for general uncertainty methodology and terminology. Do not calculate or invent the final CaseMetrology reference uncertainty until the caliper certificate is available.

---

### S-05 — JCGM 200:2012 (VIM)

**Reference**

Joint Committee for Guides in Metrology.
*International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd edition*.
JCGM 200:2012.
DOI: `10.59161/JCGM200-2012`

**Specific useful VIM concepts**

- 2.21 — measurement repeatability.
- 2.25 — measurement reproducibility.
- 2.26 — measurement uncertainty.
- 2.41 — metrological traceability.
- 2.45 — validation.

**Use in thesis**
- Sections 3.10.4, 3.13, 3.17 for repeatability/reproducibility terminology.
- Section 3.10 and certificate discussion for metrological traceability.
- Section 3.17 for uncertainty terminology.
- Potentially Section 3.1 or 3.16 if “validation” is defined formally.

**CaseMetrology-specific consequence**
Because formal manual measurements use one operator, the study can characterize within-operator repeated-measurement behavior but cannot claim a between-operator reproducibility estimate.

---

### S-06 — JCGM 106:2012 conformity assessment

**Reference**

Joint Committee for Guides in Metrology.
*Evaluation of measurement data — The role of measurement uncertainty in conformity assessment*.
JCGM 106:2012.
DOI: `10.59161/JCGM106-2012`

**Use in thesis**
- Section 3.10 when establishing the eventual reference decision rule.
- Section 3.15.9 for near-limit classification.
- Section 3.16.7 for false-pass/false-fail interpretation and decision-rule context.

**Important limitation**
Calibration-certificate inputs and the reference-system session limits are resolved. The final CaseMetrology near-specification conformity rule remains a prospective statistical decision. JCGM 106 supplies the framework; it does not determine the project-specific near-limit rule.

---

## 3. VERIFIED STANDARD / PRODUCT SOURCES

### S-07 — Gauge-block standard history

**Actual certificate basis**

The CaseMetrology gauge-block certificate T26A06624 explicitly identifies:

`ASME B89.1.9-2002`

That is the correct standard/version to name when describing the basis of the actual certified gauge block.

**Current revision context**

ASME B89.1.9-2023 is identified by ASME as a revision of B89.1.9-2002 (R2012).

**Use in thesis**
- Section 3.6.
- Prefer the certificate itself as evidence for the actual reference standard.
- Mention the 2023 revision only if discussing current general standards context.

**Prohibited wording**
Do not write that certificate T26A06624 was inspected to ASME B89.1.9-2023.

---

### S-08 — Arducam B0499 camera

**Manufacturer source**

Arducam B0499 IMX296 Global Shutter USB3.0 Camera Module datasheet.

**Verified manufacturer specifications**
- B0499 product.
- IMX296 sensor.
- Global shutter.
- 1456 × 1088.
- YUY2 USB 3.0 mode supports a maximum listed frame rate of 44 fps at 1456 × 1088.

**Use in thesis**
- Section 3.3.2.

**Evidence separation**
Manufacturer documentation establishes capability/specification. CaseMetrology camera-control and acquisition records establish that the study actually used 1456 × 1088 at 44 fps.

---

### S-09 — NVIDIA Jetson Orin Nano Super Developer Kit

**Manufacturer source**

NVIDIA official Jetson Orin Nano Developer Kit User Guide / Jetson Orin Nano Super Developer Kit product documentation.

**Verified manufacturer identity**
NVIDIA identifies the platform as the Jetson Orin Nano Super Developer Kit.

**Use in thesis**
- Section 3.3.1.
- Use NVIDIA for platform identity and any vendor hardware specifications.
- Use repository runtime records for the actual L4T, kernel, power mode, Python, OpenCV, and NumPy versions.

---

### S-10 — Mitutoyo manual reference caliper

**Primary project evidence**

Calibration certificate DDJ25P23P and the preserved instrument/case identity images identify the formal manual-reference caliper as Mitutoyo code `500-196-30`, model `CD-6"ASX`, serial `B24254849`. The certificate describes a 0–6 in digital caliper, reports 0.0000-in as-left error at 1 in, and reports expanded uncertainty of 0.000126 in at 1 in (approximately 95% confidence).

**Use in thesis**
- Section 3.10 for actual instrument identity, resolution, calibration status, 1-in indication error, and calibration uncertainty.

**Limitation**
- Do not treat the manual comparator as an error-free true value. Formal interpretation must retain the frozen session-control rules and the final prospective uncertainty treatment.

---

## 4. SOURCE STILL TO SELECT / OBTAIN

### S-11 — Gaussian filtering, morphology, connected components

A standard image-processing source should be selected for:
- Gaussian smoothing.
- Binary morphological opening and closing.
- Connected-component analysis.

A standard text such as Gonzalez and Woods, *Digital Image Processing*, is a reasonable candidate, but the exact edition/page support should be checked before insertion into the thesis.

**Status:** SOURCE TO VERIFY.

---

### S-12 — Randomization, replication, experimental unit

A strong experimental-design source should be selected to support:
- randomization,
- replication,
- experimental unit,
- avoidance of pseudoreplication.

Montgomery, *Design and Analysis of Experiments*, is a reasonable candidate. An authoritative NIST engineering-statistics source may also be used.

**Status:** SOURCE TO VERIFY.

---

### S-13 — Stratified sampling

A sampling reference should be selected if Chapter 3 explains the general rationale for stratification rather than only describing the CaseMetrology sampling procedure.

Cochran, *Sampling Techniques*, is a suitable classical candidate.

**Status:** SOURCE TO VERIFY if needed.

---

## 5. SENTENCE-LEVEL CITATION PLAN

### Section 3.1
- `[REPO]` CaseMetrology-specific study design and prospective protocol.
- `[LITERATURE]` Only if explaining general randomization/validation-design principles.

### Section 3.2
- `[REPO]` Architecture.
- No outside citation needed unless discussing general distributed-system concepts.

### Section 3.3.1
- `[MANUFACTURER]` NVIDIA platform identity/specifications.
- `[REPO]` actual installed runtime/software state.

### Section 3.3.2
- `[MANUFACTURER]` Arducam sensor/product capability.
- `[REPO]` actual acquisition configuration.
- `[REPO]` physical 16 mm lens and 8.625-in distance.

### Section 3.3.3
- `[REPO]` actual light and fixture construction.
- Do not invent missing locator dimensions.

### Section 3.3.4–3.3.5
- `[REPO]` configuration control, network persistence, dashboard.

### Section 3.4
- `[REPO]` exact sequence and parameter values.
- `[LITERATURE:S-01]` Otsu method.
- `[LITERATURE:S-11]` morphology/Gaussian explanation if retained.

### Section 3.5
- `[REPO]` actual PCA/extreme-mask estimator.
- `[LITERATURE:S-02]` PCA concept.
- `[REPO]` estimator-development chronology.

### Section 3.6
- `[CERTIFICATE]` gauge block.
- `[STANDARD:S-07]` actual certificate basis when needed.
- `[REPO]` fitted calibration planes and corrected angle convention.
- `[STANDARD:S-04/S-05]` uncertainty/metrology terminology.

### Section 3.7
- `[REPO]` prevalidation/freeze rules.
- `[LITERATURE:S-12]` only for general design principles.

### Section 3.8
- `[REPO]` population and screening procedure.
- `[PENDING]` screening distribution.

### Section 3.9
- `[REPO]` actual planned selection procedure.
- `[LITERATURE:S-13]` general stratified-sampling rationale if explained.
- `[PENDING]` final strata and sample.

### Section 3.10
- `[MANUFACTURER:S-10]` caliper model/range/resolution.
- `[CERTIFICATE:PENDING]` actual calibrated performance.
- `[STANDARD:S-04/S-05/S-06]` uncertainty/traceability/decision-rule terminology.

### Section 3.11
- `[REPO]` CV acquisition/failure method.

### Section 3.12
- `[REPO]` seeds and exact run-order procedure.
- `[LITERATURE:S-12]` randomization/replication rationale.

### Section 3.13
- `[REPO]` environmental protocol.
- `[CERTIFICATE:PENDING]` thermometer/probe traceability.
- `[STANDARD:S-04/S-05]` influence/uncertainty terminology if used.

### Section 3.14
- `[REPO]` data integrity and deviations.

### Section 3.15
- `[REPO]` exact formulas/threshold implementation defined by SAP.
- `[LITERATURE:S-03]` Bland–Altman agreement.
- `[STANDARD:S-05]` repeatability/reproducibility terminology.
- `[STANDARD:S-06]` conformity/decision-rule context.

### Section 3.16
- `[REPO]` project-specific acceptance thresholds.
- `[STANDARD:S-06]` general decision-risk context.
- Do not imply JCGM 106 supplied the numerical CaseMetrology thresholds.

### Section 3.17
- `[REPO]` actual study limitations.
- `[STANDARD:S-04/S-05]` uncertainty and repeatability/reproducibility terminology.

---

## 6. IMMEDIATE THESIS CORRECTIONS / GUARDRAILS

1. `PPI_90(x,y)` must use Y coefficient `0.00442714650`.
2. Effective PPI mapping must be the corrected August 13 mapping.
3. The supported installed lens is the 16 mm CS2316ZM02, not 25 mm.
4. Manual reference measurement should not be described as error-free truth.
5. “Metrologically traceable” should be used only where the documented calibration chain supports that claim.
6. A single-operator study must not be represented as estimating between-operator reproducibility.
7. Prevalidation estimator-comparison numbers must not be presented as formal validation results.
8. The formal Chapter 4 results remain unwritten until formal data exist.
9. Current project acceptance limits are prospective CaseMetrology criteria, not values imported from JCGM or a manufacturer catalog.
10. The reference-caliper certificate review is complete; the final near-limit conformity rule remains prospectively pending the reference-uncertainty decision.

---

## 7. CURRENT SOURCE STATUS

**Core scholarly/metrology sources verified:** 10
**Image-processing textbook source still to verify:** 1
**Experimental-design source still to verify:** 1
**Sampling source still to verify if used:** 1
**Formal certificate review:** resolved; **remaining pre-measurement statistical items:** final reference-uncertainty model and near-limit conformity rule
**Formal validation results:** not yet collected
