# CaseMetrology Final Thesis Architecture

**Date:** 2026-09-17
**Purpose:** Define the structure, research chronology, claim boundaries, and evidence basis for the final master's thesis before drafting the replacement manuscript.

## Working Title

**Engineering Evaluation of an Embedded Computer-Vision System for Static Dimensional Screening of Cartridge-Case Overall Length**

This working title intentionally emphasizes engineering evaluation and dimensional screening. It does not imply that the system has been demonstrated as a replacement for precision contact metrology or as a production-ready inline inspection system.

## Central Thesis

The completed research demonstrates substantially improved measurement stability for an embedded, backlit computer-vision system under controlled static presentation and supports the feasibility of using that architecture for cartridge-case overall-length screening. Residual absolute measurement error prevents treating the demonstrated prototype as interchangeable with precision reference metrology across the full specification interval.

Successive engineering iterations showed that part-presentation repeatability and absolute dimensional accuracy were distinct system limitations.

Controlled presentation in V3 substantially reduced placement-dependent variability, while absolute error remained materially larger. Exploratory guarded decision analysis further showed how the system could support a screening architecture in which measurements comfortably inside specification are candidates for automatic acceptance and near-limit measurements are referred for secondary inspection.

## Research Chronology

The thesis will preserve the actual chronology of the research rather than retroactively representing all analyses as prospectively planned.

### Phase 1 — Original Formal Validation: V1

V1 evaluated the original frozen CaseMetrology OAL measurement system using the PCA-based estimator.

The original prospective research question was whether the system could achieve acceptable dimensional agreement, repeated-measurement performance, availability, and classification behavior relative to an independent manual reference process.

V1 did not meet all predeclared performance criteria.

Principal V1 results included:

- Availability: 100%
- Bias: +0.001613 in
- RMSE: 0.002205 in
- P95 absolute error: 0.003960 in
- P95 repositioning: 0.004831 in

V1 therefore established the formal baseline and revealed substantial placement-dependent variability.

### Phase 2 — Post-V1 Engineering Investigation

Post-V1 diagnostic work investigated possible sources of the observed variability.

The diagnostic program included evaluation of lighting behavior, repositioning sensitivity, fixture behavior, and physical presentation.

The evidence increasingly indicated that uncontrolled or insufficiently controlled physical presentation was a major contributor to repeated-measurement variation.

These diagnostics will be presented as engineering investigation following V1, not as part of the original prospective V1 validation.

### Phase 3 — V2 Fixture Improvement

V2 introduced fixture changes intended to improve part stability while retaining the existing overall optical architecture.

Formal V2 PCA results were:

- Availability: 100%
- Bias: +0.000277 in
- RMSE: 0.001538 in
- P95 absolute error: 0.003065 in
- P95 repositioning: 0.003994 in

V2 improved several performance measures relative to V1 but did not reduce repositioning variation to the desired level.

### Phase 4 — Endface-Hybrid Estimator Development

The Endface-Hybrid estimator was developed using non-formal development data.

It was then applied retrospectively to previously acquired V2 images.

The V2 Endface-Hybrid results were:

- Availability: 100%
- Bias: -0.000505 in
- RMSE: 0.001601 in
- P95 absolute error: 0.003109 in
- P95 repositioning: 0.003021 in

These results are comparative and diagnostic evidence.

They must not be described as prospective V2 validation because the estimator was applied retrospectively to already-acquired V2 images.

### Phase 5 — Controlled-Presentation Development

Development testing following V2 investigated physical presentation more directly.

Controlled roll orientation and removal of rocking or other presentation freedom materially reduced repeated-measurement variation in development specimens.

These findings supported freezing a V3 configuration based on:

- controlled physical presentation,
- fixture retention,
- fixed roll orientation,
- the frozen Endface-Hybrid estimator,
- the existing camera and 16 mm C-mount optical configuration,
- and the existing formal specimen cohort.

### Phase 6 — Prospective V3 Formal Validation

The Endface-Hybrid estimator and V3 configuration were frozen before formal V3 acquisition.

All 180 formal V3 images were acquired before estimator-result interpretation.

V3 therefore provides the prospective formal evaluation of the frozen Endface-Hybrid system under controlled presentation.

Formal V3 results were:

- Availability: 180/180 = 100%
- Bias: -0.000435 in
- MAE: 0.001531 in
- RMSE: 0.001804 in
- P95 absolute error: 0.003267 in
- P95 repositioning: 0.000633 in
- False passes: 1
- False fails: 3

V3 met the predeclared targets for:

- availability,
- absolute bias,
- RMSE,
- and P95 repositioning.

V3 did not meet:

- the P95 absolute-error target,
- or the zero-false-pass preference under the unguarded specification rule.

## Principal Engineering Finding

The most important experimental result is the separation of repeatability from absolute accuracy.

P95 repositioning changed from:

- V1 PCA: 0.004831 in
- V2 PCA: 0.003994 in
- V2 Endface-Hybrid: 0.003021 in
- V3 Endface-Hybrid: 0.000633 in

V3 therefore reduced P95 repositioning by approximately 86.9% relative to V1.

However, V3 P95 absolute error remained 0.003267 in.

The improvement in physical repeatability therefore did not produce a proportional improvement in absolute dimensional accuracy.

The evidence supports the conclusion that placement-dependent variation and residual absolute measurement error were distinct engineering limitations.

The formal data demonstrate the existence of the residual absolute-error component but do not uniquely establish its physical cause.

Possible mechanisms may be discussed only as possible contributors unless independently supported by experimental evidence.

## Industrial Screening Interpretation

The completed prototype was not demonstrated to be interchangeable with precision contact metrology across the full 0.9900-1.0100 in specification interval.

The research does support evaluation of the system as a dimensional screening architecture.

A screening architecture can distinguish among:

1. measurements sufficiently inside the guarded acceptance interval for potential automatic acceptance;
2. measurements outside the guarded acceptance interval but near or within the original specification limits requiring secondary inspection;
3. measurements outside the original specification limits requiring rejection, confirmation, or investigation according to the eventual production decision process.

This interpretation recognizes measurement uncertainty rather than assuming it has been eliminated.

## Exploratory Guard-Band Analysis

Guard-band analysis was performed after formal V3 results were available and is therefore retrospective and exploratory.

The smallest observed symmetric guard that eliminated false passes in the 60-specimen validation cohort was 0.0006 in.

That value must not be described as a validated production guard band.

A simpler 0.0010 in symmetric guard provides a useful engineering example:

- automatic-accept interval: 0.9910-1.0090 in;
- 34 of 60 validation specimens automatically accepted;
- 9 specimens in the near-limit review zone;
- zero observed false passes.

Because the formal cohort was intentionally stratified around the specification limits, these fractions are not estimates of production yield.

The analysis demonstrates decision-behavior feasibility, not validation of a production acceptance rule.

# Research Questions

## Original Prospective Validation Question

The engineering-synthesis and industrial-feasibility questions below were formulated to organize interpretation of the completed experimental sequence; they are not presented as prospectively defined V1 hypotheses.

The original validation question remains explicitly preserved:

**Can the frozen CaseMetrology computer-vision system measure cartridge-case overall length with acceptable agreement and repeated-measurement performance relative to an independent manual reference measurement process under documented static inspection conditions?**

The thesis will answer this question using the originally established performance criteria and will report where those criteria were and were not satisfied.

## Completed-Study Engineering Synthesis Question

A second question will be identified explicitly as the engineering synthesis arising from the completed sequence of experiments:

**What do successive CaseMetrology design iterations reveal about the roles of physical presentation, estimator design, and residual measurement error in the feasibility of embedded computer-vision OAL screening?**

This question does not replace or retroactively redefine the original prospective validation question.

It synthesizes the engineering evidence produced by V1, post-V1 diagnostics, V2, estimator development, and prospective V3 validation.

## Exploratory Industrial-Feasibility Question

A third question will be identified as exploratory:

**Can guarded decision logic provide a practical pathway for using the demonstrated measurement system as a dimensional screening tool while reducing observed false-pass risk near specification limits?**

This question is addressed only as exploratory feasibility analysis.

# Thesis Objectives

The final thesis will distinguish original prospective validation objectives from subsequent engineering objectives.

## Original Validation Objectives

1. Establish and freeze the static imaging and OAL measurement configuration.
2. Establish dimensional calibration and reference-measurement controls.
3. Conduct formal comparison of CV OAL measurements with an independent manual reference process.
4. Quantify bias, error magnitude, repeated-measurement behavior, availability, and classification performance.
5. Determine whether the original system satisfied prospectively defined validation criteria.

## Subsequent Engineering Objectives

6. Investigate the dominant sources of formal repeated-measurement variability revealed by V1.
7. Evaluate fixture and physical-presentation modifications through V2 and controlled-presentation development.
8. Evaluate the frozen Endface-Hybrid estimator prospectively under the V3 controlled-presentation configuration.
9. Determine whether improved presentation repeatability also produced proportional improvement in absolute dimensional accuracy.
10. Explore whether guarded decision logic could support an industrial dimensional-screening architecture.

# Proposed Chapter Structure

## Chapter 1 — Introduction

Chapter 1 will establish:

- industrial dimensional-inspection context;
- the cartridge-case OAL measurement problem;
- distinction between dimensional measurement and dimensional screening;
- the original prospective validation question;
- the subsequent engineering-synthesis question;
- exploratory industrial-feasibility question;
- research objectives;
- scope and delimitations;
- significance of the completed research;
- contribution of the V1-V3 progression.

Chapter 1 will not present V1 as the end of the study.

## Chapter 2 — Literature Review

Most of the existing literature-review material can be reused after audit.

The final literature review should cover:

- industrial machine vision;
- backlit dimensional inspection;
- monocular dimensional metrology;
- optical geometry and measurement-plane effects;
- subpixel and boundary localization;
- calibration and traceability;
- measurement uncertainty;
- measurement-system agreement;
- repeatability and reproducibility;
- physical presentation and fixturing;
- dimensional decision rules and guard-band concepts;
- cartridge-case optical measurement and inspection.

The literature review should support the completed industrial-screening interpretation without claiming novelty where historical cartridge-case optical measurement already exists.

## Chapter 3 — Methodology

Chapter 3 will be reorganized around the experimental chronology.

### 3.1 System Architecture

- Jetson embedded platform
- Arducam IMX296 camera
- 16 mm C-mount lens
- LED backlight
- measurement geometry
- software environment
- image-processing architecture

### 3.2 Calibration and Reference Measurement

- dimensional scale
- gauge-block reference
- manual caliper reference process
- check-standard controls
- environmental observations
- reference uncertainty

### 3.3 Population and Formal Cohort

- 235 identified cases
- excluded development specimens
- screening procedure
- frozen 60-specimen stratified cohort
- randomization
- three-round measurement design

### 3.4 V1 Formal Validation

- V1 frozen configuration
- acquisition
- prospective criteria
- analysis definitions

### 3.5 Post-V1 Diagnostics

- lighting investigation
- controlled repositioning
- fixture investigation
- interpretation boundaries

### 3.6 V2 Engineering Iteration and Validation

- fixture modifications
- formal V2 PCA evaluation

### 3.7 Endface-Hybrid Development and Retrospective V2 Evaluation

- development-data boundary
- estimator freeze
- retrospective nature of V2 Hybrid analysis

### 3.8 V3 Controlled-Presentation Development and Freeze

- presentation changes
- fixture-retention verification
- controlled roll
- estimator freeze
- acquisition blinding
- preacquisition audit

### 3.9 V3 Prospective Formal Validation

- three acquisition rounds
- verification
- processing
- statistical metrics

### 3.10 Exploratory Guard-Band Analysis

- post-validation status
- decision-rule definition
- cohort limitations
- interpretation boundaries

## Chapter 4 — Results

Chapter 4 will report results, not advocacy.

### 4.1 V1 Formal Results

### 4.2 Post-V1 Diagnostic Findings

### 4.3 V2 Formal PCA Results

### 4.4 Retrospective V2 Endface-Hybrid Results

### 4.5 Controlled-Presentation Development Evidence

### 4.6 V3 Prospective Formal Results

### 4.7 V1-V2-V3 Comparative Results

A central comparison table will include:

| Metric | V1 PCA | V2 PCA | V2 Hybrid | V3 Hybrid |
|---|---:|---:|---:|---:|
| Availability | 100% | 100% | 100% | 100% |
| Bias (in) | +0.001613 | +0.000277 | -0.000505 | -0.000435 |
| RMSE (in) | 0.002205 | 0.001538 | 0.001601 | 0.001804 |
| P95 absolute error (in) | 0.003960 | 0.003065 | 0.003109 | 0.003267 |
| P95 repositioning (in) | 0.004831 | 0.003994 | 0.003021 | 0.000633 |

The table will clearly mark V2 Hybrid as retrospective.

### 4.8 Exploratory Guard-Band Results

Guard-band results will be reported separately from prospective validation results.

## Chapter 5 — Discussion and Conclusions

### 5.1 Answer to the Original Validation Question

State clearly which predefined criteria were met and which were not.

### 5.2 Engineering Progression

Interpret V1 through V3 as a sequence of evidence-based design changes rather than isolated experiments.

### 5.3 Repeatability Versus Absolute Accuracy

This will be a central discussion section.

The evidence demonstrates that controlling presentation reduced repeated-measurement variation substantially without proportionally reducing absolute measurement error.

### 5.4 Industrial Screening Feasibility

Discuss what the system can reasonably support under the demonstrated conditions.

### 5.5 Guarded Decision Logic

Discuss the exploratory guard-band analysis without representing it as production validation.

### 5.6 Limitations

At minimum:

- one operator;
- one formal 60-specimen stratified cohort;
- static measurement only;
- no production conveyor;
- no full production throughput study;
- conventional non-telecentric optics;
- manual reference uncertainty;
- residual absolute-error mechanism not uniquely isolated;
- retrospective nature of V2 Hybrid analysis;
- retrospective nature of guard-band selection;
- results limited to documented hardware, geometry, software, and specimen population.

### 5.7 Future Work

Potential future work may include:

- independent prospective validation of a predefined guard band;
- additional operators;
- additional specimen populations;
- improved optical architecture;
- automated handling;
- throughput evaluation;
- other cartridge-case dimensions;
- formal measurement-system capability studies under production conditions.

### 5.8 Final Conclusion

The final conclusion should state that the research produced a validated engineering understanding of the prototype's capabilities and limitations.

The strongest contribution is not that CaseMetrology achieved precision-gage equivalence.

The contribution is that successive controlled experiments demonstrated how physical presentation affected repeatability, separated repeatability limitations from residual absolute measurement error, and established a defensible pathway for using embedded computer vision as a guarded dimensional-screening technology.

# Claim Boundaries

The thesis will not claim that CaseMetrology is:

- production-ready;
- validated for inline conveyor inspection;
- interchangeable with the manual reference instrument;
- accurate to ±0.002 in for every measurement;
- validated with the retrospective 0.0006 in guard band;
- proven to achieve a particular production yield;
- proven faster than manual inspection unless a throughput study is completed;
- universally applicable to cartridge cases outside the tested population and configuration.

# Evidence Preservation

Every thesis-critical numerical claim should be traceable to repository evidence.

Current key records include:

- frozen V1 analysis artifacts;
- V2 formal analysis artifacts;
- V2 Endface-Hybrid retrospective analysis;
- V3 formal acquisition and estimator-processing records;
- `2026-09-17_v3_formal_performance_and_guard_band_analysis.md`;
- `2026-09-17_v1_v2_v3_engineering_progression.md`;
- V3 formal acquisition commits;
- estimator freeze evidence and SHA-256 records.

No substantive final-thesis claim should exist only in conversation history.

# Manuscript Strategy

The September 7 manuscript is retained as source material.

A new manuscript will be written from this architecture.

Existing text may be reused when:

- the factual content remains correct;
- it matches the final research scope;
- the chronology remains accurate;
- the claim is supported by preserved evidence;
- and the passage does not imply that later work was prospectively planned when it was not.

The new manuscript will therefore be a reconstruction from verified evidence rather than a line-by-line rewrite of the earlier V1-centered manuscript.