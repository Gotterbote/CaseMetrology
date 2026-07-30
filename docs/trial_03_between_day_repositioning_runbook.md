# Trial 03 Between-Day Gauge-Block Repositioning Runbook

## Purpose

Determine whether the accepted Trial 02 Lexan-fixture result can be reproduced
during an independent later session.

This trial addresses between-session confirmation. It does not establish full
multi-day reproducibility, multiple-operator reproducibility, absolute accuracy,
or total measurement uncertainty.

## Phase 1 — Repository and system readiness

1. Activate the project virtual environment.
2. Confirm the repository is synchronized.
3. Confirm the working tree is clean.
4. Run:

   `./scripts/run_research_session_preflight.sh`

5. Do not proceed unless the result is PASS.
6. Record the preflight-log path.

## Phase 2 — Stabilization and environmental observation

1. Power the camera and backlight.
2. Allow the system to stabilize.
3. Record:
   - Operator
   - Temperature
   - Units
   - Instrument used
   - Calibration or traceability classification
4. Do not claim traceable temperature evidence unless supported by the
   instrument.

## Phase 3 — Physical configuration check

Confirm:

- Camera mount unchanged
- Lens and focus unchanged
- Backlight position unchanged
- Lexan locator seated correctly and not bowed
- Gauge-block contact surfaces clean
- Gauge block resting flat
- Gauge block contacting both datum faces
- Certified 1.0000024-inch dimension vertical
- Approximately 1.375-inch dimension horizontal
- Gauge block visually wider than tall

Complete:

- `docs/physical_configuration_baseline_template.md`

## Phase 4 — Mandatory orientation-verification gate

Before beginning the repeated-cycle sequence:

1. Capture one controlled orientation-verification image.
2. Run the existing subpixel diagnostic.
3. Review the diagnostic overlay.
4. Confirm:
   - Correct component selected
   - Bounding region encloses the gauge block
   - Fitted edges follow the intended upper and lower surfaces
   - Lexan boundaries do not control the fit
   - Certified dimension is vertical
5. Save the image, diagnostic output, and disposition.
6. Do not begin Trial 03 unless this gate is accepted.

## Phase 5 — Ten-cycle removal-and-replacement sequence

For each of 10 cycles:

1. Remove the gauge block completely.
2. Replace it in the Lexan locator.
3. Gently seat it against both datum faces.
4. Confirm it rests flat.
5. Confirm the block remains wider than tall.
6. Capture the image.
7. Do not move the camera, lens, backlight, or Lexan locator.

## Phase 6 — Acquisition-integrity verification

Run the existing reusable verifier.

Required automated result:

- PASS

The verifier shall confirm:

- Requested and completed cycle counts match
- Records are sequential and unique
- Camera settings match the approved state
- Controls remain unchanged
- Files are readable
- Dimensions and sizes match metadata
- SHA-256 hashes match
- Verification method is version-controlled
- Acquisition working tree was clean

An integrity PASS does not establish physical orientation, correct seating,
edge validity, repeatability, or accuracy.

## Phase 7 — Batch subpixel analysis

Review:

- Mean fitted span
- Median fitted span
- Minimum and maximum fitted spans
- Between-image standard deviation
- Peak-to-peak variation
- Calculated inches per pixel
- Dimensional standard deviation
- Dimensional peak-to-peak variation
- Mean top- and bottom-edge angles
- Mean edge-angle difference

## Phase 8 — Diagnostic montage review

Investigate any cycle showing:

- Incorrect orientation
- Wrong component selection
- Lexan boundary controlling the fit
- Missing fitted edge
- Gross focus change
- Visible seating anomaly
- Unexplained measurement outlier

Record the manual montage disposition.

## Phase 9 — Trial 02 versus Trial 03 comparison

Use:

- `docs/trial_02_vs_trial_03_comparison_template.md`

Compare:

- Session means
- Within-session standard deviations
- Peak-to-peak variations
- Edge angles
- Environmental observations
- Setup or procedural deviations

## Acceptance framework

### Within-session objective

Trial 03 variation should remain below:

- 0.001 inch

### Between-session interpretation

Report the difference between the Trial 02 and Trial 03 means directly.

A passing within-session result does not prove between-day stability if there
is an unexplained material shift between session means.

## Final disposition

Choose one:

- Accepted between-day confirmation
- Accepted with limitation
- Inconclusive; another session required
- Rejected; investigation required

## Required preservation

Preserve:

- Preflight log
- Environmental observation
- Physical-configuration record
- Orientation-verification image and diagnostic
- Raw images and acquisition metadata
- Integrity report and manifest
- Batch CSV and report
- Diagnostic montage
- Trial comparison
- Final disposition
- Git commits
