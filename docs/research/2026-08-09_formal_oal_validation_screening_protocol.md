# Formal OAL Validation Screening Protocol

**Project:** CaseMetrology  
**Research phase:** Formal OAL validation  
**Measurement characteristic:** Cartridge-case overall length (OAL)  
**Population:** 235 uniquely laser-etched cases  
**Part identifiers:** 1 through 235  
**Specification:** 1.000 +/- 0.010 inch  
**LSL:** 0.990 inch  
**USL:** 1.010 inch  
**Calibration freeze commit:** `300c696`  
**Protocol status:** Prospective screening protocol  
**Validation status:** No official CV validation measurements authorized by this protocol

## 1. Purpose

This protocol defines the screening procedure used to characterize the
available 235-case population before formal OAL validation specimen selection.

Screening measurements are used only to:

1. characterize the available OAL distribution;
2. identify the available coverage of the specification region;
3. identify naturally occurring below-LSL and above-USL specimens;
4. support stratified random selection of the formal validation sample.

Screening measurements are not official physical ground-truth measurements
and shall not be substituted for the later formal manual reference
measurements.

## 2. Specimen identification

Each physical case is permanently identified by its existing laser-etched
integer identifier from 1 through 235.

The etched identifier shall be recorded exactly as `part_id`.

No new specimen numbering or relabeling scheme shall be introduced.

Cases may be screened in any order. Sequential part-ID order is not required.

## 3. Screening measurement

Each case shall receive one screening OAL measurement using the established
manual caliper procedure.

For each screening measurement, record at minimum:

- `part_id`;
- screening OAL in inches;
- screening date;
- screening time;
- operator;
- screening session identifier;
- any physical or measurement note requiring later review.

The recorded screening value shall be preserved as originally observed.
Values shall not be altered to improve apparent population distribution.

## 4. Screening sessions

Screening may occur across multiple sessions.

Each session shall have a unique session identifier and shall record:

- session date;
- operator;
- pre-session reference checks;
- post-session reference checks;
- relevant instrument or procedural observations.

Because specimens may be measured in arbitrary order, a screening session
shall not be defined by a sequential part-ID range.

The cases measured during a session are determined from their recorded
session identifier.

## 5. Reference checks

Reference checks are screening-session controls and do not convert the
screening measurements into formal validation ground truth.

Pre-session and post-session reference readings shall be retained in their
original form.

Any questionable session shall be flagged for review rather than silently
corrected or deleted.

The formal acceptance status of the reference caliper for official validation
will be determined separately after review of its calibration certificate.

## 6. Development-validation separation

Screening data may be examined to determine the physical OAL distribution and
to define appropriate sampling strata.

Screening data shall not be used to:

- modify the frozen computer-vision estimator;
- modify segmentation parameters;
- modify endpoint logic;
- modify the frozen OAL calibration;
- establish a bias correction;
- tune a guard band based on CV performance;
- discard specimens because their later CV results are unfavorable.

No official computer-vision validation result shall be examined when defining
the validation sample.

## 7. Screening completion checks

Before the population is considered completely screened:

1. each `part_id` from 1 through 235 shall have exactly one complete screening
   record;
2. no duplicate `part_id` shall remain unresolved;
3. no expected `part_id` shall be missing;
4. numeric OAL entries shall be checked for obvious transcription errors;
5. flagged records shall be reviewed without silently replacing original
   observations;
6. all screening sessions shall have traceable session-control records.

A corrected transcription shall preserve documentation of the original entry
and reason for correction.

## 8. Population characterization

After screening is complete, calculate and preserve:

- count;
- mean;
- median;
- standard deviation;
- minimum;
- maximum;
- range;
- quartiles;
- number below 0.990 inch;
- number from 0.990 through 1.010 inch;
- number above 1.010 inch;
- histogram of screening OAL;
- ordered OAL distribution by `part_id` and by measured OAL.

These results describe the available specimen population and are not CV
validation results.

## 9. Stratification and formal sample selection

Exact validation strata shall be finalized only after the complete screening
distribution has been reviewed.

The intended structure is:

1. below LSL;
2. near-LSL in specification;
3. central or nominal region;
4. near-USL in specification;
5. above USL.

The target formal validation sample is 60 unique cases, subject to adequate
population coverage.

Selection within each final stratum shall be random.

The selection procedure shall preserve:

- final stratum definitions;
- eligible `part_id` values in each stratum;
- requested sample count by stratum;
- random-number-generator method;
- random seed;
- selected validation IDs;
- reserve IDs;
- date of selection;
- code or script version used for selection.

The selected validation sample shall be frozen and committed before official
manual reference or CV validation measurements are collected.

## 10. Formal reference measurements

After specimen selection and authorization of the calibrated reference
instrument, every selected validation specimen shall receive a separate set of
formal manual reference measurements.

Those measurements shall consist of at least three independent readings with
complete removal and repositioning between readings.

The formal reference mean shall be calculated from those readings.

The earlier screening value shall not be included in the formal reference
mean.

## 11. Current authorization

This protocol authorizes continuation of population screening and screening
data-quality review.

It does not authorize official manual reference measurements using an
uncertified or unreviewed reference instrument.

It does not authorize modification of the frozen computer-vision estimator or
calibration.

It does not authorize official computer-vision validation acquisition until
the complete validation stop/go gate has passed.
