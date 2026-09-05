# CaseMetrology Formal OAL Statistical Analysis Plan

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Designated operator:** Timmy D. Bell
**Planned formal sample:** 60 unique specimens
**Specification:** 1.000 ± 0.010 in
**Lower specification limit (LSL):** 0.990 in
**Upper specification limit (USL):** 1.010 in
**Status:** Prospective statistical analysis plan; formal validation measurements have not begun

## 1. Purpose

This Statistical Analysis Plan (SAP) defines the analyses, performance metrics, acceptance targets, failure handling, graphical outputs, and reporting rules before formal validation data are collected.

## 2. Analysis Principle

The primary formal-validation unit shall be the **unique specimen**, not the individual replicate.

Each of 60 specimens receives three formal manual measurements and three independently repositioned formal CV attempts.

Thus:

\[
n=60
\]

is the planned maximum number of independent specimen-level observations for primary agreement analysis.

Replicates characterize repeatability and measurement availability.

## 3. Frozen Validation Sample

The formal validation sample shall consist of 60 uniquely laser-etched specimens selected using the frozen stratified-random sampling procedure.

The sample shall cover the five prospectively defined dimensional regions:

1. below LSL;
2. near-LSL but in specification;
3. central/nominal;
4. near-USL but in specification;
5. above USL.

Strata and allocation shall be frozen before selection.

## 4. Formal Manual Reference Value

For specimen \(i\):

\[
\bar{M}_i=\frac{M_{i1}+M_{i2}+M_{i3}}{3}
\]

Manual within-specimen SD:

\[
s_{M,i}=
\sqrt{\frac{\sum_{j=1}^{3}(M_{ij}-\bar{M}_i)^2}{2}}
\]

Manual range:

\[
R_{M,i}=\max(M_{i1},M_{i2},M_{i3})-\min(M_{i1},M_{i2},M_{i3})
\]

Screening readings shall not enter the formal reference value.

## 5. Formal CV Value

For valid CV measurements \(C_{ij}\):

\[
\bar{C}_i=\frac{1}{n_i}\sum C_{ij}
\]

where \(n_i\) is the number of valid formal CV measurements.

No missing CV value shall be imputed.

## 6. Analysis Populations

### Planned-attempt population

All 180 planned formal CV system attempts.

This population determines availability.

### Specimen-level agreement population

Include specimens with:

- accepted formal manual reference; and
- at least two valid formal CV measurements.

### Classification population

Include specimens with accepted formal reference classification and usable CV classification.

## 7. Primary Specimen-Level Measurement Error

\[
e_i=\bar{C}_i-\bar{M}_i
\]

Positive error means CV measures longer than reference.

Absolute error:

\[
|e_i|
\]

## 8. Mean Bias

\[
Bias=\bar{e}=\frac{1}{n}\sum e_i
\]

Report mean signed bias, median signed error, and 95% CI for mean bias.

### Performance target

\[
|\bar{e}|\le0.001\text{ in}
\]

## 9. Mean Absolute Error

\[
MAE=\frac{1}{n}\sum |e_i|
\]

## 10. RMSE

\[
RMSE=\sqrt{\frac{1}{n}\sum e_i^2}
\]

### Performance target

\[
RMSE\le0.002\text{ in}
\]

## 11. 95th-Percentile Absolute Error

Use the empirical nearest-rank definition.

For \(n=60\), the 95th percentile is the 57th ordered absolute error.

### Performance target

\[
P_{95}(|e|)\le0.003\text{ in}
\]

## 12. Maximum Absolute Error

\[
E_{max}=\max(|e_i|)
\]

### Performance target

\[
E_{max}\le0.004\text{ in}
\]

## 13. Measurement Availability

\[
Availability=
\frac{N_{VALID}}
{N_{VALID}+N_{SYSTEM\_FAILURE}}
\times100\%
\]

### Performance target

\[
Availability\ge99\%
\]

For 180 protocol-valid planned system attempts, 179/180 = 99.44% passes while 178/180 = 98.89% fails.

## 14. Formal CV Repositioning Repeatability

For three valid CV measurements per specimen, calculate all pairwise differences:

\[
d_{i,12}=|C_{i1}-C_{i2}|
\]

\[
d_{i,13}=|C_{i1}-C_{i3}|
\]

\[
d_{i,23}=|C_{i2}-C_{i3}|
\]

With 60 complete specimens, this yields 180 pairwise differences.

### Performance target

\[
P_{95}(d_{reposition})\le0.002\text{ in}
\]

Also report median, mean, and maximum pairwise difference and specimen-level CV SD/range.

## 15. Manual Reference Repeatability

Report specimen-level manual SD/range and summary distribution statistics.

This characterizes the single-operator manual reference method and is not a multi-operator Gage R&R study.

## 16. Prevalidation Static Repeatability Criterion

Previously established static qualification criterion:

\[
SD_{static}\le0.001\text{ in}
\]

Preferred target:

\[
SD_{static}\le0.0005\text{ in}
\]

Static repeatability is a prevalidation characteristic and distinct from formal remove/reposition repeatability.

## 17. Agreement Analysis

Use specimen-level paired differences.

Report:

- mean signed difference;
- SD of paired differences;
- lower 95% limit of agreement;
- upper 95% limit of agreement;
- error-versus-magnitude graphical assessment.

\[
LOA_{lower}=\bar{e}-1.96s_e
\]

\[
LOA_{upper}=\bar{e}+1.96s_e
\]

## 18. Correlation and Regression

Produce CV mean versus manual-reference scatter plot with identity line.

Regression may be secondary diagnostic evidence.

Correlation/\(R^2\) shall not be a primary agreement criterion.

## 19. Error Across Measurement Range

Evaluate signed and absolute error as functions of formal reference OAL, including near LSL, nominal region, near USL, and outside specification.

Do not fit post-validation calibration corrections to the validation set.

## 20. Stratified Results

Summarize by the five frozen sampling strata:

- specimen count;
- valid CV count;
- system failures;
- mean/median signed error;
- MAE;
- maximum absolute error;
- classification outcomes.

Primary conclusions remain based on the full frozen sample unless a criterion explicitly states otherwise.

## 21. Specification Classification

Nominal specification:

\[
0.990\le OAL\le1.010\text{ in}
\]

Reference and CV classification shall use the same limits unless a prospectively frozen uncertainty-aware guard-band rule is adopted.

## 22. False Passes and False Fails

A false pass occurs when CV classifies acceptable while reference classifies nonconforming.

A false fail occurs when CV classifies nonconforming while reference classifies acceptable.

Report confusion matrix, sensitivity for detecting nonconforming specimens, and specificity for conforming specimens.

### Performance expectation

**Zero false passes is preferred.**

Any confirmed false pass shall require root-cause investigation and block an unconditional acceptance conclusion unless a prospectively defensible decision rule has already been established.

## 23. Reference Uncertainty Near Specification Limits

**PENDING PRE-MEASUREMENT UNCERTAINTY DECISION**

Before formal measurements, define whether uncertainty-overlap cases use:

- point estimate;
- uncertainty-aware classification;
- guard band;
- indeterminate category.

This decision shall not be chosen after CV classification results are examined.

## 24. Measurement Uncertainty

Reference-method uncertainty shall consider, as applicable:

- accredited caliper calibration uncertainty;
- documented indication error;
- check-standard uncertainty;
- manual repeatability;
- instrument resolution;
- relevant environmental effects.

Preferred engineering target:

\[
\text{combined error/uncertainty}\le0.002\text{ in}
\]

Conditional upper region:

\[
0.002\text{ in}<\text{combined quantity}\le0.004\text{ in}
\]

The exact mathematical definition shall be frozen after certificate review.

## 25. Orientation and Position Findings

Earlier orientation/position criteria remain prevalidation engineering evidence unless formal validation explicitly includes orientation as a factor.

## 26. Distributional Assessment

Planned diagnostics include:

- histogram of signed error;
- absolute-error distribution;
- Q-Q assessment of signed differences;
- Bland-Altman plot.

Non-normality shall not justify deleting observations.

## 27. Outliers

Outlier status alone shall not justify exclusion.

Any sensitivity analysis excluding an extreme observation shall be secondary and explicitly labeled.

## 28. Missing CV Measurements

No imputation.

For specimen-level agreement:

- 3 valid CV values preferred;
- 2 valid CV values permit a specimen-level mean;
- fewer than 2 prevent primary specimen-level agreement analysis.

All failures remain part of availability reporting.

## 29. Protocol-Invalid Observations

Handle according to the frozen deviation/data-disposition policy.

## 30. Primary Formal Validation Performance Targets

| Metric | Target |
|---|---:|
| Valid CV measurement availability | ≥99% |
| 95th-percentile absolute repositioning difference | ≤0.002 in |
| Absolute mean bias | ≤0.001 in |
| RMSE | ≤0.002 in |
| 95th-percentile absolute specimen error | ≤0.003 in |
| Maximum absolute specimen error | ≤0.004 in |
| False passes | Zero preferred |
| Unresolved material protocol deviations | None for unconditional conclusion |

## 31. Overall Study Interpretation

If all applicable primary targets are satisfied, the system may be described as meeting the pre-specified formal validation targets.

If some are not met, report exactly which criteria passed and failed. Failure is a legitimate research result and shall not trigger retrospective tuning of the validation dataset.

## 32. No Validation-Set Retuning

The formal validation dataset shall not be used to refit calibration equations, apply newly estimated bias corrections, change segmentation thresholds, modify the estimator, alter quality gates, redefine strata, or relax acceptance criteria.

## 33. Planned Graphical Outputs

At minimum:

1. CV specimen mean vs formal reference with identity line;
2. signed error vs reference OAL;
3. Bland-Altman plot;
4. absolute-error distribution;
5. repositioning-repeatability distribution;
6. manual/CV repeatability summaries;
7. error summaries by stratum;
8. classification/confusion-matrix summary.

## 34. Planned Tables

At minimum:

1. validation sample summary;
2. reference-method repeatability;
3. CV availability;
4. CV repositioning repeatability;
5. primary dimensional agreement;
6. classification performance;
7. pre-specified criteria with observed result and met/not-met status.

## 35. Confidence Intervals

Report a 95% CI for mean bias and, where appropriate, for limits of agreement and other primary quantities.

Practical engineering error limits take precedence over p-values as validation criteria.

## 36. Statistical Software and Reproducibility

Preserve:

- analysis script;
- Python version;
- NumPy/pandas/SciPy versions where used;
- plotting library version;
- Git commit;
- input hashes;
- generated result files.

## 37. Formal Analysis Script

Recommended:

`scripts/analyze_oal_validation.py`

Recommended process:

```text
raw validation data
        ↓
dataset audit
        ↓
accepted/raw-status interpretation
        ↓
derived specimen-level dataset
        ↓
formal statistical analysis
        ↓
tables + figures + machine-readable results
```

## 38. Analysis Output Directory

Recommended:

```text
data/oal_validation/derived/
├── manual_reference_summary.csv
├── cv_summary.csv
├── oal_validation_analysis.csv
└── formal_validation_statistics.json
```

## 39. Analysis Audit Gate

Primary analysis shall not run until the audit verifies specimen/sample integrity, run-order coverage, accepted manual sessions, correct session linkage, failure classifications, documented replacements, raw file presence, and frozen software-commit information.

## 40. Remaining Pre-Measurement Statistical Decisions

Certificate evidence has been received and the calibration-correction policy has been frozen as no correction at 1 in. Before formal measurements, finalize prospectively:

1. final reference uncertainty calculation/method;
2. treatment near LSL/USL;
3. whether any guard band is required; and
4. final combined error/uncertainty definition.

## 41. Protocol Lock

Once certificate-dependent items are resolved, this SAP shall be frozen.

Any later supplemental analysis shall be labeled exploratory and shall not replace the prospectively defined primary analysis.
