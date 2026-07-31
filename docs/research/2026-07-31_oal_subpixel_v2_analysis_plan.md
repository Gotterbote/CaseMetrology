# Fixtureless OAL Subpixel Estimator Version 2  
## Prospective Analysis and Algorithm-Development Plan

**Project:** CaseMetrology  
**Study area:** Fixtureless top-down overall-length (OAL) measurement  
**Document status:** Prospective development plan  
**Plan date:** 2026-07-31  
**Plan time:** 16:55 CDT  
**Repository baseline:** `34784e0` — *Document fixtureless OAL estimator development*  
**Expected repository state at plan approval:** clean and synchronized with `origin/main`  
**Planned implementation name:** mask-anchored, polarity-aware subpixel OAL estimator, Version 2  
**Prepared before:** implementation, parameter tuning, or review of Version 2 results

---

## 1. Purpose

This document prospectively defines the research rationale, algorithmic constraints, development dataset, evaluation metrics, diagnostic requirements, decision rules, and documentation outputs for the next fixtureless OAL estimator.

The purpose of Version 2 is not merely to produce a numerically different OAL value. It is to test whether a physically consistent grayscale edge definition can reduce orientation-dependent measurement variation while maintaining static repeatability.

This plan is committed before Version 2 implementation so that later decisions can be distinguished from post-hoc tuning.

---

## 2. Background and current evidence

The current fixtureless OAL investigation has evaluated three estimators on previously accepted Trial 03 and Trial 05 data.

### 2.1 PCA plus extreme-mask-pixel estimator

This estimator derives the longitudinal axis from exposed case pixels and calculates OAL from the most extreme binary-mask projections.

**Trial 03 static performance**

- Standard deviation: `0.050349452 px`
- Range: `0.166581476 px`

**Trial 05 controlled-orientation performance**

- Range among orientation-group medians: `1.752720470 px`

This remains the provisional working baseline because it currently has the smallest orientation-group median range.

### 2.2 Binary-geometry estimator

This estimator fits straight sidewalls and binary end boundaries, derives a longitudinal center axis, and measures the axial distance between fitted end lines.

**Trial 03 static performance**

- Standard deviation: `0.025909506 px`
- Range: `0.079070832 px`

**Trial 05 controlled-orientation performance**

- Range among orientation-group medians: `2.249772382 px`

Interpretation: fitted binary geometry improved static repeatability but increased orientation dependence.

### 2.3 Maximum-gradient grayscale subpixel estimator

This estimator fits subpixel grayscale edges by selecting a local maximum-gradient response around mask-seeded boundaries.

**Trial 03 static performance**

- Standard deviation: `0.048944639 px`
- Range: `0.167674518 px`

**Trial 05 controlled-orientation performance**

- Range among orientation-group medians: `2.887565849 px`

Visual review indicated that the maximum-gradient rule could select different portions of the optical edge-spread profile at different orientations. The 90-degree group showed a pronounced positive bias, while the 70-degree group showed a lower median.

### 2.4 Research implication

The existing evidence does not support the claim that subpixel localization alone improves orientation invariance. Version 2 must define the edge by a consistent physical-intensity transition rather than by the strongest local gradient.

---

## 3. Research question

**Primary research question**

Can a mask-anchored, polarity-aware, normalized intensity-crossing estimator reduce orientation-dependent OAL variation relative to the PCA-plus-extreme-mask-pixel baseline while maintaining static repeatability?

**Secondary research question**

Can the Version 2 diagnostic criteria distinguish credible edge profiles from abnormal or ambiguous profiles without flagging all captures indiscriminately?

---

## 4. Hypotheses

### 4.1 Primary hypothesis

Using a fixed normalized dark-object-to-bright-background crossing will reduce the Trial 05 range among orientation-group medians below the PCA baseline of `1.752720470 px`.

### 4.2 Static-repeatability hypothesis

Version 2 will produce a Trial 03 static standard deviation no greater than the PCA baseline of `0.050349452 px`.

### 4.3 Diagnostic hypothesis

The Version 2 profile-quality diagnostics will be selective. They will not flag all 27 development captures, and any flagged capture will have an identifiable profile-quality or line-fit reason recorded in the output.

### 4.4 Null interpretation

If Version 2 does not improve orientation invariance, the result will indicate that the dominant error is not adequately explained by inconsistent local edge selection alone. Lens distortion, image-plane scale variation, camera alignment, depth-related magnification, illumination anisotropy, or other optical/systematic effects will then require investigation.

---

## 5. Study design

### 5.1 Design type

Retrospective algorithm development using existing controlled images and accepted segmentation masks.

### 5.2 Development dataset

The development dataset consists of the same 27 image-mask pairs used in the preceding comparisons:

- Trial 03 static: 10 captures
- Trial 05 controlled orientation:
  - 0 degrees: 3 captures
  - 20 degrees: 3 captures
  - 40 degrees: 3 captures
  - 70 degrees: 3 captures
  - 90-degree retake group: 5 captures

### 5.3 Data-role restriction

These 27 image-mask pairs are a **development dataset**.

They may be used to:

- implement the method;
- inspect diagnostic behavior;
- conduct declared sensitivity analysis;
- identify algorithmic failure modes;
- select a frozen Version 2 configuration.

They may not be used as the sole basis for a final claim of validated general performance because the same data have already influenced estimator development.

### 5.4 Segmentation control

Previously accepted binary masks will be reused without resegmentation.

The mask will be used for:

- object association;
- initial contour and orientation estimation;
- locating approximate boundary seed points;
- determining case-interior and background directions.

The grayscale source image will be used for the final subpixel edge location.

This isolates the estimator comparison from segmentation changes.

### 5.5 No additional physical data during development

No new physical images will be collected until:

1. Version 2 is implemented;
2. the development comparison is completed;
3. visual diagnostics are reviewed;
4. the algorithm and parameters are frozen;
5. the frozen implementation is committed.

---

## 6. Planned Version 2 measurement method

### 6.1 Overview

Version 2 will use the accepted mask as a geometric anchor and the original grayscale image as the source of subpixel edge information.

The principal difference from Version 1 is that Version 2 will locate a predefined normalized intensity crossing with known edge polarity instead of selecting the largest absolute gradient.

### 6.2 Processing sequence

For each accepted image-mask pair:

1. Select the accepted connected component.
2. Estimate the coarse longitudinal axis from the accepted mask.
3. Identify sidewall and end-face seed regions from the accepted mask.
4. Calculate an outward-facing local normal for each seed point.
5. Sample the grayscale intensity profile along the local normal.
6. Determine which direction is case interior and which is illuminated background.
7. Estimate local dark-interior and bright-background plateaus.
8. Normalize the profile from interior intensity `0.0` to background intensity `1.0`.
9. Locate the declared normalized intensity crossing.
10. Reject profiles that do not meet quality criteria.
11. Robustly fit the two sidewalls from accepted subpixel crossings.
12. Derive the longitudinal center axis from the fitted sidewalls.
13. Robustly fit the two physical end faces from accepted subpixel crossings.
14. Intersect the fitted end lines with the center axis.
15. Calculate OAL as the axial distance between the two intersections.
16. Record profile, line-fit, and geometry diagnostics.

### 6.3 Primary edge definition

The primary Version 2 edge location will be the:

> `50% normalized intensity crossing from case interior toward illuminated background`

The crossing must be located by interpolation between adjacent sampled profile points that bracket the `0.50` normalized level.

### 6.4 Edge polarity

The accepted profile must transition predominantly from:

- lower grayscale intensity inside the case silhouette; to
- higher grayscale intensity in the backlit background.

Profiles with reversed or indeterminate polarity will be rejected and recorded.

### 6.5 Initial fixed parameter set

The initial primary configuration will use:

- profile half-length: `6.0 px` on each side of the accepted-mask boundary;
- profile sampling interval: `0.25 px`;
- interior plateau region: samples from `-6.0 px` to `-2.0 px`;
- exterior plateau region: samples from `+2.0 px` to `+6.0 px`;
- normalized crossing: `0.50`;
- minimum usable local contrast: `30 grayscale levels`;
- minimum accepted sidewall profile count per side: `25`;
- minimum accepted end-face profile count per end: `12`;
- robust line fitting: deterministic robust fit with recorded inlier threshold and residuals;
- all random processes, if any, assigned a fixed seed.

Negative profile coordinates denote the mask-interior direction; positive coordinates denote the outward background direction.

### 6.6 Declared development sensitivity analysis

A limited sensitivity analysis may be performed only for the following parameters:

- normalized crossing: `0.40`, `0.50`, `0.60`;
- minimum local contrast: `20`, `30`, `40` grayscale levels;
- profile half-length: `5.0`, `6.0`, `7.0 px`.

The full declared grid contains 27 parameter combinations.

No other parameter will be tuned based on Trial 03 or Trial 05 numerical results without:

1. documenting a new algorithm iteration;
2. explaining the failure mode;
3. updating the decision log;
4. committing the change before rerunning the comparison.

### 6.7 Primary-configuration rule

The `0.50` crossing, `30`-level contrast threshold, and `6.0 px` half-length constitute the primary planned configuration.

A different configuration may be selected for the frozen Version 2 implementation only if:

- the primary configuration exhibits a documented failure mode;
- the selected alternative is from the declared grid;
- selection considers both quantitative outcomes and profile-quality diagnostics;
- the selection is documented as development, not independent validation;
- the final frozen configuration is committed before collecting new physical data.

---

## 7. Profile-quality diagnostics

Each sampled profile will record, at minimum:

- seed-point coordinates;
- local normal vector;
- estimated interior plateau intensity;
- estimated exterior plateau intensity;
- local contrast;
- polarity;
- crossing location;
- distance from accepted-mask boundary;
- number of threshold crossings;
- local monotonicity indicator;
- rejection reason, if rejected.

### 7.1 Profile rejection criteria

A profile will be rejected when any of the following applies:

- local contrast is below the configured threshold;
- expected dark-to-bright polarity is absent;
- the normalized profile does not cross the configured threshold;
- more than one plausible crossing exists within the central search region;
- the crossing is farther than `3.0 px` from the accepted-mask boundary;
- required plateau samples are unavailable;
- the profile contains nonfinite values;
- the local normal is undefined or unstable.

### 7.2 Capture-level diagnostic flags

Capture-level flags will be generated for:

- insufficient accepted profiles on either sidewall;
- insufficient accepted profiles on either end face;
- sidewall angular disagreement;
- excessive sidewall residual;
- excessive end-line residual;
- excessive end-line angular disagreement;
- center-axis inconsistency;
- excessive rejected-profile fraction;
- multiple-transition prevalence;
- low-contrast prevalence;
- line intersection outside the plausible object region.

A passed numerical result may still contain a diagnostic flag. All flags must be retained in machine-readable output and visual overlays.

---

## 8. Comparison estimators

Version 2 will be compared against:

1. **PCA baseline:** PCA axis plus extreme binary-mask projections.
2. **Binary geometry:** robust sidewalls plus fitted binary-mask end faces.
3. **Subpixel Version 1:** maximum-gradient grayscale edge fitting.
4. **Subpixel Version 2:** mask-anchored, polarity-aware normalized crossing.

All methods must use the same accepted source masks and corresponding source images.

---

## 9. Primary and secondary outcomes

### 9.1 Primary outcome

**Trial 05 range among orientation-group median OAL values, in pixels.**

For each orientation group:

1. calculate the median OAL among passing captures;
2. calculate the range as maximum group median minus minimum group median.

### 9.2 Primary benchmark

PCA baseline:

`1.752720470 px`

### 9.3 Secondary outcomes

- Trial 03 static standard deviation;
- Trial 03 static range;
- Trial 05 pooled standard deviation;
- Trial 05 pooled range;
- paired per-capture difference from PCA;
- median paired difference from PCA;
- orientation-specific median difference from PCA;
- percentage of passing captures;
- percentage of profiles rejected;
- diagnostic-flag count and distribution;
- end-line and sidewall residual distributions;
- visual-review pass/fail outcome.

### 9.4 Descriptive-analysis limitation

The development dataset contains repeated images of one physical case and is not a population sample. Results will therefore be interpreted primarily as algorithm-performance diagnostics. Inferential claims about general manufacturing populations will not be made from this dataset.

---

## 10. Predefined development decision criteria

### 10.1 Minimum improvement criterion

Version 2 must produce a Trial 05 orientation-group median range:

`< 1.752720470 px`

to demonstrate any improvement over the current PCA baseline.

### 10.2 Candidate acceptance criterion

For Version 2 to advance to independent physical validation, all of the following must be satisfied:

1. Trial 05 orientation-group median range is no greater than `1.402176376 px`, representing at least a 20% reduction from the PCA baseline.
2. Trial 03 static standard deviation is no greater than `0.050349452 px`.
3. At least 26 of 27 development captures produce a valid result.
4. Every Trial 05 orientation group retains:
   - at least 2 of 3 valid captures for 0°, 20°, 40°, and 70°;
   - at least 4 of 5 valid captures for the 90° retake group.
5. No orientation group has a median more than `1.0 px` from the pooled Version 2 median.
6. No gross line-placement error is identified during visual review.
7. Diagnostic flags are selective and interpretable; the estimator must not assign the same unresolved warning to all 27 captures.
8. The selected configuration is frozen and committed before new data collection.

### 10.3 Nonacceptance rule

If any candidate acceptance criterion is not met, Version 2 will remain exploratory and will not replace the PCA estimator.

### 10.4 No silent exclusion

No capture will be silently removed.

Any exclusion or failed measurement must include:

- source path;
- estimator;
- failure reason;
- diagnostic evidence;
- inclusion/exclusion status in primary statistics;
- sensitivity analysis when relevant.

The previously observed transient 90-degree anomaly will remain identifiable and will not be removed automatically.

---

## 11. Visual diagnostic review

### 11.1 Required overlays

Every capture must include an overlay showing:

- accepted mask boundary or reference contour;
- accepted subpixel sidewall points;
- rejected sidewall profile locations;
- fitted sidewall lines;
- derived center axis;
- accepted subpixel end-face points;
- rejected end-face profile locations;
- fitted end lines;
- center-axis/end-line intersections;
- measured axial segment;
- diagnostic flags.

### 11.2 Required profile diagnostics

Representative profile plots will be generated for:

- one nominal profile from each orientation;
- all rejected profile categories;
- the 70-degree group;
- the 90-degree group;
- any capture with a diagnostic flag;
- the previously identified 90-degree sensitivity candidate.

### 11.3 Visual-review questions

The reviewer will determine whether:

- sidewall crossings correspond to the same optical transition at every orientation;
- end-face crossings correspond to the same physical edge definition;
- lines are pulled toward halos, reflections, or fixture features;
- the center axis remains centered;
- the measured endpoints contact the intended physical end faces;
- 70-degree and 90-degree behavior differs systematically;
- rejected profiles correspond to visible ambiguity;
- numerical improvement is supported by credible geometry rather than overfitting.

### 11.4 Review status

Visual review will be recorded as one of:

- pass;
- pass with documented limitation;
- fail;
- indeterminate.

Numerical acceptance is prohibited without a completed visual-review record.

---

## 12. Required outputs and provenance

The Version 2 development analysis will generate:

- machine-readable per-capture CSV;
- machine-readable per-profile CSV or JSON;
- plain-text summary;
- parameter/configuration JSON;
- per-capture diagnostic overlays;
- comparison contact sheets;
- representative profile plots;
- failure and flag report;
- SHA-256 manifest;
- source-image and source-mask manifest;
- code commit identifier;
- pre-analysis Git status;
- package and library versions;
- execution timestamp;
- visual-review record;
- method decision-log entry;
- evidence-index entry.

The output directory will be treated as exploratory until formal review and acceptance are complete.

---

## 13. Reproducibility requirements

The implementation must:

- preserve the existing PCA, binary-geometry, and Version 1 estimators;
- add Version 2 as a parallel estimator;
- use deterministic processing;
- expose all material parameters through code constants, configuration, or command-line options;
- include unit tests for synthetic orientation invariance;
- include tests for polarity reversal;
- include tests for multiple crossings;
- include tests for low contrast;
- include tests for crossing interpolation;
- include tests for boundary-distance rejection;
- include tests for connected endpoint spurs;
- pass the full repository test suite;
- pass Ruff;
- pass Black;
- be committed before the real-image development comparison.

---

## 14. Independent physical validation after algorithm freeze

If Version 2 meets the candidate acceptance criteria, a new independent validation trial will be collected.

### 14.1 Proposed validation structure

**Static repeatability trial**

- 10 captures without moving the case.

**Randomized controlled-orientation trial**

- orientations: 0°, 20°, 40°, 70°, and 90°;
- 5 independent placements per orientation;
- 25 total repositioned captures;
- randomized capture order;
- centroid controlled to within the established ±5 px tolerance;
- case removed and replaced between captures;
- no algorithm changes after the first validation image is acquired.

### 14.2 Blinding and execution discipline

Where practical:

- the operator will not review OAL results during capture;
- all captures will be completed before aggregate analysis;
- failed captures will remain in the acquisition record;
- retakes will require a documented procedural reason unrelated to the numerical OAL result.

### 14.3 Validation claim restriction

Only the new frozen-algorithm validation data may support a claim that Version 2 improves fixtureless OAL orientation invariance.

The 27 existing captures remain development evidence.

---

## 15. Threats to validity

The planned analysis does not independently resolve:

- camera lens distortion;
- image-plane scale variation;
- camera optical-axis misalignment;
- case-height or measurement-plane variation;
- backlight anisotropy;
- optical halo variation with orientation;
- fixture-edge interaction;
- physical end-face geometry not represented by a single ideal line;
- generalizability to other case geometries;
- accuracy in inches without a validated calibration model.

Any claim must remain limited to pixel-domain estimator behavior on the stated development dataset until these factors are separately evaluated.

---

## 16. Planned interpretation framework

### Outcome A: orientation range and static SD both improve

Version 2 will advance to frozen-algorithm independent validation, subject to diagnostic and visual-review criteria.

### Outcome B: static SD improves but orientation range does not

The intensity-crossing method improves repeatability but does not address the dominant orientation-dependent systematic effect. Optical geometry and spatial calibration become the next research focus.

### Outcome C: orientation range improves but static SD worsens

The crossing definition may reduce systematic orientation bias while adding local profile noise. Robust aggregation, profile filtering, or repeated-frame estimation may require investigation before validation.

### Outcome D: neither outcome improves

The normalized edge-crossing hypothesis is not supported on the development dataset. The next step will shift away from local edge-selection tuning toward camera calibration, distortion correction, telecentricity, or image-plane metrology controls.

---

## 17. Documentation status labels

All Version 2 artifacts will use one of the following labels:

- **Planned**
- **Exploratory**
- **Pending visual review**
- **Candidate for validation**
- **Accepted for independent validation**
- **Rejected**
- **Superseded**

Version 2 begins with status:

> **Planned**

---

## 18. Approval and change control

Any material departure from this plan must be recorded before rerunning the affected comparison.

A material departure includes:

- changing the primary edge definition;
- adding an undeclared tuning parameter;
- changing the development dataset;
- changing accepted masks;
- excluding captures;
- altering acceptance criteria;
- changing the primary outcome;
- using Trial 05 results to select an undeclared parameter.

Each departure must include:

- date;
- reason;
- affected section;
- expected effect;
- related commit;
- whether the change occurred before or after viewing results.

---

## 19. Planned repository records

The following records will be updated or created:

- `docs/research/2026-07-31_oal_subpixel_v2_analysis_plan.md`
- `docs/research/oal_method_decision_log.md`
- `docs/research/oal_evidence_index.md`
- Version 2 implementation source
- Version 2 unit tests
- Version 2 comparison script
- Version 2 exploratory output directory
- Version 2 visual-review record

---

## 20. Plan commitment statement

This plan is intended to be committed while the repository is clean and before Version 2 implementation begins.

The plan establishes a prospective basis for distinguishing:

- hypothesis-driven development;
- declared sensitivity analysis;
- post-hoc algorithm changes;
- development evidence;
- independent validation evidence.

No Version 2 performance result exists at the time this plan is created.
