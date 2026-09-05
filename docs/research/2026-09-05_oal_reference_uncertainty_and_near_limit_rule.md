# OAL Reference Uncertainty and Near-Limit Decision Rule

Date: 2026-09-05
Operator: Timmy D. Bell
Scope: Formal M.S. OAL validation only.

## 1. Purpose

This record freezes the remaining reference-uncertainty method and
near-specification conformity rule before any formal specimen measurements
are collected.

## 2. Formal Reference Value

For specimen i, the formal manual reference value is the mean of the three
valid randomized manual observations:

M_bar_i = (M_i1 + M_i2 + M_i3) / 3

Screening measurements do not enter the formal reference value.

## 3. Calibration-Uncertainty Contribution

Calibration certificate DDJ25P23P reports expanded uncertainty at
approximately 1 in of:

U_cal = 0.000126 in

with coverage factor approximately k = 2.

The standard calibration-uncertainty contribution is therefore:

u_cal = 0.000126 / 2 = 0.000063 in

The reported as-left indication error at 1 in is 0.0000 in; therefore no
calibration correction is applied.

## 4. Resolution Contribution

The caliper display increment is:

delta = 0.0005 in

Digital indication resolution is represented by a rectangular distribution:

u_res = delta / sqrt(12)

This contribution remains separate from the pooled experimental
repeated-measurement term, consistent with the digital-indication treatment
illustrated in JCGM 100:2008, H.6.3.1. Uncertainty components shall not
otherwise be double-counted.

## 5. Formal Manual Repeated-Measurement Contribution

After completion of the formal manual phase, the pooled within-specimen
repeated-measurement standard deviation under the formal study conditions
shall be calculated from the frozen manual triplicates:

s_p = sqrt(
    sum_i sum_j (M_ij - M_bar_i)^2
    /
    [60 * (3 - 1)]
)

under the planned complete 60-specimen, three-reading design.

The corresponding standard uncertainty contribution to each three-reading
specimen mean is:

u_rep = s_p / sqrt(3)

This term represents within-specimen repeated-measurement variability under
the formal single-operator study conditions; it is not interpreted as
between-operator reproducibility.

If the formal manual dataset is not complete enough to support this calculation,
the analysis audit shall HOLD rather than silently redefine the method.

## 6. Combined Reference Uncertainty

The formal specimen-reference standard uncertainty is:

u_ref = sqrt(u_cal^2 + u_res^2 + u_rep^2)

Expanded reference uncertainty shall be reported as:

U_ref = 2 * u_ref

using coverage factor k = 2 and interpreted as an approximate 95% expanded
uncertainty for this study.

The gauge-block certificate uncertainty is not included in this specimen-level
reference uncertainty because the gauge block is used for session assurance,
not to calibrate or numerically correct each specimen measurement.

No separate numerical environmental uncertainty contribution is assigned.
Environmental effects are controlled procedurally through equipment
acclimation, start/end observations, stability assessment, and
`HOLD_FOR_REVIEW` for questionable or abnormal conditions under the frozen
environmental protocol. The Type-T surface probes are not individually
calibrated, and no defensible numerical thermal correction or uncertainty
component has been prospectively established. This is retained as a study
limitation rather than treated as zero physical effect.

## 7. Primary Specification Classification

The frozen OAL specification is:

0.9900 in <= OAL <= 1.0100 in

Primary reference classification uses the point estimate M_bar_i. This is
the prespecified research-analysis classification used for comparison of the
manual reference and CV methods; it is not asserted as a production acceptance
or product-release decision rule.

A specimen is reference-conforming when:

0.9900 <= M_bar_i <= 1.0100 in

and reference-nonconforming otherwise.

The CV result uses the same nominal specification limits.

No guard band or indeterminate category is used in the primary confusion
matrix.

## 8. Uncertainty Sensitivity Near Specification Limits

Reference uncertainty shall also be evaluated descriptively.

A specimen receives a secondary uncertainty-overlap flag when its expanded
reference-uncertainty interval reaches or crosses either specification limit.
Equivalently, flag the specimen when:

abs(M_bar_i - 0.9900) <= U_ref

or:

abs(M_bar_i - 1.0100) <= U_ref

The overlap flag:

- does not change the frozen primary reference classification;
- does not remove the specimen from the primary analysis;
- does not authorize replacement;
- shall be reported separately in the results and discussed when interpreting
  false-pass or false-fail outcomes near a specification limit.

## 9. Prospective Lock

This uncertainty model and conformity rule are frozen before formal specimen
measurements.

They shall not be changed in response to observed manual or CV validation
results.

Any alternative guard-band, probabilistic conformity, or uncertainty-aware
reclassification shall be clearly labeled secondary or exploratory and shall
not replace the primary analysis.
