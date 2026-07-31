# OAL Measurement Requirements Amendment  
## Clarification of Current OAL Tolerance and Separation of the Later Sub-0.001-Inch Research Phase

**Project:** CaseMetrology  
**Research area:** Fixtureless top-down optical metrology  
**Document type:** Formal requirements amendment and change-control record  
**Amendment date:** 2026-07-31  
**Amendment time:** 18:15 CDT  
**Repository baseline before amendment:** `3b1a49f` — *Add mask-anchored subpixel OAL estimator version 2*  
**Related prospective plan:** `docs/research/2026-07-31_oal_subpixel_v2_analysis_plan.md`  
**Document status:** Prospective clarification made before review of the complete Version 2 numerical summary

---

## 1. Purpose of this amendment

This amendment records a material clarification to the engineering requirement for the current overall-length (OAL) study.

The Version 2 prospective analysis plan was developed under a deliberately stringent pixel-domain performance framework because the actual manufacturing tolerance for the current OAL characteristic had not yet been formally recorded in the research documentation. The current OAL requirement has now been clarified as:

> **Nominal OAL ±0.010 inch**

Therefore:

\[
USL - LSL = 0.020\text{ inch}
\]

This clarification changes how practical manufacturing adequacy should be assessed. It does not invalidate the existing pixel-domain experiments, estimator comparisons, or prospective algorithm-development controls.

A separate later phase of the CaseMetrology study is expected to address a characteristic requiring performance below `0.001 inch`. That later high-precision objective is not the acceptance requirement for the current OAL phase and will require its own documented measurement characteristic, tolerance, calibration, uncertainty model, and validation plan.

---

## 2. Timing and change-control statement

This amendment was created after the first execution of the frozen Subpixel Version 2 estimator produced only the following high-level process counts:

- source image-mask pairs processed: `27`;
- Version 2 failures: `7`;
- Version 2 flagged captures: `20`;
- generated output directory present.

At the time of this amendment, the complete Version 2 numerical summary, orientation-group statistics, per-capture failure reasons, profile diagnostics, and overlays had **not yet been reviewed**.

This timing is recorded to demonstrate that the requirement clarification was not created in response to favorable or unfavorable Version 2 numerical performance. The amendment reflects the actual manufacturing OAL tolerance supplied by the researcher.

---

## 3. Clarified current OAL requirement

### 3.1 Specification structure

The current OAL study will use:

- nominal value: to be entered when the exact nominal OAL for the studied case is formally confirmed;
- lower specification limit: nominal minus `0.010 inch`;
- upper specification limit: nominal plus `0.010 inch`;
- total specification width: `0.020 inch`.

The exact nominal value must be added to the research record before formal accuracy or pass/fail validation.

### 3.2 Current study objective

The current OAL objective is to determine whether the fixtureless computer-vision system can provide sufficiently reliable OAL measurements and pass/fail decisions for a characteristic with a `0.020-inch` total tolerance window.

The objective is not to demonstrate universal sub-0.001-inch capability during this OAL phase.

### 3.3 Separate future precision objective

A later study phase is expected to require a measurement return below `0.001 inch`.

At present, the following remain to be defined for that later phase:

- the specific dimensional characteristic;
- nominal value;
- specification limits;
- whether `<0.001 inch` refers to resolution, repeatability, bias, total error, uncertainty, or another performance measure;
- calibration reference;
- ground-truth method;
- environmental controls;
- acceptance criteria;
- independent validation design.

No result from the current OAL phase will be represented as satisfying the later sub-0.001-inch objective unless it is tested under a separate approved protocol.

---

## 4. Effect on the Version 2 prospective plan

The original prospective plan remains preserved and valid as a record of the planned algorithm-development experiment.

This amendment does **not** retroactively delete or rewrite:

- the predefined Version 2 algorithm;
- the primary 50% normalized intensity crossing;
- the declared sensitivity grid;
- profile-quality diagnostics;
- no-silent-exclusion requirements;
- visual-review requirements;
- reproducibility requirements;
- independent-validation requirement;
- the original pixel-domain comparison metrics.

However, the amendment changes the interpretation of those metrics.

### 4.1 Metrics that remain scientifically useful

The following remain valid for comparing algorithms:

- Trial 03 static standard deviation in pixels;
- Trial 03 range in pixels;
- Trial 05 range among orientation-group medians in pixels;
- pooled Trial 05 variation;
- failure rate;
- diagnostic-flag distribution;
- visual line-placement quality;
- per-profile rejection reasons;
- relative performance versus PCA, binary geometry, and Subpixel Version 1.

These metrics quantify algorithm behavior and help identify systematic orientation effects.

### 4.2 Metrics that are insufficient by themselves

Pixel-domain variation alone cannot establish manufacturing adequacy.

To determine whether the current OAL method is adequate for a `0.020-inch` tolerance, the study must also establish:

- a validated pixels-per-inch or spatial calibration model;
- measurement traceability to a physical reference;
- ground-truth OAL values;
- bias or agreement relative to the reference method;
- repeatability and repositioning effects;
- orientation sensitivity expressed in inches;
- a justified estimate of total measurement-system error or uncertainty;
- pass/fail performance near both specification limits.

---

## 5. Revised engineering evaluation framework

### 5.1 Tolerance-relative reporting

After a validated spatial calibration is available, all relevant OAL variation and error metrics will be reported in:

- pixels;
- inches;
- percentage of the `0.020-inch` tolerance window.

The conversion will be documented explicitly:

\[
\text{physical variation in inches}
=
\frac{\text{variation in pixels}}{\text{validated pixels per inch}}
\]

When a spatially varying calibration model is required, the appropriate local transformation will be used instead of a single global pixels-per-inch value.

### 5.2 Provisional project-specific screening bands

The following bands are adopted as provisional engineering screening categories for the current OAL phase:

- **Preferred:** validated total measurement-system error or uncertainty no greater than `0.002 inch`, equal to 10% of the total tolerance.
- **Conditionally usable:** greater than `0.002 inch` but no greater than `0.004 inch`, equal to 10–20% of the total tolerance, with documented limitations, risk controls, or guard bands.
- **Requires further improvement:** greater than `0.004 inch`, more than 20% of the total tolerance.

These are project decision bands, not universal claims about measurement-system acceptance.

They apply to a justified combined error or uncertainty estimate. They must not be applied directly to a single statistic, such as one standard deviation or one orientation-median range, without a predefined model explaining how that statistic contributes to total measurement error.

### 5.3 Reliability requirement

A measurement method must not be accepted solely because successful measurements fall within an acceptable physical-error band.

Operational reliability remains a separate criterion.

The current Version 2 result of `7` failures among `27` development image-mask pairs is a significant robustness finding. It must be investigated even if the successful Version 2 measurements later prove small relative to the `0.020-inch` tolerance.

Potential production responses may include:

- algorithm correction;
- controlled recapture;
- a documented fallback estimator;
- automated image-quality rejection;
- operator intervention;
- guard-banded pass/fail logic.

Any fallback or recapture strategy must be evaluated explicitly rather than assumed.

---

## 6. Revised research questions

### 6.1 Algorithm-development question

Does the mask-anchored, polarity-aware intensity-crossing estimator improve repeatability, orientation invariance, diagnostic selectivity, or physical edge consistency relative to the existing estimators?

### 6.2 Manufacturing-adequacy question

After calibration and ground-truth comparison, is the total OAL measurement error sufficiently small relative to a nominal ±`0.010-inch` specification to support reliable inspection decisions?

### 6.3 Future high-precision question

Can a later system configuration measure the separately defined high-precision characteristic with the required sub-`0.001-inch` performance?

These questions must be answered independently. Success on the current OAL requirement does not establish success on the later high-precision characteristic.

---

## 7. Interpretation of existing OAL evidence

### 7.1 Trial 03 and Trial 05 results

The existing Trial 03 and Trial 05 results remain valid evidence of estimator repeatability and orientation sensitivity in the pixel domain.

They should not yet be described as proving:

- OAL accuracy in inches;
- compliance with the nominal ±`0.010-inch` specification;
- capability near the specification limits;
- total measurement-system adequacy;
- sub-`0.001-inch` performance.

### 7.2 Current PCA baseline

The PCA-plus-extreme-mask-pixel estimator remains the provisional algorithmic baseline because it currently has the smallest observed range among controlled-orientation group medians.

Its manufacturing adequacy remains undetermined until the pixel variation is converted through a validated calibration and compared with physical ground truth.

### 7.3 Binary-geometry and Subpixel Version 1 evidence

The binary-geometry and maximum-gradient subpixel comparisons remain exploratory and scientifically useful.

Their negative orientation-invariance results must be retained because they demonstrate that:

- improved static repeatability does not guarantee reduced orientation bias;
- subpixel numerical precision does not guarantee physical measurement accuracy;
- edge-definition consistency is a metrology requirement, not merely an image-processing detail.

---

## 8. Required next analysis sequence

The following sequence will be used:

1. Commit this requirements amendment before reviewing the complete Version 2 summary.
2. Review the full Version 2 numerical summary without changing parameters.
3. Classify all seven failures by explicit cause.
4. Review all diagnostic flags and overlays.
5. Determine whether Version 2 produced a valid algorithmic improvement on the development dataset.
6. Preserve the primary Version 2 result regardless of outcome.
7. Conduct only the sensitivity analyses declared in the original plan unless a separately documented algorithm iteration is approved.
8. Confirm the exact nominal OAL and specification limits.
9. establish or verify the spatial calibration appropriate to the image plane;
10. compare the selected estimator with physical ground-truth measurements;
11. report variation and error in pixels, inches, and percentage of tolerance;
12. freeze the selected algorithm before collecting new independent validation data;
13. conduct a new validation trial with pass/fail assessment near the specification limits.

---

## 9. Accuracy, precision, and classification distinction

Future reporting will distinguish:

- **Resolution:** the smallest output increment or detectable image change.
- **Repeatability:** variation under unchanged measurement conditions.
- **Reproducibility:** variation introduced by repositioning, operators, sessions, or other controlled factors.
- **Orientation sensitivity:** systematic change associated with case angle.
- **Bias:** systematic difference from the physical reference value.
- **Agreement:** closeness of computer-vision and reference measurements.
- **Uncertainty:** quantified doubt associated with the measurement result.
- **Classification performance:** ability to correctly identify in-specification and out-of-specification parts.

A low static standard deviation does not establish low bias. A small orientation range does not establish correct physical scale. A high image resolution does not establish sub-0.001-inch accuracy.

---

## 10. Future validation implications

The final OAL validation dataset should contain parts or reference conditions spanning the specification region, including measurements near:

- the lower specification limit;
- nominal;
- the upper specification limit;
- just inside each limit;
- just outside each limit, when safely and practically available.

The validation should support calculation of:

- paired error relative to ground truth;
- mean bias;
- repeatability;
- repositioning variation;
- orientation-related error;
- false-pass rate;
- false-fail rate;
- performance near decision boundaries.

A guard-band strategy may be considered if validated measurement uncertainty is non-negligible relative to the tolerance.

---

## 11. Documentation and evidence updates

This amendment will be referenced in:

- `docs/research/oal_method_decision_log.md`;
- `docs/research/oal_evidence_index.md`;
- the Version 2 comparison review;
- the future calibration and physical-validation plan;
- the thesis methods and limitations records, as appropriate.

The amendment itself will be stored as:

`docs/research/2026-07-31_oal_requirements_amendment.md`

Recommended evidence status:

> **Accepted requirements clarification**

The first Version 2 comparison remains:

> **Exploratory development evidence pending complete numerical and visual review**

---

## 12. Change-control decision

**Decision ID:** OAL-D007  
**Decision:** Evaluate the current OAL system against a nominal ±`0.010-inch` specification, while retaining pixel-domain algorithm comparisons as development diagnostics. Treat the later sub-`0.001-inch` objective as a separate research phase requiring its own approved requirements and validation protocol.

**Reason:** The true current OAL tolerance was clarified after the Version 2 implementation was frozen. The original pixel-domain plan was more stringent than necessary for the present manufacturing characteristic and did not define practical adequacy in tolerance-relative terms.

**Effect:** The original Version 2 analysis remains unchanged. Its numerical outcome will be reviewed as planned. Manufacturing adequacy will be determined only after calibrated, ground-truth, tolerance-relative evaluation.

**Prohibited interpretation:** This amendment may not be used to conceal algorithm failures, remove captures, change Version 2 parameters post hoc, or claim that the current system meets the later sub-`0.001-inch` objective.

---

## 13. Amendment approval statement

This amendment records the actual current OAL engineering requirement and preserves the methodological integrity of the previously committed prospective plan.

The research will proceed under two distinct performance contexts:

1. **Current OAL phase:** nominal ±`0.010 inch`, total tolerance `0.020 inch`.
2. **Later high-precision phase:** a separately defined characteristic requiring sub-`0.001-inch` performance.

No complete Version 2 numerical result had been reviewed when this clarification was documented.
