# CaseMetrology Formal Measurement-Order and Randomization Protocol

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Status:** Prospective protocol; formal validation measurements have not begun
**Formal validation sample:** 60 uniquely identified specimens selected by the separately defined stratified-random-sampling procedure

## 1. Purpose

This protocol defines the order in which formal manual-reference and computer-vision (CV) OAL measurements will be obtained after the 60-specimen validation sample has been selected and frozen.

The protocol is intended to prevent systematic association between specimen identity, dimensional stratum, measurement order, repeated placement, operator familiarity, and time-dependent measurement-system effects.

The screening OAL measurements used to characterize the 235-specimen population shall not be used as formal reference measurements.

## 2. Prerequisites

Formal measurement shall not begin until:

1. screening of the study population is complete;
2. validation strata and allocation have been finalized;
3. the 60 validation specimens have been randomly selected;
4. the selected specimen list has been frozen and committed to the research record;
5. the manual reference caliper and its accredited calibration documentation have been received and accepted for the study; and
6. the frozen CaseMetrology measurement configuration remains unchanged.

No formal measurements obtained before these conditions are satisfied shall be incorporated into the validation dataset.

## 3. Measurement Modality Order

Formal measurements shall be conducted in two distinct phases:

1. **Manual reference measurement phase**
2. **Computer-vision validation measurement phase**

All formal manual-reference measurements shall be obtained independently of the previous screening measurements.

During subsequent CV acquisition, the operator shall not be provided with the formal manual-reference values or calculated reference means.

CV OAL results shall also be hidden during acquisition where practical so that an observed result cannot influence repositioning, recapture, or subsequent handling.

## 4. Three-Round Measurement Design

Both measurement modalities shall use a three-round design.

For each modality:

- each of the 60 selected specimens shall appear exactly once in each round;
- each specimen therefore receives three planned independent measurements or acquisitions;
- the specimen shall be completely removed from the measurement position and independently repositioned for every observation; and
- the order of the 60 specimens shall be randomized independently within each measurement round.

Therefore:

**Manual reference:** 60 specimens × 3 rounds = **180 planned manual readings**
**Computer vision:** 60 specimens × 3 rounds = **180 planned CV acquisition attempts**

The three observations for a specimen shall not intentionally be performed consecutively.

## 5. Randomization Procedure

All 60 selected specimen IDs shall first be placed into a canonical ascending-ID list.

The complete 60-specimen set shall then be randomized separately for each of three manual-reference rounds and three CV rounds.

Randomization shall occur across the complete validation sample. Specimens shall **not** be measured in blocks according to dimensional stratum.

Separate deterministic randomization sequences shall be used for manual-reference measurement and CV acquisition.

The following prospective seeds are declared before formal results exist:

- **Manual-reference randomization seed:** `2026081901`
- **CV randomization seed:** `2026081902`

The randomization script, Python version, seed values, generated run order, and Git commit identifying the script shall be retained as part of the research record.

The generated orders shall not be regenerated merely because an order appears inconvenient, unusual, or contains an undesirable sequence of specimens.

## 6. Prevention of Consecutive Repeats

A specimen appearing last in one measurement round shall not also be measured first in the following round.

If the deterministic shuffle produces this condition, the predefined randomization script shall exchange the first and second positions of the new round.

This rule shall be implemented programmatically and prospectively rather than through operator discretion.

No other manual rearrangement of the randomized sequence shall be permitted.

## 7. Manual Reference Measurement Order

The operator shall follow the generated manual run-order record.

Each manual measurement shall consist of:

1. verification of the laser-etched specimen `part_id`;
2. placement of the specimen in the manual measurement system;
3. one independent OAL measurement;
4. recording of the reading;
5. complete removal of the specimen; and
6. progression to the next specimen in the predetermined randomized sequence.

Previous screening measurements shall not be consulted during formal measurement.

Where practical, previously recorded formal readings and calculated specimen means shall not be displayed to the operator during subsequent measurement rounds.

The formal reference mean shall be calculated from the three formal manual measurements and **not** from the screening value.

## 8. Computer-Vision Measurement Order

After completion of the manual-reference phase, CV acquisition shall follow its own independently generated randomized run order.

For each scheduled CV acquisition:

1. verify the specimen `part_id`;
2. place the specimen according to the frozen CaseMetrology measurement procedure;
3. initiate one independent image acquisition and measurement attempt;
4. completely remove the specimen from the measurement fixture; and
5. proceed to the next scheduled specimen.

Each specimen receives exactly three planned independent CV acquisition attempts, one during each CV round.

No acquisition shall be repeated because the reported OAL appears unexpected, inaccurate, out of specification, or inconsistent with another reading.

A valid measurement-pipeline failure is a result of the system under test and **shall count as a formal acquisition attempt rather than being retried**.

## 9. Protocol-Invalid Events

An observation may be classified as protocol-invalid only when the planned measurement was not actually executed according to the formal procedure.

Examples include:

- incorrect specimen placed or recorded;
- acquisition associated with the wrong `part_id`;
- accidental interruption before measurement completion;
- corrupted or missing acquisition file caused by an external recording/storage failure;
- documented operator or equipment event that prevented the intended measurement from occurring.

An unexpected measurement value is **not** grounds for invalidation.

For CV measurements, segmentation, detection, quality-gate, or other measurement-pipeline failures are not protocol-invalid merely because no valid OAL value was produced.

Any protocol-invalid event shall remain in the audit record with its original run-order position and reason for invalidation.

When a replacement observation is authorized, it shall be appended to the end of the applicable measurement round rather than inserted into or used to alter the predetermined randomized sequence.

## 10. Interruptions and Session Boundaries

If a measurement session must stop before completion of a round, the randomized order shall remain frozen.

At resumption, measurement shall continue with the next uncompleted run-order position.

The remaining specimens shall not be reshuffled.

Session identifiers, dates, times, reference checks, and documented interruptions shall provide traceability for measurements spanning multiple sessions.

## 11. Required Run-Order Record

The formal run-order record shall preserve, at minimum:

- measurement modality;
- round number;
- planned sequence number;
- `part_id`;
- selection stratum;
- randomization seed;
- actual measurement/acquisition status;
- session identifier;
- measurement timestamp;
- valid/invalid status;
- failure or invalidation classification, when applicable; and
- notes required for auditability.

The original generated run-order files shall be preserved unchanged.

## 12. Protocol Lock

Once generated and committed, the formal measurement orders shall be considered part of the frozen validation protocol.

Changes to specimen sequence, repeat count, randomization method, or handling rules after formal measurement begins shall require explicit documentation as a protocol deviation and shall not be made on the basis of observed measurement results.
