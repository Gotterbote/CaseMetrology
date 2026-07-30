# CaseMetrology Research Data Retention Policy

## Purpose

This policy defines how source code, documentation, raw research data, derived
outputs, and accepted milestone evidence are preserved.

## Repository principle

Git is the authoritative record for:

- Source code and configuration
- Protocols and runbooks
- Research summaries and accepted-result documents
- Small milestone datasets that materially support reproducibility
- Analysis reports, representative diagnostics, and evidence manifests

Git is not intended to be the only storage location for every raw image or
large experimental dataset.

## Data classifications

### Routine setup material

Temporary screenshots, installation output, connectivity checks, disposable
focus images, and transient logs may remain local unless they explain a
material system decision.

### Exploratory research data

Preserve exploratory data when they document a meaningful lesson, failure
mode, or design decision.

Requirements:

- Clearly label them exploratory
- Do not present them as accepted validation evidence
- Preserve original files
- Add a disposition record rather than rewriting the original record

### Official accepted milestone evidence

Preserve:

- Original acquisition metadata
- Hashes or evidence manifests
- Exact analysis method and source commit
- Numerical results
- Diagnostic review
- Acceptance decision
- Limitations

Small accepted datasets may be committed when they materially improve
reproducibility or portfolio review.

### Large raw datasets

Store large datasets outside normal Git history unless specifically approved.

Preserve in Git:

- Session metadata
- Evidence manifest
- Storage-location record
- Analysis method
- Git commit reference
- Accepted summary

Maintain at least one separate backup.

### Proprietary or sensitive data

Do not publish proprietary production data without authorization.

Use sanitized or representative examples for a public portfolio while
preserving the complete private research record.

## Required traceability for official sessions

Preserve, when applicable:

- Session ID
- Date and operator
- Research objective
- Preflight result and log path
- Camera and acquisition configuration
- Environmental observation and instrument classification
- Git commit and working-tree state
- Raw-data paths and hashes
- Analysis method and source commit
- Numerical results
- Diagnostic disposition
- Acceptance or rejection decision
- Limitations and deviations

## Backup principle

Accepted research evidence shall not exist in only one physical location.

Recommended locations:

1. Jetson or primary research computer
2. GitHub for committed code and milestone evidence
3. Separate backup for large or excluded datasets

## Modification principle

Original raw data and acquisition metadata shall not be silently altered.

Corrections shall use:

- Addenda
- Disposition records
- Superseding analyses
- New commits
- Explicit documentation of what changed and why
