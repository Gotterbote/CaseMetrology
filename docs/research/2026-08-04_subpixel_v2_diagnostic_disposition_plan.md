# Subpixel-v2 OAL Estimator Diagnostic and Disposition Plan

**Project:** CaseMetrology — Fixtureless Top-Down Overall Length Measurement  
**Document date:** 2026-08-04  
**Status:** Pre-execution research protocol  
**Proposed repository path:** `docs/research/2026-08-04_subpixel_v2_diagnostic_disposition_plan.md`  
**Primary platform for execution:** Jetson Orin Nano Super Developer Kit  

## 1. Purpose

This protocol defines the controlled evaluation required to determine whether the mask-anchored subpixel-v2 OAL estimator should be:

1. retained as an exploratory method,
2. revised and retested,
3. accepted as a secondary diagnostic method, or
4. promoted to the primary fixtureless OAL estimator.

The protocol is intentionally based on the existing 27 accepted image/mask pairs. No additional physical images should be collected until the current failures and quality flags have been classified and understood.

## 2. Current Evidence Base

The fixtureless top-down OAL work currently includes three estimator families:

| Estimator | Current evidence | Present research role |
|---|---:|---|
| PCA/extreme-mask estimator | Functional; controlled-orientation group medians span 1.752720 px | Historical baseline |
| Geometry estimator | 27 accepted masks available; static repeatability SD = 0.025910 px | Current primary candidate/control method |
| Subpixel-v1 estimator | 27 rows; 0 execution failures; 27 quality flags | Exploratory only |
| Subpixel-v2 estimator | 27 source pairs; 7 failures; 20 completed but flagged | Experimental; not validated |

### 2.1 Geometry-estimator static baseline

For `trial_03_static`, the geometry estimator produced:

| Metric | Result |
|---|---:|
| Count | 10 |
| Mean | 521.484317 px |
| Median | 521.486602 px |
| Standard deviation | 0.025910 px |
| Minimum | 521.437588 px |
| Maximum | 521.516659 px |
| Range | 0.079071 px |

The geometry estimator therefore remains the control method until a more complex estimator demonstrates a material and reproducible advantage.

### 2.2 Subpixel-v2 configuration already evaluated

The current subpixel-v2 comparison used:

| Parameter | Value |
|---|---:|
| Normalized crossing | 0.5 |
| Minimum local contrast | 30.0 |
| Profile half-length | 6.0 px |
| Segmentation source | Previously accepted masks |
| Grayscale source | Original grayscale images |
| Fixture-width gate | Disabled |

Observed outcome:

- Source pairs: 27
- Successful measurements: 20
- Execution failures: 7
- Quality-flagged successful measurements: 20
- Unflagged successful measurements: 0

The present evidence is insufficient to support operational use of subpixel-v2.

## 3. Research Question

Can the mask-anchored subpixel-v2 estimator provide a reliable and materially improved OAL measurement compared with the geometry estimator without image-specific tuning or unacceptable failure rates?

## 4. Evaluation Hypotheses

### H1 — Reliability

A valid subpixel method should process nearly all accepted image/mask pairs. Failures should be rare, explainable, and linked to genuine image insufficiency rather than fragile implementation behavior.

### H2 — Measurement validity

The detected subpixel crossings should coincide visually with the physical left and right end faces of the case, not with fixture edges, shadows, blur transitions, bevels, or mask artifacts.

### H3 — Repeatability benefit

A subpixel method should reduce repeated-measurement variability enough to justify its added complexity.

### H4 — Generality

A valid method should use one documented parameter set across all accepted images and controlled orientations. Per-image parameter tuning is not acceptable for the primary estimator.

## 5. Provisional Acceptance Criteria

These criteria are engineering and research decision thresholds established before re-analysis. They are not claimed to be universal metrology standards.

Subpixel-v2 may be considered for promotion only if all of the following are satisfied:

1. **Processing success:** At least 26 of 27 accepted image/mask pairs produce a measurement. This corresponds to 96.3% success and is the smallest whole-number result that meets or exceeds 95%.
2. **Static repeatability:** Standard deviation on the 10-image static trial is no greater than 0.020728 px, representing at least a 20% reduction from the geometry baseline of 0.025910 px.
3. **Visual endpoint validity:** Both detected endpoints are judged valid on at least 26 of 27 image pairs using enlarged endpoint overlays and profile plots.
4. **No image-specific tuning:** One fixed parameter set is used for the complete evaluation set.
5. **No systematic orientation dependence:** Orientation-group results show no unexplained directional trend or endpoint failure pattern.
6. **No fixture substitution:** Detected crossings correspond to the case end faces rather than fixture or background structures.
7. **Traceability:** Every failure, rejection, and parameter change is preserved in machine-readable and human-readable outputs.
8. **Regression safety:** Existing automated tests pass, and new tests cover the diagnosed failure modes.

Failure to meet any single criterion prevents promotion to the primary estimator. The method may still be retained as an exploratory or secondary diagnostic method.

## 6. Failure and Flag Taxonomy

Every failed or flagged endpoint must be assigned a primary code. A secondary code may be added when more than one mechanism contributes.

| Code | Classification | Operational definition | Typical evidence |
|---|---|---|---|
| F1 | Insufficient local contrast | The intensity profile does not provide a defensible foreground-to-background transition | Low peak-to-peak profile amplitude; weak local gradient |
| F2 | Crossing not bracketed | The selected normalized threshold is not crossed within the sampled profile | Profile remains entirely above or below threshold |
| F3 | Incorrect profile direction | The sampling line is not sufficiently normal to the physical end face | Oblique profile; transition spread; endpoint displaced in overlay |
| F4 | Mask-anchor error | The mask-derived anchor is not located on the intended case end region | Anchor lies on sidewall, burr, protrusion, or disconnected mask feature |
| F5 | Fixture interference | Fixture, notch, texture, or background structure contaminates the edge profile | Competing transitions; crossing aligns with fixture geometry |
| F6 | End-face geometry ambiguity | Burr, bevel, curvature, shadow, or non-square end creates multiple plausible edge locations | Multiple gradients or inconsistent crossing locations |
| F7 | Algorithmic over-rejection | The endpoint appears visually valid, but a quality rule rejects or flags it | Good overlay with failed threshold, contrast, slope, or confidence rule |
| F8 | Genuine image-quality failure | The original image lacks enough information for a defensible endpoint measurement | Blur, clipping, occlusion, saturation, severe shadow, or missing edge |

### 6.1 Classification discipline

- `F7` must not be used merely because the cause is unknown.
- `F8` should be reserved for evidence that the image itself is inadequate.
- Implementation defects should be documented separately as software defects and linked to the affected failure codes.
- A successful measurement may still receive a failure code at one endpoint if the output is numerically produced but visually invalid.

## 7. Required Diagnostic Outputs

The diagnostic run must produce the following artifacts for all 27 source pairs.

### 7.1 Machine-readable summary

A CSV file with one row per source image and, at minimum, these fields:

- `trial_id`
- `image_id`
- `image_path`
- `mask_path`
- `orientation_group`
- `geometry_oal_px`
- `subpixel_v2_oal_px`
- `delta_subpixel_minus_geometry_px`
- `left_success`
- `right_success`
- `overall_success`
- `left_anchor_x`
- `left_anchor_y`
- `right_anchor_x`
- `right_anchor_y`
- `left_crossing_x`
- `left_crossing_y`
- `right_crossing_x`
- `right_crossing_y`
- `left_local_contrast`
- `right_local_contrast`
- `left_gradient_magnitude`
- `right_gradient_magnitude`
- `left_quality_flag`
- `right_quality_flag`
- `overall_quality_flag`
- `left_failure_code`
- `right_failure_code`
- `primary_failure_code`
- `review_status`
- `review_notes`

### 7.2 Per-image visual diagnostic

Each source pair must have one enlarged diagnostic image showing:

- original grayscale image,
- accepted mask boundary,
- fitted longitudinal axis,
- mask-derived endpoint anchors,
- profile sampling direction,
- sampled profile extent,
- detected subpixel crossings,
- geometry-estimator end lines,
- measured OAL values from both estimators,
- quality flags and failure codes.

### 7.3 Endpoint profile plot

Each endpoint must have a profile plot containing:

- sample position in pixels,
- grayscale intensity,
- smoothed intensity if smoothing is applied,
- normalized intensity,
- selected crossing threshold,
- detected crossing location,
- anchor location,
- local contrast limits,
- gradient or slope at the crossing,
- rejection reason when applicable.

### 7.4 Human-review worksheet

A review CSV or Markdown table must record:

- whether each endpoint touches the visually defensible case end,
- whether the profile direction is appropriate,
- whether fixture interference is present,
- assigned failure code,
- reviewer rationale,
- whether the image should remain in the accepted evaluation set.

No image should be removed from the accepted set merely because subpixel-v2 performs poorly. Removal requires evidence that the original accepted image or mask is itself invalid under the previously established dataset rules.

## 8. Controlled Diagnostic Procedure

### Phase A — Reproduce the existing baseline

1. Check out the current repository state containing subpixel-v2.
2. Record the active Git commit hash.
3. Run the complete automated test suite.
4. Execute the existing subpixel-v2 comparison without changing parameters or code.
5. Confirm the previously reported totals: 27 source pairs, 7 failures, and 20 flagged successes.
6. Preserve the console output and generated comparison files.

If the baseline cannot be reproduced, stop estimator modification and first resolve the reproducibility problem.

### Phase B — Generate endpoint-level diagnostics

1. Add or enable verbose endpoint diagnostic output.
2. Export the complete machine-readable summary.
3. Generate overlays and endpoint profile plots for all 27 images, not only the failures.
4. Verify that diagnostic generation does not alter estimator behavior.
5. Record any diagnostic-generation failures separately.

### Phase C — Classify the current results

1. Review the seven failed images first.
2. Review all 20 successful-but-flagged images.
3. Assign left and right endpoint codes independently.
4. Identify recurring mechanisms across trials and orientations.
5. Count failures by code, endpoint side, trial, and orientation group.
6. Distinguish implementation defects from imaging or geometry limitations.

### Phase D — Select one evidence-supported revision

Only one conceptual change should be introduced per iteration. Permissible examples include:

- correcting profile direction using the fitted end-face normal,
- changing mask-anchor selection to use a robust end-face region,
- extending profile length when the crossing is not bracketed,
- revising a quality threshold shown to cause over-rejection,
- handling polarity consistently,
- adding a defensible competing-edge rejection rule.

The following are not acceptable:

- tuning parameters separately for individual images,
- changing segmentation while claiming only the subpixel estimator changed,
- modifying several independent behaviors in one undocumented revision,
- removing difficult images solely to improve the reported success rate.

### Phase E — Test the revision

1. Add focused unit or regression tests for the diagnosed mechanism.
2. Run the full automated test suite.
3. Rerun the complete 27-image evaluation.
4. Regenerate every CSV, overlay, and endpoint profile.
5. Compare revised results against both the original subpixel-v2 results and the geometry estimator.

### Phase F — Evaluate repeatability and orientation behavior

For the revised method, report:

- static-trial count, mean, median, standard deviation, minimum, maximum, and range,
- successful measurement rate,
- endpoint-validity rate,
- quality-flag rate,
- failures by classification,
- orientation-group median, spread, and trend,
- mean and distribution of subpixel-minus-geometry differences.

### Phase G — Make the disposition decision

Apply the decision rules in Section 10 without changing them after viewing the results.

## 9. Quantitative Comparison Table

The final report should contain a table in this form:

| Metric | Geometry | Original subpixel-v2 | Revised subpixel-v2 |
|---|---:|---:|---:|
| Accepted source pairs | 27 | 27 | 27 |
| Successful measurements | 27 or documented baseline count | 20 | TBD |
| Execution failures | documented baseline count | 7 | TBD |
| Success rate | TBD | 74.1% | TBD |
| Flagged successful results | TBD | 20 | TBD |
| Unflagged successful results | TBD | 0 | TBD |
| Static SD | 0.025910 px | TBD | TBD |
| Static range | 0.079071 px | TBD | TBD |
| Visually valid endpoint pairs | TBD | TBD | TBD |
| Orientation-group median span | TBD | TBD | TBD |
| Image-specific tuning used | No | No | No required |

Values not already established must be calculated from preserved output rather than reconstructed manually.

## 10. Disposition Rules

### Decision A — Promote to primary estimator

Subpixel-v2 may be promoted only when all provisional acceptance criteria in Section 5 are met.

### Decision B — Retain as secondary diagnostic method

Retain as a secondary method when:

- endpoint locations are generally valid,
- reliability is below the primary threshold,
- or repeatability improvement is real but not large enough to justify replacement.

In this role, subpixel-v2 may be used to compare edge behavior, investigate image quality, or estimate sub-mask edge position, but it must not produce the official OAL result.

### Decision C — Continue exploratory development

Continue development only when:

- failures are concentrated in one or two clearly correctable mechanisms,
- the revision is general rather than image-specific,
- and preliminary evidence suggests a meaningful repeatability or validity benefit.

### Decision D — Reject for the current thesis implementation

Reject subpixel-v2 as an operational estimator when:

- failures arise from multiple unstable mechanisms,
- detected crossings are frequently visually invalid,
- the method remains dependent on fixture or orientation artifacts,
- reliability remains below 95%,
- or repeatability does not materially improve on the geometry estimator.

Rejection does not mean the work lacked value. A documented negative result is research evidence demonstrating that increased numerical precision does not automatically produce improved measurement validity.

## 11. Planned Repository Outputs

Suggested paths:

```text
docs/research/2026-08-04_subpixel_v2_diagnostic_disposition_plan.md
docs/research/YYYY-MM-DD_subpixel_v2_diagnostic_results.md

data/oal_analysis/subpixel_v2_diagnostic/
    diagnostic_summary.csv
    human_review.csv
    run_metadata.json
    baseline_console.txt
    revised_console.txt
    overlays/
    profiles/

scripts/diagnose_oal_subpixel_v2.py
```

The final directory naming may be adjusted to match the repository's existing conventions, but all artifacts must remain traceable to the source image and mask.

## 12. Run Metadata Requirements

The diagnostic run should preserve:

- date and local time,
- operator,
- hostname,
- Jetson power mode,
- Python version,
- package environment or lockfile state,
- Git branch and commit hash,
- dirty/clean repository status,
- input dataset paths,
- input file checksums or existing manifest reference,
- estimator parameters,
- output paths,
- automated test count and result.

## 13. Research Documentation Requirements

The results document must clearly separate:

### Accepted evidence

- reproduced baseline results,
- unchanged input set,
- automated test results,
- quantitative comparisons,
- reviewed overlays,
- final disposition decision.

### Exploratory evidence

- trial parameter changes,
- failed revisions,
- alternative threshold tests,
- hypotheses not yet validated,
- observations requiring additional physical testing.

No exploratory result should be described as the official system performance.

## 14. Next Jetson Session Checklist

Execute in this order:

- [ ] Record `git status -sb` and current commit hash.
- [ ] Run the full existing automated test suite.
- [ ] Reproduce the original 27-pair subpixel-v2 comparison unchanged.
- [ ] Confirm 7 failures and 20 flagged successes, or document any discrepancy.
- [ ] Export the seven failed file identifiers.
- [ ] Generate overlays and endpoint profiles for all 27 source pairs.
- [ ] Classify both endpoints using F1–F8.
- [ ] Summarize failure counts by code, endpoint, trial, and orientation.
- [ ] Identify one evidence-supported conceptual revision.
- [ ] Add regression tests before or with the revision.
- [ ] Rerun the full test suite.
- [ ] Rerun the 27-pair comparison.
- [ ] Calculate static and orientation metrics.
- [ ] Apply the pre-established disposition rules.
- [ ] Write the results document.
- [ ] Commit code, tests, diagnostics, and research documentation together or in logically separated commits.

## 15. Proposed Commit Structure

A clean sequence would be:

1. `Add subpixel-v2 endpoint diagnostic tooling`
2. `Classify subpixel-v2 failure modes`
3. `Revise subpixel-v2 estimator for <identified mechanism>`
4. `Document subpixel-v2 diagnostic results and disposition`

If no estimator revision is justified after classification, omit commit 3 and document the negative result directly.

## 16. Anticipated Thesis Value

This investigation supports the thesis even if subpixel-v2 is not accepted. It provides evidence that:

- estimator complexity must be justified by measurement performance,
- repeatability and validity are separate requirements,
- mask-level geometry can outperform nominally higher-resolution edge interpolation,
- failure analysis is necessary before collecting additional data,
- and negative algorithmic results can strengthen the defensibility of the selected method.

## 17. Current Provisional Disposition

Until this protocol is executed, the estimator hierarchy remains:

1. **Geometry estimator:** primary candidate and control method.
2. **PCA/extreme-mask estimator:** historical comparison baseline.
3. **Subpixel-v1:** exploratory and quality-flagged.
4. **Subpixel-v2:** experimental, unvalidated, and not authorized for official OAL reporting.

No new physical trial is required before completing the diagnostic review of the existing 27 accepted image/mask pairs.
