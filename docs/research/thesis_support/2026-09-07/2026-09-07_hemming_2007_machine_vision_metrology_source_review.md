# Hemming (2007) — Machine-Vision Traceability and Uncertainty Source Review

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 full-source evidence review
**Status:** Verified core literature source

## 1. Source

Björn Hemming.

*Measurement Traceability and Uncertainty in Machine Vision Applications.*

Doctoral dissertation, Helsinki University of Technology.

Centre for Metrology and Accreditation (MIKES), Espoo, Finland, 2007.

ISBN: 978-952-5610-41-3.

The dissertation is an article-based doctoral thesis concerned specifically
with dimensional machine-vision metrology, calibration, traceability, and
measurement uncertainty.

---

## 2. Scope of the Work

Hemming addresses dimensional machine-vision applications from a metrological
rather than solely an image-processing perspective.

The dissertation is primarily limited to two-dimensional measurement
applications using one grayscale camera.

The work examines several machine-vision measurement systems, including:

- calibration of two-dimensional standards;
- optical coordinate measurement;
- automatic calibration of dial indicators; and
- automatic calibration of micrometers.

These applications are used to investigate the role of measurement uncertainty
and traceability in machine-vision measurement-system development.

---

## 3. Research Problem

The dissertation distinguishes algorithm-level accuracy from complete
measurement-system reliability.

Hemming notes that substantial literature addresses topics such as edge
detection and camera calibration, but evaluating individual algorithmic
components does not by itself establish the uncertainty of the complete
measurement process.

The dissertation asks, in substance:

- how uncertainty sources can be evaluated during development of a dimensional
  machine-vision instrument; and
- how traceability and reliable measurement can be achieved in a machine-
  vision application.

This framing is directly relevant to CaseMetrology because the thesis evaluates
a complete measurement process rather than only whether an image-processing
algorithm can produce a numerical OAL result.

---

## 4. Traceability

Hemming treats dimensional traceability as an unbroken relationship between the
machine-vision measurement and appropriate dimensional reference standards.

Line scales and two-dimensional standards are important reference artifacts in
the applications described.

The work reinforces that calibration is required to relate image-derived
measurements to physical dimensional units, but calibration alone does not
describe every uncertainty contribution affecting a final measurement result.

### CaseMetrology relevance

CaseMetrology similarly converts image-space dimensional information to
physical units using a calibrated dimensional reference and preserves the
associated calibration evidence.

Hemming supports the general metrological principle behind that process.

Hemming does not validate the specific CaseMetrology spatial/directional
calibration model or its numerical performance.

---

## 5. Complete-System Uncertainty

A central conclusion of the dissertation is that machine-vision dimensional
measurement uncertainty can arise from multiple parts of the complete
measurement system.

Examples discussed by Hemming include:

- illumination;
- edge effects and edge localization;
- camera and lens behavior;
- geometrical relationships;
- mechanical errors;
- operator-related effects; and
- non-ideal characteristics of the measured object.

The relative importance of these sources depends on the particular
measurement application.

This supports treating dimensional machine vision as a measurement-system
problem rather than reducing accuracy to sensor resolution or an isolated
image-processing algorithm.

---

## 6. Application-Dependent Dominant Error Sources

One of the most important findings for CaseMetrology is that the dominant
uncertainty contribution differed substantially among Hemming's applications.

For the automatic dial-indicator calibration equipment, an important
uncertainty contribution came from the machine-vision subsystem, including
camera/lens behavior and pointer edge finding.

For the automatic micrometer-calibration equipment, the machine-vision
uncertainty contribution was comparatively small and mechanical/geometrical
effects, including Abbe-related errors, were more important.

During development of the micrometer system, alignment-related cosine error was
also identified as an important potential contribution.

Hemming therefore concludes that uncertainty estimation should not be based
only on intuition. Mechanical, geometrical, and optical contributions need to
be considered individually for the particular measurement application.

### CaseMetrology relevance

This finding supports the cautious interpretation of formal V1 diagnostic
results.

CaseMetrology V1 showed:

- positive specimen-level bias;
- substantial placement-dependent repeated-measurement variation; and
- a round-associated shift in signed error.

The V1 experiment did not independently manipulate all possible physical,
optical, calibration, algorithmic, or session-level factors.

Hemming therefore provides methodological support for avoiding unsupported
assignment of the V1 behavior to one presumed mechanism.

Hemming does **not** establish which mechanism caused the CaseMetrology V1
results.

---

## 7. Illumination and Edge Measurement

In Hemming's optical-coordinate-measurement application for aperture
measurement, the selected illumination condition materially affected the
measured diameter and was identified as an important uncertainty source.

The associated uncertainty treatment also considered contributions such as:

- coordinate-system scale error;
- point repeatability;
- local edge irregularity; and
- edge detection.

This example demonstrates that apparently simple image-derived dimensional
measurements can depend materially on acquisition conditions and boundary
definition.

### CaseMetrology relevance

CaseMetrology uses transmitted backlighting and silhouette segmentation.

Hemming therefore supports the general need to consider illumination,
boundary localization, geometry, and calibration as possible contributors to
dimensional measurement behavior.

The source shall not be used to claim that illumination or edge localization
caused the formal CaseMetrology V1 disagreement unless a separate
CaseMetrology experiment demonstrates that relationship.

---

## 8. Measurement-Uncertainty Budgeting

Hemming applies GUM-oriented uncertainty evaluation to dimensional
machine-vision applications and argues that uncertainty budgeting provides a
structured way to identify and quantify important error sources.

A major conclusion is that different machine-vision applications can have
substantially different uncertainty budgets.

A generic or assumed uncertainty budget is therefore not sufficient merely
because two systems both use cameras for dimensional measurement.

### CaseMetrology relevance

This distinction is especially important for thesis wording.

CaseMetrology established a prospectively frozen uncertainty model for the
**manual reference measurement process**. That model combined:

- calibration uncertainty;
- manual-instrument display resolution; and
- pooled manual repeated-measurement variation.

CaseMetrology did **not** construct a complete GUM uncertainty budget for the
entire CV measurement system.

The formal V1 CV system was instead characterized empirically using:

- repeated-placement behavior;
- specimen-level bias;
- MAE;
- RMSE;
- empirical P95 absolute error;
- maximum absolute error;
- Bland-Altman agreement;
- classification performance; and
- measurement availability.

The thesis must therefore avoid describing the calculated specimen-level
`U_ref` as the uncertainty of the CaseMetrology CV system.

---

## 9. Appropriate Chapter 2 Claims

Hemming can support statements that:

1. dimensional machine vision should be treated as a measurement process, not
   merely an image-processing application;
2. calibration and dimensional traceability are essential to defensible
   physical measurements;
3. complete measurement uncertainty can depend on optical, mechanical,
   geometrical, algorithmic, environmental, operator, and object-related
   factors;
4. dominant uncertainty sources are application specific;
5. evaluating only camera calibration or edge-detection accuracy is not
   necessarily sufficient to characterize complete-system dimensional
   reliability; and
6. structured uncertainty analysis can reveal important error sources that
   may not be apparent from intuition.

---

## 10. Claims Hemming Does Not Support

The dissertation shall not be used to claim that:

- CaseMetrology has a complete GUM-compliant CV uncertainty budget;
- the CaseMetrology V1 positive bias was caused by illumination;
- the V1 round-associated shift was caused by calibration drift;
- free specimen placement was the sole source of V1 dimensional error;
- edge detection was the dominant CaseMetrology error source;
- the CaseMetrology calibration model is metrologically equivalent to
  Hemming's systems; or
- Hemming's reported uncertainty values are transferable numerical limits for
  CaseMetrology.

Those questions require CaseMetrology-specific evidence.

---

## 11. Role in Chapter 2

Hemming should be treated as a core source in:

### Section 2.2 — Vision-Based Dimensional Metrology

Use to establish that dimensional machine vision must be considered as a
complete measurement system.

### Section 2.4 — Calibration, Traceability, and Measurement Uncertainty

Use as one of the strongest application-specific sources connecting GUM-style
metrology with two-dimensional machine vision.

### Section 2.8 — Literature Synthesis and Research Position

Use to support the argument that a defensible machine-vision metrology study
requires attention to the complete measurement chain rather than algorithmic
performance alone.

---

## 12. Implication for CaseMetrology Research Position

Hemming strengthens the CaseMetrology research rationale without supplying a
novelty claim.

The important connection is methodological:

CaseMetrology treats dimensional computer vision as an integrated measurement
system that requires controlled calibration, an independent reference process,
repeatability characterization, quantified agreement, and explicit limitations.

Hemming provides strong historical metrological support for viewing
machine-vision dimensional measurement in that complete-system manner.

The CaseMetrology contribution must still be established through the complete
Chapter 2 literature synthesis rather than inferred from this source alone.
