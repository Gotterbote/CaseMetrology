# Prevalidation Measurement-Assurance Postcheck

**Project:** CaseMetrology
**Date:** 2026-08-13
**Research phase:** Prevalidation estimator review
**Repository commit during optical acquisition:** `6e68cc5696980630577d55a38c54e0993e8d9535`
**Formal validation status:** Not started

## 1. Purpose

A post-session measurement-assurance check was performed after the five-case
OAL estimator checkpoint.

The purpose was to determine whether either the manual comparison instrument
or the optical reference measurement showed evidence of a gross same-session
offset or instability that would undermine interpretation of the estimator
checkpoint.

This activity is not formal validation and does not establish independent
traceable accuracy of the complete CaseMetrology system.

No estimator, calibration equation, camera setting, or manual result was
adjusted as a consequence of this check.

## 2. Manual 1-Inch Reference Check

The Mitutoyo digital caliper, serial `B23090910`, was used to measure the
1-inch dimensional reference five times with complete removal and
repositioning between readings.

Raw readings:

1. `1.0000 in`
2. `1.0000 in`
3. `1.0000 in`
4. `1.0000 in`
5. `1.0000 in`

Mean:

`1.0000000 in`

Range:

`0.0000000 in`

The dimensional reference has a certified central length of `1.0000024 in`.

The absence of an instrument-specific current calibration certificate for the
caliper remains a limitation. These readings therefore document same-session
measurement assurance and repeatability at approximately 1 inch; they do not
make the caliper a certified or traceable formal ground-truth instrument.

Raw manual postcheck data:

`data/oal_validation/prevalidation/2026-08-13_measurement_assurance_postcheck/manual_1in_reference_postcheck.csv`

## 3. Optical Reference Check — Initial Attempt

Initial image:

`raw_images/acquisition/prevalidation_oal_1in_standard_postcheck_20260813_20260813_200616/prevalidation_oal_1in_standard_postcheck_20260813_20260813_200619_168734_01.png`

The subpixel gauge-block diagnostic reported:

- detected bounding box: `x=383, y=257, w=532, h=726`
- valid columns: `212`
- mean subpixel span: `720.548548 px`
- median subpixel span: `720.536244 px`
- span SD: `0.162600 px`
- fitted center span: `720.548548 px`
- preliminary scale: `720.546818 px/in`
- analyzer status: `PRELIMINARY SUBPIXEL DIAGNOSTIC`

This result is **invalid for calibration-stability or measurement-assurance
interpretation**.

The block was presented with the 1.375-inch dimension vertical while the
analyzer assumes that the certified `1.0000024 in` dimension is vertical.

The raw image and diagnostic outputs are retained rather than deleted so the
procedural error remains traceable.

No calibration or software change was made in response.

## 4. Optical Reference Check — Corrected Attempt

The same standard was rotated 90 degrees so the certified 1-inch dimension was
vertical as required by the analyzer.

Corrected image:

`raw_images/acquisition/prevalidation_oal_1in_standard_postcheck_corrected_20260813_20260813_200953/prevalidation_oal_1in_standard_postcheck_corrected_20260813_20260813_200955_409702_01.png`

Acquisition remained at the same locked camera configuration.

The corrected subpixel gauge-block diagnostic reported:

- detected bounding box: `x=388, y=258, w=724, h=525`
- valid columns: `290`
- mean subpixel span: `523.147633 px`
- median subpixel span: `523.096027 px`
- span SD: `0.211174 px`
- span range: `522.800439 to 523.787037 px`
- peak-to-peak span: `0.986598 px`
- top-edge fitted angle: `0.073289 deg`
- bottom-edge fitted angle: `0.195593 deg`
- fitted center span: `523.147633 px`
- preliminary scale: `523.146377 px/in`
- analyzer status: `PRELIMINARY SUBPIXEL DIAGNOSTIC`

This corrected result is usable as a same-session optical measurement-assurance
check.

Because the gauge block participates in the calibration lineage, this check is
not an independent validation of system accuracy.

## 5. Interpretation

The manual postcheck produced five identical displayed readings at `1.0000 in`
with zero displayed range.

The correctly oriented optical postcheck produced a scale in the expected
approximately 523 px/in operating region.

Together, these observations provide no evidence of a gross same-session
manual-reference or optical-scale failure large enough to explain the
systematic negative discrepancy observed with the geometry OAL estimator.

This supports continuing the estimator-selection review.

It does not convert the five-case prevalidation comparison into formal
validation evidence and does not remove the limitation associated with the
caliper's unavailable instrument-specific current calibration certificate.

## 6. No Post-Hoc Adjustment

Neither the manual reference readings nor the optical reference result shall
be used to derive a post-hoc correction to the five cartridge-case
measurements.

No constant offset, pixel correction, endpoint shift, or calibration change is
authorized by this record.

## 7. Evidence Identity

### Initial incorrectly oriented optical attempt

Raw image SHA-256:

`f8f1d492df555d8ed23e08a89f92d67beb7853fba93ef6f4eb0f67a2118c7ddf`

Acquisition metadata SHA-256:

`b1a6595aeddd714ff1ce1e1b435af4d627cc14883e2b2b69cc00e41afda8ce5b`

Analyzer per-column CSV SHA-256:

`a7bde48cc47c8fc5a5abbfd13d92f74b89039f2f80ec2b094522d8d7fb8a069a`

Diagnostic image SHA-256:

`dff3fd7ecac2dff43ed758cb5b8f1f38eb1f521b0432de27cf7a52c69b6044f0`

### Corrected optical attempt

Raw image SHA-256:

`49c312c3abf0d814a6a540aa5b1d7096eb77d57da74ded0095844554cf95ce65`

Acquisition metadata SHA-256:

`db4fb462fa3ae8926228ac7bf9fde1de37e5fe597b4a6300fdea1244727f04ca`

Analyzer per-column CSV SHA-256:

`ff5bd4b50d58071cf16abd58c99b89108f0953c135be94c0fe408ac9ca13ed9e`

Diagnostic image SHA-256:

`59147c4ed5323795dd7a9b1efddf786e003d5923ef01f322faa06845fc078f76`

## 8. Disposition

**POST-SESSION MEASUREMENT-ASSURANCE CHECK: COMPLETE**

**MANUAL REFERENCE CHECK: NO GROSS OFFSET OR DISPLAYED REPEATABILITY ISSUE OBSERVED**

**OPTICAL REFERENCE CHECK: NO GROSS SAME-SESSION SCALE FAILURE OBSERVED**

**FORMAL VALIDATION: REMAINS ON HOLD**

The next activity is documentation and freezing of the selected primary OAL
pixel-length estimator before formal validation begins.
