# Chapter 3 — Methodology

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Degree:** M.S. Integrated Systems Design & Dynamics, Kansas State University
**Working draft date:** 2026-08-20
**Status:** Integrated evidence-audited working draft; formal validation results do not yet exist.

> **Draft-control note:** Citation labels in square brackets are working placeholders and should be converted to the final committee/program citation style only after that style is confirmed. Certificate- and formal-data-dependent statements remain prospective.

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

The installed clear Lexan measurement assembly remained in place through calibration and formal V1 validation. During formal CV acquisition, however, the 0.125-in nominal Lexan locator was not used to register or mechanically constrain the specimens. Each cartridge case was laid freely on the clear working surface within the camera viewing region. The case long axis was generally positioned approximately vertically, and the base-to-mouth direction was maintained consistently, but exact image-plane position and small angular variation were otherwise unconstrained. Physical endpoint interpretation uses specimen geometry: the base/head is the end with rounded corner geometry, whereas the mouth is the straighter trimmer-cut end. Base-versus-mouth identity is therefore not inferred solely from the sign of PCA minimum and maximum projections.

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

## 3.4 Image Acquisition and Segmentation

Images used for OAL measurement are acquired using the locked CaseMetrology camera configuration and processed as grayscale images by the frozen segmentation pipeline. For each measurement image, the corresponding blank reference is subtracted using `cv2.subtract(blank, image)` so that regions darkened by the specimen are emphasized relative to the illuminated background.

The resulting darkening image is smoothed with a 5 × 5 Gaussian filter before thresholding. Gaussian smoothing is commonly used to attenuate localized high-frequency variation prior to segmentation [IMAGE-PROCESSING SOURCE]. The blurred image is then converted to a binary mask using Otsu thresholding. Otsu's method determines an image threshold from the gray-level histogram by maximizing separation between the resulting classes [OTSU 1979].

The binary mask is processed using 3 × 3 morphological opening followed by 3 × 3 morphological closing. These operations are used to suppress small binary irregularities and stabilize the segmented object region [IMAGE-PROCESSING SOURCE]. Connected components are then evaluated, and only the largest connected foreground component is retained as the candidate cartridge-case silhouette.

The segmentation stage also produces quality information used by downstream measurement logic. During formal validation, threshold values, morphology parameters, and component-selection behavior are not adjusted on a specimen-by-specimen basis. The frozen implementation is maintained in `src/image_processing/oal_segmentation.py` and is incorporated into the verified OAL measurement pipeline.

---

## 3.5 Overall-Length Measurement Algorithm

The primary OAL pixel-length estimator selected for formal validation is the PCA/extreme-mask method implemented in `src/measurement/topdown_oal.py`. Principal component analysis constructs orthogonal principal directions from the observed data, with successive components selected to account for decreasing amounts of variation [JOLLIFFE AND CADIMA 2016]. In CaseMetrology, PCA is used geometrically to establish an initial longitudinal direction for the segmented cartridge-case point set rather than as a general dimensionality-reduction stage.

The implementation subsequently refines the longitudinal axis using exposed specimen points. OAL in pixel space is defined from the minimum and maximum accepted-mask projections along the refined measurement axis. This endpoint definition is specific to the CaseMetrology measurement method. The estimator additionally records the specimen centroid, measurement-axis angle, endpoint coordinates, component-size information, and pass/fail state required by the integrated physical-unit pipeline.

Several alternative endpoint methods were evaluated during prevalidation engineering, including a binary-geometry estimator and grayscale subpixel approaches. The development chronology was preserved under version control. PCA/extreme-mask initially served as the development baseline; a geometry-based estimator was temporarily selected on August 7, 2026; subsequent five-specimen prevalidation comparison demonstrated more favorable aggregate dimensional agreement for PCA/extreme-mask; and PCA/extreme-mask was therefore selected and frozen as the primary formal-validation estimator on August 13, 2026.

The five specimens used in the physical-unit estimator comparison—121, 146, 178, 187, and 197—are classified as development/prevalidation specimens and are excluded from the formal validation sample. Selection of the estimator during prevalidation does not constitute evidence of formal dimensional accuracy. Once formal validation begins, the segmentation behavior, endpoint definition, axis logic, quality gates, and pixel-length calculation are prohibited from being retuned using validation outcomes.

---

## 3.6 Spatial Calibration Method

Pixel measurements are converted to physical units using a Mitutoyo Grade 0 steel gauge block, identification number 253568, as the certified dimensional reference. Certificate T26A06624 reports a nominal length of 1.0000000 in and a certified central length of 1.0000024 in. The certificate reports an expanded uncertainty for central deviation of 2.4 microinches for lengths up to 4 in and identifies ASME B89.1.9-2002 as the inspection basis.

Formal calibration characterization was performed at the installed OAL measurement plane with the permanent clear Lexan measurement/locator surface in place. A coordinate-controlled 2 × 2 spatial grid, designated positions A through D, was measured using two principal gauge-block orientations. An independent position E near the center of the grid was withheld from model fitting and used for principal-direction and oblique holdout evaluation.

The accepted calibration observations demonstrated that effective image scale varied with both image position and measurement direction. Consequently, a single global pixels-per-inch value was not retained. Separate first-order spatial calibration planes were fitted to the accepted A–D observations:

\[
PPI_0(x,y)
=
516.907045
+
0.00843326411x
+
0.000817091863y,
\]

and

\[
PPI_{90}(x,y)
=
518.408825
+
0.00322556849x
+
0.00442714650y.
\]

The historical labels \(PPI_0\) and \(PPI_{90}\) are retained because they identify the gauge-block acquisition orientations from which the calibration models were derived.

A prevalidation implementation audit on August 13, 2026 identified an orientation-convention difference between the gauge-block analyzer and the cartridge-case PCA estimator. The gauge-block analyzer reported the reference block's long-axis orientation while measuring the certified short dimension perpendicular to that axis. The cartridge-case PCA estimator, by contrast, reports the direction of the OAL measurement itself. The angle-to-calibration mapping was therefore corrected before formal validation without refitting the accepted A–D calibration data.

For a segmented specimen centroid \((x_c,y_c)\) and PCA OAL direction \(\theta\), the frozen implementation resolves the effective image scale as

\[
PPI_{\mathrm{effective}}
=
\sqrt{
\left[PPI_{90}(x_c,y_c)\cos\theta\right]^2
+
\left[PPI_0(x_c,y_c)\sin\theta\right]^2
}.
\]

Under this convention, a horizontal cartridge-case OAL direction resolves to the historical \(PPI_{90}\) calibration surface, whereas a vertical OAL direction resolves to the historical \(PPI_0\) surface. Physical OAL is then calculated as

\[
L_{\mathrm{OAL}}
=
\frac{L_{\mathrm{px}}}{PPI_{\mathrm{effective}}},
\]

where \(L_{\mathrm{px}}\) is the frozen PCA/extreme-mask pixel-length result.

The August 13 correction changed only the directional interpretation of the existing calibration surfaces; it did not alter the accepted calibration observations, fitted plane coefficients, segmentation method, or PCA pixel-length estimator. Reinterpretation of the preserved oblique holdout using the corrected convention produced an equivalent dimensional residual of approximately -0.000412622 in over the approximately 1-in reference.

Accordingly, the calibration characterization supports the frozen spatial and directional conversion within the tested measurement region and physical configuration. It is not interpreted as evidence of universal sub-0.001-in calibration accuracy at arbitrary image positions or orientations. Measurement-uncertainty and traceability terminology in the final thesis should follow the JCGM Guide to the Expression of Uncertainty in Measurement and the International Vocabulary of Metrology [JCGM 100:2008; JCGM 200:2012].

---

## 3.7 Prevalidation Engineering and Method Freeze

Development and prevalidation activities were completed before formal validation and included segmentation development, estimator comparison, spatial calibration characterization, integrated-pipeline verification, and measurement-assurance checks. These activities were used to select and freeze the measurement method; their numerical outcomes are not treated as formal validation results.

The development record was intentionally preserved under version control. PCA/extreme-mask initially served as the development baseline, a geometry-based estimator was temporarily selected during the August 7, 2026 development stage, and subsequent physical-unit comparison favored PCA/extreme-mask for aggregate dimensional agreement. PCA/extreme-mask was therefore selected and frozen as the primary formal-validation estimator on August 13, 2026. Specimens 121, 146, 178, 187, and 197, which were used during that comparison, are excluded from the formal validation sample.

The frozen method includes the segmentation sequence and parameters, endpoint and axis logic, spatial/directional calibration mapping, quality gates, physical-unit conversion, and formal failure-status behavior. Any subsequent change capable of affecting dimensional output is subject to explicit validation change control. Once formal validation begins, validation outcomes cannot be used to retune the measurement method, acceptance criteria, or prespecified primary statistical analysis. This prospective separation between method development and validation is consistent with established principles of preplanned experimental design [NIST/SEMATECH DOE SOURCE].

---

## 3.8 Specimen Population and Screening

The available study population consists of 235 cartridge cases previously laser etched with unique integer identifiers from 1 through 235. The existing laser-etched identifier is used directly as the specimen `part_id`, avoiding the introduction of a second identification system. The population contains specimens spanning the available OAL range, including specimens intentionally prepared shorter or longer than nominal during earlier study preparation.

The five specimens previously used during estimator prevalidation—121, 146, 178, 187, and 197—are excluded from eligibility for formal validation. All other eligible specimens remain in the screening population regardless of whether they appear nominal, short, or long.

Before formal sample selection, the eligible population is screened using the designated manual screening process to characterize its dimensional distribution for stratification. Screening measurements are population-characterization measurements only and are not substituted for the three-replicate formal manual reference measurements subsequently obtained from selected validation specimens.

The screening record preserves specimen identity, screening reading, date, time, operator, caliper identity, session identity, reference-check information, screening classification, selection status, and explanatory notes. Screening sessions are bracketed by reference checks against the certified 1-in gauge block under the prospective measurement-assurance procedure. Final numerical session-acceptance limits remain dependent on review of the calibrated manual-reference instrument certificate.

Because screening has not yet been completed, the final population distribution and resulting stratum boundaries are not reported at this stage.

---

## 3.9 Formal Validation Sample Selection

The formal validation sample will contain 60 unique specimens selected from the eligible screened population. Selection will occur after screening using a stratified random procedure intended to preserve representation across the observed OAL distribution rather than relying on convenience or discretionary specimen selection. Stratified random sampling partitions a population into defined subgroups and applies random selection within those groups [SAMPLING SOURCE].

The CaseMetrology strata will be established from the completed screening dataset before the formal sample is drawn. Intentionally short and long eligible specimens remain within the sampling frame and are subject to the same prospective stratification and random-selection process as other eligible specimens. The five specimens used during prevalidation are removed from the eligible sampling frame before selection.

The selection process will preserve the screened population input, eligibility rules, stratification logic, random-selection procedure, and final selected identifiers so that the sample draw can be reproduced and audited. Exact stratum boundaries, counts, allocation, and the identities of the 60 selected specimens will be reported only after population screening and formal selection have been completed.

---

## 3.10 Manual Reference Measurement Method

Formal manual reference measurements use a Mitutoyo digital caliper, model 500-196-30 / CD-6"ASX, serial number B24254849, with 0.0005-in (0.01-mm) display resolution. Calibration certificate DDJ25P23P identifies the instrument as a 0–6 in digital caliper and reports an as-left indication error of 0.0000 in at 1 in. The reported expanded uncertainty at 1 in is 0.000126 in at approximately 95% confidence. The formal reference-system review accepted the caliper with documented session-control limitations before formal specimen measurement.

No calibration correction is applied to formal manual observations because the accepted certificate reports zero as-left indication error at 1 in. Metrological traceability and uncertainty are treated using the certificate evidence and the applicable VIM/GUM framework [JCGM 200:2012; JCGM 100:2008].

Before and after each formal manual measurement session, five readings of the certified gauge block are obtained with full removal and repositioning between readings. The gauge block has a certified central length of 1.0000024 in under certificate T26A06624. Session acceptance is prospectively based on reference error, within-check spread, and pre-to-post drift criteria. The frozen limits are 0.0005 in for absolute mean indication error, five-reading range, and pre-to-post mean drift.

Each selected validation specimen is measured manually three times. The specimen is fully removed and repositioned between replicate readings so that the repeated-measurement series includes positioning variation inherent in the stated manual procedure. Formal manual run order is randomized independently of computer-vision acquisition order using the preserved manual randomization seed `2026081901`. Randomization and replication are established experimental-design principles used to control run-order effects and characterize repeated-observation behavior [NIST/SEMATECH DOE SOURCE].

The formal manual study is conducted by a single operator. Accordingly, the repeated manual measurements characterize within-operator behavior under the specified measurement conditions; they do not estimate between-operator measurement reproducibility. This distinction follows the VIM separation of measurement repeatability from measurement reproducibility [JCGM 200:2012].

The manual process is treated as the study's reference measurement process rather than as an error-free determination of “true” OAL. Its calibration status, resolution, repeatability, and measurement uncertainty remain relevant to interpretation of agreement with the computer-vision method. The calibration-correction policy is frozen as no correction at 1 in. The remaining prospective statistical decision concerns the final reference-uncertainty model and treatment near the specification limits, which will follow the applicable GUM and conformity-assessment framework [JCGM 100:2008; JCGM 106:2012].

Raw manual replicate readings are preserved individually. Any specimen-level manual reference mean used in the agreement analysis is derived from those preserved observations rather than replacing the underlying measurements.

---

## 3.11 Computer-Vision Validation Measurement Method

Formal computer-vision validation used the frozen PCA/extreme-mask OAL pipeline after completion of the manual reference measurement phase. The formal study included 60 unique specimens with three CV acquisition attempts per specimen, yielding 180 planned acquisition opportunities. Each specimen was fully removed from the measurement surface between replicate acquisitions and independently replaced for the subsequent randomized round. The clear Lexan measurement assembly remained installed, but the nominal Lexan locator was not used to mechanically register or constrain specimen position. Consequently, the three formal CV observations per specimen characterize placement-dependent repeatability under independent free placement with consistent gross base-to-mouth orientation rather than repeatability under mechanically constrained location.

The CV run order is randomized independently of the manual reference-measurement order using the preserved seed `2026081902`. Each formal CV attempt is assigned one of three prospective statuses: `VALID`, `SYSTEM_FAILURE`, or `PROTOCOL_INVALID`. A system failure represents a genuine failure of the system to produce a valid result during an otherwise valid attempt and remains part of formal system-performance accounting. It is not automatically repeated merely to replace an unsuccessful result. A protocol-invalid attempt represents a documented procedural nonconformance rather than measurement-system performance; when permitted by the prospective deviation procedure, such an attempt may receive a documented replacement while the original invalid record remains preserved.

No CV result is imputed for a system failure. At least two valid CV replicates are required for calculation of the specimen-level CV mean used in the primary agreement analysis. Specimens with fewer than two valid CV replicates remain represented in availability and failure reporting but are excluded from the primary specimen-level agreement analysis. The experimental unit for the primary between-method analysis is the unique specimen rather than the individual replicate acquisition.

---

## 3.12 Randomization and Replication

Manual and computer-vision measurements use independently randomized run orders. The manual sequence uses seed `2026081901`, whereas the CV sequence uses seed `2026081902`. Each method obtains three repeated measurements per selected specimen with full removal and repositioning between replicates.

Randomization and replication are established experimental-design principles that support control of run-order effects and characterization of repeated-observation behavior [NIST/SEMATECH ENGINEERING STATISTICS HANDBOOK]. Within the present study, the replicate measurements are used to characterize repeated-measurement behavior and to construct specimen-level means for the primary agreement analysis. Replicates obtained from one specimen are not treated as independent specimens; the principal agreement dataset contains at most 60 unique specimen-level pairs.

---

## 3.13 Environmental and Measurement-Assurance Controls

Formal measurement sessions include environmental observation and reference-standard checks to document measurement conditions and identify material changes during data collection. The planned environmental instrumentation consists of a Digi-Sense WD-20250-91 thermocouple thermometer and WD-08519-54 Type-T self-adhesive surface probes. Formal claims of calibrated or metrologically traceable environmental measurement will be made only after the applicable calibration documentation has been reviewed.

Environmental conditions are treated as potential influence quantities when they can affect the measurement result [JCGM 100:2008; JCGM 200:2012]. The formal protocol records temperature observations but does not apply an automatic thermal correction to the cartridge-case or CV measurement. Earlier approximate temperature observations obtained during prevalidation are not substituted for formal calibrated environmental evidence.

Manual reference sessions are bracketed by five pre-session and five post-session readings of the certified 1-in gauge block. These checks are used to assess reference error, within-check spread, and pre-to-post drift. Final numerical acceptance limits for those checks remain dependent on review of the calibrated manual-reference instrument certificate. Formal temperature observations, session-check results, and any associated deviations will be reported only after data collection.

---

## 3.14 Data Integrity, Traceability, and Protocol Deviations

Formal study records preserve raw observations separately from derived summaries. Manual replicate readings, CV attempt-level records, status codes, specimen identifiers, timestamps, and applicable acquisition artifacts are retained so that specimen-level results can be regenerated from the underlying evidence.

Research-relevant software, protocols, calibration records, methodological decisions, and corrections are preserved under version control. The OAL evidence index and method decision log provide an additional claim-to-evidence and chronology layer over the underlying artifacts. Where SHA-256 manifests or transport records are used, they provide integrity checks for preserved or transferred artifacts.

Formal observations are not deleted solely because they are statistically inconvenient or appear to be outliers. Questionable observations are retained and dispositioned using the prospective failure/deviation framework. Material protocol deviations are documented and assessed for their effect on study validity. Methodological corrections preserve both the original evidence and the later correction rather than silently rewriting the research history.

---

## 3.15 Statistical Analysis

The primary unit of between-method agreement analysis is the unique validation specimen. For each specimen with sufficient valid CV replicates, the specimen-level CV mean is compared with the corresponding specimen-level manual reference mean. Signed error is defined as

\[
e_i = \bar{x}_{CV,i} - \bar{x}_{REF,i},
\]

such that positive values indicate CV measurements greater than the reference value and negative values indicate CV measurements less than the reference value.

The prespecified primary statistical summaries include mean bias, mean absolute error, root mean squared error, empirical 95th percentile of absolute specimen error, and maximum absolute specimen error. The empirical P95 is calculated using the prespecified nearest-rank convention; with 60 evaluable specimen-level observations, the 57th ordered absolute error represents the nearest-rank P95.

Repeated-measurement behavior is examined separately from between-method agreement using absolute differences among replicate measurements. The term repeatability is used consistently with the International Vocabulary of Metrology [JCGM 200:2012]. Error is also examined as a function of measurement magnitude and the final screening-defined strata.

Agreement between the two measurement methods is further examined using a Bland–Altman-style difference-versus-magnitude analysis. Bland and Altman showed that correlation can be misleading when the scientific question concerns agreement between measurement methods [BLAND AND ALTMAN 1986]. Correlation, if included, is therefore supplementary and does not replace the prespecified error and agreement metrics.

Classification performance is evaluated relative to the project OAL specification limits of 0.990 in and 1.010 in. Interpretation of classifications near a specification limit will incorporate the applicable reference-measurement uncertainty and prospective decision rule [JCGM 106:2012].

Computer-vision availability is defined as

\[
Availability =
\frac{N_{\mathrm{VALID}}}
{N_{\mathrm{VALID}} + N_{\mathrm{SYSTEM\_FAILURE}}}.
\]

Protocol-invalid attempts are not counted as system failures because they represent invalid procedure rather than system performance; however, the original invalid records and any permitted replacements remain documented. No observation is removed solely because its inclusion worsens the statistical performance metrics. Numerical results will be reported only after collection and analysis of the formal prospective dataset.

---

## 3.16 Validation Acceptance Criteria

The primary validation acceptance criteria were defined before formal validation data collection and will not be revised after formal results are observed. The frozen criteria require:

- CV availability of at least 99%;
- P95 absolute repositioning difference no greater than 0.002 in;
- absolute mean specimen-level bias no greater than 0.001 in;
- specimen-level RMSE no greater than 0.002 in;
- empirical P95 absolute specimen error no greater than 0.003 in; and
- maximum absolute specimen error no greater than 0.004 in.

With 180 planned CV acquisition opportunities, 179 valid attempts correspond to approximately 99.44% availability and satisfy the 99% requirement, whereas 178 valid attempts correspond to approximately 98.89% and do not.

Zero false-pass classifications are preferred. False acceptance is a recognized conformity-assessment risk, and guarded decision rules may be used to reduce that risk when appropriate [JCGM 106:2012]. The final reference classification of a specimen sufficiently near a specification limit remains dependent on the calibrated manual-reference instrument certificate and the prospectively established uncertainty/decision rule.

Unresolved material protocol deviations prevent an unconditional validation conclusion even when numerical performance thresholds are otherwise met. The numerical acceptance criteria above are CaseMetrology-specific prospective criteria and are not attributed to external standards or manufacturer specifications.

---

## 3.17 Methodological Limitations

The formal study is limited to cartridge-case overall length. It does not validate rim geometry, primer-pocket dimensions, concentricity, or other dimensional characteristics. The study evaluates a static, backlit, fixture-based measurement configuration and does not directly establish performance for conveyor-based, robotic, or otherwise dynamic production acquisition.

The validation conclusion applies to the documented camera, 16 mm CS-mount lens, measurement-plane geometry, illumination, fixture, software, segmentation, estimator, and calibration configuration used during the formal study. A materially changed optical, mechanical, lighting, calibration, or software configuration should not automatically inherit the validation conclusion without an appropriate verification or revalidation assessment.

The manual comparator is a reference measurement process rather than an error-free value. Its resolution, repeatability, calibration status, and measurement uncertainty limit the interpretation of agreement [JCGM 100:2008; JCGM 200:2012]. Because the manual study is performed by one operator, the study does not estimate between-operator reproducibility.

The formal agreement analysis contains 60 unique specimens and therefore provides a finite empirical characterization of the selected study population rather than proof of worst-case performance for every possible cartridge case. The empirical P95 and maximum observed error describe the formal sample and are not interpreted as universal physical bounds. Although the sampling population includes intentionally short and long specimens, generalization to future manufacturing populations remains constrained by the source population, sampling design, and documented study configuration.

The formal study is therefore designed to determine whether the frozen CaseMetrology OAL system satisfies its prespecified validation criteria under the documented conditions. Broader dimensional, operational, and production-line claims are reserved for future research.

---

---

# Working citation key

- `[NIST/SEMATECH ENGINEERING STATISTICS HANDBOOK]` — NIST/SEMATECH e-Handbook of Statistical Methods.
- `[NVIDIA SOURCE]` — NVIDIA official Jetson Orin Nano Developer Kit User Guide.
- `[ARDUCAM B0499 SOURCE]` — Arducam official B0499 IMX296 Global Shutter USB3.0 Camera Module datasheet.
- `[IMAGE-PROCESSING SOURCE]` — Gonzalez, R. C., & Woods, R. E., *Digital Image Processing*, 4th ed., Pearson.
- `[OTSU 1979]` — Otsu, N. (1979), “A Threshold Selection Method from Gray-Level Histograms.”
- `[JOLLIFFE AND CADIMA 2016]` — Jolliffe, I. T., & Cadima, J. (2016), PCA review.
- `[SAMPLING SOURCE]` — Lohr, S. L. (2022), *Sampling: Design and Analysis*, 3rd ed.
- Calibration certificate DDJ25P23P and preserved instrument/case identity images — primary project evidence for the actual manual-reference instrument.
- `[JCGM 100:2008]` — Guide to the Expression of Uncertainty in Measurement (GUM).
- `[JCGM 200:2012]` — International Vocabulary of Metrology (VIM).
- `[JCGM 106:2012]` — role of measurement uncertainty in conformity assessment.
- `[BLAND AND ALTMAN 1986]` — Bland, J. M., & Altman, D. G. (1986), measurement-method agreement.
- Gauge-block certificate T26A06624 — primary project certificate evidence; ASME B89.1.9-2002 is its stated inspection basis.

# Explicitly unresolved before final Chapter 3

1. Final manual-reference uncertainty model and near-specification decision rule.
2. Certificate-derived correction, uncertainty treatment, `E_limit`, `R_limit`, and `D_limit`.
3. Environmental thermometer/probe calibration documentation.
4. Completed 235-case screening distribution.
5. Final stratum boundaries and allocation.
6. Final 60-specimen selection.
7. Any formal-session environmental observations or deviations.
8. Final citation/reference style specified by the program or supervisory committee.

# Formal-results boundary

No formal validation numerical result belongs in this Chapter 3 working draft. Bias, MAE, RMSE, empirical P95 error, maximum error, availability, Bland–Altman results, classification performance, and final pass/fail conclusions belong in Chapter 4 only after the prospective formal dataset exists.
