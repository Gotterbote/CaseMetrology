# V3 Protocol Amendment 002
## Fixture 2 Friction Retention — Pre-Acquisition Verification

Date: 2026-09-15

Status: PRE-ACQUISITION

No formal V3 CV observations had been collected when this amendment was issued.

## Change

Fixture 2 is retained against the established left datum using a
friction-based holding method.

The holding method is outside the camera field of view and does not alter:

- specimen contact geometry;
- base measurement plane;
- controlled roll-orientation procedure;
- camera or lens position;
- lighting;
- calibration; or
- estimator logic.

## Pre-Acquisition Verification

The revised Fixture 2 retention method was evaluated using excluded
development specimen 178.

A diagnostic blank image confirmed that the new friction-holding mechanism
did not intrude into the camera field of view.

Specimen 178 was then independently removed and replaced five times using
the planned V3 controlled presentation:

- Fixture 2 retained against the left datum;
- base-to-mouth rocking controlled;
- engraving oriented toward the camera;
- independent removal and replacement between images.

The frozen V3 estimator implementation was applied to all five diagnostic
images.

### Results

| Estimator | Valid | P95 Pairwise Difference | Maximum Pairwise Difference | 5-Placement Range | Sample SD |
|---|---:|---:|---:|---:|---:|
| PCA | 5/5 | 0.000696 in | 0.000716 in | 0.000716 in | 0.000298 in |
| Geometry | 5/5 | 0.000476 in | 0.000537 in | 0.000537 in | 0.000201 in |
| Endface Hybrid | 5/5 | 0.000264 in | 0.000284 in | 0.000284 in | 0.000122 in |

Endface Hybrid OAL observations:

1. 0.996781684 in
2. 0.996593043 in
3. 0.996548679 in
4. 0.996736675 in
5. 0.996832843 in

All five Endface Hybrid observations were valid. Each placement accepted
41/41 sampled profiles on both end faces.

## Disposition

The Fixture 2 friction-retention method is accepted for V3 formal
acquisition.

The five-placement diagnostic is a pre-acquisition mechanical verification
only and is not included in the formal V3 performance dataset.

No additional fixture or estimator development is planned before formal
V3 acquisition unless a predefined stop condition occurs.

## Unchanged Frozen Elements

This amendment does not change:

- Arducam IMX296 camera;
- 16 mm lens;
- working geometry;
- backlighting;
- camera controls;
- existing calibration;
- controlled specimen roll orientation;
- Endface Hybrid primary estimator;
- PCA historical comparator;
- Geometry secondary estimator;
- frozen 60-specimen formal cohort;
- three randomized V3 CV run orders; or
- prospective V3 performance criteria.

The next formal activity is V3-CV-S001.
