# CaseMetrology Research Session Summary — 2026-07-28

## Record classification

This document is a retrospective research-session summary reconstructed on
2026-07-30 from contemporaneous acquisition metadata, analysis reports,
file-integrity records, timestamps, preserved images, written disposition
records, and Git history.

It was not written as a real-time laboratory log. It does not replace or modify
the original evidence files.

## Session purpose

The July 28 session evaluated whether the clear Lexan locator was suitable for
continued computer-vision metrology development and whether it could support
repeatable gauge-block removal, replacement, seating, image acquisition, and
subpixel dimensional measurement.

The planned sequence was defined in:

\- `docs/lexan\_fixture\_validation\_runbook\_2026-07-28.txt`

## Operator

Timmy Bell

## Approximate session period

The documented experimental work occurred during the evening of 2026-07-28.

Contemporaneous records identify:

\- Trial 01 acquisition beginning at approximately 18:22 CDT
\- Research preflight completed at approximately 18:56 CDT
\- Corrected-orientation verification acquired at approximately 20:00 CDT
\- Trial 02 acquisition beginning at approximately 20:14 CDT
\- Trial 02 batch-analysis report generated at approximately 21:09 CDT

These times are derived from saved session identifiers, metadata, and report
timestamps.

## Equipment and controlled configuration

### Imaging system

\- Compute platform: NVIDIA Jetson Orin Nano
\- Camera: Arducam B0499 USB3 global-shutter camera
\- Persistent device path: `/dev/case-metrology-camera`
\- Resolution: 1456 x 1088 pixels
\- Pixel format: YUYV
\- Reported frame rate: 44 frames per second
\- Warmup frames: 20

### Locked camera controls

\- Brightness: 0
\- Contrast: 10
\- Saturation: 0
\- Automatic white balance: disabled
\- White-balance temperature: 2498
\- Gain: 100
\- Exposure mode: manual
\- Exposure value: 5

Camera settings were verified as unchanged before and after the Lexan optical
comparison and before, during, and after the official Trial 02 acquisition.

### Mechanical and optical configuration

\- Clear Lexan locator installed between the fixture side rails
\- Gauge block seated against the locator datum surfaces
\- Gauge block allowed to rest without intentional clamping
\- Camera, lens, backlight, and locator remained fixed during each official
&#x20; acquisition sequence
\- Certified gauge-block dimension: 1.0000024 inches
\- Correct official orientation:
&#x20; - Certified 1.0000024-inch dimension vertical
&#x20; - Approximately 1.375-inch dimension horizontal
&#x20; - Gauge block visually wider than tall

## Environmental observation

Approximate ambient temperature:

\- 73.2 degrees Fahrenheit

Temperature-data classification:

The reading was obtained using a non-calibrated or approximate instrument.
It is retained only as a supporting environmental observation and shall not
be represented as traceable temperature-metrology evidence.

No temperature-compensation calculation was applied.

## Research preflight

Research-session preflight result:

\- PASS

Preflight evidence:

\- `logs/research\_preflight/research\_preflight\_20260728\_185615.txt`

The preflight confirmed that the system was operational and suitable to proceed
under the documented configuration.

## Phase 1 — Preliminary Lexan optical comparison

### Purpose

Evaluate whether installing the Lexan fixture surface materially changed
illumination within an unobstructed central measurement region.

### Fixed region of interest

\- x = 500:1300
\- y = 350:900
\- ROI size = 800 x 550 pixels

### Results

Without Lexan:

\- Mean grayscale: 225.1456
\- Standard deviation: 8.2595
\- Minimum: 189
\- Maximum: 237

With Lexan:

\- Mean grayscale: 225.0625
\- Standard deviation: 8.3692
\- Minimum: 187
\- Maximum: 237

Difference results:

\- Mean grayscale change: -0.0831
\- Mean percent change: -0.0369%
\- Mean absolute pixel difference: 0.8864
\- RMSE: 1.2830
\- 95th-percentile absolute difference: 3.0000

### Preliminary interpretation

The Lexan did not produce a practically meaningful change in mean illumination
within the selected unobstructed central ROI under the tested conditions.

### Optical-test limitations and deviations

This comparison must remain classified as preliminary because:

\- It used one paired image comparison
\- It did not independently establish optical repeatability
\- The selected ROI did not directly evaluate both final gauge-block
&#x20; measurement-edge regions
\- The visible Lexan or fixture boundaries remained capable of creating false
&#x20; edges if included in a dimensional-analysis ROI
\- The optical comparison was completed before the formal research preflight
\- The captures and ROI comparison did not follow every execution detail of the
&#x20; original runbook
\- Environmental temperature was not recorded with a traceable instrument
\- The result does not establish complete optical neutrality across the full field

### Optical evidence

\- `data/lexan\_test/00\_camera\_settings\_before.txt`
\- `data/lexan\_test/01\_blank\_no\_lexan.png`
\- `data/lexan\_test/01\_blank\_no\_lexan\_metadata.txt`
\- `data/lexan\_test/02\_blank\_with\_lexan.png`
\- `data/lexan\_test/02\_blank\_with\_lexan\_metadata.txt`
\- `data/lexan\_test/03\_camera\_settings\_after.txt`
\- `data/lexan\_test/04\_lexan\_roi\_comparison.txt`
\- `data/lexan\_test/04\_roi\_absolute\_difference.png`
\- `data/lexan\_test/04\_roi\_difference\_normalized.png`
\- `data/lexan\_test/05\_lexan\_optical\_test\_summary.txt`
\- `data/lexan\_test/06\_sha256\_manifest.txt`

Associated Git commit:

\- `3c11993` — Document Lexan optical comparison test

## Phase 2 — Trial 01 orientation-error exploratory dataset

### Session

\- `lexan\_gauge\_block\_repositioning\_trial\_01\_20260728\_182212`

### Acquisition result

\- 10 of 10 removal-and-replacement cycles completed
\- Camera controls remained unchanged
\- All images passed file-integrity validation
\- Repository was clean at acquisition commit
&#x20; `3c119936d9f6c500fe921481fd292f6c62bad715`

### Protocol deviation

The gauge block was installed approximately 90 degrees from the orientation
required by the approved protocol.

Incorrect Trial 01 orientation:

\- Approximately 1.375-inch dimension vertical
\- Certified 1.0000024-inch dimension horizontal

### Disposition

Trial 01 is preserved as exploratory evidence only.

Permitted uses include exploratory evaluation of:

\- Removal and replacement
\- Mechanical locator seating
\- Operator seating consistency
\- Image-acquisition stability
\- Pixel-level positional and edge repeatability

Trial 01 shall not be used as:

\- The official certified repositioning trial
\- A certified one-inch dimensional calibration
\- Evidence of absolute dimensional accuracy
\- Final acceptance evidence for the Lexan locator
\- A source of inch-based results using the vertical one-inch calibration

### Corrective action

The experiment was repeated after confirming:

\- Certified 1.0000024-inch dimension vertical
\- Approximately 1.375-inch dimension horizontal
\- Gauge block visually wider than tall
\- Camera, lens, backlight, and Lexan locator unchanged

### Trial 01 evidence

\- `data/fixture\_repositioning/2026-07-28\_trial\_01/00\_trial\_disposition.txt`
\- `data/fixture\_repositioning/2026-07-28\_trial\_01/01\_trial\_integrity\_manifest.sha256`

Associated Git commit:

\- `edac004` — Preserve orientation-error exploratory repositioning trial

## Phase 3 — Corrected-orientation verification

### Session

\- `trial\_02\_corrected\_orientation\_verification\_20260728\_200026`

### Source repository state

\- Git commit:
&#x20; `edac00426a59833aa1f434816e57bc0524f1f529`
\- Working tree clean during acquisition

### Verified orientation

\- Certified 1.0000024-inch dimension vertical
\- Approximately 1.375-inch dimension horizontal
\- Gauge block visually wider than tall

### Diagnostic results

\- Otsu threshold: 99.0
\- Bounding box: x=379, y=255, w=725, h=528
\- Valid columns: 289
\- Mean fitted vertical span: 523.068111 pixels
\- Median fitted vertical span: 523.005495 pixels
\- Preliminary scale: 523.066855 pixels per inch
\- Preliminary resolution: 0.001911802 inches per pixel
\- Top fitted angle: 0.324833 degrees
\- Bottom fitted angle: 0.485038 degrees

### Manual diagnostic review

The detected component boundary followed the gauge-block silhouette. The
fitted upper and lower segments followed the intended gauge-block measuring
surfaces in the central analysis region. Visible Lexan boundaries did not appear
to control the fitted measurement edges.

### Disposition

The corrected physical orientation and image-processing response were accepted
for beginning the official Trial 02 sequence.

This verification did not independently establish repositioning repeatability or
absolute dimensional accuracy.

Evidence document:

\- `docs/trial\_02\_orientation\_verification\_2026-07-28.txt`

Associated Git commit:

\- `2895471` — Verify corrected gauge-block orientation for Trial 02

## Phase 4 — Reproducible acquisition-integrity verification

A reusable repositioning-session verifier and written protocol were added to
ensure that accepted sessions could be checked using a version-controlled
method.

Evidence:

\- `src/utils/verify\_repositioning\_session.py`
\- `docs/repositioning\_session\_integrity\_verification\_protocol\_2026-07-28.txt`

Associated Git commit:

\- `0faff44` — Add reproducible repositioning-session verifier

The verifier establishes acquisition and file integrity. It does not establish
correct orientation, correct physical seating, dimensional accuracy, optical
validity, environmental control, or diagnostic-edge correctness.

## Phase 5 — Official Trial 02 repositioning experiment

### Test designation

Lexan Gauge-Block Repositioning Trial 02

### Session ID

\- `lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_201449`

### Purpose

Evaluate the combined repeatability associated with complete gauge-block
removal, replacement, locator seating, image acquisition, and subpixel
dimensional measurement.

### Experimental sequence

\- 10 independent removal-and-replacement cycles
\- Gauge block completely removed between cycles
\- Gauge block replaced and seated in the Lexan locator
\- Camera, lens, backlight, and locator left unchanged
\- Correct orientation maintained throughout the sequence

### Automated integrity verification

Result:

\- PASS

The verifier confirmed:

\- 10 cycles requested and 10 completed
\- Sequential and unique cycle records
\- Unique image records
\- Camera configuration matched the approved state
\- Camera controls remained unchanged before, during, and after acquisition
\- All images were readable
\- All images were 1456 x 1088 pixels
\- Recorded and actual file sizes matched
\- Recalculated SHA-256 hashes matched acquisition metadata
\- Verification method was version-controlled and unchanged
\- Acquisition working tree was clean

### Trial 02 acquisition evidence

\- `measurements/repositioning/lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_201449.json`
\- `measurements/repositioning/lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_201449\_integrity\_verification.txt`
\- `measurements/repositioning/lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_201449\_evidence\_manifest.sha256`

Associated Git commit:

\- `5584f1e` — Preserve verified Trial 02 repositioning dataset

## Phase 6 — Trial 02 subpixel repeatability analysis

### Results

\- Mean fitted span: 523.056377 pixels
\- Median fitted span: 523.056308 pixels
\- Minimum fitted span: 523.009429 pixels
\- Maximum fitted span: 523.098684 pixels
\- Between-image standard deviation: 0.031861 pixels
\- Peak-to-peak variation: 0.089255 pixels
\- Calculated scale: 0.001911844 inches per pixel
\- Between-image standard deviation: 0.000060913 inches
\- Dimensional peak-to-peak variation: 0.000170642 inches

### Alignment results

\- Mean top-edge angle: 0.343583 degrees
\- Mean bottom-edge angle: 0.496957 degrees
\- Mean edge-angle difference: 0.153375 degrees

### Visual diagnostic review

All ten diagnostic overlays were reviewed as a montage.

The detected component boundaries consistently enclosed the gauge block. The
fitted edge segments followed the intended upper and lower measurement edges.
The measurement lines spanned the certified vertical dimension.

No cycle showed:

\- Incorrect block orientation
\- Gross component-selection failure
\- Obvious false-edge selection from the Lexan locator
\- Missing measurement edges
\- A visually apparent seating or measurement outlier

### Acceptance criterion

Project repeatability objective:

\- Less than 0.001 inch

### Accepted result

\- Between-image standard deviation: 0.000060913 inch
\- Peak-to-peak variation: 0.000170642 inch

Both values were below the project repeatability objective.

### Accepted conclusion

Under the documented single-operator, single-session conditions, the Lexan
fixture demonstrated acceptable gauge-block removal-and-replacement
repeatability for continued computer-vision metrology development.

### Evidence

\- `measurements/repositioning/trial\_02\_analysis/lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_210944.csv`
\- `measurements/repositioning/trial\_02\_analysis/lexan\_gauge\_block\_repositioning\_trial\_02\_20260728\_210944.txt`
\- `processed\_images/repositioning/trial\_02\_analysis/trial\_02\_diagnostic\_montage.png`
\- `docs/trial\_02\_repositioning\_repeatability\_results\_2026-07-28.txt`

Associated Git commit:

\- `183bfbf` — Document accepted Trial 02 repeatability results

## Deviations and lessons incorporated into future work

The July 28 session identified several process improvements:

1\. Physical orientation confirmation alone is insufficient.
&#x20;  Future official sessions shall require a saved orientation-verification image,
&#x20;  subpixel diagnostic, and manual overlay acceptance before the repeated-cycle
&#x20;  sequence begins.

2\. Preliminary optical comparisons must remain clearly separated from complete
&#x20;  optical validation.

3\. Automated acquisition-integrity verification must remain separate from
&#x20;  physical and dimensional acceptance.

4\. Approximate environmental readings must not be represented as traceable
&#x20;  temperature evidence.

5\. Trial 01 shall remain preserved rather than deleted, altered, or silently
&#x20;  replaced.

6\. Original Trial 02 metadata shall not be retrospectively modified. Later
&#x20;  summaries and addenda may clarify the record but may not rewrite the original
&#x20;  acquisition evidence.

## Research limitations

The July 28 results do not independently establish:

\- Absolute dimensional accuracy
\- Calibration uncertainty
\- Temperature compensation
\- Total measurement uncertainty
\- Between-day reproducibility
\- Between-operator reproducibility
\- Long-term fixture wear or drift
\- Cartridge-case measurement performance
\- Production-machine-cycle performance
\- Production inspection capability

## July 28 Git traceability chain

1\. `3c11993` — Document Lexan optical comparison test
2\. `edac004` — Preserve orientation-error exploratory repositioning trial
3\. `2895471` — Verify corrected gauge-block orientation for Trial 02
4\. `0faff44` — Add reproducible repositioning-session verifier
5\. `5584f1e` — Preserve verified Trial 02 repositioning dataset
6\. `183bfbf` — Document accepted Trial 02 repeatability results

## Final session disposition

The preliminary Lexan optical comparison was retained with defined limitations.

Trial 01 was preserved as an orientation-error exploratory dataset and prohibited
from use as official certified dimensional evidence.

Trial 02 passed acquisition-integrity verification, diagnostic review, and
subpixel repeatability analysis. Trial 02 was accepted as evidence of
single-operator, single-session gauge-block repositioning repeatability under the
documented configuration.

The next fixture-validation milestone is an independent between-day repetition
using the corrected orientation-verification gate.


