# OAL Case Screening Randomization Record

**Date:** 2026-07-31  
**Status:** Prospective screening-order record  
**Screening population:** 235 laser-etched cases  
**Part identifiers:** Sequential integers 1 through 235  
**Randomization seed:** `20260731`  
**Reference caliper serial number:** `B24254849`

## Purpose

This record establishes the case-screening order before any official
screening measurements are collected. Randomizing the case order reduces
the risk that time-dependent effects, operator learning, temperature drift,
or instrument drift become confounded with part identifier or case length.

## Identification control

The existing laser-etched number will be preserved exactly as the specimen
`part_id`. Cases will not be renumbered.

## Randomization method

The 235 identifiers were randomized using Python
`random.Random(20260731).shuffle`.

The fixed random seed makes the order independently reproducible.

## First 20 scheduled case identifiers

`120, 134, 159, 79, 106, 185, 73, 166, 81, 107, 209, 89, 36, 50, 42, 154, 195, 19, 224, 110`

The complete order is stored in:

- `templates/oal_case_screening_run_sheet.csv`
- `config/oal_case_screening_run_order.json`

## Integrity record

Run-sheet SHA-256:

`22e0ae9463a3b70abd01c293467abfaead8bf9272306d0411bc1639ab6ce66d5`

## Measurement status

No screening measurements have been entered. Official measurements remain
on hold pending review and acceptance of the caliper calibration result.
