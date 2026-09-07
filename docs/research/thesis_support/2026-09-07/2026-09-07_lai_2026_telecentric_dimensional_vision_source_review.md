# Lai et al. (2026) — Telecentric Dimensional-Vision Source Review

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 literature-source verification
**Status:** Publisher-verified with substantial article sections available; full PDF review pending

## 1. Source

Zhibin Lai, Hai Li, Nianfeng Wang, and Xianmin Zhang.

"A telecentric vision system tailored for high-precision dimensional
measurement: Calibration and subpixel edge detection."

*Measurement*, Volume 274, Article 121239, 2026.

DOI: 10.1016/j.measurement.2026.121239.

The publisher record exposes the abstract, highlights, substantial
introductory material, methodological descriptions, experimental-summary
material, and conclusion material.

The source is therefore more strongly verified than an abstract-only record,
although a complete PDF review remains desirable before relying on details not
visible in the publisher text.

---

## 2. Study Purpose

The paper develops a telecentric machine-vision system specifically for
high-precision dimensional measurement.

The authors focus on two closely coupled measurement problems:

- calibration accuracy; and
- subpixel boundary localization.

The study treats these as fundamental contributors to dimensional measurement
performance rather than independent image-processing conveniences.

---

## 3. Dimensional-Vision Context

The authors distinguish between two-dimensional and three-dimensional
vision-based measurement.

For two-dimensional measurement, physical dimensions are recovered by
establishing a mapping between image coordinates and physical coordinates
through image processing and geometric modeling.

The authors identify calibration precision and boundary-localization accuracy
as central limitations on high-precision two-dimensional dimensional
measurement.

This provides contemporary literature support for treating image-derived
dimensional accuracy as a combined calibration-and-feature-localization
problem.

---

## 4. Telecentric Optical Architecture

The system uses telecentric optics.

The paper emphasizes several properties of telecentric imaging relevant to
dimensional metrology:

- reduced perspective effects;
- reduced sensitivity of magnification to object depth;
- relatively constant magnification within the usable depth range; and
- suitability for high-precision dimensional measurement.

The authors also note disadvantages including:

- higher cost; and
- smaller field of view compared with many conventional imaging systems.

---

## 5. Imaging-Model Distinction

The authors explicitly distinguish the telecentric imaging model from the
perspective pinhole model commonly used with conventional lenses.

Telecentric imaging is modeled using an affine / orthographic-type projection
relationship rather than ordinary perspective projection.

The paper notes that directly applying conventional pinhole-camera calibration
methods to telecentric systems can introduce additional error if the
telecentric geometry is not accommodated appropriately.

### CaseMetrology relevance

This distinction is important for the thesis because it demonstrates that
calibration models must correspond to the optical architecture actually used.

CaseMetrology V1 does not use a telecentric imaging model.

Its conventional-lens spatial/directional calibration therefore shall not be
described as equivalent to Lai et al.'s telecentric calibration framework.

---

## 6. Calibration Framework

The authors propose a calibration framework designed specifically for
telecentric dimensional measurement.

Rather than relying only on sparse calibration-point centers, the method uses
richer geometric information from the calibration target, including:

- position;
- shape;
- size; and
- edge / contour information.

The authors argue that dimensional measurement depends strongly on object
contours and that calibration procedures should therefore make greater use of
contour geometry.

---

## 7. Distortion Correction

The proposed framework includes a line-constraint-based distortion-correction
method.

The method uses straight-line constraints from the calibration pattern to
improve estimation of lens-distortion behavior.

The authors report particular benefit near the boundaries of the field of view,
where distortion effects can otherwise degrade dimensional measurement
accuracy.

### CaseMetrology relevance

This supports the general proposition that dimensional accuracy can vary with
image position and that calibration quality should be considered across the
usable measurement field.

It does not establish that field-position distortion caused the formal
CaseMetrology V1 errors.

---

## 8. Shape-Constrained Calibration Optimization

The paper incorporates a two-stage nonlinear optimization process.

The second stage uses shape information derived from circular calibration
features and their projected edges to refine the system parameters.

This differs from calibration strategies based only on isolated feature
centers.

The approach is explicitly motivated by dimensional measurement, for which
accurate contour geometry is particularly important.

---

## 9. Subpixel Edge Localization

The authors incorporate a subpixel edge-detection algorithm based on an error
function model.

The edge-localization method is used for both:

- calibration-feature extraction; and
- practical dimensional measurement.

The authors treat subpixel boundary localization as essential because
pixel-level edge localization is generally insufficient for the targeted
high-precision measurement regime.

---

## 10. Lighting-Intensity Compensation

The subpixel edge-detection method includes compensation for changing lighting
intensity.

The authors identify uneven illumination and exposure variation as potential
sources of edge-position error.

The compensation strategy is intended to improve robustness when illumination
conditions vary.

### CaseMetrology relevance

CaseMetrology V1 also depends on a backlit object boundary.

Lai et al. therefore supports the general principle that illumination behavior
can influence boundary localization in dimensional vision.

The source does not establish that illumination variation caused any observed
CaseMetrology V1 error.

---

## 11. Experimental Validation

The paper reports a series of experiments intended to evaluate:

- the subpixel edge-detection method;
- lighting compensation;
- distortion correction;
- calibration;
- dimensional measurement; and
- overall system performance.

The methodological components were tested individually and then as part of the
complete telecentric dimensional-measurement system.

This component-wise experimental approach is useful as a methodological
example of isolating candidate contributors to complete-system performance.

---

## 12. Reported Dimensional Performance

The authors report that the proposed telecentric system achieved:

- average measurement error below approximately 1 micrometer; and
- maximum measurement error below approximately 2 micrometers.

The corresponding reported image-space errors were:

- below approximately 0.12 pixel on average; and
- below approximately 0.25 pixel maximum.

The authors also report robustness under changing lighting conditions.

These numerical results apply only to the Lai et al. system and its
experimental conditions.

They shall not be treated as general machine-vision accuracy limits.

---

## 13. Accuracy Versus Pixel Resolution

The results provide a modern example in which dimensional accuracy substantially
smaller than one image pixel was obtained through:

- calibrated imaging geometry;
- distortion modeling;
- nonlinear calibration optimization; and
- subpixel boundary localization.

This supports the general proposition that pixel size alone does not determine
the ultimate resolution or accuracy of an image-based dimensional measurement
system.

### Important qualification

Subpixel numerical localization does not automatically establish comparable
physical measurement accuracy in another optical system.

The complete imaging, calibration, target, lighting, and measurement
conditions remain important.

---

## 14. Comparison with CaseMetrology Optical Architecture

The two systems differ materially.

Lai et al. uses:

- telecentric optics;
- a telecentric-specific calibration model;
- purpose-designed calibration features;
- distortion correction;
- contour-constrained parameter optimization; and
- dedicated subpixel boundary localization.

CaseMetrology V1 uses:

- a conventional 16 mm CS-mount lens;
- a fixed area camera;
- transmitted backlighting;
- a clear Lexan measurement surface;
- spatial and directional image-to-physical calibration;
- Otsu-based silhouette segmentation; and
- a PCA/extreme-mask OAL estimator.

The systems shall not be treated as directly equivalent.

---

## 15. Specimen-Depth Guardrail

Telecentric optics are specifically intended to reduce sensitivity of
magnification to small object-depth changes.

CaseMetrology V1 does not use telecentric optics.

However, Lai et al. shall not be used to infer that uncontrolled object depth
caused the formal V1 bias or round-associated behavior.

The V1 experiment did not prospectively isolate specimen-depth variation as an
experimental factor.

---

## 16. Edge-Localization Guardrail

Lai et al. demonstrates that subpixel edge localization can materially support
high-precision dimensional measurement.

The source does not establish that the CaseMetrology PCA/extreme-mask estimator
requires the same edge-localization algorithm.

It also does not establish that CaseMetrology V1 error was dominated by
pixel-level endpoint localization.

The CaseMetrology estimator operates on a complete segmented silhouette and has
different endpoint logic.

---

## 17. Calibration Guardrail

The Lai calibration framework was developed for telecentric imaging.

It shall not be used to claim that:

- CaseMetrology's calibration model was inadequate;
- telecentric calibration equations should have been applied to V1;
- the formal V1 positive bias resulted from calibration-model error; or
- the observed round-associated shift resulted from distortion.

Those questions require CaseMetrology-specific experimental evidence.

---

## 18. Lighting Guardrail

The paper demonstrates experimentally that lighting compensation can improve
edge-localization robustness in its telecentric measurement system.

It shall not be used to claim that:

- CaseMetrology backlight output varied materially during V1;
- lighting variation caused the formal V1 bias;
- lighting variation caused the round-associated shift; or
- lighting compensation alone would resolve the V1 disagreement.

Those mechanisms remain unverified for CaseMetrology.

---

## 19. Appropriate Chapter 2 Claims

Lai et al. can support statements that:

1. high-precision two-dimensional machine-vision measurement depends strongly
   on calibration accuracy and boundary localization;
2. optical architecture determines the appropriate imaging and calibration
   model;
3. telecentric optics can reduce perspective-related dimensional sensitivity;
4. distortion correction can be important across the measurement field;
5. calibration can benefit from using contour and shape information rather
   than sparse point centers alone;
6. subpixel edge localization can support dimensional precision finer than one
   image pixel;
7. illumination variation can influence subpixel edge localization; and
8. calibration, image formation, feature localization, and dimensional
   conversion should be evaluated as an integrated measurement process.

---

## 20. Claims the Source Does Not Support for CaseMetrology

Lai et al. shall not be used to claim that:

- telecentric optics are required for CaseMetrology;
- the CaseMetrology V1 system could necessarily achieve micrometer-level
  accuracy by changing lenses;
- CaseMetrology calibration was invalid;
- the PCA/extreme-mask estimator is inferior to subpixel edge detection;
- lighting variation caused the V1 errors;
- lens distortion caused the V1 round shift;
- specimen-depth variation caused the V1 placement-dependent result;
- telecentric optics would eliminate CaseMetrology positive bias; or
- Lai's numerical errors are appropriate acceptance limits for CaseMetrology.

---

## 21. Relation to Wang et al. (2024)

Wang et al. and Lai et al. provide complementary literature perspectives.

Wang et al. examines how relative geometry between calibration and measurement
planes can affect monocular dimensional accuracy and includes conventional and
telecentric lenses.

Lai et al. focuses on maximizing dimensional accuracy within a telecentric
architecture through:

- telecentric-specific calibration;
- distortion correction;
- shape-based optimization; and
- robust subpixel edge localization.

Together, these sources reinforce the importance of matching:

- optical architecture;
- calibration model;
- measurement geometry; and
- feature-localization method.

Neither source establishes the cause of the CaseMetrology V1 results.

---

## 22. Relation to Hemming and Lazzari/Iuculano

Hemming and Lazzari/Iuculano provide the metrological framework for treating
machine vision as a complete dimensional measurement system.

Lai et al. provides a contemporary implementation example showing how that
complete-system problem can manifest technically through:

- optical architecture;
- calibration;
- distortion;
- contour geometry;
- edge localization; and
- lighting sensitivity.

The sources are therefore complementary rather than interchangeable.

---

## 23. Information Still Needed from Full PDF Review

A complete article copy should be reviewed to verify:

1. camera make and model;
2. camera resolution and pixel size;
3. telecentric lens specifications;
4. working distance;
5. depth of field;
6. field of view;
7. calibration-target dimensions and certification status;
8. exact distortion model;
9. exact nonlinear optimization equations;
10. full subpixel error-function formulation;
11. illumination-compensation equations;
12. measurement specimens;
13. dimensional reference instruments or standards;
14. reference traceability;
15. number of repeated measurements;
16. exact average-error calculation;
17. exact maximum-error calculation;
18. repeatability statistics;
19. uncertainty analysis, if any;
20. field-position dependence;
21. robustness experiments;
22. limitations explicitly stated by the authors; and
23. applicability limits of the proposed calibration model.

---

## 24. Chapter 2 Role

### Section 2.2 — Vision-Based Dimensional Metrology

Use as a current example of high-precision two-dimensional dimensional vision
in which calibration and edge localization are treated jointly.

### Section 2.3 — Image Segmentation, Thresholding, and Geometric Measurement

Use to contrast pixel-level boundary detection with measurement-oriented
subpixel edge localization.

Do not imply that CaseMetrology should have used the same algorithm.

### Section 2.4 — Calibration, Traceability, and Measurement Uncertainty

Use to show that the imaging model and calibration method must correspond to
the optical architecture used.

Do not characterize the Lai system as metrologically traceable unless the full
paper establishes the traceability chain.

### Section 2.8 — Literature Synthesis and Research Position

Use as modern evidence that high-precision dimensional machine vision depends
on integrated control and characterization of optics, calibration, image
formation, and boundary measurement.

---

## 25. CaseMetrology Interpretation Guardrail

Lai et al. identifies several factors that are scientifically plausible targets
for future CaseMetrology engineering investigation:

- optical architecture;
- distortion;
- spatial calibration;
- edge localization;
- illumination stability; and
- specimen-depth sensitivity.

These are prospective engineering questions.

They shall not be used retrospectively to assign causes to the preserved V1
formal results.

The mechanism of the V1 positive bias, placement-dependent variation, and
round-associated shift remains unresolved.
