# CaseMetrology Formal OAL Validation Infrastructure

This package contains **pre-measurement infrastructure only**. It does not
contain formal validation observations and does not generate an official
validation sample unless the selection script is deliberately executed with
the finalized screening population, allocation file, and declared selection
seed.

## Included templates

Header-only templates are under:

`data/oal_validation/templates/`

They are intentionally separate from the future official files in
`data/oal_validation/`.

Included templates:

- `validation_selection_input.csv`
- `manual_reference_observations.csv`
- `manual_reference_checks.csv`
- `manual_sessions.csv`
- `environmental_observations.csv`
- `cv_observations.csv`
- `protocol_deviations.csv`

## Included scripts

- `scripts/generate_oal_validation_sample.py`
- `scripts/generate_oal_manual_run_order.py`
- `scripts/generate_oal_cv_run_order.py`
- `scripts/audit_oal_validation_data.py`

The official validation sample must **not** be generated until:

1. screening is complete;
2. selection strata and allocations are frozen;
3. prevalidation specimen exclusions are finalized;
4. a selection seed is prospectively declared;
5. the selection script is committed.

The manual and CV run-order scripts use the already prospectively declared
seeds:

- manual: `2026081901`
- CV: `2026081902`

## Selection allocation

`config/oal_validation/selection_allocation.template.json` deliberately
contains `null` values. Replace them only after the final allocation has been
decided and documented. Allocation values must be nonnegative integers and
must sum to 60.

The `selection_stratum` labels in the screening input must exactly match the
keys used in the finalized allocation JSON.

## Deterministic randomization

The selection and run-order scripts use SHA-256 ranking keyed by the declared
seed, operation, round/stratum, and `part_id`. This provides deterministic
pseudo-random ordering without depending on NumPy or Python's PRNG state.

## Safe verification now

The audit script can be tested without formal data:

```bash
python scripts/audit_oal_validation_data.py --self-test
```

Expected ending:

```text
SELF-TEST PASS
```

## Formal outputs later

After the formal sample is legitimately frozen, the intended output paths are:

- `data/oal_validation/formal_validation_specimens.csv`
- `data/oal_validation/manual_run_order.csv`
- `data/oal_validation/cv_run_order.csv`

Do not create those official outputs merely to test the scripts. Use temporary
or mock paths for tests.
