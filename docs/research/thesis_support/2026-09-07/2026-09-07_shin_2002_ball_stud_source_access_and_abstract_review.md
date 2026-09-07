# Shin, Han, and Moon (2002) — Ball-Stud Machine-Vision Source Review

**Project:** CaseMetrology
**Date:** 2026-09-07
**Purpose:** Chapter 2 literature-source verification
**Status:** Abstract-verified; full article review pending

## 1. Source

Dongik Shin, Changsoo Han, and Young Shik Moon.

"Ball stud inspection system using machine vision."

*ISA Transactions*, 41(1), 3-11, 2002.

DOI: 10.1016/S0019-0578(07)60197-9.

PMID: 12014800.

The bibliographic record is independently confirmed by the publisher and
PubMed.

---

## 2. Verified Source-Level Claims

The publisher abstract supports the following claims.

The study designed and implemented a machine-vision system for dimensional
inspection of a ball stud.

The system:

- acquired silhouetted images using backlighting;
- extracted object outlines at subpixel accuracy;
- modeled boundary data using geometric primitives;
- estimated geometric-model parameters by an error-minimizing procedure;
- incorporated jig fixtures and servo systems;
- rotated the inspected object to address geometry not confined to one plane;
- moved the object vertically to acquire images of different portions of the
  part; and
- evaluated system performance using a standard ball, a standard cylinder, and
  a ball stud.

These statements are supported directly by the published abstract.

---

## 3. Relevance to CaseMetrology

The source is a strong conceptual comparator for CaseMetrology because both
systems use machine vision for dimensional measurement of manufactured metal
components and both rely on silhouette information produced by backlighting.

The study is especially relevant to Chapter 2 themes involving:

- transmitted-light dimensional imaging;
- silhouette boundary localization;
- subpixel edge measurement;
- geometric interpretation of image boundaries;
- physical specimen presentation; and
- use of dimensional standards or reference objects during performance
  evaluation.

---

## 4. Physical-Presentation Contrast

The abstract explicitly states that jig fixtures and servo systems were
developed for the inspection system.

The object was also actively rotated and translated vertically during
inspection.

This provides a useful architectural contrast with formal CaseMetrology V1.

CaseMetrology V1 used independent free specimen placement on the clear Lexan
measurement surface, with gross base-to-mouth orientation maintained but
without mechanical registration of exact image-plane position.

The Shin et al. system therefore appears to use substantially more controlled
physical presentation and motion.

The full article must be reviewed before describing the exact fixture geometry,
registration tolerances, or positioning repeatability.

---

## 5. Boundary and Geometric Measurement

The abstract states that silhouetted object outlines were extracted with
subpixel accuracy and that boundary data were modeled using geometric
primitives.

This is relevant to the general principle that dimensional measurement from a
silhouette depends not only on binary object detection but also on how object
boundaries are localized and interpreted geometrically.

The abstract does not provide enough detail to establish:

- the specific subpixel algorithm;
- its numerical localization uncertainty;
- the exact geometric fitting equations;
- whether edge localization was the dominant error contribution; or
- whether the method is directly comparable to the CaseMetrology
  PCA/extreme-mask endpoint estimator.

Those details remain pending full-paper review.

---

## 6. Standards and Performance Evaluation

The abstract states that system performance was evaluated by measuring:

- a standard ball;
- a standard cylinder; and
- a ball stud.

This supports the statement that the system was evaluated against known or
standard dimensional objects.

The abstract does not establish:

- certificate traceability of those standards;
- calibration uncertainty;
- the number of repeated measurements;
- statistical repeatability;
- bias;
- RMSE;
- limits of agreement;
- measurement uncertainty; or
- prospectively defined acceptance criteria.

These points must not be inferred without the full article.

---

## 7. Important Claims Not Yet Verified

The following information is required from the full article before being used
in Chapter 2:

1. camera and lens configuration;
2. field of view and nominal pixel scale;
3. exact illumination arrangement;
4. fixture design and specimen-location constraints;
5. calibration procedure;
6. dimensional-reference values and traceability;
7. subpixel edge-detection algorithm;
8. geometric-fitting model;
9. reported dimensional accuracy;
10. reported repeatability or standard deviation;
11. number of validation measurements;
12. whether repeated removal/repositioning was studied;
13. whether error across image position was evaluated;
14. whether measurement uncertainty was estimated; and
15. how measured ball-stud dimensions were compared with reference values.

---

## 8. Appropriate Chapter 2 Claims at Current Evidence Level

Until the full article is reviewed, Shin et al. can safely support statements
that:

- backlit silhouette imaging has been used for dimensional machine-vision
  inspection of manufactured components;
- subpixel boundary extraction can be incorporated into such dimensional
  systems;
- geometric fitting can be used to derive dimensional information from
  extracted boundaries;
- mechanically controlled presentation using fixtures and servo motion has
  been used in machine-vision dimensional inspection; and
- standard geometric objects have been used to evaluate dimensional
  machine-vision performance.

---

## 9. Claims the Abstract Does Not Support

The source shall not yet be used to claim that:

- the Shin et al. system achieved a particular dimensional accuracy;
- it met a specified tolerance;
- it had lower or higher repeatability than CaseMetrology;
- jig fixturing caused its performance;
- subpixel edge extraction caused improved accuracy;
- its calibration was traceable to a national standard;
- it performed a GUM uncertainty analysis;
- it studied independent repeated placement; or
- its validation design was equivalent to the CaseMetrology formal study.

---

## 10. Chapter 2 Role

At the current evidence level, Shin et al. belongs primarily in:

### Section 2.2 — Vision-Based Dimensional Metrology

Use as a peer-reviewed example of backlit, silhouette-based dimensional machine
vision using subpixel boundary localization and geometric modeling.

### Section 2.8 — Literature Synthesis and Research Position

Use to show that physical specimen presentation, imaging geometry, and boundary
measurement are integral elements of a dimensional machine-vision system.

Do not make numerical performance comparisons until the full article has been
obtained and reviewed.

---

## 11. Source-Access Status

Publisher access confirms the article metadata and abstract but does not expose
the full article without organizational or paid access.

PubMed independently confirms the bibliographic record and abstract.

The full article should be obtained through Kansas State University library
access, interlibrary loan, or another legitimate scholarly-access route before
the source is promoted to full-review status.

Once obtained, the full article should be preserved or referenced according to
the project's literature-evidence governance process.
