# Formal OAL CV Storage

> Historical storage convention recorded before acquisition. Formal acquisition is complete; V3 records are under [`../v3_formal/`](../v3_formal/). See the [current evidence guide](../../../docs/research/THESIS_DEFENSE_START_HERE.md).

Formal CV sessions use sequential IDs:

`CV-S001`, `CV-S002`, `CV-S003`, ...

Each new continuous CV acquisition session receives the next unused ID.
Session IDs shall not be reused or renumbered.

Artifact storage:

- raw images: `raw/`
- masks: `masks/`
- diagnostics: `diagnostics/`

The immutable `cv_run_id` is the file stem.

Examples:

- raw: `CV-R1-001.png`
- mask: `CV-R1-001_mask.png`
- diagnostic: `CV-R1-001_diagnostic.png`

The corresponding repository-relative paths are recorded in
`cv_observations.csv`.

No formal CV data have been collected at creation of this record.
