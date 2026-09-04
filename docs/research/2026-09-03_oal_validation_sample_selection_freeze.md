# OAL Validation Sample Selection Freeze

Date: 2026-09-03  
Operator: Timmy D. Bell  
Scope: M.S. thesis formal validation, OAL only.

The completed 235-case screening population is the source population for formal validation sample selection.

Five prevalidation specimens are excluded from eligibility and are physically segregated:
187, 121, 178, 146, 197.

Selection strata and allocations:

| Stratum | Screening OAL boundary (in) | Eligible | Select |
|---|---:|---:|---:|
| below_lsl | L < 0.9900 | 10 | 8 |
| near_lsl_in_spec | 0.9900 <= L <= 0.9950 | 34 | 14 |
| central_nominal | 0.9950 < L < 1.0050 | 137 | 16 |
| near_usl_in_spec | 1.0050 <= L <= 1.0100 | 24 | 14 |
| above_usl | L > 1.0100 | 25 | 8 |

Total eligible: 230  
Formal validation sample: 60

Sampling is intentionally stratified and not population-proportional.

Official selection seed: `2026090301`

Within each stratum, specimens are ranked using:

`SHA256("CaseMetrology|selection|<seed>|<stratum>|<part_id>")`

The allocated number of highest-ranked eligible specimens forms the formal sample.

Reserve specimens are the next two unselected SHA-ranked eligible specimens in each stratum. Reserves are replacements only and are not additional routine validation measurements.

The selection input, allocation, seed, boundaries, exclusion rule, and reserve rule are frozen before the official selection is generated. No formal manual-reference or computer-vision validation measurements are authorized by this freeze record.
