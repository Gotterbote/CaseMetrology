# Chapter 5 Discussion and Conclusions — Reviewed Rebuild Audit

**Project:** CaseMetrology  
**Date:** 2026-09-17  
**Target manuscript:** `docs/research/thesis_support/2026-09-17/2026-09-17_thesis_manuscript_rebuild.md`  
**Starting repository state:** branch `main`, commit `4d534de`  
**Status:** Second-pass rigorous review after initial Chapter 5 draft

## Review Basis

The second-pass review checked Chapter 5 against:

- the September 17 final thesis architecture;
- the rebuilt Chapter 3 definition of the six quantitative criteria;
- the corrected Chapter 4 specimen-level V3 agreement basis supplied for the final results chapter;
- preserved V1 formal results;
- the evidentiary distinction among prospective validation, exploratory diagnostics, retrospective estimator comparison, and post hoc guard-band analysis; and
- thesis-wide claim boundaries for static OAL screening.

## Architecture Compliance

The reviewed chapter retains all required sections:

- 5.1 Answer to the Original Validation Question
- 5.2 Engineering Progression
- 5.3 Repeatability Versus Absolute Accuracy
- 5.4 Industrial Screening Feasibility
- 5.5 Guarded Decision Logic
- 5.6 Limitations
- 5.7 Future Work
- 5.8 Final Conclusion

## Corrected V3 Basis

The reviewed Chapter 5 uses the corrected 60-specimen agreement metrics:

- mean bias: -0.000435 in;
- MAE: 0.001517 in;
- RMSE: 0.001794 in;
- nearest-rank P95 absolute specimen error: 0.003170 in;
- maximum absolute specimen error: 0.003913 in.

Separate measurement bases are preserved:

- availability: 180/180 acquisition opportunities;
- P95 repositioning: pairwise differences among repeated CV presentations;
- agreement metrics: 60 specimen means versus accepted manual-reference means.

## Criterion Disposition

| Criterion | Target | V3 result | Disposition |
|---|---:|---:|---|
| Availability | >=99% | 100% | MET |
| Absolute mean bias | <=0.0010 in | 0.000435 in | MET |
| RMSE | <=0.0020 in | 0.001794 in | MET |
| P95 absolute specimen error | <=0.0030 in | 0.003170 in | NOT MET |
| Maximum absolute specimen error | <=0.0040 in | 0.003913 in | MET |
| P95 pairwise repositioning | <=0.0020 in | 0.000633 in | MET |

V3 therefore met **five of six quantitative criteria**.

Zero false passes remains a preferred decision outcome, not a seventh quantitative criterion. V3 retained one false pass and three false fails under the unguarded rule.

## Important Revisions Made During Second Pass

### 1. Original V1 question kept distinct from later V3 validation

The first draft risked describing the original research question as being answered "in two stages." The reviewed version now states explicitly:

- V1 answers the original prospective validation question;
- that answer remains negative;
- V3 is a later prospective evaluation of a modified frozen system;
- V3 does not replace or retroactively revise the V1 outcome.

### 2. Causal attribution of the 86.9% repositioning improvement narrowed

The total V1-to-V3 reduction from 0.004831 in to 0.000633 in is a **system-level comparison**. It spans changes in both estimator and physical presentation and therefore is not attributed solely to presentation.

The reviewed discussion instead uses the V2 Endface-Hybrid-to-V3 comparison as the stronger presentation-related evidence:

- V2 Hybrid P95 repositioning: 0.003021 in;
- V3 Hybrid P95 repositioning: 0.000633 in;
- reduction: approximately 79.0%.

Because those data were acquired in different phases rather than in a randomized factorial experiment, the chapter describes the result as **consistent with** a major presentation contribution, not as a pure isolated causal effect.

### 3. Repeatability and agreement measurement bases explicitly separated

The reviewed chapter now states that:

- P95 repositioning is based on pairwise repeated-presentation differences;
- bias/MAE/RMSE/P95/max agreement are based on specimen-level CV means versus manual-reference means;
- the metrics describe different properties and are not directly interchangeable.

### 4. Small mean bias not equated with small specimen error

The revised discussion explicitly explains that the V3 bias of -0.000435 in can coexist with MAE 0.001517 in and P95 absolute error 0.003170 in because positive and negative specimen-level differences can partially cancel in the signed mean.

### 5. Screening claim narrowed

The reviewed chapter does not state that CaseMetrology is a validated production screening system. It states that V3 supports **further development/evaluation of a static dimensional-screening architecture** under controlled presentation.

### 6. Guard-band inference tightened

The reviewed chapter emphasizes that:

- 0.0006 in is the smallest observed zero-false-pass symmetric margin in this cohort;
- 0.0010 in is an engineering example;
- both are retrospective and cohort dependent;
- neither establishes future false-pass probability;
- an eventual production margin requires a prospective risk basis and independent validation.

## Limitations Added or Strengthened

The second pass explicitly includes:

- reuse of the same 60-specimen cohort across V1-V3 as a paired-comparison strength but not independent replication;
- the experimental nature of controlled roll/seating for production translation;
- configuration-specific conventional-lens calibration limits;
- finite-sample interpretation of nearest-rank P95 and maximum observed error;
- absence of production throughput, economics, long-term calibration stability, and environmental robustness evidence.

## Manuscript-Wide Stale-Value Warning

The September 17 final architecture and at least one rebuilt-manuscript copy still contain older V3 values:

- MAE `0.001531`
- RMSE `0.001804`
- P95 absolute error `0.003267`

The authoritative corrected thesis-facing V3 values are:

- MAE `0.001517`
- RMSE `0.001794`
- nearest-rank P95 absolute specimen error `0.003170`
- maximum absolute specimen error `0.003913`

The manuscript should be audited before the Chapter 5 commit. In particular, Chapter 1 currently contains at least one stale `0.003267` statement. Historical evidence files should not be rewritten merely because they contain the older calculation; the correction applies to the current thesis narrative and summary tables.

## Final Second-Pass Disposition

The reviewed Chapter 5 is internally consistent with the corrected V3 specimen-level basis and preserves the required evidentiary distinctions.

The central conclusion is:

- V1 did not satisfy the complete original validation requirements;
- V3 met five of six retained quantitative criteria;
- repeated-presentation behavior improved substantially;
- residual specimen-level absolute agreement remained the limiting metrology issue;
- the unguarded system retained one observed false pass;
- exploratory guarded logic supports screening feasibility but is not production validation;
- the thesis supports further development of a controlled static OAL screening architecture, not a claim of precision-metrology replacement or production readiness.
