---
title: Fixtureless OAL Method Decision Log
project: CaseMetrology
researcher: Timmy Bell
status: Living document
last_updated: 2026-07-31
---

# Fixtureless OAL Method Decision Log

This file records major research and implementation decisions. It is not a chronological terminal log. Each entry identifies the decision, evidence basis, alternatives, limitations, and status.

---

## OAL-D001 — Preserve the PCA estimator as an unchanged comparator

- **Date:** 2026-07-31
- **Decision:** Develop candidate estimators in separate modules and leave `src/measurement/topdown_oal.py` unchanged.
- **Rationale:** A stable comparator is required to attribute differences to endpoint estimation rather than simultaneous changes to segmentation or public interfaces.
- **Alternatives considered:** Replace the existing function in place.
- **Evidence:** Trial 03 and Trial 05 baseline results at repository snapshot `cb3bf01`.
- **Status:** Active.

## OAL-D002 — Reuse accepted masks and images before collecting new data

- **Date:** 2026-07-31
- **Decision:** Evaluate new estimators on the existing 10 Trial 03 and 17 Trial 05 records before additional physical acquisition.
- **Rationale:** Paired reuse isolates estimator behavior, avoids introducing reacquisition variability, and conserves research effort.
- **Limitations:** Reuse cannot establish generalizability to new cases, positions, or imaging conditions.
- **Status:** Completed for binary geometry and first grayscale subpixel estimator.

## OAL-D003 — Disable the fixture-width gate for accepted-mask endpoint comparisons

- **Date:** 2026-07-31
- **Decision:** Set `minimum_fixture_width_ratio = 0.0` only in comparison scripts processing previously accepted masks.
- **Rationale:** Object/fixture acceptance had already occurred; retaining the gate caused all 27 records to fail before estimator evaluation and confounded the intended endpoint-only comparison.
- **Safeguard:** The production/default estimator parameter remains unchanged.
- **Status:** Active for accepted-mask retrospective comparisons only.

## OAL-D004 — Retain the 90° sensitivity candidate

- **Date:** 2026-07-31
- **Decision:** Retain the algorithmically identified 90° sensitivity capture in primary statistics and report it rather than automatically excluding it.
- **Rationale:** Excluding a difficult capture after observing its effect would bias the comparison.
- **Evidence:** Binary comparison identified `capture_02_mask` as the largest absolute deviation from the 90° median.
- **Status:** Active.

## OAL-D005 — Classify binary geometry as exploratory

- **Date:** 2026-07-31
- **Decision:** Do not replace the PCA baseline with the binary-geometry estimator.
- **Evidence:** Static SD improved 48.54%, but Trial 05 orientation-group median range increased 28.36% from `1.752720470 px` to `2.249772382 px`.
- **Visual evidence:** No widespread gross fit failure; likely orientation-dependent rasterization remained.
- **Status:** Final for estimator version represented by commit `8bb3a9f` and comparison evidence commit `e690127`.

## OAL-D006 — Investigate grayscale subpixel localization

- **Date:** 2026-07-31
- **Decision:** Develop a grayscale edge estimator initialized from accepted-mask geometry.
- **Rationale:** Binary line fitting remained sensitive to integer-grid boundaries.
- **Implementation:** Commit `4dca7b1`.
- **Status:** Completed for maximum-gradient version.

## OAL-D007 — Classify maximum-gradient subpixel geometry as exploratory

- **Date:** 2026-07-31
- **Decision:** Do not replace the PCA baseline with the first grayscale subpixel estimator.
- **Evidence:** Trial 05 orientation-group median range increased 64.75% to `2.887565849 px`; Trial 05 SD increased 69.54%.
- **Visual evidence:** The strongest local gradient did not consistently represent the same physical edge across orientation, especially at 70° and 90°.
- **Status:** Final for the version represented by commit `4dca7b1`.

## OAL-D008 — Retain PCA as the provisional working baseline

- **Date:** 2026-07-31
- **Decision:** Continue using PCA plus extreme mask pixels as the comparator, not as a declared final metrology solution.
- **Rationale:** It produced the smallest range among Trial 05 orientation-group medians of the three evaluated methods.
- **Limitation:** It still exhibits `1.752720470 px` orientation dependence and has not been validated for absolute accuracy.
- **Status:** Provisional.

## OAL-D009 — Define the next edge physically, not only numerically

- **Date:** 2026-07-31
- **Decision:** Develop a mask-anchored, polarity-aware normalized intensity-crossing estimator.
- **Required behavior:** Use local interior/exterior plateaus, a consistent crossing criterion, and rejection of ambiguous multi-transition profiles.
- **Rationale:** Subpixel resolution without a consistent edge definition increased orientation bias.
- **Status:** Planned.

## OAL-D010 — Defer additional physical acquisition

- **Date:** 2026-07-31
- **Decision:** Do not collect new OAL images until the next estimator has been compared on the existing 27 records.
- **Rationale:** The current unresolved issue is algorithmic edge definition; additional data would not isolate that cause.
- **Status:** Active.
