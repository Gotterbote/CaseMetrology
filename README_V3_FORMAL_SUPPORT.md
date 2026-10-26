# V3 Formal Support Package (Historical)

> This document records the pre-acquisition support-package instructions. V3 formal acquisition and analysis were completed in September 2026. Begin with the [thesis defense evidence guide](docs/research/THESIS_DEFENSE_START_HERE.md) for the completed study. The instructions below are retained as a historical record.

This package adds the capture-only V3 formal acquisition implementation.

## Install

From the CaseMetrology repository root, copy the package contents into the repo
while preserving paths.

The files added are:

- scripts/v3_freeze_common.py
- scripts/capture_v3_formal_blank.py
- scripts/run_v3_formal_capture.py
- scripts/analyze_v3_formal_images.py
- scripts/finalize_v3_formal_freeze.py
- docs/research/v3_formal_validation/V3_ACQUISITION_AND_ANALYSIS_IMPLEMENTATION.md

Historical instruction before formal acquisition:

> Do not run a formal capture yet.

First commit this support package together with the already generated V3
prospective plan/run-order files. Then run `scripts/finalize_v3_formal_freeze.py`
from the clean committed state and commit the generated freeze evidence.
