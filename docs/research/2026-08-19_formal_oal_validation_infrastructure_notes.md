# CaseMetrology Formal OAL Validation Infrastructure Notes

**Date:** 2026-08-19
**Status:** Pre-measurement infrastructure; no formal validation data generated

This implementation package operationalizes the prospective formal OAL
validation protocols committed before formal measurement begins.

The package intentionally separates **templates** from future **official formal
data files**. Header-only templates are placed under
`data/oal_validation/templates/`. The frozen validation sample and formal run
orders are not created by package installation.

The selection implementation requires an explicit, prospectively declared
selection seed and a finalized allocation JSON. It does not define stratum
boundaries or allocation counts.

Manual and CV run-order generation use the prospectively declared seeds
`2026081901` and `2026081902`, respectively.

All deterministic selection/order operations use SHA-256 keyed ranking. The
algorithm is therefore reproducible from the input data, seed, and committed
script without dependence on library-specific random-number-generator state.

The audit script includes a `--self-test` mode that validates its structural
checks using temporary mock data. The self-test does not create or modify
formal validation records.
