# Endface Hybrid OAL Estimator — Pre-Retrospective Freeze

Date: 2026-09-11

## Purpose

This record freezes the developmental endface-hybrid OAL estimator before
retrospective application to the formal V2 image dataset.

V1 and V2 formal results remain unchanged.

The estimator was developed using only non-formal diagnostic/development
images, including specimens excluded from the formal validation population.

## Architecture

The estimator:

1. Uses the existing geometry estimator to determine the specimen longitudinal axis.
2. Does not perform subpixel sidewall refinement.
3. Uses grayscale subpixel localization only at the two OAL end faces.
4. Robustly fits the base and mouth end-face datums.
5. Computes OAL as the axial separation between those fitted end faces.

## Frozen implementation

Script:

    scripts/evaluate_oal_endface_hybrid_dev.py

SHA-256:

    3f332ef097f5f39e6e1447a61756c7ecc4c8e7c8170fe8933ab362daffb2a2af

## Frozen parameters

    END_SAMPLE_COUNT = 41
    MINIMUM_END_PROFILE_COUNT = 12
    END_FACE_TRANSVERSE_FRACTION = 0.30

    profile_half_length_pixels = 6.0
    profile_step_pixels = 0.25
    interior_plateau_limit_pixels = (-6.0, -2.0)
    exterior_plateau_limit_pixels = (2.0, 6.0)
    normalized_crossing = 0.50
    minimum_local_contrast = 30.0
    maximum_anchor_distance_pixels = 3.0
    maximum_crossing_distance_pixels = 3.0

## Development evidence

Controlled specimen 121:

- availability: 30/30
- within-placement P95 pairwise: 0.000151873 in
- between-placement P95 pairwise: 0.000763953 in
- maximum between-placement pairwise: 0.000821757 in

Fixture-2 independent-placement results:

- specimen 146: P95 pairwise 0.003271088 in
- specimen 178: P95 pairwise 0.000351631 in
- specimen 187: P95 pairwise 0.000036843 in
- specimen 197: P95 pairwise 0.000493431 in

Specimen 146 fixed-position 10-frame sequence:

- availability: 10/10
- P95 pairwise: 0.000096338 in
- maximum pairwise: 0.000115151 in

Specimen 146 therefore remains an identified repositioning/pose-sensitive
development case rather than a basis for further estimator tuning.

## Methodological guardrail

No estimator architecture or numerical parameter may be changed in response
to results obtained from retrospective processing of the formal V2 images.

The V2 retrospective analysis is exploratory and may be used to determine
whether this already-frozen estimator warrants prospective V3 validation.

It is not itself an independent prospective validation of the estimator.
