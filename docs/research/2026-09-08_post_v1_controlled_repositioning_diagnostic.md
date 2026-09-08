# Post-V1 Controlled-Repositioning Diagnostic

Date: 2026-09-08

## Purpose

Determine how much OAL variability remains when specimen 121 is repeatedly
removed and reseated using the existing Lexan locator under controlled ambient
lighting.

This is a post-V1 exploratory engineering diagnostic only.

Formal V1 remains complete, immutable, and primary.

## Specimen

Prevalidation specimen 121.

## Lighting

- Window blocked
- Ceiling light OFF
- Ceiling fan OFF
- Backlight continuously ON

## Frozen blank reference

postv1_reposition_blank_20260908_174242_592657_01.png

This same blank shall be used for all measurements in the diagnostic.

## Placement rule

Ten independent controlled placements shall be performed.

For each placement:

1. Completely remove specimen 121 from the Lexan fixture.
2. Reinsert it in the normal base-to-mouth OAL orientation.
3. Bring the specimen gently into the locator's normal mechanically seated position.
4. Do not force, twist, intentionally angle, or manually fine-tune the specimen after seating.
5. Release the specimen completely.
6. Wait approximately 3 seconds.
7. Acquire three consecutive images at approximately 2-second intervals without touching the specimen.
8. Remove the specimen completely before the next placement.

One seating action constitutes one independent placement.

The three images within a placement measure short-term frame-to-frame variability
without repositioning.

## Sample size

- 10 controlled placements
- 3 images per placement
- 30 total diagnostic specimen images

## Exclusion of setup capture

The setup image acquired before this protocol was frozen is retained as
engineering setup evidence but is excluded from the controlled-repositioning
analysis.

## Prohibited changes

No changes shall be made to:

- estimator
- segmentation
- thresholds
- calibration
- software
- camera
- lens
- focus
- measurement plane
- backlight
- camera controls

## Interpretation

The principal comparison will be between:

- within-placement frame-to-frame variation;
- between-placement controlled-repositioning variation; and
- V1 independent free-placement variation.

The V1 independent-placement pairwise P95 was 0.004831 in.

Results from this diagnostic shall not replace or modify V1.
