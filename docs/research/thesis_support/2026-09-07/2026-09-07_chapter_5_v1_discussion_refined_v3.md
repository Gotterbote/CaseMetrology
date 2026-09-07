# Chapter 5 — Discussion

## 5.1 Overview

The purpose of the formal CaseMetrology validation study was to determine whether the frozen computer-vision overall-length (OAL) measurement system satisfied prospectively established performance criteria relative to an independently acquired calibrated manual reference process. The evaluation addressed measurement availability, repeated-measurement behavior under independent specimen placement, dimensional agreement, error magnitude, and specification-classification performance.

The formal study produced a clear answer to that research question. CaseMetrology achieved complete measurement availability and exhibited strong linear association with the formal manual reference, but the frozen V1 system did not satisfy the complete set of prespecified dimensional-agreement and placement-dependent repeatability criteria. The formal outcome therefore does not support unconditional acceptance of the V1 configuration as a validated OAL conformance-measurement system.

This finding does not represent a failure of the experimental design. The prospective protocol, randomized repeated measurements, preserved raw observations, independent manual-reference process, frozen analysis rules, and predefined performance criteria allowed system limitations to be identified without retrospective adjustment of the estimator, calibration, thresholds, or dataset.

The principal V1 findings requiring interpretation are the positive CV-minus-manual bias, placement-dependent repeated-measurement variation, specification-classification errors near the nominal limits, and the observed round-associated shift in signed error.

## 5.2 Interpretation of Dimensional Agreement

The formal specimen-level mean signed error was +0.001613 in, exceeding the prespecified absolute mean-bias criterion of 0.001 in. The 95% confidence interval for mean bias, +0.001222 to +0.002005 in, remained entirely positive. In addition, mean signed error was positive within each of the five frozen sampling strata.

Taken together, these results provide evidence that the V1 CV method exhibited a systematic positive measurement tendency under the formal validation conditions. This tendency is important because a dimensional measurement system may track relative differences among specimens while still disagreeing materially with the reference measurement process.

The formal regression results illustrate this distinction. Pearson correlation was 0.992737 and the coefficient of determination was 0.985526, demonstrating strong linear association between the two measurement methods. However, strong correlation does not establish measurement agreement. The Bland–Altman results showed a mean difference of +0.001613 in with limits of agreement from -0.001357 to +0.004583 in. Thus, the formal results demonstrate that high correlation and acceptable measurement-system agreement are separate properties, consistent with the methodological distinction described by Bland and Altman [BLAND AND ALTMAN 1986].

The additional specimen-level metrics led to the same overall conclusion. RMSE was 0.002205 in compared with a prespecified limit of 0.002 in, the empirical 95th-percentile absolute specimen error was 0.003960 in compared with a limit of 0.003 in, and maximum absolute specimen error was 0.004799 in compared with a limit of 0.004 in.

The positive bias alone therefore does not fully describe V1 performance. Both systematic disagreement and specimen-to-specimen error dispersion contributed to failure of the formal dimensional-agreement criteria.

## 5.3 Placement-Dependent Repeatability

The largest departure from the prespecified repeatability target occurred under the independent free-placement condition used for formal V1 acquisition.

The empirical 95th-percentile absolute pairwise difference among the three CV rounds was 0.004831 in, more than twice the prespecified 0.002-in criterion. The maximum observed pairwise difference was 0.007081 in.

As documented in Chapter 3, the clear Lexan measurement assembly remained installed during formal acquisition, but the nominal Lexan locator was not used to mechanically register specimen position. Each case was placed freely on the clear measurement surface, gross base-to-mouth orientation was maintained, and exact image-plane position and small angular variation were otherwise unconstrained.

The formal repeated-measurement result must therefore be interpreted as placement-dependent repeatability under independent free placement rather than repeatability at a mechanically fixed position.

This result demonstrates that the complete V1 measurement system was sensitive to repeated physical presentation of the specimen under the tested acquisition condition. It does not identify which individual component of the measurement chain produced that sensitivity.

Maximum specimen-level placement variation showed little association with specimen-level absolute CV-versus-manual agreement error. Pearson correlation was -0.083989 and Spearman correlation was -0.113087.

These near-zero correlations do not establish statistical independence between the two quantities. They do show that, within the formal V1 sample, specimens with the greatest placement-dependent variation were not systematically the same specimens with the largest specimen-mean dimensional disagreement.

Accordingly, improved control of specimen placement is a plausible engineering target for reducing repeated-placement variation, but the V1 evidence does not justify assuming that positioning control alone would eliminate the positive mean bias or all specimen-level agreement error.

## 5.4 Consequences for Specification Classification

The nominal OAL acceptance interval was 0.9900 through 1.0100 in, inclusive. Using the formal manual-reference mean as the reference classification, the V1 results included 37 true-conforming specimens, 14 true-nonconforming specimens, eight false fails, and one false pass.

The single false pass is particularly important from a conformance-assessment perspective because the CV method classified a reference-nonconforming specimen as acceptable. The frozen statistical analysis plan prospectively identified zero false passes as the preferred result and required any confirmed false pass to prevent an unconditional acceptance conclusion absent a prospectively established alternative decision rule.

Part 143 produced the false-pass outcome. Its formal manual-reference mean was 0.989833 in, below the 0.9900-in lower specification limit, whereas its CV mean was 0.992173 in. The corresponding signed error was +0.002340 in.

The eight false fails represent a different operational consequence. A false fail rejects a specimen that the reference process classifies as conforming. Seven of the eight false fails occurred on the upper side of the specification region. This pattern is directionally consistent with the positive CV-minus-manual bias observed across the dataset, although the formal study does not establish bias as the sole cause of those individual classification outcomes.

The classification results demonstrate why agreement metrics and decision performance must both be evaluated. Measurement error that appears small relative to the complete dimensional range may still alter pass/fail decisions for specimens located close to a specification boundary.

## 5.5 Reference Uncertainty and Near-Limit Interpretation

The formal manual reference was treated as a calibrated measurement process rather than an error-free determination of true OAL. The prospectively defined uncertainty model produced an expanded reference uncertainty of 0.000712 in using a coverage factor of \(k=2\).

Thirteen of the 60 formal specimens met the secondary uncertainty-overlap criterion because the reference uncertainty interval reached or crossed one of the nominal specification limits.

Seven of the nine classification errors occurred among uncertainty-overlap specimens, including the single false pass. However, six uncertainty-overlap specimens were classified concordantly by the CV and reference methods, and two classification errors occurred among specimens that did not carry the uncertainty-overlap flag.

Within this formal sample, uncertainty overlap was therefore neither necessary nor sufficient for a classification error. It was an important indicator of proximity to a specification boundary, but it did not account for all observed disagreement.

Under the frozen analysis plan, the uncertainty-overlap designation remained secondary. Primary classification was based on the formal manual-reference point estimate and the inclusive nominal specification limits. The overlap flag did not create an indeterminate category, alter a specimen's primary classification, remove a specimen from analysis, or impose a retrospective guard band.

This treatment preserves the distinction between measurement uncertainty and the prospectively defined conformity decision rule. Reference uncertainty is therefore relevant context for interpreting near-limit cases, but it cannot be used retrospectively to redefine unfavorable formal outcomes [JCGM 100:2008; JCGM 106:2012].

## 5.6 Round-Associated Shift in Signed Error

Post-validation exploratory analysis identified a round-specific pattern in mean signed error.

Mean signed error was:

- +0.000764 in in Round 1;
- +0.001721 in in Round 2; and
- +0.002355 in in Round 3.

The difference between the Round 3 and Round 1 means was +0.001591 in.

Within each round, however, signed error showed essentially no linear relationship with acquisition sequence. The sequence regressions produced \(R^2\) values of 0.0060, 0.0010, and 0.0027 for Rounds 1, 2, and 3, respectively.

The observed pattern was therefore manifested primarily as a difference among rounds rather than as a detectable monotonic trend across acquisition sequence within an individual 60-specimen round.

The study design does not permit the source of that between-round difference to be isolated. Round identity, acquisition session, elapsed time, and other conditions that could vary between sessions were not independently manipulated as separate experimental factors. Consequently, the observed pattern should not be interpreted as proof of a causal round effect.

Additional exploratory diagnostics also did not establish a mechanism. Maximum placement-dependent variation showed negligible association with specimen-level absolute agreement error. Signed specimen error showed essentially no linear dependence on formal OAL. Effective PPI was associated with individual observation error, but effective PPI is an endogenous component of the frozen dimensional-conversion equation, and its mean values remained similar across the three rounds.

The mechanism responsible for the round-associated shift therefore remains unresolved. The formal evidence does not justify assigning the shift specifically to specimen placement, spatial calibration, effective PPI, environmental conditions, segmentation, estimator behavior, or another individual source.

The unresolved between-round behavior is a limitation of the V1 measurement system characterization and identifies session-to-session dimensional stability as an appropriate subject for subsequent investigation.

## 5.7 Measurement Availability Versus Measurement Quality

CaseMetrology produced a valid result for all 180 planned formal CV observations, giving a measurement availability of 100%.

This result demonstrates that the frozen V1 image-acquisition, segmentation, measurement, and data-recording pipeline operated without formal system failures during the validation study.

Availability, however, addresses whether the system produces a measurement; it does not establish whether the measurement is sufficiently accurate or repeatable for the intended dimensional decision.

The V1 study illustrates this distinction clearly. Availability exceeded the 99% requirement while multiple agreement and repeatability criteria were not met.

For an automated or semi-automated inspection system, both properties are required. A system that produces measurements reliably but with excessive agreement error or placement sensitivity cannot be judged adequate solely on the basis of high measurement availability.

## 5.8 Study Limitations

Several limitations define the scope within which the formal V1 results should be interpreted.

First, the study used one operator for both the manual-reference and CV acquisition processes. The manual repeated measurements therefore characterize within-operator behavior and do not quantify between-operator reproducibility [JCGM 200:2012].

Second, formal validation was performed using one frozen hardware and software configuration. The results apply to the tested CaseMetrology V1 configuration and should not be generalized automatically to different cameras, lenses, lighting systems, calibration geometries, image-processing algorithms, or physical positioning arrangements.

Third, the formal sample contained 60 specimens selected using prospectively defined strata that intentionally represented the dimensional range and specification-boundary regions required for validation. The resulting classification counts therefore characterize this designed validation sample and should not be interpreted as estimates of production defect prevalence.

Fourth, the formal V1 CV measurements used independent free specimen placement rather than mechanically constrained location. The observed repeated-placement performance is specific to that acquisition condition.

Fifth, the formal manual reference had finite calibration uncertainty, display resolution, and repeated-measurement variation. Although these components were incorporated prospectively into the reference-uncertainty analysis, the manual reference should not be interpreted as error-free truth.

Sixth, the empirical 95th-percentile and maximum-error statistics are based on the finite formal sample. They characterize the observed validation population but do not establish a universal worst-case error bound for all possible cartridge cases or operating conditions.

Finally, the post-validation round-associated shift was identified descriptively but its causal mechanism was not established.

These limitations constrain the breadth of the conclusions but do not invalidate the formal comparison. Rather, they define the conditions under which the conclusions are supported.

## 5.9 Implications for CaseMetrology System Development

The V1 results identify two related but experimentally distinct development questions.

The first concerns control of specimen presentation. The formal placement-dependent repeatability result substantially exceeded the prospectively defined target under independent free placement. A subsequent CaseMetrology configuration could therefore test whether a more controlled and reproducible specimen-positioning method reduces repeated-placement variation.

Such a positioning change would constitute a new measurement-system configuration. Its performance would need to be evaluated prospectively rather than treated as a correction to the preserved V1 result.

The second question concerns dimensional agreement and between-round stability. Because the specimens with the greatest placement-dependent variation were not systematically the specimens with the greatest specimen-mean agreement error, improved positioning should not be assumed to eliminate the positive bias or the observed round-associated pattern.

A subsequent development program should therefore evaluate these questions separately:

1. whether controlled specimen positioning reduces repeated-placement variation; and
2. whether the modified system also improves dimensional agreement and session-to-session stability relative to the manual reference.

The preserved V1 results may appropriately inform engineering development. However, if V1 specimens or V1 measurement outcomes are used to choose, tune, or select a later configuration, those data become development evidence for that configuration and cannot simultaneously provide independent confirmation of its performance.

Any later V2 claim of independent validation should therefore be supported by prospectively defined confirmatory data that were not used to optimize or select the V2 measurement system.

## 5.10 Answer to the Research Question

The formal research question asked whether the frozen CaseMetrology OAL method satisfied the prespecified criteria for measurement availability, placement-related repeated-measurement behavior, dimensional agreement, error magnitude, and classification performance relative to an independent calibrated manual reference process.

The answer is **no for the complete V1 validation criterion set**.

The system met the measurement-availability criterion, producing valid measurements for all 180 formal CV acquisition opportunities. It also exhibited strong linear association with the manual reference.

However, it did not meet the prespecified limits for independent-placement P95 difference, absolute mean bias, RMSE, empirical 95th-percentile absolute specimen error, or maximum absolute specimen error. It also produced one false pass, contrary to the prospectively preferred zero-false-pass outcome.

The V1 configuration therefore cannot be described as having satisfied the complete formal OAL validation requirements.

At the same time, the formal study successfully quantified the magnitude and structure of the observed disagreement and identified specific engineering limitations that can guide subsequent system development.

## 5.11 Conclusions and Future Work

The CaseMetrology V1 configuration completed all 180 planned formal CV acquisitions with 100% measurement availability and exhibited strong specimen-to-specimen linear association with the calibrated manual reference.

Those characteristics were not sufficient to establish metrological adequacy. Under independent free specimen placement, placement-dependent variation exceeded the prospective repeatability criterion, the CV method exhibited a positive specimen-level bias, multiple dimensional-agreement criteria were not met, and specification classification included both false-fail and false-pass outcomes.

The formal V1 results therefore do not support unconditional acceptance of the tested configuration as a validated OAL conformance-measurement system.

At the same time, the study established a preserved quantitative baseline for subsequent CaseMetrology development. Future work should prioritize more controlled specimen positioning, investigation of the unresolved round-associated measurement shift, and evaluation of whether any modified configuration improves both repeated-placement behavior and dimensional agreement relative to the manual reference.

Other cartridge-case dimensions, multiple operators, alternative optical configurations, and dynamic manufacturing inspection remain outside the formal scope of the present study and may be evaluated separately in later work.

The V1 formal result should remain an immutable baseline. Any subsequent CaseMetrology configuration should be identified as a new system version and evaluated prospectively rather than used to reinterpret, modify, or replace the preserved V1 validation outcome.
