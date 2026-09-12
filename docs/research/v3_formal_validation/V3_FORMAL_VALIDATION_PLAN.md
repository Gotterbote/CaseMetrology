# CaseMetrology V3 Formal OAL Validation Plan

Generated: 2026-09-11T23:23:10-05:00

Development baseline: `cdd76a7`

Status: **PROSPECTIVE — PRE-ACQUISITION**

---

## 1. Study Purpose

The V3 formal validation will determine whether the frozen CaseMetrology
configuration provides improved overall-length agreement and
repositioning repeatability when specimen rocking and roll orientation
are mechanically controlled.

V3 is a prospective confirmation study.

Formal V3 observations shall not be used to modify the system.

---

## 2. Formal Measurement Configuration

The planned V3 configuration is:

- Arducam IMX296 global-shutter camera
- 16 mm lens
- existing accepted OAL calibration
- rocking-controlled fixture
- Fixture 2 positively registered
- controlled specimen roll orientation
- specimen engraving used as roll-registration reference
- existing backlight configuration
- existing locked camera controls
- unchanged working geometry

No hardware modification is planned.

---

## 3. Estimator Hierarchy

Primary estimator:

**Endface Hybrid**

Historical comparator:

**PCA**

Secondary/exploratory estimator:

**Geometry**

The exact source files and SHA-256 hashes for these estimators shall be
recorded in the final V3 freeze evidence before formal data acquisition.

No estimator modification is permitted after final freeze.

---

## 4. Development Independence

Development/prevalidation specimens:

121, 146, 178, 187, 197

These specimens remain outside the frozen V3 formal cohort.

The controlled-presentation procedure and V3 estimator work were
developed using prevalidation/development data.

No measurement from the prospective V3 formal acquisition may be used
to tune the V3 system.

---

## 5. Formal Specimen Cohort

The V3 formal cohort is the same retained 60-specimen cohort used in
the completed V1 formal validation.

Allocation:

| Stratum | n |
|---|---:|
| below LSL | 8 |
| near LSL in specification | 14 |
| central nominal | 16 |
| near USL in specification | 14 |
| above USL | 8 |
| Total | 60 |

No specimen shall be replaced because of poor V3 performance.

---

## 6. Manual Reference Strategy

The accepted three-round V1 manual-reference mean remains the primary
reference value for each retained specimen.

Before formal V3 CV acquisition, all 60 specimens shall receive one
new randomized manual stability-check measurement.

The stability check verifies that the retained physical specimens have
not materially changed.

It does not replace the frozen reference means.

Manual stability randomization seed:

`2026091201`

A difference greater than 0.0015 in from the frozen manual-reference
mean triggers review.

A triggered specimen receives two additional stability-check readings.

A review trigger shall not result in silent exclusion or specimen
replacement.

---

## 7. V3 Formal CV Design

Each of the 60 specimens shall undergo three independent formal
placements.

Total formal CV observations:

**180**

Each observation requires removal and independent replacement of the
specimen.

Repeated images of an untouched specimen do not constitute independent
placements.

CV randomization seed:

`2026091202`

Formal sessions:

- V3-CV-S001
- V3-CV-S002
- V3-CV-S003

---

## 8. Controlled Presentation

For every formal placement:

1. specimen is removed from the measurement position;
2. specimen is independently replaced;
3. specimen is seated against the established fixture datum;
4. base-to-mouth rocking is mechanically controlled;
5. roll orientation is registered using the frozen presentation rule;
6. proper seating is confirmed;
7. image is acquired.

The presentation procedure shall not be changed because of observed
measurement results.

---

## 9. Primary Statistical Unit

The primary independent experimental unit is the specimen.

Primary agreement sample size:

**n = 60**

For each specimen, the three V3 Endface Hybrid measurements shall be
averaged and compared with the frozen manual-reference mean.

The 180 CV observations shall not be treated as 180 independent
specimens.

---

## 10. Prospective Performance Targets

| Endpoint | Frozen target |
|---|---:|
| Endface Hybrid availability | >= 99% |
| Absolute mean bias | <= 0.0010 in |
| RMSE | <= 0.0020 in |
| P95 absolute error | <= 0.0030 in |
| Maximum absolute error | <= 0.0040 in |
| P95 pairwise repositioning difference | <= 0.0020 in |

Failure of a target is a study result.

It does not authorize system modification.

---

## 11. Agreement Analysis

The formal specimen-level analysis shall report:

- mean signed bias
- 95% confidence interval for bias
- median signed error
- MAE
- RMSE
- P95 absolute error
- maximum absolute error

The P95 calculation shall remain consistent with the V1 analysis
implementation.

---

## 12. Repositioning Analysis

For each specimen, three independent measurements produce three
pairwise absolute differences.

The analysis shall report:

- specimen three-placement range
- pairwise absolute differences
- P95 pairwise absolute difference
- maximum pairwise absolute difference
- worst-performing specimens

---

## 13. Classification Analysis

Frozen specification limits:

LSL = 0.9900 in

USL = 1.0100 in

Each specimen shall be classified as:

- true pass
- true fail
- false pass
- false fail

All misclassified specimens shall be individually reported.

No post-hoc guard band shall be introduced.

---

## 14. V1-to-V3 Comparison

Because V1 and V3 use the same retained specimens and frozen manual
reference, paired comparison is permitted.

Three conditions shall be distinguished:

1. V1 PCA with V1 specimen presentation
2. V3 PCA with controlled presentation
3. V3 Endface Hybrid with controlled presentation

This permits mechanical-presentation effects and estimator effects to
be discussed separately.

---

## 15. Stop Conditions

Formal acquisition shall stop or enter HOLD status for:

- failed required reference checks
- failed calibration verification
- loss of Fixture 2 registration
- fixture movement or modification
- camera movement
- lens movement
- focus change
- working-geometry change
- unintended camera-control change
- physical specimen damage
- systematic acquisition/software failure
- inability to establish the frozen presentation procedure
- loss of specimen/data traceability

These are NOT stop conditions:

- large measurement error
- poor repeatability
- unexpected bias
- false pass
- false fail
- estimator disagreement
- unusual specimen geometry

Those are formal results.

---

## 16. Raw-Data Preservation

All formal images shall be retained.

Blank/reference images shall be retained.

Protocol-invalid attempts shall remain preserved.

A technically valid measurement shall not be repeated merely because
its value is unfavorable.

---

## 17. Configuration-Change Rule

A material change after final freeze to:

- hardware
- calibration
- fixture
- presentation rule
- segmentation
- estimator logic
- camera configuration

ends acquisition under the frozen V3 configuration until the change is
formally dispositioned.

A materially changed system requires a new prospective validation
decision.

---

## 18. Interpretation Boundary

Successful V3 results may support approximately thousandth-inch-class
repositioning performance under the tested controlled-presentation
conditions.

Repeatability shall not be described as equivalent to absolute
accuracy.

Results apply only to the tested system and OAL task.

No claim of automated production-line performance or uncontrolled
specimen orientation is implied.

---

## 19. Final Freeze Requirement

Formal acquisition may begin only after:

- V3 plan exists;
- frozen 60-specimen cohort passes audit;
- manual stability order is frozen;
- all three CV run orders are frozen;
- estimator source files are identified;
- calibration/configuration files are identified;
- all frozen files receive SHA-256 hashes;
- configuration commit is recorded;
- freeze evidence is committed;
- repository is clean.
