# Chapter 3 Sentence-Level Evidence Audit — Sections 3.1–3.3.5

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Scope:** K-State M.S. Integrated Systems Design & Dynamics thesis — cartridge-case OAL only
**Status:** Working audited draft; repository commit deferred by researcher.

## Tag legend

- `[REPO]` — supported by CaseMetrology repository evidence.
- `[LITERATURE]` — general scientific/engineering concept requiring outside citation.
- `[MANUFACTURER]` — supported by official manufacturer documentation.
- `[STANDARD]` — supported by recognized engineering/metrology guidance.
- `[PENDING]` — cannot yet be finalized.
- `[GUARDRAIL]` — wording needed to prevent an unsupported or overly broad claim.

---

# A. Annotated evidence-audit version

## 3.1 Research Methodology Overview

`[REPO]` The CaseMetrology thesis evaluates a static computer-vision system for dimensional measurement of cartridge-case overall length (OAL).

`[REPO]` The study is organized as a prospective engineering validation in which a frozen computer-vision measurement method is compared with an independently acquired manual reference measurement process.

`[REPO]` Development, calibration characterization, estimator comparison, and prevalidation engineering are treated as method-development activities and are kept analytically separate from formal validation.

`[REPO]` The formal validation plan, acquisition procedures, failure definitions, randomization rules, and primary statistical analysis were specified before formal validation data collection.

`[REPO] [GUARDRAIL]` Prevalidation observations may be used to explain why the final method was selected, but they are not reported as formal validation results.

`[LITERATURE]` Prospective planning and randomized run sequencing are consistent with established experimental-design principles intended to support valid, objective interpretation of experimental data.
**Recommended source:** NIST/SEMATECH Engineering Statistics Handbook.

`[REPO]` The formal study is limited to OAL and does not attempt to validate other cartridge-case dimensions.

### Audit disposition for Section 3.1

**Supported now:** study purpose, scope, prospective design, development/validation separation.
**External citation:** optional but useful for general experimental-design principles.
**Formal-data dependency:** no numerical validation results belong here.

---

## 3.2 System Architecture

`[REPO]` CaseMetrology is implemented as a static backlit vision-metrology system in which image acquisition, segmentation, dimensional computation, and primary measurement-artifact creation occur on the Jetson embedded platform.

`[REPO]` The Jetson-local measurement record is authoritative for the dimensional result.

`[REPO]` Supporting network services transfer completed measurement artifacts to an office computer for persistence, engineering review, and read-only dashboard display.

`[REPO]` Network transfer is intentionally outside the dimensional-computation path; loss of the office connection does not change an already computed local OAL result.

`[REPO]` The transfer subsystem uses a durable local outbox and records delivery state so that a completed measurement can remain pending during temporary network unavailability.

`[REPO]` The office receiver verifies the transmitted record/artifact identity before treating the record as delivered.

`[REPO]` The office engineering dashboard is read-only and does not provide controls capable of altering segmentation, calibration, measurement logic, or the formal study result.

`[GUARDRAIL]` The network receiver and dashboard are supporting systems-engineering contributions and should not be presented as evidence of dimensional accuracy.

### Audit disposition for Section 3.2

**Supported now:** implemented architecture, local-authoritative result, durable transfer, read-only monitoring.
**External citation:** not required for describing the system as built.
**Formal validation dependency:** none for architectural description.

---

## 3.3 Hardware and Software Configuration

### 3.3.1 Embedded Computing Platform

`[REPO] [MANUFACTURER]` The measurement system is executed on an NVIDIA Jetson Orin Nano Super Developer Kit.

`[MANUFACTURER]` NVIDIA identifies the Jetson Orin Nano Super Developer Kit as a Jetson edge-computing developer platform.
**Source:** NVIDIA official Jetson Orin Nano Developer Kit User Guide.

`[REPO]` The actual study platform was verified on August 15, 2026, rather than inferred from the current NVIDIA software documentation.

`[REPO]` The verified platform reported aarch64 NVIDIA L4T release R39 revision 2.0 with kernel `6.8.12-1021-tegra`.

`[REPO]` `nvpmodel` reported the system operating in the 15 W power mode, mode index 0.

`[REPO]` The verified software environment included Python 3.12.3, OpenCV 4.6.0, and NumPy 1.26.4.

`[GUARDRAIL]` Current NVIDIA documentation may describe newer JetPack/L4T releases and different power modes; those current vendor descriptions must not replace the runtime state actually verified for the study platform.

### Audit disposition for 3.3.1

**Manufacturer support:** platform identity/general vendor description.
**Repository support:** actual runtime, kernel, power mode, Python/OpenCV/NumPy versions.
**Critical guardrail:** do not backfill current JetPack 7.x details into the thesis environment.

---

### 3.3.2 Camera and Optical Configuration

`[REPO] [MANUFACTURER]` Image acquisition uses an Arducam B0499 USB 3 camera based on the Sony IMX296 sensor.

`[MANUFACTURER]` Arducam's B0499 datasheet identifies the IMX296 sensor, global shutter, 1456 × 1088 active image area, YUY2 output, and a listed maximum USB 3 frame rate of 44 fps at 1456 × 1088.
**Source:** Arducam B0499 official datasheet.

`[REPO]` CaseMetrology acquisition records establish that the study configuration uses 1456 × 1088 acquisition at 44 fps.

`[REPO]` The project camera is identified by serial `Arducam_20231211_0001` and is accessed through the persistent device link `/dev/case-metrology-camera`.

`[REPO]` The installed thesis optical configuration uses an Arducam HQ Lens CS2316ZM02 with 16 mm effective focal length and CS mount.

`[REPO]` Optical-configuration continuity was verified physically without disturbing the installed lens, and the documented 16 mm configuration is the supported configuration for the validation study.

`[GUARDRAIL]` The B0499 camera datasheet describes a camera-module lens configuration that includes a 6 mm lens in the manufacturer product specification. That manufacturer lens entry must not be used to describe the actual CaseMetrology validation optic, which is independently documented as the installed 16 mm CS2316ZM02 lens.

`[GUARDRAIL]` An earlier unsupported recollection of a 25 mm lens is not thesis evidence and must not appear as the validation configuration.

`[REPO]` The camera-to-measurement-plane distance is 8.625 in, measured vertically from the front lens-barrel edge to the gauge-block resting surface.

### Audit disposition for 3.3.2

**Supported now:** camera identity, sensor, acquisition mode, serial/symlink, 16 mm lens, 8.625-in distance.
**Manufacturer source:** B0499 camera/sensor capability.
**Critical guardrail:** do not confuse the B0499 datasheet's bundled/default 6 mm lens information with the physically installed 16 mm thesis optic.

---

### 3.3.3 Backlighting and Specimen Arrangement

`[REPO]` The measurement system uses transmitted backlighting so that the cartridge case is segmented primarily from its silhouette.

`[REPO]` The physical baseline identifies a VALIKIY LED backlight sheet rated at 24 V and 36 W, installed within the measurement enclosure.

`[REPO]` The backlight is mounted within the lower panel of the 80/20 enclosure and illuminates the specimen through the clear working surface.

`[REPO]` The measurement working surface is 0.250-in nominal clear Lexan, and the installed locator material is 0.125-in nominal Lexan.

`[REPO]` The final installed fixture is maintained in place through calibration and formal validation unless a documented change becomes necessary.

`[REPO]` The cartridge case is positioned on its side for OAL imaging.

`[REPO]` Physical endpoint interpretation uses the cartridge geometry: the base/head end has rounded corner geometry and the mouth is the straighter trimmer-cut end.

`[GUARDRAIL]` Base-versus-mouth identity is not inferred solely from the algebraic sign of the PCA minimum/maximum projection.

`[REPO] [GUARDRAIL]` Exact external dimensions of the installed Lexan locator were not preserved in the current physical-baseline record and must not be invented for the thesis.

### Audit disposition for 3.3.3

**Supported now:** backlight, clear working surface, nominal material thicknesses, specimen orientation, endpoint physical rule.
**Missing detail:** exact locator external dimensions.
**Action:** omit those dimensions unless independently measured and documented without compromising the frozen system.

---

### 3.3.4 Software Environment and Configuration Control

`[REPO]` CaseMetrology software is maintained under Git version control so that measurement-affecting source changes and research decisions can be associated with preserved repository history.

`[REPO]` The formal measurement path separates image-processing, calibration, measurement, workflow, transport, and office-receiver responsibilities into distinct source modules.

`[REPO]` The frozen segmentation implementation resides in `src/image_processing/oal_segmentation.py`.

`[REPO]` The frozen PCA/extreme-mask estimator resides in `src/measurement/topdown_oal.py`.

`[REPO]` Spatial/directional calibration behavior is implemented in the OAL calibration module and was verified against the corrected August 13 angle convention before formal validation.

`[REPO]` Precommit checks used during development include Ruff linting, Black formatting verification, and Python syntax checks where applicable.

`[REPO]` Research-relevant numerical results, corrections, protocols, data controls, and configuration-verification records are documented separately from source code so that the thesis evidence chain is not dependent on code comments alone.

`[GUARDRAIL]` Version control demonstrates configuration history and traceability of development decisions; it does not by itself demonstrate metrological validity.

### Audit disposition for 3.3.4

**Supported now:** actual software environment, module separation, Git/configuration control, quality checks.
**External citation:** unnecessary for project-specific implementation.

---

### 3.3.5 Networked Data Persistence and Engineering Monitoring

`[REPO]` Completed local OAL measurements can be queued for transfer through a durable SQLite outbox.

`[REPO]` Outbox state distinguishes pending and delivered records and retains transmission-attempt and error information.

`[REPO]` Measurement transfer packages the structured measurement record with its annotated image artifact and verifies artifact identity before delivery acknowledgment is accepted.

`[REPO]` The office receiver stores received records using a local SQLite database configured for durable office-side persistence.

`[REPO]` The office engineering dashboard reads receiver data without providing write or measurement-control functions.

`[REPO]` The dashboard exposes engineering-status and recent-measurement views for supporting system observation.

`[REPO] [GUARDRAIL]` A failure of the office receiver, network path, or dashboard does not retroactively invalidate a successfully completed Jetson-local dimensional measurement; such a failure is a supporting-infrastructure condition unless it also prevents or corrupts the local formal acquisition.

`[PENDING]` Full live Windows deployment verification of the dashboard remains an integration task and is not a prerequisite for the dimensional validation method.

### Audit disposition for 3.3.5

**Supported now:** software design, durable outbox, receiver, read-only dashboard.
**Pending:** live Windows deployment verification.
**Critical scope rule:** supporting infrastructure must remain analytically separate from dimensional accuracy.

---

# B. Clean thesis-ready version

## 3.1 Research Methodology Overview

The CaseMetrology study evaluates a static computer-vision system for dimensional measurement of cartridge-case overall length (OAL). The research is structured as a prospective engineering validation in which a frozen computer-vision measurement method is compared with an independently acquired manual reference measurement process.

Development, calibration characterization, estimator comparison, and prevalidation engineering are treated as method-development activities and are analytically separated from formal validation. The formal validation plan, acquisition procedures, failure definitions, randomization rules, and primary statistical analysis were specified before formal validation data collection. Prevalidation observations are used to explain method selection and configuration freeze but are not reported as formal validation results. This prospective separation is consistent with established experimental-design principles emphasizing preplanned experimental structure and randomized run sequencing [NIST/SEMATECH ENGINEERING STATISTICS HANDBOOK].

The formal thesis validation is limited to OAL. Other cartridge-case dimensional characteristics are outside the present validation scope and are reserved for future research.

---

## 3.2 System Architecture

CaseMetrology is implemented as a static backlit vision-metrology system in which image acquisition, segmentation, dimensional computation, and primary measurement-artifact creation occur on the Jetson embedded platform. The Jetson-local measurement record is authoritative for the dimensional result.

Supporting network services transfer completed artifacts to an office computer for persistence, engineering review, and read-only dashboard display. Network transfer is intentionally outside the dimensional-computation path; temporary loss of the office connection does not alter an OAL result already computed and preserved locally. A durable local outbox records pending and delivered transfer state, while the office receiver verifies the received record and artifact before acknowledging delivery.

The office engineering dashboard provides read-only access to receiver status and recent measurements. It contains no measurement-control path capable of modifying segmentation, calibration, endpoint logic, or the formal study result. These network and monitoring components are therefore treated as supporting systems-engineering infrastructure rather than as evidence of dimensional accuracy.

---

## 3.3 Hardware and Software Configuration

### 3.3.1 Embedded Computing Platform

The measurement system is executed on an NVIDIA Jetson Orin Nano Super Developer Kit [NVIDIA SOURCE]. The actual study runtime was verified directly on August 15, 2026. The platform reported aarch64 NVIDIA L4T R39 revision 2.0 with kernel `6.8.12-1021-tegra` and was operating in the 15 W power mode. The verified software environment included Python 3.12.3, OpenCV 4.6.0, and NumPy 1.26.4.

Manufacturer documentation is used to identify the hardware platform, whereas the repository runtime record is used to describe the software and power configuration actually present during the study. Current NVIDIA software releases are therefore not substituted for the verified experimental environment.

### 3.3.2 Camera and Optical Configuration

Image acquisition uses an Arducam B0499 USB 3 camera based on the Sony IMX296 sensor. Arducam manufacturer documentation identifies the B0499 as a 1.58-MP global-shutter camera with a 1456 × 1088 active image area and a listed maximum YUY2 USB 3 frame rate of 44 fps at that resolution [ARDUCAM B0499 SOURCE]. CaseMetrology acquisition records establish use of 1456 × 1088 images at 44 fps.

The project camera is identified by serial `Arducam_20231211_0001` and is accessed using the persistent device link `/dev/case-metrology-camera`. The installed validation optic is an Arducam HQ Lens CS2316ZM02 with 16 mm effective focal length and CS mount. Optical-configuration continuity was physically verified without disturbing the lens before formal validation preparation.

The camera-to-measurement-plane distance is 8.625 in, measured vertically from the front lens-barrel edge to the gauge-block resting surface. Although the B0499 camera datasheet includes manufacturer lens information for the camera module, that specification does not define the installed CaseMetrology validation optic. The thesis optical configuration is the independently documented 16 mm CS2316ZM02 lens.

### 3.3.3 Backlighting and Specimen Arrangement

The system uses transmitted backlighting so that the cartridge case is segmented primarily from its silhouette. The physical baseline identifies a VALIKIY LED backlight sheet rated at 24 V and 36 W installed within the measurement enclosure. The specimen is supported by a 0.250-in nominal clear Lexan working surface with a 0.125-in nominal Lexan locator.

The installed fixture is maintained in place through calibration and formal validation unless a documented change becomes necessary. For OAL acquisition, the cartridge case lies on its side within the measurement region. Physical endpoint interpretation uses specimen geometry: the base/head is the end with rounded corner geometry, whereas the mouth is the straighter trimmer-cut end. Base-versus-mouth identity is therefore not inferred solely from the sign of PCA minimum and maximum projections.

Exact external dimensions of the installed locator were not preserved in the current physical-baseline record and are not asserted in the thesis.

### 3.3.4 Software Environment and Configuration Control

CaseMetrology software is maintained under Git version control so that measurement-affecting source changes and research decisions can be associated with preserved repository history. The implementation separates image processing, calibration, dimensional measurement, workflow, transport, and office-receiver responsibilities into distinct modules.

The frozen segmentation implementation is maintained in `src/image_processing/oal_segmentation.py`, while the PCA/extreme-mask estimator is implemented in `src/measurement/topdown_oal.py`. Spatial/directional calibration is implemented separately and was verified against the corrected directional convention before formal validation.

Development quality checks include Ruff linting, Black formatting verification, and Python syntax checks where applicable. Research-relevant numerical results, protocols, calibration records, corrections, and configuration decisions are also preserved as explicit research records so that thesis evidence is not dependent on source code alone. Version control provides configuration and chronology evidence but is not itself treated as proof of metrological validity.

### 3.3.5 Networked Data Persistence and Engineering Monitoring

Completed local OAL measurements can be queued for transfer using a durable SQLite outbox that records pending/delivered state, transmission attempts, and error information. The transfer workflow packages the structured measurement record with its annotated image artifact and verifies artifact identity as part of the delivery process.

The office receiver provides independent persistence of received records, and the engineering dashboard exposes read-only status and recent-measurement views. These supporting components do not modify the locally computed dimensional result. Failure of the office receiver, network path, or dashboard therefore does not retroactively invalidate a successfully completed Jetson-local measurement unless the condition also affects the local formal acquisition itself.

Live Windows deployment verification of the office dashboard remains a supporting integration task and is not a prerequisite for the dimensional validation method.

---

# C. Verified source-placement record

## NVIDIA Jetson Orin Nano Super Developer Kit

**Source:** NVIDIA official Jetson Orin Nano Developer Kit User Guide.

**Use:** Section 3.3.1 for platform identity and vendor-level platform description.

**Do not use:** current NVIDIA documentation as evidence of the actual 2026-08-15 study runtime. The repository runtime record controls that claim.

---

## Arducam B0499 IMX296 Global Shutter USB3.0 Camera

**Source:** Arducam official B0499 datasheet.

Verified vendor-level items:
- IMX296 sensor;
- global shutter;
- 1456 × 1088 active area;
- YUY2 output;
- USB 3 listed frame rate of 44 fps at 1456 × 1088.

**Use:** Section 3.3.2.

**Important optical distinction:** the B0499 datasheet's own lens specification is not the installed CaseMetrology thesis lens. The installed validation optic is separately documented as the CS2316ZM02 16 mm CS-mount lens.

---

## NIST/SEMATECH Engineering Statistics Handbook

**Use:** Section 3.1 only for general prospective/randomized experimental-design principles.

**Do not imply:** CaseMetrology is a factorial process DOE merely because NIST DOE terminology is cited.

---

# D. Chapter 3 sentence-level audit coverage after this artifact

- 3.1 — audited
- 3.2 — audited
- 3.3.1 — audited
- 3.3.2 — audited
- 3.3.3 — audited
- 3.3.4 — audited
- 3.3.5 — audited
- 3.4 — audited in separate artifact
- 3.5 — audited in separate artifact
- 3.6 — audited in separate artifact
- 3.7 — audited in separate artifact
- 3.8 — audited in separate artifact
- 3.9 — audited in separate artifact
- 3.10 — audited in separate artifact
- 3.11 — audited in separate artifact
- 3.12 — audited in separate artifact
- 3.13 — audited in separate artifact
- 3.14 — audited in separate artifact
- 3.15 — audited in separate artifact
- 3.16 — audited in separate artifact
- 3.17 — audited in separate artifact

**Result:** Chapter 3 now has complete section-level evidence/citation coverage from 3.1 through 3.17, subject to the remaining certificate/formal-data dependencies and final source-formatting pass.
