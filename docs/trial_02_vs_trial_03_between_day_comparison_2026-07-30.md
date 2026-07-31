# Trial 02 versus Trial 03 Between-Day Comparison

## Record status

Completed on 2026-07-30 after Trial 03 acquisition, automated integrity
verification, subpixel batch analysis, and manual review of all ten diagnostic
overlays.

## Research question

Can the accepted Trial 02 single-session Lexan-fixture result be reproduced
during an independent later session?

## Session comparison

| Field | Trial 02 | Trial 03 |
|---|---|---|
| Date | 2026-07-28 | 2026-07-30 |
| Session ID | `lexan_gauge_block_repositioning_trial_02_20260728_201449` | `lexan_gauge_block_repositioning_trial_03_20260730_202839` |
| Operator | Timmy Bell | Timmy Bell |
| Preflight result | PASS | PASS |
| Ambient temperature | Approx. 73.2 °F | Approx. 78.5 °F |
| Temperature classification | Approximate, non-traceable | Approximate, non-traceable contact-probe observation |
| Orientation gate | PASS | PASS |
| Integrity verification | PASS | PASS |
| Montage review | PASS | PASS |

## Numerical comparison

| Metric | Trial 02 | Trial 03 | Difference |
|---|---:|---:|---:|
| Mean fitted span, px | 523.056377 | 523.078242 | +0.021865 |
| Median fitted span, px | 523.056308 | 523.068739 | +0.012431 |
| Minimum fitted span, px | 523.009429 | 523.036171 | +0.026742 |
| Maximum fitted span, px | 523.098684 | 523.165257 | +0.066573 |
| Within-session SD, px | 0.031861 | 0.040645 | +0.008784 |
| Peak-to-peak, px | 0.089255 | 0.129086 | +0.039831 |
| Inches per pixel | 0.001911844 | 0.001911764 | -0.000000080 |
| Within-session SD, in | 0.000060913 | 0.000077703 | +0.000016790 |
| Peak-to-peak, in | 0.000170642 | 0.000246782 | +0.000076140 |
| Mean top-edge angle, deg | 0.343583 | 0.375774 | +0.032191 |
| Mean bottom-edge angle, deg | 0.496957 | 0.525595 | +0.028638 |
| Mean edge-angle difference, deg | 0.153375 | 0.149821 | -0.003554 |

## Difference between session means

- Trial 02 mean: 523.056377 pixels
- Trial 03 mean: 523.078242 pixels
- Difference in pixels: +0.021865 pixels
- Approximate pixel-span equivalent in inches: +0.000041802 inches
- Direction of shift: Trial 03 produced a slightly larger fitted vertical span

The inch-equivalent value is provided to aid interpretation of the pixel-span
shift. It does not independently establish a physical change in the certified
gauge-block dimension.

## Trial 03 diagnostic review

- Orientation consistency: Correct orientation observed in all ten cycles
- Component-selection consistency: Gauge block correctly selected in all ten cycles
- Edge-fit consistency: Upper and lower fitted segments followed the gauge-block edges in all ten cycles
- Lexan-boundary influence: No fitted segment followed a Lexan locator boundary
- Focus consistency: Focus remained visually acceptable across all ten cycles
- Seating anomalies: No visible seating failure identified
- Outlier cycles: No failed or visually invalid cycle identified; cycle 8 produced the maximum fitted span but retained an accepted diagnostic fit

## Setup and environmental differences

- Temperature difference: Trial 03 was approximately 5.3 °F warmer than Trial 02
- Stabilization difference: Trial 03 documented that the backlight had remained continuously energized for multiple weeks; an equivalent exact stabilization record was not available for Trial 02
- Camera or lens change: No intentional change
- Backlight change: No intentional change
- Locator change: No intentional change
- Operator or seating difference: Same operator and no intentional change to the seating procedure
- Other deviation: Trial 03 contained visible surface or locator marks outside the central fitted edge region; they did not intersect the accepted measurement fits

## Interpretation

1. **Trial 03 within-session repeatability**

   Trial 03 produced a within-session standard deviation of 0.000077703 inches
   and a peak-to-peak variation of 0.000246782 inches. Both values were below
   the project's 0.001-inch development objective.

2. **Difference between session means**

   The Trial 03 mean fitted span was 0.021865 pixels larger than the Trial 02
   mean. This corresponds to an approximate pixel-span equivalent of
   0.000041802 inches and is small relative to the 0.001-inch development
   objective.

3. **Alignment consistency**

   The mean edge-angle difference changed from 0.153375 degrees in Trial 02 to
   0.149821 degrees in Trial 03. This small difference indicates comparable
   top-to-bottom edge alignment between sessions.

4. **Environmental and setup differences**

   Trial 03 was observed at an approximately 5.3 °F higher temperature. Both
   temperature observations were approximate and non-traceable, so the effect
   of temperature cannot be isolated or compensated. No intentional changes
   were made to the camera, lens, focus lock, backlight, Lexan working surface,
   locator, operator, or seating procedure.

5. **Between-day confirmation claim**

   Trial 03 reproduced the accepted Trial 02 result during a separate session
   two days later. The within-session variation remained below the development
   objective, the session-mean shift was small, and all diagnostic fits passed
   manual review. The evidence therefore supports a limited between-day
   confirmation claim under the documented single-operator conditions.

## Final disposition

- [x] Accepted between-day confirmation
- [ ] Accepted with limitation
- [ ] Inconclusive; another session required
- [ ] Rejected; investigation required

## Defensible conclusion

> Under the documented single-operator conditions, Trial 03 reproduced the
> accepted Trial 02 gauge-block removal-and-replacement performance during an
> independent session two days later. Trial 03 produced a within-session
> standard deviation of 0.000077703 inches and peak-to-peak variation of
> 0.000246782 inches, while the difference between session mean spans was
> approximately 0.000041802 inch equivalent. These results support between-day
> confirmation of the Lexan fixture and image-acquisition process for continued
> computer-vision metrology development. They do not establish absolute
> dimensional accuracy, total measurement uncertainty, temperature
> compensation, multiple-operator reproducibility, long-term stability, or
> cartridge-case performance.

## Limitations

This comparison does not independently establish:

- Absolute dimensional accuracy
- Total measurement uncertainty
- Temperature compensation
- Multiple-operator reproducibility
- Long-term stability
- Cartridge-case performance
- Production validation

The environmental observations were approximate and non-traceable. Only one
operator, one gauge block, two sessions, and ten repositioning cycles per
session were evaluated.

## Trial 03 evidence paths

- Acquisition metadata: `measurements/repositioning/lexan_gauge_block_repositioning_trial_03_20260730_202839.json`
- Integrity report: `measurements/repositioning/lexan_gauge_block_repositioning_trial_03_20260730_202839_integrity_verification.txt`
- Evidence manifest: `measurements/repositioning/lexan_gauge_block_repositioning_trial_03_20260730_202839_evidence_manifest.sha256`
- Analysis CSV: `measurements/repositioning/trial_03_analysis/lexan_gauge_block_repositioning_trial_03_20260730_203952.csv`
- Analysis report: `measurements/repositioning/trial_03_analysis/lexan_gauge_block_repositioning_trial_03_20260730_203952.txt`
- Diagnostic montage: `processed_images/repositioning/trial_03_analysis/trial_03_diagnostic_montage.png`
- Final disposition: `docs/trial_02_vs_trial_03_between_day_comparison_2026-07-30.md`

## Trial 03 Git traceability

- Acquisition commit: `0803f242bb0267faabc0468000cf355b9634d6ab`
- Analysis commit: `8b23e289f7575a0d643fa49b66151bcdb3062072`
- Acceptance commit: Pending completion and commit of this comparison record
