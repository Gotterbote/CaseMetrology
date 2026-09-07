# Xiang et al. (2018) — Brake-Pad Dimensional Vision Source Review

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 literature-source verification
**Status:** Publisher-verified; full article review pending

## 1. Source

Rong Xiang, Wenhui He, Xinna Zhang, Dong Wang, and Yuekang Shan.

"Size measurement based on a two-camera machine vision system for the bayonets
of automobile brake pads."

*Measurement*, Volume 122, 106-116, 2018.

DOI: 10.1016/j.measurement.2018.03.017.

The bibliographic record and principal methodological and performance claims
below are confirmed by the publisher record.

---

## 2. Study Purpose

The study developed a two-camera machine-vision system for high-accuracy
dimensional measurement of automobile brake-pad bayonets.

The target bayonet dimension was approximately 130.9 mm.

The work was intended for quantitative online dimensional measurement rather
than only qualitative go/no-go inspection.

---

## 3. Measurement Architecture

The system used two cameras to capture local images around the left and right
measurement regions of the brake-pad bayonet.

The method used backlighting so that dimensional edge locations could be
identified from the captured images.

The authors used a specially designed dimensional standard with known left and
right standard edges.

The standard was used during calibration, while the corresponding left and
right edges of the measured bayonet were used during measurement.

---

## 4. Relative Measurement Principle

The method was based on relative dimensional measurement.

The measurement process included two general stages:

1. calibration using the specially designed standard; and
2. measurement of the brake-pad bayonet.

Images of the standard edges were acquired during calibration.

During measurement, images of the corresponding detected bayonet edges were
acquired.

The final dimensional result was derived from the relative positions of the
standard and measured edges using the authors' measurement equation.

This approach differs from a simple global pixels-per-unit conversion.

---

## 5. Image Processing

The reported method included:

- automatic definition of regions of interest around detected edges;
- edge detection;
- linear fitting of detected edges; and
- calculation of the bayonet dimension from the derived measurement equation.

The available publisher material does not provide enough detail to reproduce
the exact edge detector, fitting implementation, or complete uncertainty
behavior.

Those details remain pending full-paper review.

---

## 6. Prospective Performance Requirements

The study stated target performance requirements for the dimensional
measurement system.

For the approximately 130.9 mm bayonet dimension, the reported design goals
included:

- bias smaller than approximately +/-0.02 mm; and
- repeatability smaller than approximately +/-0.02 mm.

These were application-specific requirements for the brake-pad measurement
system.

They shall not be interpreted as general machine-vision dimensional-metrology
standards.

---

## 7. Reported Performance

The publisher-reported experimental results were:

- repeatability: approximately +/-0.019 mm;
- average bias: approximately 0.003 mm; and
- average measurement time: approximately 0.396 s per brake pad.

The authors reported that these results satisfied the stated requirements for
online measurement of the brake-pad bayonet.

These values characterize the Xiang et al. system only.

They are not directly transferable as numerical benchmarks for CaseMetrology.

---

## 8. Relevance to CaseMetrology

Xiang et al. is relevant because it demonstrates a manufacturing dimensional
machine-vision system that integrates:

- backlit imaging;
- dimensional calibration;
- known reference edges;
- edge localization;
- geometric fitting;
- quantitative dimensional output;
- explicit bias evaluation; and
- repeatability evaluation.

This makes the source especially useful for Chapter 2 discussion of the
difference between merely obtaining an image-derived dimension and evaluating
the measurement behavior of the complete vision system.

---

## 9. Important Architectural Differences

The Xiang et al. system and CaseMetrology address different dimensional
measurement problems.

Xiang et al. used:

- two cameras;
- local edge images;
- a specially designed standard;
- a relative edge-position measurement principle; and
- a large approximately 130.9 mm measured feature.

CaseMetrology V1 used:

- one two-dimensional area camera;
- a complete cartridge-case silhouette;
- a certified 1-in dimensional reference for spatial/directional calibration;
- a PCA/extreme-mask OAL estimator; and
- cartridge-case dimensions near 1 in.

The numerical performance of the two systems therefore shall not be compared
as though they were equivalent measurement architectures.

---

## 10. Bias and Repeatability Comparison Guardrail

Xiang et al. explicitly reported both bias and repeatability.

This supports the general Chapter 2 proposition that dimensional machine-vision
performance can and should be evaluated with more than a single accuracy or
correlation claim.

However, the term repeatability must be interpreted according to the experiment
actually performed in that study.

Until the full article is reviewed, it is not established whether the reported
repeatability incorporated:

- complete removal and replacement of the workpiece;
- repeated physical repositioning;
- repeated calibration;
- different acquisition sessions; or
- only repeated observations under substantially fixed presentation.

The Xiang repeatability result therefore shall not be represented as equivalent
to the CaseMetrology V1 independent-free-placement repeatability metric.

---

## 11. Appropriate Chapter 2 Claims

At the current evidence level, Xiang et al. can support statements that:

1. backlit machine vision has been used for quantitative dimensional
   measurement in manufacturing;
2. dimensional standards can be incorporated directly into image-based
   calibration or relative measurement;
3. edge detection and geometric fitting can be used to derive physical
   dimensions;
4. bias and repeatability can be evaluated explicitly for a machine-vision
   dimensional measurement system; and
5. vision-derived dimensional measurements can be assessed against
   application-specific performance requirements.

---

## 12. Claims Not Yet Supported

Until the complete article is reviewed, Xiang et al. shall not be used to claim
that:

- its repeatability incorporated independent workpiece repositioning;
- its reference standard was metrologically traceable to a national standard;
- it performed a complete GUM uncertainty analysis;
- its dimensional bias was dominated by calibration error;
- its edge detector was the principal source of error;
- its calibration approach is equivalent to CaseMetrology's spatial/directional
  calibration model; or
- its numerical bias/repeatability values constitute appropriate acceptance
  limits for CaseMetrology.

---

## 13. Information Still Needed from the Full Article

Full-paper review should determine:

1. camera models and resolutions;
2. lens type and optical geometry;
3. exact backlight configuration;
4. specimen-support and positioning method;
5. dimensional-standard material and certification status;
6. calibration procedure;
7. exact measurement equations;
8. edge-detection method;
9. linear-fitting method;
10. number of repeated measurements;
11. definition and calculation of repeatability;
12. definition and calculation of bias;
13. reference instrument or assigned value used for bias calculation;
14. whether position dependence was tested;
15. whether calibration drift was evaluated;
16. whether measurement uncertainty was estimated; and
17. whether the validation dataset was independent of algorithm development.

---

## 14. Chapter 2 Role

### Section 2.2 — Vision-Based Dimensional Metrology

Use as a modern peer-reviewed example of backlit dimensional measurement using
multiple cameras, calibrated standard edges, image processing, and relative
measurement.

### Section 2.4 — Calibration, Traceability, and Measurement Uncertainty

Use cautiously to illustrate incorporation of a dimensional standard into
machine-vision calibration.

Do not describe the standard as traceable unless the full article establishes
that fact.

### Section 2.8 — Literature Synthesis and Research Position

Use to support the broader conclusion that dimensional machine-vision systems
are evaluated through calibration, bias, repeatability, and application-specific
requirements rather than image-processing output alone.

---

## 15. CaseMetrology Interpretation Guardrail

The Xiang et al. results may provide useful methodological comparison but shall
not be used retrospectively to explain the formal CaseMetrology V1 performance.

In particular, the source does not establish the cause of:

- the CaseMetrology positive bias;
- placement-dependent repeated-measurement variation; or
- the round-associated shift in signed error.

Those mechanisms remain unresolved within the V1 experimental evidence.
