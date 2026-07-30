# CaseMetrology

Computer-vision metrology research platform developed on the NVIDIA Jetson Orin Nano Super Developer Kit.

CaseMetrology integrates controlled illumination, mechanical positioning, global-shutter imaging, edge computing, subpixel measurement, research-grade data acquisition, and manual reference measurements to evaluate dimensional inspection of cartridge cases.

## Project status

**Classification:** Graduate research prototype  
**Degree program:** M.S. Integrated Systems Design and Dynamics  
**Institution:** Kansas State University  
**Researcher:** Timmy Bell  
**Current phase:** Fixture validation and cartridge-case overall-length measurement development

> This system has not been validated for autonomous production inspection, automatic rejection, PLC control, or production-release decisions.

## Research objective

The project evaluates whether a controlled computer-vision metrology system can measure cartridge-case dimensions with acceptable:

- Repeatability
- Agreement with manual inspection
- Stability across controlled sessions
- Diagnostic traceability
- Reproducibility of acquisition and analysis

The current thesis implementation uses a static measurement fixture. Conveyor integration, PLC communication, and automated rejection remain future work.

## Integrated system architecture

CaseMetrology combines several interacting subsystems:

```mermaid
flowchart LR
    A[Operator and Fixture] --> B[Backlit Workpiece]
    B --> C[Global-Shutter Camera]
    C --> D[Jetson Acquisition]
    D --> E[Image Validation]
    E --> F[Subpixel Measurement]
    F --> G[Dimensional Result]
    G --> H[Evidence and Analysis]
    I[Manual Reference Measurement] --> H
```

| Layer | Current implementation |
|---|---|
| Physical measurement | Gauge block, cartridge case, Lexan locator, fixture, and backlight |
| Imaging | Arducam B0499 USB3 global-shutter camera |
| Edge computing | NVIDIA Jetson Orin Nano |
| Acquisition | Locked controls, persistent camera alias, and session metadata |
| Measurement | Silhouette detection, subpixel edge fitting, and dimensional conversion |
| Assurance | Preflight, file hashes, Git traceability, and diagnostic review |
| Human process | Part placement, manual reference measurement, and interpretation |

## Current imaging configuration

- Camera: Arducam B0499 USB3 global-shutter camera
- Persistent device path: `/dev/case-metrology-camera`
- Resolution: 1456 × 1088 pixels
- Pixel format: YUYV
- Reported frame rate: 44 frames per second
- Warmup frames: 20
- Brightness: 0
- Contrast: 10
- Saturation: 0
- Automatic white balance: disabled
- White-balance temperature: 2498
- Gain: 100
- Exposure mode: manual
- Exposure value: 5

## Current research findings

### Preliminary Lexan optical comparison

A controlled paired comparison evaluated illumination with and without the clear Lexan locator inside a fixed unobstructed central region of interest.

| Metric | Result |
|---|---:|
| Mean grayscale change | −0.0831 |
| Percentage change | −0.0369% |
| Mean absolute pixel difference | 0.8864 |
| RMSE | 1.2830 |
| 95th-percentile absolute difference | 3.0000 |

The Lexan did not produce a practically meaningful change in mean illumination within the selected central ROI.

This result remains classified as **preliminary central-field evidence**, not complete full-field optical validation.

### Trial 01 — Exploratory orientation-error dataset

Ten gauge-block removal-and-replacement cycles were captured with valid image integrity and stable camera controls. The gauge block was later found to be rotated approximately 90 degrees from the approved certified orientation.

The dataset was preserved as exploratory evidence and may support evaluation of:

- Mechanical seating
- Operator placement
- Acquisition stability
- Pixel-level edge behavior

It may not be used as certified dimensional calibration or final fixture-acceptance evidence.

### Trial 02 — Accepted fixture-repositioning result

Trial 02 evaluated ten complete removal-and-replacement cycles with the certified 1.0000024-inch gauge-block dimension oriented vertically.

| Metric | Result |
|---|---:|
| Cycles completed | 10 of 10 |
| Acquisition-integrity verification | PASS |
| Mean fitted span | 523.056377 px |
| Between-image standard deviation | 0.031861 px |
| Peak-to-peak variation | 0.089255 px |
| Dimensional standard deviation | 0.000060913 in |
| Dimensional peak-to-peak variation | 0.000170642 in |
| Project repeatability objective | Less than 0.001 in |

Accepted conclusion:

> Under the documented single-operator, single-session conditions, the Lexan fixture demonstrated acceptable gauge-block removal-and-replacement repeatability for continued computer-vision metrology development.

Trial 02 does not independently establish absolute accuracy, between-day reproducibility, total measurement uncertainty, cartridge-case performance, or production readiness.

## Research evidence

The primary evidence index is:

- [`docs/research_evidence_index.md`](docs/research_evidence_index.md)

Additional research records include:

- [`docs/research_session_summary_2026-07-28.md`](docs/research_session_summary_2026-07-28.md)
- [`docs/trial_02_orientation_verification_2026-07-28.txt`](docs/trial_02_orientation_verification_2026-07-28.txt)
- [`docs/trial_02_repositioning_repeatability_results_2026-07-28.txt`](docs/trial_02_repositioning_repeatability_results_2026-07-28.txt)
- [`docs/repositioning_session_integrity_verification_protocol_2026-07-28.txt`](docs/repositioning_session_integrity_verification_protocol_2026-07-28.txt)
- [`docs/lexan_optical_test_deviation_2026-07-28.md`](docs/lexan_optical_test_deviation_2026-07-28.md)
- [`docs/research_data_retention_policy.md`](docs/research_data_retention_policy.md)

## Repository structure

```text
CaseMetrology/
├── docs/               Protocols, runbooks, results, and evidence index
├── scripts/            Research preflight and workflow scripts
├── src/
│   ├── acquisition/    Controlled camera acquisition
│   ├── calibration/    Gauge-block and illumination analysis
│   └── utils/          Integrity-verification utilities
├── data/               Selected exploratory and milestone evidence
├── raw_images/         Raw research images
├── processed_images/   Diagnostic and annotated images
├── measurements/       Metadata, CSV files, and analysis reports
├── logs/               Preflight and session logs
└── requirements-dev.txt
```

Large datasets may remain outside normal Git tracking. Accepted milestone evidence may be committed when it materially improves reproducibility.

See:

- [`docs/research_data_retention_policy.md`](docs/research_data_retention_policy.md)

## Research-session startup

On the Jetson:

```bash
cd ~/Projects/CaseMetrology
source .venv/bin/activate
git status -sb
./scripts/run_research_session_preflight.sh
```

Official acquisition should not begin unless:

- The preflight passes
- The repository state is documented
- Camera controls match the approved configuration
- The physical configuration is inspected
- The required orientation or part-placement gate is accepted

## Acquisition traceability

Controlled sessions may record:

- Session identifier
- Capture timestamps
- Camera settings
- Git commit and working-tree state
- Image dimensions and file sizes
- SHA-256 hashes
- Experimental mode
- Analysis outputs
- Diagnostic-review disposition

The reusable repositioning verifier is:

`src/utils/verify_repositioning_session.py`

An automated integrity PASS verifies acquisition records and file integrity. It does not independently establish correct orientation, physical seating, dimensional accuracy, or valid edge selection.

## Next milestones

### Trial 03 — Between-day confirmation

Trial 03 will repeat the accepted fixture experiment during an independent later session.

The comparison will evaluate:

- Difference between session means
- Within-session variation
- Peak-to-peak variation
- Edge-angle consistency
- Diagnostic consistency
- Environmental observations
- Physical setup deviations

Runbook:

- [`docs/trial_03_between_day_repositioning_runbook.md`](docs/trial_03_between_day_repositioning_runbook.md)

### Cartridge-case overall-length measurement

After fixture confirmation, the project will:

1. Develop the cartridge-case OAL measurement pipeline
2. Complete a small development pilot
3. Lock the fixture, acquisition method, and algorithm
4. Conduct an official 235-part validation study
5. Compare computer-vision results with manual reference measurements

## Current limitations

The project has not yet established:

- Absolute dimensional accuracy
- Traceable calibration uncertainty
- Total measurement uncertainty
- Temperature compensation
- Multiple-operator reproducibility
- Long-term fixture stability
- Cartridge-case measurement agreement
- Production-level classification performance
- PLC or reject-system integration

## Future development

Potential future work includes:

- Operator-facing measurement dashboard
- Per-cycle pass/fail reporting
- Multiple dimensional measurements
- Data historian integration
- PLC communication
- Conveyor-triggered acquisition
- Automated stopping or rejection
- Production-scale validation

## Author

**Timmy Bell**  
M.S. Integrated Systems Design and Dynamics candidate  
Kansas State University

GitHub: `Gotterbote`
