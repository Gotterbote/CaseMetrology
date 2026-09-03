# Formal OAL Reference-System Amendment and Limit Freeze

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation preparation
**Designated operator:** Timmy D. Bell
**Amendment date:** 2026-09-03
**Status:** Prospective; created before any formal reference-system check or
formal specimen measurement

## 1. Purpose

This amendment completes the certificate-dependent decisions required to
perform the first pre-use reference-system check.

It:

1. replaces the previously proposed manual-reference caliper;
2. records the completed certificate review;
3. freezes the session-check reference-value treatment;
4. freezes `E_limit`, `R_limit`, and `D_limit`; and
5. records the environmental-monitoring limitation.

This amendment authorizes the pre-use reference-system check only. Formal
specimen measurement remains `NO-GO` until that check passes and all remaining
master-protocol prerequisites are closed.

## 2. Scope and Preservation of Historical Records

For prospective formal validation use, references to Mitutoyo CD-8"ASX,
code 500-197-30, serial B23090910, are superseded by the instrument designated
in Section 3.

Historical screening, prevalidation, and measurement-assurance records that
correctly document use of B23090910 shall not be altered.

## 3. Designated Manual-Reference Instrument

- Manufacturer: Mitutoyo
- Model: CD-6"ASX
- Code number: 500-196-30
- Serial number: B24254849
- Resolution: 0.0005 in / 0.01 mm
- Calibration certificate/control number: DDJ25P23P
- Calibration date: 2025-09-25
- Certificate file:
  `calibration/instruments/mitutoyo_B24254849/2025-09-25_calibration_certificate_DDJ25P23P.png`
- Certificate SHA-256:
  `fdd5fb0c5632e30749c4d86e02152942b9343f2f52fde6226e04e48684d45693`

## 4. Caliper Certificate Review

Certificate DDJ25P23P was issued by the Mitutoyo America Calibration
Laboratory, Aurora, Illinois. It bears the A2LA-accredited calibration mark
with certificate number 0750.01 and states conformity to ISO/IEC 17025:2017.

The certificate reports:

- calibration environment of 20 degrees C +/- 3 degrees C and relative
  humidity below 70%;
- traceability to the SI unit of length through listed Mitutoyo reference
  standards and NIST;
- ASME B89.1.14-2018 as the applicable caliper standard;
- as-found condition `NEW`;
- as-left condition `PASS`;
- outside-measurement tolerance of +/- 0.0010 in at 1, 2, 4, and 6 in;
- as-left outside-measurement errors of 0.0000, 0.0000, +0.0005, and
  0.0000 in at 1, 2, 4, and 6 in, respectively; and
- expanded measurement uncertainty of +/-(120 + 6L) microinches, where
  `L` is expressed in inches, at approximately 95% confidence with coverage
  factor approximately equal to 2.

At 1 in, the reported expanded uncertainty is:

`U_cal = 126 microinches = 0.000126 in`

No numeric as-found error is reported because the instrument condition is
identified as `NEW`. No adjustment or repair is reported.

The certificate assigns no fixed calibration due date. It recommends
considering an initial calibration interval of 6 to 12 months after the
instrument is placed into service.

Three closed-jaw checks documented at evidence intake on 2026-09-02 each
displayed 0.0000 in.

### Caliper disposition

`ACCEPT_WITH_LIMITATION`

The caliper is suitable for the immediate pre-use check and prospective formal
manual-reference work only when:

- its identity is verified before use;
- its measuring faces and operation remain acceptable;
- it displays 0.0000 in when gently closed before the check;
- the pre-use reference-system check passes; and
- every later formal manual session satisfies the frozen pre-session and
  post-session checks.

## 5. Designated Check Standard

- Manufacturer: Mitutoyo
- Artifact: steel gauge block
- Grade: ASME Grade 0
- Identification number: 253568
- Certificate number: T26A06624
- Inspection date: 2026-01-21
- Nominal length: 1.0000000 in
- Certified central length: 1.0000024 in
- Expanded uncertainty: 0.0000024 in
- Coverage factor: `k = 2`
- Reference temperature: 20 degrees C +/- 1 degree C
- Inspection basis: ASME B89.1.9-2002
- Inspection method: comparator
- Certificate file:
  `calibration/reference_standards/mitutoyo_gauge_block_253568/2026-01-21_calibration_certificate_T26A06624.png`
- Certificate SHA-256:
  `91d797c3b9582ca0def4b7ac797eecaf2891dab2f266983e3da06d4adee3ab0b`

The physical standard displays identification number 253568, matching its
certificate.

### Check-standard disposition

`ACCEPT`

## 6. Certified-Value and Correction Policy

The full assigned value retained in the research record is:

`L_ref = 1.0000024 in`

No correction is applied to formal caliper observations because certificate
DDJ25P23P reports an as-left indication error of 0.0000 in at 1 in.

The expected display value for the 0.0005-in-resolution caliper is:

`L_display = 1.0000 in`

The full certified value shall remain in every reference-check record.
Individual observations shall be recorded exactly as displayed.

For session-control disposition, indication error is calculated against the
expected display value:

`E = mean(observed readings) - L_display`

The additional descriptive certified-value error may be calculated as:

`E_cert = mean(observed readings) - L_ref`

`E_cert` does not independently govern session acceptance because the
0.0000024-in difference between `L_ref` and `L_display` is below the caliper's
display resolution.

## 7. Frozen Reference-Check Limits

The following inclusive limits are frozen before any reference-check readings
are observed:

- `E_limit = 0.0005 in`
- `R_limit = 0.0005 in`
- `D_limit = 0.0005 in`

The technical basis is:

- the certificate reports zero as-left error at 1 in;
- the caliper resolution is 0.0005 in;
- the mean-error limit permits no more than one display increment from the
  expected display value;
- the range limit permits no more than one display increment of spread among
  five independent readings;
- the drift limit permits no more than one display increment between the
  pre-session and post-session means; and
- each limit is tighter than the certificate's +/-0.0010-in outside-
  measurement tolerance at 1 in.

The limits shall not be widened in response to observed check or validation
results.

## 8. Pre-Use Check Acceptance

The first pre-use check requires exactly five independent readings with
complete removal and repositioning between readings.

It passes only when:

1. instrument and standard identities are verified;
2. measuring surfaces and general condition are acceptable;
3. the caliper operates in inches and closes at 0.0000 in;
4. environmental conditions are acceptable under the environmental protocol;
5. `abs(E) <= 0.0005 in`;
6. the five-reading range is `<= 0.0005 in`; and
7. no unresolved abnormality exists.

No reading may be discarded or replaced because another value appears more
desirable.

A failed check remains in the research record. A new check may be attempted
only after the reason and any corrective action are documented.

The standalone pre-use check does not evaluate `D_limit`. That limit governs
the required pre-to-post comparison during later formal manual sessions.

## 9. Environmental and Temperature Treatment

The designated meter is Cole-Parmer 20250-91, serial 2605139793,
asset CP435995, under calibration report 1817067 dated 2026-08-10.

Report 1817067 verifies the meter using simulated thermocouple inputs. It does
not individually calibrate the Cole-Parmer 08519-54 Type-T surface probes.

Temperature observations therefore document equilibration and stability only.
The probes shall not be described as individually NIST calibrated. No
dimensional temperature correction or numerical environmental acceptance
limit is imposed.

Record the acclimation start time, check start and end times, room and
gauge-block surface temperatures before and after the five readings, meter and
probe identities, units, abnormalities, and notes. Questionable or unstable
conditions require `HOLD_FOR_REVIEW`.

## 10. Remaining Formal-Validation Gate

Passing this check establishes immediate reference-system readiness but does
not authorize formal specimen measurements. The remaining master-protocol
prerequisites must be closed before the first formal specimen observation.

## 11. Prospective Lock

This amendment and its limits shall be committed before the first pre-use
check reading. No formal specimen measurements had begun when these decisions
were made.
