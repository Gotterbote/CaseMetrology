# Wang et al. (2024) — Camera External Parameters and Measurement Accuracy Source Review

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 literature-source verification
**Status:** Publisher-verified; complete article review pending

## 1. Source

Shun Wang, Xianyou Li, Yufei Zhang, and Ke Xu.

"Effects of camera external parameters error on measurement accuracy in
monocular vision."

*Measurement*, Volume 229, Article 114413, 2024.

DOI: 10.1016/j.measurement.2024.114413.

The bibliographic record, abstract, principal theoretical conclusions, and
publisher-exposed experimental details below are confirmed by the publisher
record.

---

## 2. Study Purpose

The study investigates dimensional measurement error in monocular vision when
the physical measurement plane does not coincide with the plane used during
camera calibration.

The authors focus specifically on camera external-parameter effects involving
relative translation and rotation between the calibration plane and the
measurement plane.

This differs from studies concerned primarily with:

- image-feature extraction;
- internal camera calibration parameters;
- lens distortion; or
- image-coordinate localization error.

---

## 3. Metrological Problem

The authors identify a practical problem in monocular dimensional measurement.

A vision system may be calibrated for a defined physical plane, but the actual
measured object or surface may later occupy a different position or
orientation.

Potential causes discussed by the authors include:

- motion mechanisms;
- repeated-motion error; and
- equipment vibration.

If the physical measurement plane differs from the calibration plane, the
mapping between image coordinates and physical dimensions can change and
produce dimensional error.

---

## 4. Theoretical Framework

The paper analyzes measurement-plane misalignment using:

- a two-dimensional camera imaging model;
- the pinhole-camera model; and
- a projection-transformation-matrix formulation.

The authors derive mathematical expressions for dimensional measurement error
when translation and rotation occur between the measurement plane and the
calibration plane.

The purpose of the derivation is to quantify relationships that are often
treated only qualitatively in practical machine-vision systems.

---

## 5. Perpendicular Optical-Axis Case

For the case in which the camera optical axis is perpendicular to the
measurement plane, the publisher abstract reports several theoretical
conclusions.

Under the authors' model, measurement error is independent of:

- the camera principal-point coordinates;
- translation within the measurement plane; and
- rotation about the camera optical axis.

The derived measurement error instead exhibits:

- a linear relationship with translation in the optical-axis direction; and
- an inverse relationship with normalized focal length.

These conclusions apply to the particular geometric assumptions and
measurement model developed in the paper.

They shall not be generalized beyond those assumptions without full review of
the derivation.

---

## 6. Nonperpendicular Geometry

When the camera optical axis is not perpendicular to the calibration plane,
the authors report a more complex relationship.

Measurement error then depends nonlinearly on combinations of camera internal
and external parameters.

This reinforces the general principle that dimensional image calibration is
geometry dependent.

The accessible source does not justify reducing the nonperpendicular case to a
single transferable correction factor.

---

## 7. Experimental Verification

The authors constructed an experimental monocular vision system to evaluate
translation and rotation effects separately.

Publisher-exposed experimental details identify:

- a Basler acA5472-5gm grayscale industrial camera;
- image resolution of 5472 x 3648 pixels;
- an industrial lens;
- a telecentric lens;
- diffuse backlighting; and
- a height-adjustment table.

The system was configured so that controlled translation and rotation could be
introduced between the calibrated and measured geometry.

---

## 8. Conventional and Telecentric Optics

The theoretical model was evaluated experimentally with both:

- a conventional industrial lens; and
- a telecentric lens.

This is particularly useful for Chapter 2 because it demonstrates that the
authors examined external-geometry effects across two materially different
optical configurations.

The source shall not be used to imply that the conventional industrial lens
used by Wang et al. is optically equivalent to the CaseMetrology 16 mm
CS-mount lens.

---

## 9. Evaluation of the Model

The authors compared experimental measurement behavior with the theoretical
error relationships.

The publisher record states that experimental data were evaluated using:

- root mean square error; and
- Pearson correlation coefficient.

The experimental and theoretical functions showed consistent trends, which the
authors interpreted as supporting the validity of the derived error model.

These statistics evaluate agreement between the predicted and observed error
behavior in the Wang et al. experiment.

They are not equivalent to the CaseMetrology specimen-level RMSE or
measurement-method agreement analysis.

---

## 10. Relevance to CaseMetrology

Wang et al. provides strong literature support for the general proposition that
monocular dimensional measurement depends on maintaining or correctly modeling
the geometric relationship among:

- camera;
- calibration plane;
- measurement plane; and
- measured object.

The source is therefore relevant to CaseMetrology's emphasis on:

- fixed camera-to-measurement geometry;
- spatial calibration;
- directional calibration;
- measurement-plane control; and
- preservation of the frozen physical configuration.

It also supports the broader Chapter 2 argument that dimensional measurement
accuracy cannot be inferred from image resolution or segmentation performance
alone.

---

## 11. Important CaseMetrology Geometry Distinction

Formal CaseMetrology V1 used independent free placement on the same clear
Lexan measurement surface.

Free placement allowed variation in:

- lateral image-plane position; and
- small in-plane angular orientation.

The formal study did not prospectively manipulate or independently quantify:

- translation of the specimen support surface along the camera optical axis;
- tilt of the support plane relative to the calibrated plane; or
- camera-to-plane displacement between individual acquisitions.

Accordingly, Wang et al.'s measurement-plane-displacement mechanism is not
demonstrated to have occurred in CaseMetrology V1.

---

## 12. Calibration-Plane Causality Guardrail

Wang et al. shall not be used to claim that CaseMetrology V1 errors were caused
by departure from the calibration plane.

In particular, the source does not establish the cause of:

- the positive V1 specimen-level mean bias;
- the round-associated shift in signed error;
- the observed independent-placement repeatability result;
- the largest specimen-level errors; or
- the classification errors.

Those outcomes remain empirical CaseMetrology results whose mechanisms were not
isolated by the V1 design.

---

## 13. Placement Terminology Guardrail

The word "placement" has different meanings in the two studies.

Wang et al. primarily analyzes relative pose differences between the
measurement plane and calibration plane, including translation and rotation in
three-dimensional camera geometry.

CaseMetrology V1 "placement-dependent repeatability" refers to complete removal
and independent replacement of a cartridge case on the same clear Lexan
measurement surface, with unconstrained lateral position and small in-plane
angle.

These concepts overlap only at a broad physical-geometry level.

They shall not be treated as experimentally equivalent.

---

## 14. Appropriate Chapter 2 Claims

At the current evidence level, Wang et al. can support statements that:

1. dimensional accuracy in monocular vision depends on the relationship between
   the calibrated geometry and the actual measurement geometry;
2. displacement of the measurement plane from the calibration plane can
   introduce systematic dimensional error;
3. external camera / plane geometry can be analyzed quantitatively rather than
   only qualitatively;
4. optical-axis translation can have a predictable effect under simplified
   perpendicular-plane assumptions;
5. external-parameter effects can differ when more general rotational and
   translational geometry is considered; and
6. such behavior can be evaluated experimentally using both conventional and
   telecentric optical systems.

---

## 15. Claims the Source Does Not Support for CaseMetrology

Wang et al. shall not be used to claim that:

- CaseMetrology specimens moved out of the calibration plane during V1;
- the V1 positive bias was caused by axial displacement;
- the V1 round shift was caused by camera or fixture motion;
- lateral free placement caused the formal V1 bias;
- small in-plane rotation necessarily caused dimensional error;
- a telecentric lens would automatically resolve the V1 disagreement;
- CaseMetrology's effective-PPI model is theoretically incorrect; or
- the Wang error equations can be applied numerically to V1 without matching
  the required geometric assumptions and measured inputs.

---

## 16. Information Still Needed from Complete Article Review

Complete review should determine:

1. industrial-lens model and focal length;
2. telecentric-lens specifications;
3. pixel size of the camera;
4. exact calibration procedure;
5. dimensional target or reference artifact;
6. measurement feature used in experiments;
7. range of axial translations tested;
8. range of rotations tested;
9. exact measurement-error equations;
10. normalized-focal-length definition;
11. quantitative experimental error values;
12. RMSE values for theoretical-versus-experimental behavior;
13. Pearson correlation results;
14. uncertainty or repeatability of the introduced translation and rotation;
15. whether repeated measurements were performed at each condition;
16. whether image-field position was independently varied;
17. whether lens distortion was corrected; and
18. limitations explicitly stated by the authors.

---

## 17. Chapter 2 Role

### Section 2.2 — Vision-Based Dimensional Metrology

Use to demonstrate that camera/measurement-plane geometry is a fundamental
component of monocular dimensional measurement.

### Section 2.4 — Calibration, Traceability, and Measurement Uncertainty

Use to illustrate that calibration is valid within a defined geometric
relationship and that departure from that relationship can introduce
measurement error.

Do not use the source as evidence of metrological traceability unless the
complete article establishes traceability of the experimental references.

### Section 2.8 — Literature Synthesis and Research Position

Use to support the broader conclusion that dimensional machine-vision
performance depends on the complete physical and calibration configuration,
not solely image-processing accuracy.

---

## 18. Implication for Future CaseMetrology Work

Wang et al. identifies measurement-plane geometry as a scientifically
reasonable factor to control or manipulate in future machine-vision metrology
experiments.

A future CaseMetrology engineering study could prospectively test effects such
as:

- controlled out-of-plane displacement;
- support-plane tilt;
- known lateral image position;
- controlled in-plane rotation; and
- optical configuration.

Such work would constitute a new experiment.

The Wang et al. source does not justify retrospective causal attribution of the
preserved formal V1 results.

---

## 19. Research Interpretation Guardrail

The role of this source is explanatory and prospective.

It helps establish why physical geometry is an important consideration in
monocular dimensional metrology and why future investigations should isolate
geometric variables experimentally.

It does not resolve the mechanism responsible for CaseMetrology V1 behavior.

The V1 mechanism remains unresolved.
