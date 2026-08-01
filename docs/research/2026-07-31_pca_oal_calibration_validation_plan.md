# PCA Fixtureless OAL Calibration and Physical-Validation Plan

**Project:** CaseMetrology  
**Research area:** Fixtureless top-down computer-vision metrology  
**Measurement characteristic:** Overall length (OAL)  
**Candidate estimator:** PCA axis plus extreme accepted-mask projections  
**Document type:** Prospective calibration and validation protocol  
**Plan date:** 2026-07-31  
**Current specification:** nominal OAL ±0.010 inch  
**Total tolerance width:** 0.020 inch  
**Dataset status:** Future independent physical-validation data  
**Existing Trial 03 and Trial 05 images:** Development evidence only  
**Plan status:** Draft for approval before new physical data collection

---

## 1. Purpose

This plan defines the calibration, ground-truth, data-collection, analysis, acceptance, and documentation procedures required to determine whether the PCA-based fixtureless OAL estimator is adequate for the current manufacturing specification of nominal ±0.010 inch.

The PCA estimator remains the provisional candidate because, among the algorithms evaluated on the existing development dataset, it produced:

- the smallest range among Trial 05 orientation-group medians;
- the smallest full observed Trial 05 range;
- complete measurement availability;
- the simplest implementation and lowest operational complexity.

This plan does not assume that the PCA estimator is accurate in inches. It establishes how accuracy, repeatability, repositioning effects, orientation effects, bias, and pass/fail performance will be measured prospectively.

---

## 2. Research questions

### 2.1 Primary question

Can the frozen PCA OAL estimator measure fixtureless case OAL with sufficiently small total error and uncertainty to support reliable decisions for a nominal ±0.010-inch specification?

### 2.2 Secondary questions

1. Is the image scale stable at the actual case measurement plane?
2. Does the estimator exhibit measurable bias relative to physical ground truth?
3. How much variation is attributable to:
   - repeated imaging without moving the case;
   - case repositioning;
   - orientation;
   - part-to-part differences?
4. Is the measurement error acceptably small relative to the 0.020-inch total tolerance?
5. Does the system produce unacceptable false-pass or false-fail decisions near the specification limits?
6. Is a guard band required?

---

## 3. Scope

### 3.1 Included

- PCA OAL estimator frozen before validation;
- camera, lens, lighting, and image acquisition settings used for the OAL rig;
- calibration at the actual case measurement plane;
- physical ground-truth measurements;
- static repeatability;
- repositioning repeatability;
- controlled orientation effects;
- paired computer-vision versus reference comparison;
- tolerance-relative evaluation;
- pass/fail analysis;
- diagnostic overlays and evidence manifests.

### 3.2 Excluded

- automatic PLC rejection;
- conveyor timing;
- dynamic motion blur;
- production-speed throughput;
- characteristics requiring sub-0.001-inch performance;
- other dimensions such as head diameter, rim diameter, or concentricity;
- claims of universal performance across all case families.

The later sub-0.001-inch research phase will use a separate plan.

---

## 4. Frozen candidate estimator

The validation candidate is the existing PCA-plus-extreme-mask-pixel method implemented in:

`src/measurement/topdown_oal.py`

The estimator must be frozen and committed before validation data are collected.

No algorithm parameter, segmentation rule, endpoint rule, failure criterion, or post-processing step may be changed after acquisition begins unless:

1. validation is stopped;
2. the change is documented;
3. the current validation dataset is reclassified as development data;
4. a new frozen implementation is committed;
5. a new independent validation dataset is collected.

---

## 5. Specification and decision structure

### 5.1 Specification

The current specification is:

\[
\text{Nominal OAL} \pm 0.010\text{ inch}
\]

Therefore:

\[
LSL = \text{Nominal} - 0.010
\]

\[
USL = \text{Nominal} + 0.010
\]

\[
USL - LSL = 0.020\text{ inch}
\]

The exact nominal OAL must be entered before final validation.

### 5.2 Decision categories

Each part will be classified by physical ground truth as:

- below LSL;
- within specification;
- above USL.

The computer-vision system will independently classify each measurement using the same limits.

### 5.3 Guard-band evaluation

If measurement uncertainty is non-negligible relative to the tolerance, an exploratory guard band may be evaluated.

A guard band must not be applied until:

- the uncertainty basis is documented;
- the effect on false-pass and false-fail rates is quantified;
- the business and quality implications are reviewed.

---

## 6. Calibration plan

### 6.1 Calibration objective

Establish a traceable relationship between image-space distance and physical distance at the actual case measurement plane.

### 6.2 Calibration artifact

Use a traceable or independently verified dimensional reference positioned at the same height and plane as the measured case centerline or effective silhouette plane.

The existing 1.000-inch gauge-block result of `523.066855 px/in` may be used only as a preliminary comparison value. It is not automatically accepted as the final OAL calibration.

### 6.3 Calibration conditions

Record:

- camera model and serial number;
- lens model and focal length;
- focus setting or mechanical focus position;
- camera height;
- reference-to-camera distance;
- image resolution;
- pixel format;
- exposure;
- gain;
- brightness;
- contrast;
- saturation;
- white-balance settings;
- backlight position and settings;
- measurement-surface height;
- ambient lighting;
- Jetson commit;
- acquisition script version;
- date, time, and operator.

### 6.4 Calibration positions

Measure the calibration reference at a minimum of:

- image center;
- left;
- right;
- upper;
- lower;
- four diagonal positions.

This evaluates spatial scale variation and potential lens distortion.

### 6.5 Calibration orientations

At each relevant position, acquire the reference at:

- 0°;
- 45°;
- 90°.

This evaluates direction-dependent scale and edge response.

### 6.6 Replication

At each position-orientation combination:

- acquire at least 5 repeated images without moving the reference;
- remove and replace the reference for at least 3 independent placements where physically practical.

### 6.7 Calibration outputs

Calculate and report:

- local pixels per inch;
- mean, median, SD, minimum, maximum, and range;
- spatial scale map;
- directional scale differences;
- calibration residuals;
- uncertainty contribution from scale estimation;
- evidence that the chosen calibration model is appropriate.

### 6.8 Calibration model decision

Possible models include:

1. single global pixels-per-inch value;
2. orientation-specific scale;
3. spatially varying scale surface;
4. camera calibration and image rectification followed by a global scale.

The simplest model supported by the evidence will be selected.

---

## 7. Ground-truth measurement plan

### 7.1 Reference instrument

Use a calibrated reference instrument appropriate for case OAL.

Record:

- instrument type;
- manufacturer;
- model;
- serial number;
- resolution;
- calibration status;
- calibration due date;
- operator;
- measurement method;
- contact-force considerations;
- environmental conditions.

### 7.2 Ground-truth procedure

For each study part:

1. assign a unique permanent identifier;
2. clean the measurement surfaces if required;
3. measure OAL using the documented reference method;
4. acquire at least 3 independent reference readings;
5. remove and reposition the part between readings;
6. record all readings, not only the average;
7. calculate the reference mean and reference repeatability;
8. flag any unstable part or ambiguous physical surface.

### 7.3 Reference adequacy

The reference instrument and procedure must have resolution and repeatability sufficiently smaller than the 0.020-inch tolerance to support the intended comparison.

The study must distinguish:

- instrument display resolution;
- observed repeatability;
- calibration uncertainty;
- operator influence.

---

## 8. Validation sample

### 8.1 Minimum sample composition

The validation sample should include at least 30 uniquely identified parts.

Preferred composition:

- 10 near nominal;
- 5 near LSL but inside specification;
- 5 near USL but inside specification;
- 5 below LSL or engineered low;
- 5 above USL or engineered high.

When actual out-of-specification production parts are unavailable, controlled sample preparation may be used if documented and physically appropriate.

### 8.2 Coverage requirement

The sample should span as much of the 0.020-inch tolerance region as practical.

A sample concentrated only near nominal cannot validate pass/fail performance near specification limits.

### 8.3 Development versus validation separation

Parts and images used to tune the estimator must not be treated as independent validation evidence.

If the same physical parts are reused, the validation captures must be newly collected after the estimator and calibration model are frozen.

---

## 9. Image-acquisition protocol

### 9.1 Static repeatability

Select at least 3 representative parts:

- near nominal;
- near LSL;
- near USL.

For each part:

- place once;
- acquire 10 images without moving the part.

### 9.2 Repositioning repeatability

For each validation part:

- remove and replace the part between captures;
- acquire at least 3 independent placements;
- verify centroid remains within the established placement control or record the actual centroid.

### 9.3 Orientation study

For a minimum of 10 parts spanning the specification region, acquire at:

- 0°;
- 20°;
- 40°;
- 70°;
- 90°.

Use randomized orientation order.

Acquire at least 3 independent placements per orientation.

### 9.4 Randomization

Randomize:

- part order;
- orientation order;
- repeated-placement order where practical.

This reduces confounding with time, temperature, illumination drift, and operator learning.

### 9.5 Blinding

Where practical:

- hide the computer-vision result during image acquisition;
- complete all captures before reviewing aggregate estimator performance;
- do not retake a capture because of its measured OAL result.

A retake requires a documented procedural reason such as focus loss, obstruction, or acquisition failure.

---

## 10. Data integrity and provenance

Each capture must record:

- part ID;
- capture ID;
- orientation;
- placement number;
- timestamp;
- operator;
- source image path;
- mask path;
- estimator result;
- pass/fail status;
- failure reason;
- centroid;
- angle;
- endpoints;
- pixel length;
- calibrated length;
- Git commit;
- configuration hash;
- camera settings;
- SHA-256 image hash.

The working tree must be clean before official analysis.

Generated outputs must include:

- CSV results;
- plain-text summary;
- analysis configuration;
- overlays;
- contact sheets;
- calibration model;
- failure report;
- SHA-256 manifest;
- visual-review record;
- evidence-index entry;
- method-decision entry.

---

## 11. Statistical analysis

### 11.1 Paired error

For each valid capture:

\[
e_i = CV_i - Reference_i
\]

Report:

- mean error (bias);
- median error;
- SD of error;
- minimum and maximum error;
- RMSE;
- mean absolute error;
- 95th percentile absolute error;
- maximum absolute error.

### 11.2 Agreement analysis

Prepare:

- scatter plot of CV versus reference;
- residual plot versus reference OAL;
- error versus image position;
- error versus orientation;
- error versus centroid;
- Bland–Altman-style agreement plot where appropriate.

### 11.3 Repeatability

Report separately:

- static repeatability;
- repositioning repeatability;
- within-orientation repeatability;
- part-to-part variation;
- reference-method repeatability.

### 11.4 Orientation effect

For each part with multi-angle data:

- calculate orientation-specific error;
- calculate range across orientations;
- calculate median orientation effect across parts;
- identify systematic 70°–90° behavior;
- report whether orientation correction is justified.

### 11.5 Tolerance-relative metrics

Report each relevant error metric as:

- inches;
- percentage of the 0.020-inch tolerance.

### 11.6 Classification analysis

Using physical ground truth:

- true pass;
- true fail;
- false pass;
- false fail;
- sensitivity to out-of-specification parts;
- specificity for in-specification parts;
- performance near LSL;
- performance near USL.

False passes are particularly important because they represent acceptance of an out-of-specification part.

---

## 12. Acceptance criteria

The PCA OAL system may be considered a candidate for operational demonstration only if all of the following are met.

### 12.1 Measurement availability

- at least 99% of validly acquired images produce a measurement;
- no systematic orientation or position produces repeated failures.

### 12.2 Static repeatability

- static SD no greater than 0.001 inch for each representative part;
- preferred target no greater than 0.0005 inch.

### 12.3 Repositioning and orientation

- 95th percentile absolute repositioning error no greater than 0.002 inch;
- maximum median orientation effect no greater than 0.002 inch;
- no unexplained orientation-specific bias greater than 0.003 inch.

### 12.4 Accuracy and agreement

Preferred:

- absolute mean bias no greater than 0.001 inch;
- RMSE no greater than 0.002 inch;
- 95th percentile absolute error no greater than 0.003 inch;
- maximum absolute error no greater than 0.004 inch.

Conditional usability may be considered when:

- 95th percentile absolute error is greater than 0.003 inch but no greater than 0.004 inch;
- limitations and guard bands are documented;
- false-pass risk remains acceptable.

### 12.5 Tolerance relationship

Preferred combined error or uncertainty:

- no greater than 10% of tolerance = 0.002 inch.

Conditional:

- greater than 0.002 inch but no greater than 20% of tolerance = 0.004 inch.

### 12.6 Classification performance

For the validation sample:

- zero false passes is the preferred requirement;
- any false pass requires root-cause investigation and prevents acceptance without a revised decision rule;
- false-fail performance must be reported and evaluated for operational impact.

### 12.7 Visual diagnostics

- no gross endpoint-placement failure;
- measurement line contacts intended physical ends;
- no systematic fixture or halo capture;
- diagnostic flags are selective and interpretable.

---

## 13. Decision framework

### Outcome A: all criteria met

Freeze the validated configuration and proceed to an operator-facing demonstration using documented decision logic.

### Outcome B: physical error acceptable but near-limit classification uncertain

Develop and validate a guard band or controlled review zone.

### Outcome C: repeatability acceptable but systematic bias present

Investigate calibration model, scale variation, distortion correction, or bias correction. Any correction must be prospectively validated.

### Outcome D: orientation effect remains excessive

Investigate spatial calibration, optical alignment, lens distortion, measurement-plane geometry, or controlled orientation constraints.

### Outcome E: criteria not met

Retain the PCA method as exploratory and do not claim manufacturing adequacy.

---

## 14. Threats to validity

Potential threats include:

- preliminary rather than validated calibration;
- image-plane scale variation;
- lens distortion;
- camera optical-axis misalignment;
- part-height variation;
- reference-instrument uncertainty;
- operator influence;
- insufficient near-limit parts;
- use of engineered rather than naturally occurring out-of-specification parts;
- reuse of development parts;
- uncontrolled environmental drift;
- nonindependence of repeated images.

Each threat must be addressed or reported as a limitation.

---

## 15. Required research documents

Before official data collection:

- this prospective validation plan;
- exact nominal and specification record;
- calibration-artifact record;
- reference-instrument record;
- frozen estimator commit;
- acquisition checklist;
- randomized run order;
- part-identification list.

After analysis:

- calibration report;
- ground-truth report;
- PCA validation results;
- visual diagnostic review;
- tolerance-relative adequacy decision;
- method-decision update;
- evidence-index update;
- limitations and next-step record.

---

## 16. Immediate prerequisites

Before collecting validation images, complete the following:

1. Confirm and document the exact nominal OAL.
2. Confirm the physical reference instrument and calibration status.
3. Identify the available part sample and expected OAL distribution.
4. Verify the camera and measurement fixture are unchanged or document changes.
5. Perform calibration at the actual case measurement plane.
6. Review the calibration spatial-variation result.
7. Freeze the calibration model.
8. Freeze the PCA analysis code and configuration.
9. Generate randomized acquisition order.
10. Commit all plans and configuration files.

---

## 17. Plan status

Current status:

> **Planned — awaiting nominal value, reference-instrument definition, sample definition, and calibration execution**

No new validation result exists at the time this plan is created.
