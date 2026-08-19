# CaseMetrology Formal Manual-Reference Measurement Protocol

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Measurement modality:** Manual reference measurement
**Designated operator:** Timmy D. Bell
**Status:** Prospective protocol; formal validation measurements have not begun

## 1. Purpose

This protocol defines the procedure for obtaining the formal manual-reference OAL measurements against which the frozen CaseMetrology computer-vision measurement system will subsequently be evaluated.

The manual-reference dataset shall be generated independently from all preliminary screening measurements and shall provide the formal specimen-level reference values used in the validation analysis.

## 2. Reference Instrument

The designated manual-reference instrument is:

- **Manufacturer:** Mitutoyo
- **Instrument:** Digimatic Caliper
- **Model:** CD-8"ASX
- **Code:** 500-197-30
- **Serial number:** B23090910
- **Display resolution:** 0.0005 in / 0.01 mm
- **Measurement units used for study:** inches

The instrument's accredited calibration certificate shall be reviewed and accepted before formal reference measurements begin.

The certificate review shall verify, at minimum:

- agreement between the certificate and instrument serial number;
- calibration date;
- calibration laboratory and accreditation information;
- calibration status and interval, where stated;
- as-found measurement results;
- as-left measurement results, if applicable;
- whether adjustment or repair occurred;
- reported measurement uncertainty;
- measurement results at or sufficiently near the approximately 1.000-in study region; and
- any limitations, qualifications, or conditions stated on the certificate.

**Pending protocol item:** The treatment of any calibration correction or documented indication error shall be determined only after the actual calibration certificate has been reviewed.

No calibration correction shall be retrospectively selected on the basis of validation results.

## 3. Formal Reference Measurements Are Independent of Screening

The preliminary screening measurement associated with a specimen shall **not** constitute one of its formal reference measurements.

Each selected validation specimen shall receive three new formal manual-reference measurements after the formal validation protocol is frozen.

For specimen \(i\), the formal readings are:

\[
M_{i1},\ M_{i2},\ M_{i3}
\]

The screening measurement shall not be included in the formal reference calculation.

## 4. Operator Control

All primary formal manual-reference measurements shall be performed by **Timmy D. Bell**.

This is a single-operator reference-measurement study. Any substitution of another operator after formal data collection begins shall be documented as a protocol deviation.

A future multi-operator reproducibility or Gage R&R study, if performed, shall be treated as a separate experiment.

## 5. Measurement-Round Structure

The manual-reference measurements shall follow the frozen three-round randomized measurement-order protocol.

Each of the 60 validation specimens shall receive:

- one measurement during Manual Round 1;
- one measurement during Manual Round 2; and
- one measurement during Manual Round 3.

Each round shall contain all 60 specimens exactly once.

The specimen shall be completely removed from the caliper after every formal measurement.

## 6. Blinding of Previous Measurements

During acquisition of a formal manual reading, the operator shall not consult:

- the specimen's screening OAL;
- previous formal manual readings for that specimen;
- the running mean of the specimen;
- dimensional stratum information; or
- subsequent CV results.

Previously entered measurements shall be hidden where practical.

## 7. Instrument Preparation

Before the beginning of a formal manual-measurement session:

1. verify that the caliper is serial number B23090910;
2. verify accepted calibration status;
3. inspect the external measuring jaws;
4. clean measuring surfaces when necessary;
5. gently close the jaws;
6. verify the expected closed-jaw indication;
7. verify operation in inches; and
8. complete the required pre-session reference-standard checks.

The instrument shall not be adjusted to force the reference-standard result to its nominal value.

## 8. Pre-Session Reference Check

Before specimen measurements begin, the designated reference standard shall be measured **five times**.

Each reading shall include complete removal and repositioning of the standard.

The five individual readings shall be retained along with the calculated mean, minimum, maximum, and range.

The final numerical acceptance criterion remains **PENDING CERTIFICATE REVIEW**.

If the pre-session check fails the frozen acceptance criterion, formal specimen measurements shall not begin.

## 9. Individual Specimen Measurement Procedure

For each run-order position:

1. identify the scheduled specimen;
2. verify the laser-etched `part_id`;
3. visually inspect relevant measurement surfaces for obvious foreign material;
4. place the case lengthwise between the external caliper faces;
5. establish axial OAL contact between base/head and mouth;
6. maintain a consistent measurement orientation;
7. use only sufficient force to establish gentle contact;
8. allow the displayed reading to stabilize;
9. record the displayed value exactly;
10. do not round, interpolate, or add digits;
11. completely remove the specimen; and
12. proceed to the next scheduled specimen.

The operator shall not repeatedly rock, sweep, rotate, or remeasure a specimen for the purpose of obtaining a preferred value.

## 10. Unexpected Measurements

A measurement shall not be repeated merely because it:

- differs from screening;
- differs from a prior formal reading;
- appears unusually short or long;
- falls outside nominal specification; or
- may later disagree with the CV result.

Such observations are legitimate experimental data unless a documented procedural error occurred.

## 11. Protocol-Invalid Manual Measurements

A measurement may be classified as protocol-invalid only when the intended measurement was not properly executed.

Examples include:

- wrong specimen measured;
- incorrect `part_id` entered;
- specimen displaced before completion;
- contamination discovered during the observation;
- instrument malfunction;
- unrecoverable data-entry failure;
- confirmed incorrect transcription.

The original observation shall not be silently deleted or overwritten.

## 12. Post-Session Reference Check

At completion of each formal manual-measurement session, the designated reference standard shall again be measured **five times** using complete removal and repositioning.

The five readings, mean, minimum, maximum, and range shall be retained.

A failed post-session check shall place the session on `HOLD_FOR_REVIEW` rather than automatically delete the specimen measurements.

## 13. Session Interruptions

If the session is interrupted:

- completed observations remain valid unless evidence indicates otherwise;
- the randomized run order shall not be regenerated;
- measurement shall resume with the next uncompleted run-order position;
- a new session shall receive a new unique `session_id` and required pre-session checks.

## 14. Environmental Records

Environmental and reference-standard temperature monitoring shall follow the separately frozen environmental-control protocol.

No temperature correction shall be introduced retrospectively unless prospectively defined before formal results are examined.

## 15. Required Measurement Record

Each formal manual observation shall preserve, at minimum:

- `part_id`;
- laser-etched-ID verification status;
- manual round;
- planned sequence;
- `reading_in`;
- date;
- time;
- operator;
- caliper manufacturer/model/code/serial;
- `session_id`;
- validity status;
- protocol-invalid status and reason, if applicable;
- replacement linkage, if applicable; and
- notes.

## 16. Formal Reference Value

After completion and acceptance of the three formal manual observations for specimen \(i\), the uncorrected arithmetic mean shall initially be:

\[
\bar{M_i}=\frac{M_{i1}+M_{i2}+M_{i3}}{3}
\]

The individual readings shall remain the primary raw observations.

The final metrologically qualified reference value may incorporate only a prospectively justified calibration correction determined from certificate review.

## 17. Data Preservation

No raw observation shall be silently deleted, replaced by an average, edited to agree with another observation, or excluded because it disagrees with CV.

Corrections to transcription errors shall preserve the original entry and an auditable correction record.

## 18. Protocol Lock

Before the first formal specimen measurement, the following shall be resolved and frozen:

1. acceptance of the accredited caliper certificate;
2. designated reference-standard identity and certificate;
3. numerical pre-session criterion;
4. numerical post-session criterion;
5. calibration-correction policy;
6. applicable environmental requirements; and
7. final manual-reference data schema.
