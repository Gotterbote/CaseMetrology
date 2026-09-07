# Modern Vision-Based Dimensional Metrology — Candidate Source Matrix

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 targeted literature discovery
**Status:** Candidate-source screening record; full-paper review pending

## 1. Purpose

This record documents the targeted discovery stage for modern scholarly
literature relevant to CaseMetrology.

Inclusion at this stage means that bibliographic metadata, abstract material,
or publisher-provided source information indicates potential relevance.

Inclusion does not mean that the source has yet been approved for a specific
thesis claim. Full-paper review is required before substantive source-dependent
claims are incorporated into Chapter 2.

---

## 2. Priority A — Direct Technical or Metrological Comparators

### A1. Shin, Han, and Moon (2002)

Dongik Shin, Changsoo Han, and Young Shik Moon.

"Ball stud inspection system using machine vision."

ISA Transactions, 41(1), 3-11, 2002.

DOI: 10.1016/S0019-0578(07)60197-9

Candidate relevance:
- dimensional machine-vision inspection;
- backlit silhouette acquisition;
- subpixel boundary extraction;
- geometric modeling of measured boundaries;
- fixture-based specimen presentation.

Why important to CaseMetrology:
This is a strong comparison for silhouette-based dimensional inspection while
also providing a useful contrast between mechanically controlled presentation
and the independent free-placement condition used in CaseMetrology V1.

Disposition:
FULL-PAPER REVIEW — HIGH PRIORITY.

---

### A2. Lazzari and Iuculano (2004)

Annarita Lazzari and Gaetano Iuculano.

"Evaluation of the uncertainty of an optical machine with a vision system for
contact-less three-dimensional measurement."

Measurement, 36(3-4), 215-231, 2004.

DOI: 10.1016/j.measurement.2004.09.003

Candidate relevance:
- optical dimensional measurement;
- vision systems as measurement instruments;
- measurement uncertainty;
- industrial dimensional control.

Why important to CaseMetrology:
Provides a metrological bridge between general machine vision and formal
measurement-system characterization.

Disposition:
FULL-PAPER REVIEW — HIGH PRIORITY.

---

### A3. Hemming (2007)

Björn Hemming.

Measurement Traceability and Uncertainty in Machine Vision Applications.

Doctoral dissertation, Helsinki University of Technology / Centre for
Metrology and Accreditation (MIKES), 2007.

Candidate relevance:
- machine vision for dimensional measurement;
- SI traceability;
- calibration;
- measurement uncertainty;
- GUM-based uncertainty analysis;
- optical coordinate measurement.

Why important to CaseMetrology:
Directly addresses the distinction between obtaining dimensions from images and
establishing a traceable dimensional measurement process.

Disposition:
FULL-TEXT REVIEW — HIGH PRIORITY.

Authoritative full-text record is available through Aalto University / MIKES.

---

### A4. Xiang et al. (2018)

Rong Xiang, Wenhui He, Xinna Zhang, Dong Wang, and Yuekang Shan.

"Size measurement based on a two-camera machine vision system for the bayonets
of automobile brake pads."

Measurement, 122, 106-116, 2018.

DOI: 10.1016/j.measurement.2018.03.017

Candidate relevance:
- backlit dimensional measurement;
- calibration using designed standard edges;
- relative dimensional measurement;
- edge detection;
- bias evaluation;
- repeatability evaluation;
- manufacturing inspection.

Publisher-reported performance:
- average bias approximately 0.003 mm;
- repeatability approximately +/-0.019 mm;
- average measurement time approximately 0.396 s per brake pad.

Why important to CaseMetrology:
Provides a peer-reviewed example in which calibration, bias, and repeatability
are explicitly evaluated for a backlit industrial dimensional measurement
system.

Disposition:
FULL-PAPER REVIEW — HIGH PRIORITY.

---

### A5. Che and Ratnam (2018)

J. K. Che and M. M. Ratnam.

"Real-time monitoring of workpiece diameter during turning by vision method."

Measurement, 126, 369-377, 2018.

DOI: 10.1016/j.measurement.2018.05.089

Candidate relevance:
- LED backlighting;
- dimensional measurement;
- subpixel edge localization;
- pixel-to-physical correction;
- direct comparison with digital-caliper measurements;
- real-time manufacturing context.

Why important to CaseMetrology:
Provides a useful example of a vision-derived dimension evaluated against a
manual contact measurement.

Disposition:
FULL-PAPER REVIEW — HIGH PRIORITY.

---

### A6. Wang et al. (2024)

Shun Wang, Xianyou Li, Yufei Zhang, and Ke Xu.

"Effects of camera external parameters error on measurement accuracy in
monocular vision."

Measurement, 229, 114413, 2024.

DOI: 10.1016/j.measurement.2024.114413

Candidate relevance:
- monocular dimensional measurement;
- camera external parameters;
- measurement-plane misalignment;
- quantitative measurement error;
- conventional industrial lens;
- telecentric lens comparison.

Why important to CaseMetrology:
Directly supports investigation of how physical measurement geometry and
departure from calibration conditions can affect dimensional results.

Important guardrail:
This source shall not be used to claim that measurement-plane misalignment
caused the V1 CaseMetrology error. V1 did not experimentally isolate that
mechanism.

Disposition:
FULL-PAPER REVIEW — HIGH PRIORITY.

---

## 3. Priority B — Modern Integrated Dimensional-Vision Comparators

### B1. Li et al. (2021)

Xuebing Li, Yan Yang, Yingxin Ye, Songhua Ma, and Tianliang Hu.

"An online visual measurement method for workpiece dimension based on deep
learning."

Measurement, 185, 110032, 2021.

DOI: 10.1016/j.measurement.2021.110032

Candidate relevance:
- online workpiece dimensional measurement;
- image preprocessing;
- edge extraction;
- industrial measurement;
- modern computer-vision implementation.

Publisher-reported measurement accuracy:
approximately 0.02 mm.

Important distinction:
The method uses deep-learning-based processing and shall not be treated as
algorithmically equivalent to the frozen CaseMetrology segmentation/estimator.

Disposition:
FULL-PAPER REVIEW — MEDIUM PRIORITY.

---

### B2. Ullah et al. (2021)

"IoT-enabled computer vision-based parts inspection system for SME 4.0."

Microprocessors and Microsystems, 87, 104354, 2021.

DOI: 10.1016/j.micpro.2021.104354

Candidate relevance:
- integrated camera-based parts inspection;
- multiple area cameras;
- backlighting;
- camera/lens-distortion calibration;
- binarization and edge extraction;
- pixel-to-physical measurement mapping;
- total-length measurement;
- embedded / connected manufacturing architecture.

Publisher-reported maximum dimensional difference:
approximately +/-0.05 mm for the reported test parts.

Why useful:
Provides a modern integrated-system comparison rather than an isolated image-
processing algorithm.

Disposition:
FULL-PAPER REVIEW — MEDIUM PRIORITY.

---

### B3. Lai et al. (2026)

Zhibin Lai, Hai Li, Nianfeng Wang, and Xianmin Zhang.

"A telecentric vision system tailored for high-precision dimensional
measurement: Calibration and subpixel edge detection."

Measurement, 274, 121239, 2026.

DOI: 10.1016/j.measurement.2026.121239

Candidate relevance:
- modern precision dimensional vision;
- calibration;
- distortion correction;
- object contours;
- subpixel edge detection;
- lighting sensitivity.

Why important:
Provides contemporary evidence that calibration quality and edge localization
remain central limitations even in modern high-precision dimensional vision
systems.

Important distinction:
The system uses telecentric optics. It is therefore a useful technological
contrast, not a direct hardware-performance comparator for conventional-lens
CaseMetrology V1.

Disposition:
FULL-PAPER REVIEW — MEDIUM/HIGH PRIORITY.

---

## 4. Cross-Source Questions for Full Review

For each candidate source, the full-paper review should determine:

1. What physical dimension was measured?
2. Was the object imaged by transmitted backlighting, reflected light, or
   another illumination geometry?
3. Was an area camera, line camera, or other detector used?
4. Was the optical system conventional/entocentric, telecentric, or otherwise
   specialized?
5. How was the specimen physically positioned or constrained?
6. How was pixel/image space mapped to physical units?
7. What reference standard or comparator was used?
8. Was bias/trueness evaluated?
9. Was repeatability or repeated-placement behavior evaluated?
10. Was measurement uncertainty evaluated?
11. Was accuracy evaluated across the image field or at multiple specimen
    positions/orientations?
12. Were the validation specimens independent from method development?
13. Were numerical acceptance criteria defined prospectively?
14. What claims does the source actually support for Chapter 2?
15. What claims must NOT be inferred from the source?

---

## 5. Emerging Literature Themes

The candidate literature presently suggests that defensible vision-based
dimensional measurement commonly requires attention to multiple interacting
elements:

- optical geometry;
- calibration;
- location of the measurement plane;
- specimen presentation;
- image contrast and illumination;
- boundary or edge localization;
- pixel-to-physical transformation;
- comparison with an appropriate reference;
- repeatability; and
- measurement uncertainty.

This is a working synthesis only.

It shall not be converted into a definitive literature conclusion until the
priority sources have undergone full-paper review.

---

## 6. CaseMetrology Interpretation Guardrail

Sources concerning calibration-plane error, edge localization, optical
distortion, or specimen position may identify plausible mechanisms that are
relevant to future CaseMetrology engineering investigation.

They shall not be used retrospectively to assign a cause to the formal V1
round-associated shift, positive bias, or placement-dependent repeatability
result unless the CaseMetrology experimental evidence independently supports
that causal attribution.

The V1 mechanism remains unresolved.
