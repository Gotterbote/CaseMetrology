# Chapter 1 Evidence and Citation Audit

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Degree:** M.S. Integrated Systems Design & Dynamics, Kansas State University
**Scope:** Computer-vision measurement of cartridge-case overall length (OAL)
**Status:** Evidence-audited working draft; formal validation has not begun.

## 1. Purpose of this audit

Chapter 1 should establish the research problem, motivation, purpose, research question, objectives, scope, significance, and thesis organization without prematurely arguing the full literature review that belongs in Chapter 2.

The main evidence rule is:

- **General claims about machine vision, metrology, uncertainty, and measurement-method validation require external sources.**
- **Claims about what CaseMetrology is, does, or will validate are supported by the project record.**
- **A definitive literature-gap claim must wait for the systematic Chapter 2 literature review.**

---

# A. Section-level evidence and citation matrix

| Section | Principal claim / role | Support type | Recommended source(s) | Disposition |
|---|---|---|---|---|
| **1.1 Background and Motivation** | Machine vision is used in industrial inspection, including dimensional-quality applications | Literature | Malamas et al. (2003); Hashmi et al. (2022) | **CITE** |
| **1.1** | Vision-based measurement can support non-contact / image-based manufacturing measurement | Literature | Hashmi et al. (2022); machine-vision metrology literature | **CITE** |
| **1.1** | Measurement results must be interpreted with calibration, uncertainty, and traceability in mind | Standard/metrology | JCGM 100:2008; JCGM 200:2012 | **CITE** |
| **1.1** | Computerized optical imaging of cartridge cases exists in published forensic work | Literature/NIST | NIST SRM 2461 page; Yammen & Muneesawang (2013); Le Bouthillier et al. (2023) | **CITE CAREFULLY** |
| **1.1** | CaseMetrology applies controlled backlit computer vision specifically to OAL measurement | Repository/project | CaseMetrology research record | **SUPPORTED NOW** |
| **1.2 Problem Statement** | Development success does not by itself establish validated dimensional agreement | Metrology + project logic | JCGM validation/verification concepts; CaseMetrology prospective protocol | **SUPPORTED + CITE CONCEPT** |
| **1.2** | Need to quantify agreement of the frozen CV method relative to an independent manual reference process | Project | Master protocol/SAP | **SUPPORTED NOW** |
| **1.2** | Literature lacks a validated cartridge-case OAL CV method | Literature-review conclusion | Chapter 2 only | **DO NOT CLAIM YET** |
| **1.3 Purpose** | Evaluate the frozen CaseMetrology OAL method under controlled static conditions | Project | Master protocol | **NO EXTERNAL CITATION NEEDED** |
| **1.4 Research Question** | Can the system meet prespecified dimensional/repeatability/agreement criteria relative to manual reference? | Project | Master protocol/SAP | **NO EXTERNAL CITATION NEEDED** |
| **1.5 Objectives** | Define the concrete research tasks that answer the question | Project | Chapter 3 / protocol mapping | **NO EXTERNAL CITATION NEEDED** |
| **1.6 Scope and Delimitations** | OAL only; static setup; one operator; one frozen configuration; no conveyor/dynamic validation | Project | Master protocol/configuration record | **SUPPORTED NOW** |
| **1.6** | Single-operator design does not estimate between-operator reproducibility | Metrology terminology | JCGM 200:2012 | **CITE** |
| **1.7 Significance** | Demonstrates a rigorous embedded machine-vision dimensional-metrology workflow if validated | Literature + project | Industrial machine-vision literature; CaseMetrology method | **SUPPORTED AS PROSPECTIVE SIGNIFICANCE** |
| **1.7** | “Low-cost” or production-speed superiority | Requires cost/throughput evidence | None currently | **DO NOT CLAIM WITHOUT DATA** |
| **1.8 Organization** | Describe chapter sequence | Thesis structure | None | **NO CITATION NEEDED** |

---

# B. Annotated sentence-level working draft

## 1.1 Background and Motivation

`[LITERATURE]` Machine vision has long been used in industrial inspection to extract measurable information from images, including applications concerned with dimensional quality, structural quality, surface quality, and operational quality.
**Primary background source:** Malamas et al. (2003), *Image and Vision Computing*, DOI `10.1016/S0262-8856(02)00152-X`.

`[LITERATURE]` Manufacturing-oriented reviews also describe vision-based measurement as a means of integrating cameras, computing hardware, and image-processing methods for rapid, non-contact assessment of geometric and process-related characteristics.
**Source:** Hashmi et al. (2022), DOI `10.1016/j.matpr.2021.11.271`.

`[STANDARD]` However, a dimensional result is not established as reliable merely because an image-processing algorithm produces a plausible numerical value. Calibration, measurement uncertainty, measurement conditions, and the relationship of the result to an appropriate reference remain central metrological considerations.
**Sources:** JCGM 100:2008; JCGM 200:2012.

`[LITERATURE/NIST]` Cartridge cases are already the subject of computerized optical measurement and image-analysis research, particularly in forensic applications involving breech-face, firing-pin, ejector, and other surface/toolmark features. NIST SRM 2461, for example, was developed to support quality assurance and measurement traceability for computerized optical imaging of cartridge-case topography.

`[GUARDRAIL]` Published forensic cartridge-case imaging should not be represented as direct evidence that manufacturing OAL can be measured accurately by the present system. The measurement targets, imaging geometry, and intended use differ.

`[REPO]` The present CaseMetrology study addresses a narrower manufacturing-metrology problem: measurement of cartridge-case overall length from a controlled static, backlit side-view image using a frozen computer-vision pipeline.

`[REPO]` Overall length was selected as the thesis measurement characteristic so that the research can concentrate on a single dimensional quantity, establish a controlled reference process, and evaluate the complete calibration-to-agreement chain without expanding the thesis into multiple simultaneous dimensional studies.

### Section 1.1 audit disposition

**External support required:** industrial machine vision; image-based measurement; metrology terminology; optional cartridge-case imaging context.
**Project support:** CaseMetrology scope and OAL choice.
**Avoid:** unsupported claims that the system is cheaper, faster, or superior to commercial inspection.

---

## 1.2 Problem Statement

`[STANDARD/REPO]` A functioning computer-vision measurement algorithm is not equivalent to a validated measurement method. Validation requires evidence that the specified requirements are adequate for the intended use and that the resulting measurement performance is acceptable under the defined conditions.

`[REPO]` CaseMetrology development and prevalidation established a frozen segmentation, estimator, spatial/directional calibration method, physical configuration, and prospective statistical analysis plan.

`[REPO]` What remains unanswered is whether that frozen system produces OAL measurements with acceptable agreement, repeated-measurement behavior, availability, and classification performance relative to the independent manual reference process on a prospectively selected specimen sample.

`[GUARDRAIL]` Chapter 1 should not state categorically that no prior cartridge-case OAL computer-vision method exists unless Chapter 2's literature search supports that conclusion.

`[LITERATURE-REVIEW PENDING]` A defensible gap statement should instead emerge from Chapter 2, which will distinguish manufacturing dimensional metrology from the much larger body of forensic cartridge-case surface-imaging and comparison research.

### Section 1.2 audit disposition

**Problem is supportable now.**
**Definitive novelty/gap wording remains Chapter-2 dependent.**

---

## 1.3 Purpose of the Study

`[REPO]` The purpose of this study is to evaluate the dimensional performance of the frozen CaseMetrology computer-vision system for static measurement of cartridge-case overall length under controlled inspection conditions.

`[REPO]` The evaluation compares specimen-level computer-vision measurements with independently acquired manual reference measurements and applies prospectively defined criteria for agreement, repeatability-related behavior, system availability, and classification performance.

`[GUARDRAIL]` The purpose is validation of the documented OAL method, not validation of all potential cartridge-case dimensions and not demonstration of an inline production inspection system.

### Section 1.3 audit disposition

**No external citation required for the purpose statement.**

---

## 1.4 Research Question

`[REPO]`

**Primary research question**

> Can the frozen CaseMetrology computer-vision system measure cartridge-case overall length with acceptable agreement and repeated-measurement performance relative to an independent manual reference measurement process under the documented static inspection conditions?

`[REPO]` The phrase **acceptable** is operationalized by the prospectively frozen validation criteria rather than determined after formal data are observed.

### Optional more explicit version

> Does the frozen CaseMetrology OAL method satisfy the prespecified criteria for computer-vision availability, repositioning-related repeated-measurement behavior, mean bias, RMSE, empirical P95 absolute error, maximum absolute error, and classification performance when evaluated against an independent manual reference measurement process?

### Audit recommendation

Use the shorter question in Chapter 1. Let Section 3.16 define the individual numerical criteria.

---

## 1.5 Research Objectives

The objectives should map directly into the methodology and later results.

### Objective 1 — Establish and freeze the measurement configuration

`[REPO]` Define and document the static backlit imaging configuration, acquisition settings, segmentation procedure, PCA/extreme-mask OAL estimator, and software environment before formal validation.

### Objective 2 — Characterize and freeze the physical-unit calibration method

`[REPO]` Characterize spatial and directional image scale using the certified gauge-block reference and freeze the calibration model and angle convention before formal validation.

### Objective 3 — Establish the independent manual reference process

`[REPO]` Define a controlled manual reference measurement procedure with instrument calibration review, certified check-standard controls, repeated measurements, and documented session acceptance criteria.

### Objective 4 — Conduct prospective formal validation

`[REPO]` Screen the eligible 235-specimen source population, select a 60-specimen stratified random sample, and obtain three manual reference measurements and three computer-vision attempts per selected specimen under independent randomized run orders.

### Objective 5 — Quantify measurement performance against prespecified criteria

`[REPO]` Evaluate repeated-measurement behavior, availability, bias, MAE, RMSE, empirical P95 absolute error, maximum absolute error, Bland–Altman-style agreement, and pass/fail classification performance using the frozen statistical analysis plan.

### Objective mapping

| Objective | Primary Chapter 3 location | Primary Chapter 4 output |
|---|---|---|
| 1. Freeze measurement configuration | 3.2–3.5, 3.7 | Configuration/precondition confirmation |
| 2. Freeze calibration | 3.6 | Calibration context; no post-hoc refit |
| 3. Establish manual reference | 3.10, 3.13 | Reference-session evidence |
| 4. Execute formal validation | 3.8–3.12 | Formal dataset/sample description |
| 5. Quantify performance | 3.15–3.16 | Agreement, availability, classification, disposition |

### Section 1.5 audit disposition

**Objectives are now aligned directly with Chapter 3 and planned Chapter 4.**

---

## 1.6 Scope and Delimitations

`[REPO]` The thesis evaluates **overall length only**. Rim geometry, primer-pocket dimensions, concentricity, and other cartridge-case characteristics are outside the formal validation scope and are reserved for future work.

`[REPO]` The measurement configuration is static. The study does not validate a conveyor, moving production part, robotic handling system, or high-speed inline inspection process.

`[REPO]` Validation is configuration-specific and applies to the documented camera, 16 mm CS-mount optic, lighting, measurement plane, installed fixture, segmentation, estimator, calibration model, and software state used during the study.

`[REPO]` The formal source population contains 235 uniquely laser-etched cases. Five development/prevalidation cases are excluded from formal eligibility, and 60 unique specimens are planned for the prospective formal sample after screening and stratification.

`[REPO/STANDARD]` The formal manual reference study uses a single operator. It therefore supports within-operator repeated-measurement characterization but does not estimate between-operator reproducibility as defined in metrology terminology.
**Source:** JCGM 200:2012.

`[REPO]` Formal conclusions will be based on the selected sample and study conditions and will not be presented as universal worst-case bounds for every cartridge case or every future optical configuration.

### Section 1.6 audit disposition

**Supported now.**
No scope expansion is needed for the M.S. thesis.

---

## 1.7 Significance of the Study

`[LITERATURE]` Industrial machine-vision systems can support dimensional inspection and automated extraction of manufacturing-quality information, but reliable implementation depends on clear measurement definitions, controlled image acquisition, and application-specific performance evaluation.

`[REPO]` The significance of CaseMetrology is therefore not merely that it applies image processing to a cartridge case. Its research contribution is the complete, prospectively controlled measurement workflow: physical configuration control, certified calibration reference, frozen segmentation and estimator logic, independent reference measurement, prospective specimen selection, explicit failure accounting, prespecified statistical analysis, and evidence-preserving research governance.

`[REPO]` If the formal acceptance criteria are satisfied, the study will provide evidence that the documented static computer-vision configuration is suitable for the defined OAL measurement purpose under the tested conditions.

`[GUARDRAIL]` Until formal validation is complete, Chapter 1 should describe this as the **intended contribution** or **potential significance**, not as a demonstrated accuracy achievement.

`[GUARDRAIL]` Do not characterize the system as “low-cost,” “production-ready,” “faster than manual inspection,” or “capable of 100% production inspection” unless those claims are supported by explicit cost, throughput, and production-environment evidence.

`[REPO]` The study can additionally provide a reusable research foundation for future work on other case dimensions, multiple operators, additional optical configurations, and dynamic manufacturing inspection, while keeping those extensions outside the present thesis.

### Section 1.7 audit disposition

**Strong prospective significance statement available now.**
**Final significance language must be updated after formal results.**

---

## 1.8 Organization of the Thesis

`[THESIS STRUCTURE]` Chapter 1 introduces the research problem, purpose, question, objectives, scope, and significance.

`[THESIS STRUCTURE]` Chapter 2 reviews relevant literature in industrial machine vision, vision-based dimensional metrology, calibration and uncertainty, measurement-method agreement, and cartridge-case imaging where relevant to the research context.

`[THESIS STRUCTURE]` Chapter 3 describes the CaseMetrology system, frozen OAL measurement method, calibration, prevalidation controls, specimen-selection procedure, manual reference process, formal computer-vision acquisition method, data governance, statistical analysis plan, acceptance criteria, and methodological limitations.

`[FORMAL-DATA-PENDING]` Chapter 4 will report only the prospectively collected formal validation results.

`[FORMAL-DATA-PENDING]` Chapter 5 will interpret those results, answer the research question, state the resulting limitations and conclusions, and identify appropriate future work.

### Section 1.8 audit disposition

**No external citation required.**

---

# C. Clean Chapter 1 working draft

## 1.1 Background and Motivation

Machine vision has become an established approach for industrial inspection and measurement, including applications concerned with dimensional quality, surface condition, structural characteristics, and operational state [MALAMAS ET AL. 2003]. Manufacturing-oriented research has also demonstrated the use of cameras, computing hardware, and image-processing methods for rapid, non-contact assessment of geometric and process-related characteristics [HASHMI ET AL. 2022].

For dimensional applications, however, the production of a plausible numerical value by an image-processing algorithm is not sufficient by itself to establish measurement suitability. Calibration, measurement uncertainty, measurement conditions, and the relationship of the result to an appropriate reference remain important metrological considerations [JCGM 100:2008; JCGM 200:2012].

Computerized optical analysis of cartridge cases is well established in forensic research, particularly for the acquisition, segmentation, and comparison of breech-face, firing-pin, ejector, and related surface features. NIST Standard Reference Material 2461, for example, supports quality assurance and measurement traceability for computerized optical imaging of cartridge-case topography [NIST SRM 2461]. This forensic literature demonstrates that cartridge cases can be analyzed using controlled optical and computational methods, but its measurement targets and intended use differ from manufacturing dimensional inspection.

The present research addresses a narrower manufacturing-metrology problem: computer-vision measurement of cartridge-case overall length from a controlled static, backlit side-view image. Overall length was selected as the formal thesis measurement characteristic so that the calibration, measurement, reference, repeated-measurement, and agreement problems could be studied rigorously without expanding the project into simultaneous validation of multiple case dimensions.

## 1.2 Problem Statement

A functioning computer-vision algorithm is not equivalent to a validated dimensional measurement method. CaseMetrology development and prevalidation have established a frozen segmentation pipeline, PCA/extreme-mask OAL estimator, spatial and directional calibration model, controlled physical configuration, and prospective statistical analysis plan. What remains unanswered is whether that frozen system produces OAL measurements with acceptable agreement, repeated-measurement behavior, availability, and classification performance relative to an independent manual reference measurement process on a prospectively selected specimen sample.

The literature review in Chapter 2 will determine how the present manufacturing OAL problem relates to prior vision-based dimensional-metrology research and to the broader cartridge-case imaging literature. Accordingly, the thesis does not assume a categorical novelty claim before that review is completed.

## 1.3 Purpose of the Study

The purpose of this study is to evaluate the dimensional performance of the frozen CaseMetrology computer-vision system for static measurement of cartridge-case overall length under controlled inspection conditions. The evaluation compares specimen-level computer-vision measurements with independently acquired manual reference measurements and applies prospectively defined criteria for agreement, repeated-measurement behavior, system availability, and classification performance.

The study is limited to validation of the documented OAL measurement method. It does not attempt to validate all cartridge-case dimensions or an inline production inspection system.

## 1.4 Research Question

The primary research question is:

> **Can the frozen CaseMetrology computer-vision system measure cartridge-case overall length with acceptable agreement and repeated-measurement performance relative to an independent manual reference measurement process under the documented static inspection conditions?**

Acceptable performance is defined by prospectively established validation criteria rather than by thresholds selected after formal data are observed.

## 1.5 Research Objectives

The study has five objectives:

1. Define and freeze the static backlit imaging configuration, acquisition settings, segmentation procedure, PCA/extreme-mask OAL estimator, and software environment before formal validation.
2. Characterize spatial and directional image scale using a certified gauge-block reference and freeze the physical-unit calibration model and angle convention before formal validation.
3. Establish a controlled manual reference measurement procedure incorporating calibration-certificate review, certified check-standard controls, repeated measurements, and documented session-acceptance criteria.
4. Screen the eligible source population, select a 60-specimen stratified random validation sample, and acquire three manual reference measurements and three computer-vision attempts per selected specimen using independently randomized run orders.
5. Quantify repeated-measurement behavior, availability, measurement agreement, error magnitude, and classification performance using the prospectively frozen statistical analysis plan and acceptance criteria.

## 1.6 Scope and Delimitations

The formal thesis evaluates cartridge-case overall length only. Rim geometry, primer-pocket dimensions, concentricity, and other case characteristics are outside the validation scope and are reserved for future research.

The measurement system is evaluated in a static configuration. The study does not validate conveyor-based inspection, moving workpieces, robotic handling, or high-speed inline manufacturing operation. The validation conclusion is specific to the documented camera, 16 mm CS-mount lens, illumination, measurement-plane geometry, installed fixture, segmentation pipeline, estimator, calibration model, and software configuration used during the study.

The source population consists of 235 uniquely laser-etched cases. Five specimens previously used during estimator prevalidation are excluded from formal eligibility. Following screening, 60 unique specimens are planned for prospective stratified random selection.

The manual reference study uses a single operator. Consequently, the design can characterize within-operator repeated-measurement behavior under the specified conditions but does not estimate between-operator measurement reproducibility [JCGM 200:2012]. Results will be interpreted as empirical findings for the selected population and documented study configuration rather than universal worst-case limits.

## 1.7 Significance of the Study

Industrial machine vision can support dimensional inspection and automated extraction of manufacturing-quality information, but application-specific measurement definitions, controlled image acquisition, calibration, and performance evaluation remain necessary for defensible dimensional use [MALAMAS ET AL. 2003; HASHMI ET AL. 2022].

The intended contribution of CaseMetrology is therefore the development and prospective evaluation of a complete embedded computer-vision metrology workflow rather than image processing alone. The study integrates physical configuration control, a certified calibration reference, a frozen segmentation and OAL estimator, an independent manual reference process, prospective specimen selection, explicit failure accounting, prespecified statistical analysis, and research-evidence preservation.

If the formal acceptance criteria are satisfied, the study will provide evidence that the documented static configuration is suitable for the defined OAL measurement purpose under the tested conditions. Regardless of the final validation outcome, the methodology and evidence record will provide a basis for future research involving additional cartridge-case dimensions, operators, optical configurations, or dynamic production inspection.

The present thesis does not claim that CaseMetrology is lower cost, faster than manual inspection, production-ready, or suitable for full-rate inline inspection because those questions are outside the formal study design.

## 1.8 Organization of the Thesis

Chapter 1 introduces the research problem, purpose, research question, objectives, scope, and significance. Chapter 2 reviews relevant literature in industrial machine vision, vision-based dimensional metrology, calibration and uncertainty, measurement-method agreement, and cartridge-case imaging where applicable to the research context.

Chapter 3 describes the CaseMetrology hardware and software configuration, frozen OAL measurement method, spatial and directional calibration, prevalidation and method-freeze controls, specimen population and sample-selection method, manual reference procedure, computer-vision validation procedure, randomization, environmental and measurement-assurance controls, data governance, statistical analysis plan, acceptance criteria, and methodological limitations.

Chapter 4 will report the formal validation results generated from the prospective study. Chapter 5 will interpret those findings, answer the research question, state the resulting conclusions and limitations, and identify appropriate directions for future work.

---

# D. Chapter 1 source dossier

## C1-S01 — Industrial vision systems

D. A. Malamas, E. G. M. Petrakis, M. Zervakis, L. Petit, and J.-D. Legat.
“A survey on industrial vision systems, applications and tools.”
*Image and Vision Computing*, 21(2), 171–188, 2003.
DOI: `10.1016/S0262-8856(02)00152-X`.

**Use:** Section 1.1 and, if desired, Section 1.7.

**Supported point:** industrial vision systems include dimensional-quality inspection and require application-specific definition of measurements, inputs, outputs, robustness, and inspection rules.

---

## C1-S02 — Machine vision measurement in manufacturing

A. W. Hashmi, H. S. Mali, A. Meena, I. A. Khilji, M. F. Hashmi, and S. N. M. Saffe.
“Machine vision for the measurement of machining parameters: A review.”
*Materials Today: Proceedings*, 56(4), 1939–1946, 2022.
DOI: `10.1016/j.matpr.2021.11.271`.

**Use:** Sections 1.1 and 1.7.

**Supported point:** manufacturing research uses machine vision and image-processing methods for non-contact measurement and assessment of geometric/manufacturing characteristics.

**Qualification:** this review emphasizes machining/tool-condition applications; do not make it carry the entire dimensional-metrology literature review.

---

## C1-S03 — Metrology uncertainty

**JCGM 100:2008** — *Evaluation of measurement data — Guide to the expression of uncertainty in measurement (GUM).*
DOI: `10.59161/JCGM100-2008E`.

**Use:** Section 1.1 and later methodology/limitations.

---

## C1-S04 — Metrology vocabulary and validation

**JCGM 200:2012** — *International Vocabulary of Metrology (VIM), 3rd edition.*

Useful concepts:
- measurement uncertainty;
- repeatability;
- reproducibility;
- metrological traceability;
- verification;
- validation.

**Use:** Sections 1.1, 1.2, and 1.6.

---

## C1-S05 — NIST cartridge-case optical reference context

NIST. **Standard Bullets and Cartridge Cases** — Standard Reference Material 2461 Standard Cartridge Case.

**Use:** Section 1.1 as cartridge-case optical-measurement context.

**Supported point:** computerized optical acquisition and measurement-quality-assurance methods are established for cartridge-case surface/topography work in forensic laboratories.

**Critical qualification:** SRM 2461 is not an OAL dimensional standard and should not be presented as validating the CaseMetrology manufacturing problem.

---

## C1-S06 — Cartridge-case image matching example

S. Yammen and P. Muneesawang.
“Cartridge case image matching using effective correlation area based method.”
*Forensic Science International*, 229(1–3), 27–42, 2013.
DOI: `10.1016/j.forsciint.2013.03.015`.

**Use:** Chapter 2 more than Chapter 1.

**Role:** demonstrates image-based computational analysis of cartridge-case base marks in forensic identification.

---

## C1-S07 — Cartridge-case ROI segmentation example

M.-E. Le Bouthillier, L. Hrynkiw, A. Beauchamp, L. Duong, and S. Ratté.
“Automated detection of regions of interest in cartridge case images using deep learning.”
*Journal of Forensic Sciences*, 68, 1958–1971, 2023.
DOI: `10.1111/1556-4029.15319`.

**Use:** primarily Chapter 2.

**Role:** contemporary example of automated image analysis of cartridge-case base regions; again, not manufacturing OAL metrology.

---

# E. Chapter 1 guardrails

1. Do not claim a definitive literature gap until Chapter 2 supports it.
2. Do not use forensic cartridge-case imaging as proof of OAL measurement accuracy.
3. Do not call the manual reference “ground truth” or “true OAL.”
4. Do not claim between-operator reproducibility from the single-operator design.
5. Do not claim production throughput, inline operation, or cost advantage.
6. Do not claim successful validation before Chapter 4 exists.
7. Keep other case dimensions outside the formal thesis scope.
8. Keep the primary research question short; place the numerical acceptance criteria in Chapter 3.
9. Ensure every objective produces a corresponding Chapter 3 method and Chapter 4 result/disposition.
10. Revisit Sections 1.2 and 1.7 after Chapter 2 and formal validation, respectively.

---

# F. Current Chapter 1 readiness

| Area | Status |
|---|---|
| Background framing | **PASS — source-supported working version** |
| Problem statement | **PASS — novelty wording intentionally conservative** |
| Purpose | **PASS** |
| Research question | **PASS** |
| Objectives | **PASS — mapped to methodology/results** |
| Scope/delimitations | **PASS** |
| Significance | **PASS as prospective wording** |
| Thesis organization | **PASS** |
| Definitive literature-gap statement | **OPEN — Chapter 2 dependent** |
| Final significance/contribution wording | **OPEN — formal-results dependent** |
| Final citation formatting | **OPEN — program/committee style dependent** |

**Overall:** Chapter 1 is structurally mature and now has a defensible evidence/citation plan. Its two legitimate future revisions are the final Chapter 2 gap conclusion and the post-validation significance/contribution wording.
