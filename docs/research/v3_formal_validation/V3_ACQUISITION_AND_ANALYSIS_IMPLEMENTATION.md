# V3 Formal Acquisition and Analysis Implementation

## Purpose

This document defines the implementation used to execute the prospective V3
formal CV study without allowing measurement results to influence specimen
placement or reacquisition decisions.

## Acquisition architecture

The V1 formal runner is not reused unchanged because it is tied to the V1
configuration commit, V1 run-order schema, and the PCA production workflow.

V3 instead uses the already validated controlled research acquisition layer,
`src/acquisition/capture_research.py`, to capture exactly one raw image for each
scheduled placement.

No OAL estimator is executed during formal specimen acquisition.

The operator therefore does not see Endface Hybrid, PCA, or Geometry OAL values
while collecting the 180 planned placements.

## Session blank

Each V3 CV session receives one preserved blank-reference image acquired under
the same locked camera-control procedure.

Formal blank files are named:

- `V3-CV-S001_blank_reference.png`
- `V3-CV-S002_blank_reference.png`
- `V3-CV-S003_blank_reference.png`

## Formal specimen capture

The frozen randomized run order is enforced by software.

For every scheduled observation, the capture runner verifies:

- round;
- sequence;
- expected specimen ID;
- existence of the session blank;
- completion of preceding sequence positions;
- frozen measurement-system SHA-256 manifest;
- locked camera controls.

One raw image and its acquisition metadata are preserved for every scheduled
placement.

The runner intentionally prints no OAL result.

## Post-acquisition estimator processing

Estimator processing is allowed only after all 180 scheduled formal images have
been acquired.

The frozen Endface Hybrid development implementation is loaded directly from:

`scripts/evaluate_oal_endface_hybrid_dev.py`

Its pre-validation SHA-256 is:

`3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af`

The same raw image and same segmentation/calibration lineage are used to obtain:

- Endface Hybrid — primary V3 estimator;
- PCA — historical V1 comparator;
- Geometry — secondary estimator.

Detailed estimator results are preserved as per-observation JSON records and
summary values are written to the V3 observation table.

## Scientific rationale

Separating image acquisition from estimator evaluation prevents numerical
measurement outcomes from influencing operator handling, repetition, or
reacquisition during the prospective study.

It also guarantees that all estimator comparisons are performed on identical
formal images.
