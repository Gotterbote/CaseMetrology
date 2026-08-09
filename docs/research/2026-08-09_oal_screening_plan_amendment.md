# OAL Screening Plan Amendment

**Project:** CaseMetrology
**Date:** 2026-08-09
**Status:** Prospective amendment before formal population screening
**Governing screening protocol:** `docs/research/2026-08-09_formal_oal_validation_screening_protocol.md`
**Protocol commit:** `5f8b92c`
**Calibration freeze commit:** `300c696`

## 1. Purpose

This amendment reconciles the earlier July 31 OAL screening and validation
sample-planning records with the formal screening protocol established on
2026-08-09.

The earlier records are retained unchanged as historical prospective planning
evidence. This amendment documents which provisions were superseded before
formal screening data collection.

## 2. Screening order

The July 31 screening-order record established a reproducible randomized order
for part identifiers 1 through 235.

That fixed-order requirement is superseded.

Practical screening may occur in any specimen order because the physical cases
are not expected to be presented in the previously randomized sequence.

Each specimen remains uniquely traceable through its permanent laser-etched
`part_id`, and each screening record shall include its session identifier,
date, time, and operator.

The previously generated randomized order, seed, run sheet, JSON configuration,
and SHA-256 record shall be retained as historical planning evidence and shall
not be deleted or rewritten.

## 3. Calibration-certificate dependency

The July 31 plan stated that screening would begin only after calibration
testing of the Mitutoyo reference caliper.

That restriction is superseded for population screening only.

Population screening is permitted before formal calibration-certificate
acceptance because screening measurements are used exclusively to characterize
the available specimen distribution and support stratified sample selection.

Screening measurements are not official ground-truth measurements.

Official manual reference measurements remain prohibited until the reference
instrument calibration certificate has been reviewed and the instrument has
been formally authorized for validation use.

## 4. Validation sample size

The July 31 sample-design record established:

- minimum sample: 30 unique cases;
- preferred sample: 40 unique cases.

The formal screening protocol now establishes a target of 60 unique validation
cases, subject to adequate coverage of the observed screening population.

The 60-case target does not require artificial creation of unavailable strata
and shall not justify exclusion or alteration of inconvenient observations.

The exact stratum boundaries and allocation counts will be finalized only
after all 235 screening records have been reviewed.

## 5. Unchanged controls

The following July 31 controls remain in force:

- existing laser-etched identifiers remain the permanent `part_id`;
- all 235 available cases are intended for population screening;
- screening values are not formal reference values;
- validation selection occurs only after the complete screening distribution
  is known;
- cases shall not be excluded because their lengths are inconvenient;
- gaps in available specification-region coverage shall be reported;
- remaining cases shall serve as a reserve population;
- formal CV validation images shall be newly acquired after sample selection;
- the frozen estimator and calibration shall not be modified using validation
  data.

## 6. Research disposition

The July 31 randomized run-order files remain preserved as historical
prospective records but are not the governing physical screening sequence.

Beginning with commit `5f8b92c`, the governing screening method is the formal
2026-08-09 screening protocol together with this amendment.

No screening result was used to create this amendment.
