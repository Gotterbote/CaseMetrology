# Chapter 3 Draft Tables

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Status:** Working thesis tables; formal-data-dependent entries remain explicitly pending.

---

## Table 3.1. CaseMetrology hardware and software configuration

| Component | Study configuration | Evidence status |
|---|---|---|
| Embedded computer | NVIDIA Jetson Orin Nano Super Developer Kit | Verified |
| Architecture | aarch64 | Verified |
| NVIDIA runtime | L4T R39, revision 2.0 | Verified 2026-08-15 |
| Kernel | `6.8.12-1021-tegra` | Verified 2026-08-15 |
| Power mode | 15 W, mode index 0 | Verified 2026-08-15 |
| Python | 3.12.3 | Verified 2026-08-15 |
| OpenCV | 4.6.0 | Verified 2026-08-15 |
| NumPy | 1.26.4 | Verified 2026-08-15 |
| Camera | Arducam B0499 USB 3.0, Sony IMX296 global-shutter sensor | Verified configuration + manufacturer support |
| Acquisition resolution | 1456 × 1088 pixels | Verified |
| Acquisition frame rate | 44 fps | Verified |
| Camera project serial | `Arducam_20231211_0001` | Verified |
| Persistent camera device | `/dev/case-metrology-camera` | Verified |
| Lens | Arducam HQ Lens CS2316ZM02 | Verified physical continuity |
| Lens focal length | 16 mm effective | Verified physical continuity |
| Lens mount | CS mount | Verified physical continuity |
| Camera-to-measurement-plane distance | 8.625 in | Verified physical baseline |
| Illumination | VALIKIY LED backlight sheet | Verified physical baseline |
| Backlight rating | 24 V, 36 W | Verified physical baseline |
| Working surface | Clear Lexan, 0.250 in nominal | Verified physical baseline |
| Locator material | Clear Lexan, 0.125 in nominal | Verified physical baseline |
| Locator external dimensions | Not recorded | Intentionally not asserted |

**Table note:** Manufacturer documentation supports vendor specifications. Repository and physical-baseline evidence establish the configuration actually used in CaseMetrology.

---

## Table 3.2. Frozen image-processing, measurement, and calibration configuration

| Stage | Frozen configuration | Validation status |
|---|---|---|
| Input | Grayscale measurement image and corresponding blank reference | Frozen before formal validation |
| Background operation | `cv2.subtract(blank, image)` | Frozen |
| Smoothing | 5 × 5 Gaussian filter | Frozen |
| Thresholding | Otsu thresholding | Frozen |
| Morphological opening | 3 × 3 structuring element | Frozen |
| Morphological closing | 3 × 3 structuring element | Frozen |
| Component selection | Largest connected foreground component | Frozen |
| Pixel-length estimator | PCA/extreme-mask | Frozen 2026-08-13 |
| Axis definition | PCA-derived longitudinal direction with exposed-point refinement | Frozen |
| Endpoint definition | Minimum and maximum accepted-mask projections along refined axis | Frozen |
| Physical endpoint interpretation | Rounded-corner end = base/head; straighter trimmer-cut end = mouth | Verified prevalidation rule |
| Calibration model | Separate first-order `PPI_0(x,y)` and `PPI_90(x,y)` spatial surfaces | Frozen |
| `PPI_0` | `516.907045 + 0.00843326411x + 0.000817091863y` | Frozen |
| `PPI_90` | `518.408825 + 0.00322556849x + 0.00442714650y` | Frozen |
| Directional scale | `sqrt((PPI_90 cosθ)^2 + (PPI_0 sinθ)^2)` evaluated at specimen centroid | Corrected and frozen before formal validation |
| Physical OAL | `L_px / PPI_effective` | Frozen |
| Formal retuning | Prohibited after formal validation begins except documented study disposition | Prospective control |

**Table note:** The `PPI_90` Y coefficient shown here is the corrected supported coefficient. The earlier unsupported draft value `0.000436889756` is not part of the frozen model.

---

## Table 3.3. Formal OAL validation study design

| Phase | Population / sample | Measurement count | Repositioning | Randomization / selection | Primary purpose |
|---|---|---:|---|---|---|
| Population screening | Eligible members of 235-case source population, excluding prevalidation specimens | One screening reading per eligible specimen | Per screening protocol | Screening sequence does not determine final validation order | Characterize OAL distribution for stratification |
| Formal sample selection | Screened eligible population | 60 unique specimens selected | Not applicable | Prospective stratified random selection | Establish formal validation sample |
| Manual reference phase | 60 selected specimens | 3 readings/specimen = 180 planned manual readings | Full removal and repositioning between readings | Independent randomized order; seed `2026081901` | Establish specimen-level manual reference values and within-operator repeated-measurement behavior |
| CV validation phase | Same 60 selected specimens | 3 attempts/specimen = 180 planned CV opportunities | Full removal and repositioning between attempts | Independent randomized order; seed `2026081902` | Evaluate frozen CV method, repeated-measurement behavior, availability, and agreement |
| Statistical analysis | Up to 60 specimen-level manual/CV pairs | Derived from preserved replicate-level data | Not applicable | Prespecified SAP | Evaluate agreement and acceptance criteria |

**Table note:** The primary experimental unit for the agreement analysis is the unique specimen (`n = 60`), not the 180 replicate acquisitions.

**Pending after screening:** final stratum definitions, allocation, and selected specimen IDs.

---

## Table 3.4. Formal computer-vision attempt-status definitions

| Status | Definition | Availability treatment | Replacement treatment | Agreement-analysis treatment |
|---|---|---|---|---|
| `VALID` | Formal attempt completed under protocol and produced a valid CV measurement | Included in numerator and denominator | No replacement required | Eligible replicate |
| `SYSTEM_FAILURE` | Otherwise valid formal attempt in which the CV system failed to produce a valid measurement | Included in availability denominator, not numerator | Not automatically replaced | No value imputed; retained in failure reporting |
| `PROTOCOL_INVALID` | Attempt invalidated by documented procedural nonconformance rather than system performance | Excluded from system availability calculation | Documented appended replacement may be permitted by deviation procedure | Original invalid attempt excluded; replacement handled prospectively |

**Specimen-level rule:** at least two valid CV replicates are required for the specimen-level CV mean used in the primary agreement analysis. A specimen with fewer than two valid CV measurements remains represented in availability/failure reporting.

---

## Table 3.5. Prospective formal validation acceptance criteria

| Performance characteristic | Prospective criterion | Analysis level | Status |
|---|---:|---|---|
| CV availability | ≥ 99% | Attempt level | Frozen before formal validation |
| Repositioning absolute difference, P95 | ≤ 0.002 in | Repeated-measurement analysis | Frozen |
| Absolute mean bias | ≤ 0.001 in | Specimen-level agreement | Frozen |
| RMSE | ≤ 0.002 in | Specimen-level agreement | Frozen |
| Absolute specimen error, empirical P95 | ≤ 0.003 in | Specimen-level agreement | Frozen |
| Maximum absolute specimen error | ≤ 0.004 in | Specimen-level agreement | Frozen |
| False-pass outcome | Zero desired; any confirmed false pass is material to validation disposition | Classification | Frozen principle; near-limit decision rule certificate-dependent |
| Material protocol deviations | No unresolved material deviations for unconditional validation | Study level | Frozen |

**Availability interpretation for 180 planned CV opportunities:**
- 179/180 valid = 99.44% → satisfies ≥99%.
- 178/180 valid = 98.89% → does not satisfy ≥99%.

**Table note:** These are project-specific prospective acceptance criteria. They are not manufacturer tolerances or numerical limits supplied by JCGM, Bland–Altman, ASME, or another external source.

---

# Placement recommendations

- **Table 3.1:** Section 3.3, after hardware/software overview.
- **Table 3.2:** End of Section 3.7, where the method freeze is summarized.
- **Table 3.3:** After Section 3.12, once screening, manual, CV, and randomization procedures have all been introduced.
- **Table 3.4:** Section 3.11, immediately after the status definitions.
- **Table 3.5:** Section 3.16.

# Tables intentionally deferred

Do not create result tables yet for:
- screening distribution;
- final stratum allocation;
- final 60 specimen IDs;
- manual reference summary;
- CV repeatability;
- bias/MAE/RMSE/P95/max error;
- Bland–Altman results;
- classification matrix;
- final validation disposition.

Those belong to the formal-data phase and Chapter 4.
