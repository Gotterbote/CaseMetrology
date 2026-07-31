# Fixtureless OAL Subpixel Version 2 Development Review

**Project:** CaseMetrology  
**Research area:** Fixtureless top-down overall-length measurement  
**Review date:** 2026-07-31  
**Algorithm implementation commit:** `3b1a49f` — *Add mask-anchored subpixel OAL estimator version 2*  
**Prospective plan:** `docs/research/2026-07-31_oal_subpixel_v2_analysis_plan.md`  
**Requirements amendment:** `docs/research/2026-07-31_oal_requirements_amendment.md`  
**Dataset role:** Development data; not independent validation  
**Evidence status:** Exploratory development result  
**Candidate decision:** Does not advance to independent physical validation in the primary configuration

---

## 1. Purpose

This record documents the numerical, diagnostic, and visual review of the primary Subpixel Version 2 configuration defined prospectively before implementation and real-image analysis.

The estimator used:

- accepted binary masks for object association and boundary anchoring;
- original grayscale source images for final edge localization;
- a polarity-aware dark-object-to-bright-background transition;
- a fixed normalized crossing of `0.50`;
- a minimum local contrast of `30 grayscale levels`;
- a profile half-length of `6.0 px`;
- robust fitted sidewalls and fitted physical end faces.

The primary purpose was to test whether a physically consistent intensity-crossing definition would reduce orientation-dependent OAL variation while maintaining static repeatability and producing selective diagnostics.

---

## 2. Evidence reviewed

The review used the following generated evidence:

- `analysis_configuration.json`
- `oal_subpixel_v2_estimator_comparison_results.csv`
- `oal_subpixel_v2_estimator_comparison_summary.txt`
- `oal_subpixel_v2_failure_and_flag_report.csv`
- `oal_subpixel_v2_profile_diagnostics.csv`
- Trial 03 static comparison contact sheet
- Trial 05 controlled-orientation comparison contact sheet

The analysis processed:

- 10 Trial 03 static image-mask pairs;
- 17 Trial 05 controlled-orientation image-mask pairs;
- 27 total development pairs.

Previously accepted masks were reused without resegmentation. Original grayscale source images were used.

---

## 3. Primary numerical results

### 3.1 Trial 03 static sequence

| Estimator | Valid count | Mean (px) | SD (px) | Range (px) |
|---|---:|---:|---:|---:|
| PCA plus extreme mask pixels | 10 | 523.620541 | 0.050349 | 0.166581 |
| Binary geometry | 10 | 521.484317 | 0.025910 | 0.079071 |
| Subpixel Version 1 | 10 | 524.368290 | 0.048945 | 0.167675 |
| Subpixel Version 2 | 3 | 523.120425 | 0.024597 | 0.044729 |

The Version 2 static SD and range cannot be interpreted as representative repeatability estimates because only 3 of 10 captures produced valid results. The seven rejected captures make the apparently favorable three-capture SD vulnerable to selection effects.

The automated criterion `static_sd_no_worse_than_pca = pass` is numerically correct for the retained values but is not sufficient scientific evidence of improved static repeatability.

### 3.2 Trial 05 controlled-orientation sequence

| Estimator | Valid count | SD (px) | Overall range (px) | Range among orientation-group medians (px) |
|---|---:|---:|---:|---:|
| PCA plus extreme mask pixels | 17 | 0.641593 | 2.183819 | 1.752720 |
| Binary geometry | 17 | 0.779169 | 2.273582 | 2.249772 |
| Subpixel Version 1 | 17 | 1.087747 | 2.983334 | 2.887566 |
| Subpixel Version 2 | 17 | 0.844780 | 2.482877 | 2.437877 |

Version 2 reduced the orientation-group median range by approximately `15.6%` relative to Subpixel Version 1. It nevertheless remained:

- approximately `39.1%` worse than the PCA baseline;
- approximately `8.4%` worse than binary geometry.

Therefore, the primary hypothesis that Version 2 would reduce the Trial 05 orientation-group median range below the PCA result was not supported.

### 3.3 Version 2 orientation-group medians

| Orientation group | Version 2 median (px) |
|---|---:|
| 0° | 522.247706 |
| 20° | 521.972391 |
| 40° | 522.073004 |
| 70° | 520.760129 |
| 90° retake | 523.198006 |

The largest separation remained between the 70° and 90° groups:

\[
523.198006 - 520.760129 = 2.437877\text{ px}
\]

The polarity-aware normalized crossing moderated the extreme Version 1 behavior but did not remove the systematic orientation pattern.

---

## 4. Failure analysis

### 4.1 Failure distribution

Version 2 produced:

- 20 valid results among 27 captures;
- 7 failed results;
- overall valid-result rate: `74.1%`.

All seven failures occurred in the Trial 03 static sequence. Trial 05 produced 17 of 17 valid measurements.

Every failure had the same capture-level reason:

> `Insufficient accepted profiles on the minimum sidewall.`

### 4.2 Minimum-sidewall profile counts in Trial 03

The configured minimum was 25 accepted profiles from 72 requested profiles.

| Capture | Accepted minimum-sidewall profiles | Result |
|---|---:|---|
| Cycle 01 | 24 | Fail |
| Cycle 02 | 23 | Fail |
| Cycle 03 | 20 | Fail |
| Cycle 04 | 25 | Pass |
| Cycle 05 | 21 | Fail |
| Cycle 06 | 24 | Fail |
| Cycle 07 | 25 | Pass |
| Cycle 08 | 26 | Pass |
| Cycle 09 | 22 | Fail |
| Cycle 10 | 21 | Fail |

The three passing static captures were immediately adjacent to the fixed profile-count threshold. The outcome therefore reflects a discontinuous threshold response among otherwise nearly identical static images.

### 4.3 Profile-level rejection mechanisms

Across the ten Trial 03 minimum sidewalls:

- `320` profiles were rejected because a mask anchor was not found;
- `169` profiles were rejected for local contrast below `30`;
- no other rejection category caused the static failures.

The opposite sidewall accepted all 72 requested profiles in every Trial 03 capture.

This one-sided behavior is a significant finding. It indicates that the primary robustness limitation is not the end-face estimator. It is the interaction among:

- the minimum-sidewall seed geometry;
- the accepted binary-mask boundary;
- mask-anchor availability within the fixed search distance;
- local sidewall contrast;
- the fixed minimum accepted-profile count.

### 4.4 Contrast-threshold implication

The rejected low-contrast profiles commonly had positive dark-to-bright polarity but fell below the fixed `30`-level threshold.

A diagnostic count shows that, before considering any subsequent crossing-quality rejection, lowering the threshold to `20` could potentially increase the Trial 03 minimum-sidewall accepted counts into the mid-30s for all ten captures.

This observation does not authorize an undeclared parameter change. It supports conducting the contrast sensitivity analysis already declared prospectively at `20`, `30`, and `40` grayscale levels.

---

## 5. Diagnostic-flag review

Version 2 produced:

- 20 passed measurements;
- 20 flagged captures;
- four distinct flag patterns.

Thus, every successful Version 2 result carried at least one diagnostic warning.

### 5.1 Sidewall diagnostics

All passed captures were flagged for elevated sidewall residuals.

Observed sidewall RMS values were generally approximately `1.0–2.3 px`, exceeding the configured `0.75-px` diagnostic threshold.

Additional systematic patterns included:

- Trial 03: high rejected-profile fraction on the minimum sidewall;
- 0°, 20°, and 40°: fitted sidewalls differed by more than the 1° parallelism threshold;
- 70°: high rejected-profile fraction on the minimum sidewall;
- selected 90° captures: high rejected-profile fraction and low-contrast prevalence on the maximum sidewall.

These patterns are more informative than Version 1's identical warning on all captures, but the current residual threshold still does not separate nominal passed captures from clearly abnormal captures.

### 5.2 End-face diagnostics

The end-face profiles behaved substantially better than the sidewalls:

- all Trial 05 end-face profiles were accepted;
- end-face contrasts were high;
- fitted end-face residuals were generally low;
- no systematic end-face rejection pattern caused a capture failure;
- no gross end-line placement error was evident in the contact sheets.

This supports the conclusion that the dominant Version 2 limitation is sidewall-based axis construction and sidewall profile robustness, not the normalized end-face crossing alone.

---

## 6. Visual diagnostic review

### 6.1 Trial 03

The three passed static overlays showed:

- visually plausible sidewall lines;
- end lines located on the intended physical ends;
- a center axis passing through the case;
- no gross endpoint-placement error.

The seven failed overlays showed partial accepted and rejected profile markers but no completed measurement geometry because processing stopped after the minimum-sidewall profile-count requirement was not met.

At contact-sheet scale, the case itself did not visibly move enough to explain a seven-of-ten failure rate. The failures are therefore interpreted as algorithmic robustness failures under nearly unchanged physical conditions.

### 6.2 Trial 05

All 17 controlled-orientation overlays were visually plausible at review scale:

- the center axis generally remained centered;
- end lines contacted the intended end regions;
- no catastrophic fit occurred at 70° or 90°;
- accepted sidewall points followed the visible long edges.

However, plausible overlays did not correspond to improved orientation invariance. The persistent 70°–90° separation shows that visually reasonable line placement can still contain orientation-dependent metrological bias.

### 6.3 Visual-review status

**Status:** Pass as exploratory diagnostic evidence; fail for candidate advancement.

The overlays support the numerical results and do not reveal a simple catastrophic outlier that would justify excluding a capture or orientation group.

---

## 7. Prospective-criteria decision

The predefined criteria produced the following outcomes:

| Criterion | Result |
|---|---|
| At least 20% better orientation range than PCA | Fail |
| Static SD no worse than PCA | Nominal numerical pass, scientifically inconclusive due to 3/10 validity |
| At least 26 of 27 valid captures | Fail |
| Minimum valid count per Trial 05 orientation group | Pass |
| No orientation median more than 1 px from pooled median | Fail |
| Diagnostics more selective than identical warnings on all captures | Pass |
| Clean committed source before analysis | Pass |
| No gross visual line-placement failure | Pass |

The complete candidate criteria were not met.

**Decision:** The primary Version 2 configuration does not advance to independent physical validation.

---

## 8. Relation to the current ±0.010-inch OAL specification

The current OAL requirement has been clarified as:

\[
\text{nominal OAL} \pm 0.010\text{ in}
\]

for a total tolerance width of `0.020 in`.

This clarification materially affects the later manufacturing-adequacy analysis, but it does not reverse the present algorithm-development decision.

The current evidence is still in pixels. The study cannot determine whether the PCA or another estimator is practically adequate for the `0.020-inch` tolerance until it establishes:

- the exact nominal OAL;
- a validated spatial calibration;
- reference measurements;
- estimator bias;
- orientation effect in inches;
- repeatability and repositioning effects in inches;
- decision performance near the specification limits.

The seven Version 2 failures remain a robustness concern regardless of the tolerance width.

The later sub-`0.001-inch` research objective remains a separate phase and is not evaluated by this OAL result.

---

## 9. Scientific interpretation

The primary Version 2 result supports the following interpretation:

> A mask-anchored, polarity-aware 50% normalized intensity crossing improved the maximum-gradient subpixel estimator but did not outperform the PCA baseline in orientation invariance. The estimator produced credible end-face fits but exhibited one-sided sidewall profile loss, elevated sidewall residuals, and a persistent 70°–90° orientation effect. The result indicates that inconsistent gradient-lobe selection was not the sole source of orientation dependence.

The data suggest that further work should distinguish between:

1. parameter sensitivity within the prospectively declared Version 2 method;
2. structural sidewall-anchor limitations;
3. spatial calibration, lens distortion, camera alignment, and other optical-system effects.

---

## 10. Approved next step

The next analysis will be the sensitivity analysis already declared in the prospective plan:

- normalized crossing: `0.40`, `0.50`, `0.60`;
- minimum local contrast: `20`, `30`, `40`;
- profile half-length: `5.0`, `6.0`, `7.0 px`.

The primary result documented here must remain unchanged and preserved.

The sensitivity analysis must:

- retain all 27 development captures;
- report all failed captures and reasons;
- distinguish exploratory parameter selection from independent validation;
- use the same accepted masks and source images;
- generate machine-readable outputs;
- record the implementation commit and repository status;
- avoid adding undeclared tuning parameters.

A lower contrast threshold is scientifically justified for planned evaluation because low contrast was a predefined sensitivity factor and directly contributed to the observed static failures.

No new physical data will be collected until a candidate configuration is selected, frozen, committed, and separately validated.

---

## 11. Claims supported by this result

The evidence supports the claims that:

- Version 2 processed all 17 controlled-orientation captures;
- Version 2 failed 7 of 10 static captures;
- all static failures resulted from insufficient accepted minimum-sidewall profiles;
- mask-anchor unavailability and low contrast were the only Trial 03 profile-rejection causes;
- Version 2 improved on Version 1 but did not outperform PCA orientation invariance;
- end-face fitting was more robust than sidewall fitting;
- the primary Version 2 configuration does not meet the prospective advancement criteria.

---

## 12. Claims not supported

The evidence does not establish:

- accuracy in inches;
- compliance with the ±0.010-inch OAL specification;
- total measurement uncertainty;
- production pass/fail capability;
- sub-0.001-inch performance;
- population-level manufacturing capability;
- independent validation;
- superiority of any untested sensitivity configuration.

---

## 13. Evidence classification

**Primary configuration:** Rejected for advancement; retained as exploratory evidence.  
**Generated dataset:** Development evidence.  
**Visual review:** Complete for contact-sheet-level review.  
**Sensitivity analysis:** Authorized under the existing prospective plan.  
**Independent validation:** Not authorized until a candidate configuration is frozen.
