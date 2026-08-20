# Chapter 3 Narrative-Flow Review and Visual/Appendix Plan

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Status:** Working thesis-support record; repository commit deferred.

## 1. Overall assessment

Chapter 3 is now methodologically complete enough to read as a coherent thesis methodology chapter rather than a collection of engineering notes. The principal remaining gaps are evidence that does not yet exist—manual-reference certificate review, environmental calibration evidence, screening/sample data, and formal validation results—not missing methodology.

The narrative-polished revision does **not** change the frozen method. It only improves organization and terminology.

## 2. Consistency edits made

### Estimator chronology centralized

The detailed estimator-selection chronology now lives primarily in **Section 3.7 Prevalidation Engineering and Method Freeze**.

Section 3.5 now concentrates on:
- what the PCA/extreme-mask estimator does;
- how pixel length is defined;
- which general PCA concept requires literature support.

This avoids telling the August 7/August 13 development history twice.

### Randomization centralized

Sections 3.10 and 3.11 still state the required three replicates and full removal/repositioning because those are part of the manual and CV procedures.

The actual randomization seeds and design rationale are centralized in **Section 3.12 Randomization and Replication**:
- manual seed `2026081901`;
- CV seed `2026081902`.

### Measurement-assurance repetition reduced

Section 3.10 remains the primary location for the five pre-session and five post-session gauge-block readings.

Section 3.13 now cross-references that procedure rather than reproducing it in full.

### “Traceability” terminology clarified

Section 3.14 was renamed from:

> Data Integrity, Traceability, and Protocol Deviations

to:

> **Data Integrity, Research Provenance, and Protocol Deviations**

This prevents confusion between:
- **metrological traceability**, which has a specific VIM meaning and depends on calibration chains; and
- repository/data provenance, which is supported by Git, manifests, identifiers, and preserved artifacts.

### False-pass language strengthened

Section 3.16 now states that zero false passes are the prospective desired outcome and that any confirmed false pass is a material validation result.

This is more defensible than treating “zero false passes preferred” as a vague preference.

### Transitions added

Short transitions were added:
- from hardware/software into image processing;
- from final method description into prevalidation freeze;
- from method freeze into specimen selection;
- from acquisition/governance into statistical analysis.

These make the chapter read as one research process rather than 17 independent subsections.

---

## 3. Recommended main-chapter figures

### Figure 3.1 — CaseMetrology system architecture

**Purpose:** show the dimensional-computation path and distinguish it from supporting network infrastructure.

Include:
- backlit specimen/fixture;
- Arducam camera;
- Jetson acquisition;
- segmentation;
- PCA OAL measurement;
- spatial calibration;
- local authoritative measurement artifact;
- durable outbox;
- office receiver/dashboard as a separate supporting branch.

**Important:** visually show that network/dashboard components do not feed back into dimensional computation.

### Figure 3.2 — Physical OAL imaging configuration

**Purpose:** make the optical geometry understandable without burying the reader in prose.

Show:
- camera;
- 16 mm CS2316ZM02 lens;
- measurement plane;
- 8.625-in camera-to-plane distance;
- clear Lexan working surface;
- backlight;
- cartridge case lying horizontally;
- locator.

Do not add unrecorded external locator dimensions.

### Figure 3.3 — Frozen segmentation pipeline

Recommended sequence:

`Measurement image + blank → blank subtraction → 5×5 Gaussian → Otsu → 3×3 open → 3×3 close → largest component → quality gates`

**Purpose:** allows Section 3.4 to remain concise while making the exact frozen processing sequence obvious.

### Figure 3.4 — PCA/extreme-mask OAL geometry

Show:
- accepted specimen mask;
- PCA/refined longitudinal axis;
- centroid;
- minimum and maximum projections;
- pixel OAL vector;
- rounded base/head versus straight-cut mouth.

**Purpose:** explains the estimator more clearly than prose alone.

### Figure 3.5 — Spatial/directional calibration model

Show:
- A–D fitting locations;
- E holdout location;
- the two principal calibration directions;
- cartridge-case OAL angle theta;
- relationship between `PPI_0`, `PPI_90`, and `PPI_effective`.

This figure is particularly valuable because the historical plane labels and corrected directional convention are easy to misunderstand verbally.

### Figure 3.6 — Formal validation workflow

Recommended flow:

`235-case population`
→ `exclude prevalidation specimens`
→ `screen eligible population`
→ `define strata`
→ `randomly select 60`
→ `manual reference phase: 3 reps/specimen`
→ `CV phase: 3 attempts/specimen`
→ `frozen statistical analysis`
→ `acceptance-criteria disposition`

**Purpose:** gives the committee a one-page view of the prospective design.

---

## 4. Recommended main-chapter tables

### Table 3.1 — Hardware and software configuration

Suggested rows:
- Jetson platform;
- L4T/kernel;
- power mode;
- Python;
- OpenCV;
- NumPy;
- camera;
- acquisition mode;
- lens;
- working distance;
- backlight;
- working-surface material.

This can shorten Sections 3.3.1–3.3.3.

### Table 3.2 — Frozen image-processing and measurement configuration

Suggested rows:
- blank subtraction;
- Gaussian filter;
- threshold method;
- morphology;
- component rule;
- estimator;
- calibration model;
- quality/failure behavior.

This makes method freeze easy to audit.

### Table 3.3 — Formal validation design

Suggested columns:
- phase;
- population/sample;
- repetitions;
- repositioning;
- randomization;
- output.

Rows:
- screening;
- manual reference;
- CV validation.

### Table 3.4 — Formal CV attempt-status definitions

Rows:
- `VALID`;
- `SYSTEM_FAILURE`;
- `PROTOCOL_INVALID`.

Columns:
- definition;
- included in availability denominator?;
- automatic replacement?;
- agreement-analysis treatment.

This will prevent ambiguity during defense questioning.

### Table 3.5 — Validation acceptance criteria

Rows:
- availability;
- repositioning P95;
- absolute mean bias;
- RMSE;
- P95 absolute specimen error;
- maximum absolute specimen error;
- false-pass disposition;
- material-deviation requirement.

This should remain in Chapter 3 because the criteria were frozen prospectively.

---

## 5. Material better suited to appendices or supplementary records

### Appendix candidate A — Detailed hardware/software environment

Move lower-level details here if Section 3.3 becomes too dense:
- complete OS/runtime dump;
- device enumeration;
- persistent symlink rule;
- detailed package/version outputs.

Keep the key configuration in the main chapter.

### Appendix candidate B — Calibration evidence

Possible contents:
- certificate summary;
- full calibration grid definition;
- fitting observations;
- holdout observations;
- calibration residual tables;
- historical angle-convention correction record.

Keep the equations and corrected interpretation in Section 3.6.

### Appendix candidate C — Estimator-development chronology

Possible contents:
- geometry alternative;
- maximum-gradient subpixel work;
- Subpixel V2;
- visual overlays;
- comparative prevalidation tables.

The main chapter should preserve only enough chronology to explain and defend the final method choice.

### Appendix candidate D — Formal validation operational controls

Possible contents:
- screening protocol;
- session-reference forms;
- deviation form;
- attempt-status decision tree;
- full master protocol;
- full statistical analysis plan.

The main chapter should summarize them sufficiently for reproducibility.

### Appendix candidate E — Formal study identifiers and run orders

After formal selection:
- final 60 specimen IDs;
- stratum membership;
- randomized manual order;
- randomized CV order.

These are important audit artifacts but would clutter the methodology narrative.

---

## 6. Material that should remain in the main chapter

Do **not** move these out of Chapter 3:

- core research design;
- primary physical configuration;
- 16 mm optical configuration;
- segmentation sequence;
- PCA/extreme-mask definition;
- spatial calibration equations;
- corrected angle convention;
- development/formal-validation separation;
- population/sample design;
- manual reference methodology;
- CV failure rules;
- statistical definitions;
- acceptance criteria;
- methodological limitations.

Those items are necessary to understand and reproduce the thesis method.

---

## 7. Defense-oriented consistency questions now answered

### “Why did you use PCA?”
The chapter can answer this at two levels:
1. PCA provides a geometric longitudinal axis.
2. The final PCA/extreme-mask method was selected prospectively after prevalidation comparison, before formal validation.

### “Why didn't you use the geometry estimator?”
The method history is preserved: it was temporarily selected during development, then superseded after physical-unit comparison favored PCA/extreme-mask.

### “Is the caliper ground truth?”
No. It is the independent manual reference measurement process and has calibration, resolution, repeatability, and uncertainty limitations.

### “Are 180 CV readings your sample size?”
No. The primary experimental unit is the unique specimen, with n = 60. The 180 planned acquisitions are repeated opportunities across those specimens.

### “Did you tune the algorithm after seeing validation data?”
The prospective method-freeze/change-control design is explicitly documented to prevent that.

### “What happens when the CV system fails?”
A genuine `SYSTEM_FAILURE` is preserved and affects availability; it is not automatically retaken to manufacture a successful result.

### “Does the dashboard affect the measurement?”
No. The Jetson-local measurement is authoritative; the network and dashboard are supporting infrastructure outside the dimensional-computation path.

### “Can the results be generalized to an inline production system?”
No. The thesis explicitly limits validation to the documented static configuration.

---

## 8. Current Chapter 3 readiness assessment

### Method definition
**PASS**

### Evidence mapping
**PASS**

### External scholarly/standard source plan
**PASS**

### Development-versus-validation separation
**PASS**

### Configuration continuity
**PASS**

### Statistical analysis prespecification
**PASS**

### Acceptance criteria prespecification
**PASS**

### Manual-reference calibration evidence
**OPEN — external dependency**

### Environmental calibration evidence
**OPEN — external dependency**

### Screening/final sample
**OPEN — formal work not yet performed**

### Formal results
**OPEN — correctly absent**

### Final citation formatting
**OPEN — committee/program style decision**

## Overall

**Chapter 3 is structurally and methodologically mature. Remaining open items are principally legitimate certificate/formal-study dependencies rather than unresolved research design.**
