# Formal OAL CV Storage

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
