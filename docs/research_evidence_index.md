# CaseMetrology Research Evidence Index

> **Historical index:** This index preserves early development and planning. V1–V3 formal evaluation is complete. Use the [thesis defense evidence guide](research/THESIS_DEFENSE_START_HERE.md) for current results and interpretation boundaries.

## Purpose

This index links each material research finding to its status, supporting
evidence, limitations, and Git traceability.

## Status definitions

- **Development baseline:** establishes system capability but is not calibrated
  research evidence
- **Exploratory:** retained for development or failure-mode learning
- **Preliminary:** controlled evidence with narrowly defined limitations
- **Accepted:** reviewed evidence supporting the stated conclusion
- **Planned:** future work not yet executed

---

## E-001 — Baseline camera acquisition

**Status:** Development baseline

The Arducam B0499 produced full-resolution OpenCV images at:

- 1456 x 1088 pixels
- YUYV
- Reported 44 frames per second

**Use:** Establishes initial camera-acquisition capability and configuration
history.

**Limitation:** Not calibrated dimensional evidence.

**Representative evidence:**

- `docs/camera_baseline_controls.txt`
- `src/acquisition/capture_baseline.py`
- `raw_images/baseline/`
- `measurements/baseline/`

---

## E-002 — Persistent camera identity

**Status:** Accepted system configuration

The acquisition system uses:

- `/dev/case-metrology-camera`

rather than relying on a changing `/dev/video#` assignment.

**Use:** Improves acquisition reliability and reproducibility.

**Known Git commit:**

- `e238a94`

---

## E-003 — Preliminary Lexan optical comparison

**Status:** Preliminary

**Research question:**

Did installation of the Lexan fixture materially alter illumination within the
selected unobstructed central ROI?

**Results:**

- Mean grayscale without Lexan: 225.1456
- Mean grayscale with Lexan: 225.0625
- Mean change: -0.0831
- Percent change: -0.0369%
- Mean absolute pixel difference: 0.8864
- RMSE: 1.2830
- 95th-percentile absolute difference: 3.0000

**Defensible conclusion:**

The Lexan did not produce a practically meaningful change in mean illumination
within the selected unobstructed central ROI under the tested conditions.

**Limitations:**

- One paired comparison
- Central ROI only
- Optical repeatability not established
- Full-field optical neutrality not established
- Both final measurement-edge regions were not directly evaluated
- Comparison occurred before the formal research preflight
- Temperature was not measured using a traceable instrument

**Evidence:**

- `data/lexan_test/`
- `docs/research_session_summary_2026-07-28.md`

**Git commit:**

- `3c11993` — Document Lexan optical comparison test

---

## E-004 — Trial 01 orientation-error dataset

**Status:** Exploratory

**Session ID:**

- `lexan_gauge_block_repositioning_trial_01_20260728_182212`

**Finding:**

Ten removal-and-replacement cycles were completed with stable camera controls
and valid file integrity, but the gauge block was rotated approximately
90 degrees from the approved certified orientation.

**Permitted use:**

- Mechanical seating exploration
- Operator-placement consistency
- Image-acquisition stability
- Pixel-level positional and edge-repeatability exploration

**Prohibited use:**

- Official certified gauge-block calibration
- Absolute dimensional accuracy
- Final Lexan-fixture acceptance
- Inch-based results using the one-inch vertical reference

**Evidence:**

- `data/fixture_repositioning/2026-07-28_trial_01/00_trial_disposition.txt`
- `data/fixture_repositioning/2026-07-28_trial_01/01_trial_integrity_manifest.sha256`

**Git commit:**

- `edac004` — Preserve orientation-error exploratory repositioning trial

---

## E-005 — Corrected Trial 02 orientation verification

**Status:** Accepted acquisition gate

**Session ID:**

- `trial_02_corrected_orientation_verification_20260728_200026`

**Verified condition:**

- Certified 1.0000024-inch dimension vertical
- Approximately 1.375-inch dimension horizontal
- Gauge block visually wider than tall
- Diagnostic edges followed the intended gauge-block surfaces
- Lexan boundaries did not control the fitted measurement edges

**Key diagnostic values:**

- Mean fitted span: 523.068111 pixels
- Preliminary scale: 523.066855 pixels per inch
- Preliminary resolution: 0.001911802 inches per pixel

**Limitation:**

This verification did not independently establish repeatability or absolute
accuracy.

**Evidence:**

- `docs/trial_02_orientation_verification_2026-07-28.txt`

**Git commit:**

- `2895471` — Verify corrected gauge-block orientation for Trial 02

---

## E-006 — Repositioning-session integrity method

**Status:** Accepted assurance method

A reusable version-controlled verifier checks:

- Requested and completed cycle counts
- Unique and sequential records
- Camera-control consistency
- Image readability
- Image dimensions
- File sizes
- SHA-256 hashes
- Method traceability
- Repository state

**Limitation:**

An integrity PASS does not establish:

- Correct physical orientation
- Correct seating
- Optical validity
- Diagnostic-edge correctness
- Repeatability
- Accuracy

**Evidence:**

- `src/utils/verify_repositioning_session.py`
- `docs/repositioning_session_integrity_verification_protocol_2026-07-28.txt`

**Git commit:**

- `0faff44` — Add reproducible repositioning-session verifier

---

## E-007 — Trial 02 single-session repositioning repeatability

**Status:** Accepted

**Session ID:**

- `lexan_gauge_block_repositioning_trial_02_20260728_201449`

**Research question:**

Can the Lexan locator support repeatable gauge-block removal, replacement,
seating, image acquisition, and subpixel measurement during one controlled
operator session?

**Results:**

- 10 of 10 cycles completed
- Acquisition-integrity verification: PASS
- Mean fitted span: 523.056377 pixels
- Between-image standard deviation: 0.031861 pixels
- Peak-to-peak variation: 0.089255 pixels
- Between-image standard deviation: 0.000060913 inches
- Dimensional peak-to-peak variation: 0.000170642 inches

**Project objective:**

- Less than 0.001 inch repeatability variation

**Accepted conclusion:**

Under the documented single-operator, single-session conditions, the Lexan
fixture demonstrated acceptable gauge-block removal-and-replacement
repeatability for continued computer-vision metrology development.

**Limitations:**

- Not absolute dimensional accuracy
- Not calibration uncertainty
- Not temperature compensation
- Not total measurement uncertainty
- Not between-day reproducibility
- Not multiple-operator reproducibility
- Not cartridge-case measurement performance
- Not production validation

**Evidence:**

- `measurements/repositioning/lexan_gauge_block_repositioning_trial_02_20260728_201449.json`
- `measurements/repositioning/lexan_gauge_block_repositioning_trial_02_20260728_201449_integrity_verification.txt`
- `measurements/repositioning/lexan_gauge_block_repositioning_trial_02_20260728_201449_evidence_manifest.sha256`
- `measurements/repositioning/trial_02_analysis/`
- `processed_images/repositioning/trial_02_analysis/trial_02_diagnostic_montage.png`
- `docs/trial_02_repositioning_repeatability_results_2026-07-28.txt`
- `docs/research_session_summary_2026-07-28.md`

**Git commits:**

- `5584f1e` — Preserve verified Trial 02 repositioning dataset
- `183bfbf` — Document accepted Trial 02 repeatability results

---

## E-008 — Trial 03 between-day confirmation

**Status:** Planned

**Purpose:**

Repeat the accepted Trial 02 method during an independent later session and
compare:

- Session means
- Within-session variation
- Peak-to-peak variation
- Edge alignment
- Diagnostic overlays
- Environmental observations
- Setup deviations

**Required evidence:**

- Passing research preflight
- Physical-configuration record
- Saved orientation-verification image
- Accepted diagnostic overlay
- Ten removal-and-replacement cycles
- Integrity-verification report
- Batch-analysis report
- Diagnostic montage
- Trial 02-versus-Trial 03 comparison

---

## E-009 — Cartridge-case OAL study

**Status:** Superseded planning

The completed study screened 235 source cases and used a frozen formal cohort of 60 specimens. The original planning text below is retained for traceability; it does not describe the final sample size.

**Planned sequence:**

1. Development pilot
2. Lock the fixture, acquisition method, algorithm, and protocol
3. Complete the official 235-part validation study

**Planned outputs:**

- Unique part identifier
- Manual OAL
- Vision OAL
- Signed error
- Absolute error
- Annotated image
- Detection disposition
- Session identifier
- Agreement and repeatability analysis
