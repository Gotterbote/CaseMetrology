# Lexan Optical Test Deviation Addendum — 2026-07-28

## Record classification

This retrospective addendum was created from preserved images, camera-setting
records, comparison outputs, the original validation runbook, and Git history.

It supplements the original evidence. It does not modify the original captures,
metadata, results, or interpretation.

## Planned method

The planned method was documented in:

- `docs/lexan_fixture_validation_runbook_2026-07-28.txt`

The runbook called for:

- A passing research preflight before testing
- Ambient-temperature recording
- Controlled captures using `capture_research.py`
- Comparison using `compare_illumination.py`
- Numerical and visual inspection near the intended measurement region

## Actual execution

The preserved comparison used:

- One blank image without Lexan
- One blank image with Lexan
- Locked camera settings verified before and after acquisition
- Fixed ROI: x=500:1300, y=350:900
- Saved difference images and numerical results
- SHA-256 evidence manifest

## Deviations

1. The comparison occurred before the formal research preflight recorded later
   that evening.
2. The captures did not use the exact `capture_research.py` workflow specified
   in the runbook.
3. The comparison used a central ROI rather than supporting a full-field claim.
4. The ROI did not directly evaluate both final measurement-edge regions.
5. Only one image pair was evaluated, so optical repeatability was not
   established.
6. Temperature was not measured using a traceable instrument.
7. Lexan or fixture boundaries could still create false edges if included in a
   dimensional-analysis ROI.

## Preserved result

- Mean grayscale without Lexan: 225.1456
- Mean grayscale with Lexan: 225.0625
- Mean change: -0.0831
- Percent change: -0.0369%
- Mean absolute pixel difference: 0.8864
- RMSE: 1.2830
- 95th-percentile absolute difference: 3.0000

## Defensible interpretation

The Lexan did not produce a practically meaningful change in mean illumination
within the selected unobstructed central ROI under the tested conditions.

The finding is classified as:

> Preliminary central-field illumination evidence

It is not complete optical validation.

## Evidence

- `data/lexan_test/`
- `docs/research_session_summary_2026-07-28.md`

## Git traceability

- `3c11993` — Document Lexan optical comparison test
