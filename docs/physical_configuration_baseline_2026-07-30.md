# CaseMetrology Physical Configuration Baseline

## Record status

Template — complete at the Jetson before Trial 03.

## Session information

- Date: 2026-07-30
- Time: 18:34:00 CDT (UTC-05:00)
- Operator: Timmy Bell
- Git commit: `0cb57343e3cca1e09dab8318cebf5c821d45f1e4`
- Working tree clean: Yes, before creating this session record
- Preflight log: `logs/research_preflight/research_preflight_20260730_183641.txt`

## Camera

- Manufacturer/model: Arducam B0499 USB3 global-shutter camera
- Persistent device path: `/dev/case-metrology-camera`
- Sensor orientation: Native 1456 x 1088 landscape acquisition; when facing the long side of the light enclosure, the right side of the camera body faces the observer. Sensor rotation relative to the enclosure was not independently measured.
- Camera-support reference height: Not separately measured; the reproducible optical reference is the 8.625-inch lens-front-to-measurement-plane distance
- Camera-to-measurement-plane distance: 8.625 inches, measured vertically from the front-most edge of the lens barrel to the gauge-block resting surface
- Measurement method and instrument: Caliper measurement from the front-most edge of the lens barrel to the gauge-block resting surface
- Mount fasteners checked: Yes; visually and manually confirmed secure
- Visible looseness or movement: None detected during manual inspection
- Photograph path:

## Lens

- Manufacturer/model: Arducam HQ Lens CS2316ZM02
- Focal length: 16 mm effective focal length
- Mount type: CS
- Aperture position: No position markings visible; exact setting not quantified
- Focus position: Manually adjusted and left unchanged for this baseline
- Focus-lock method: Mechanical locking screw
- Witness mark present: No; focus is retained by the mechanical locking screw
- Photograph path:

## Backlight

- Manufacturer/model: VALIKIY LED Backlight Sheet
- Voltage: 24 V rated
- Power: 36 W rated
- Position relative to measurement plane: Backlight adhered to the inside surface of the 0.250-inch black-plastic bottom panel within an 80/20 aluminum enclosure. External enclosure dimensions, measured from the outer edges of the 80/20 frame (L × W × H): 16.500 in × 7.000 in × 7.625 in.
- Warm-up duration: Backlight had remained continuously energized for multiple weeks before this session; exact energization start time was not recorded
- Visible contamination or damage: Visible surface or locator marks are present in the field of view outside the central fitted edge region; no damage or obstruction of the accepted fitted edges was observed
- Photograph path:

## Lexan working surface

- Material: Lexan sheet
- Thickness: 0.250 in nominal
- Surface condition: Working face exposed; opaque protective film retained on the opposite, non-working face
- Function: Primary support and measurement surface beneath the removable locator fixture

## Lexan locator

- Material: Lexan sheet
- Thickness: 0.125 in nominal
- External dimensions: Not recorded during the installed baseline; locator was not removed or disturbed
- Datum-face description: Locator rests directly on top of the 0.250-inch Lexan working surface; both protective films removed
- Internal-corner relief: Present; prevents the gauge-block corner from contacting the locator cut radius
- Fit between rails: Captured securely between the 80/20 rails with no detectable looseness
- Bowing observed: No noticeable bow under visual inspection
- Movement observed: No movement detected during manual observation
- Retention method: Friction fit between the 80/20 rails
- Photograph path:

## Gauge block

- Certified dimension: 1.0000024 inches
- Certified dimension vertical: Yes; the certified 1.0000024-inch dimension is oriented vertically
- Approximately 1.375-inch dimension horizontal: Yes
- Block visually wider than tall: Yes
- Measuring faces clean: Yes; visually confirmed
- Block rests flat: Yes; visually confirmed
- Contacts both datum faces: Yes; contact with both perpendicular locator datum faces visually confirmed
- Photograph path:

## Locked camera configuration

- Resolution: 1456 x 1088
- Pixel format: YUYV
- Frame rate: 44 fps
- Warmup frames: 20
- Brightness: 0
- Contrast: 10
- Saturation: 0
- Automatic white balance: disabled
- White-balance temperature: 2498
- Gain: 100
- Exposure mode: manual
- Exposure value: 5

## Environmental observation

- Temperature: 78.5 degrees Fahrenheit
- Units: degrees Fahrenheit
- Instrument: Unknown contact-probe instrument placed on a separate steel witness block
- Instrument accuracy: Unknown
- Calibration status: No current calibration documentation available
- Classification: Approximate, non-traceable contact-probe observation
- Stabilization condition: Backlight had remained continuously energized for multiple weeks before this session
- Stabilization duration: No session-specific warm-up interval applicable; exact original energization time was not recorded

## Visual acceptance

- Full gauge block visible: Yes
- Correct orientation: Yes; the block is visibly wider than tall and the certified dimension is vertical
- Focus acceptable: Yes; the upper and lower block edges support stable subpixel fitting
- No clipped edges: Yes
- No obvious backlight artifact in measurement region: Yes; no artifact obstructs the central fitted edge segments
- Lexan boundaries excluded from fitted region: Yes
- Orientation-verification diagnostic accepted: Yes; manually reviewed and accepted on 2026-07-30

## Deviations or limitations

- Visible surface or locator marks are present outside the central fitted edge region; they did not intersect the accepted upper or lower fit segments in the orientation diagnostic.

## Final disposition

- [x] Accepted for Trial 03
- [ ] Accepted with limitation
- [ ] Not accepted; correction required

## Evidence paths

- Physical setup photograph:
- Lens witness-mark photograph:
- Representative raw image: `raw_images/acquisition/trial_03_orientation_verification_20260730_200358/trial_03_orientation_verification_20260730_200401_183580_01.png`
- Orientation diagnostic: `processed_images/calibration/trial_03_orientation_verification/trial_03_orientation_verification_20260730_200401_183580_01_subpixel_diagnostic.png`
- Preflight log: `logs/research_preflight/research_preflight_20260730_183641.txt`
