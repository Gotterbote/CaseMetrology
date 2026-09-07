# CaseMetrology Thesis — Working Manuscript v3

**Researcher:** Timmy D. Bell
**Degree:** M.S. Integrated Systems Design & Dynamics
**Institution:** Kansas State University
**Status:** Whole-manuscript review copy; not final ETDR formatting

---

# Chapter 1 — Introduction

## 1.1 Background and Motivation

Machine vision has become an established approach for industrial inspection and measurement, including applications concerned with dimensional quality, surface condition, structural characteristics, and operational state (Malamas et al., 2003). Manufacturing-oriented research has also demonstrated the use of cameras, computing hardware, and image-processing methods for rapid, non-contact assessment of geometric and process-related characteristics (Hashmi et al., 2022).

For dimensional applications, however, the production of a plausible numerical value by an image-processing algorithm is not sufficient by itself to establish measurement suitability. Calibration, measurement uncertainty, measurement conditions, and the relationship of the result to an appropriate reference remain important metrological considerations (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b).

Computerized optical analysis of cartridge cases is well established in forensic research, particularly for the acquisition, segmentation, and comparison of breech-face, firing-pin, ejector, and related surface features. NIST Standard Reference Material 2461, for example, supports quality assurance and measurement traceability for computerized optical imaging of cartridge-case topography (National Institute of Standards and Technology, n.d.). This forensic literature demonstrates that cartridge cases can be analyzed using controlled optical and computational methods, but its measurement targets and intended use differ from manufacturing dimensional inspection.

The present research addresses a narrower manufacturing-metrology problem: computer-vision measurement of cartridge-case overall length from a controlled static, backlit side-view image. Overall length was selected as the formal thesis measurement characteristic so that the calibration, measurement, reference, repeated-measurement, and agreement problems could be studied rigorously without expanding the project into simultaneous validation of multiple case dimensions.

## 1.2 Problem Statement

A functioning computer-vision algorithm is not equivalent to a validated dimensional measurement method. CaseMetrology development and prevalidation established a frozen segmentation pipeline, PCA/extreme-mask OAL estimator, spatial and directional calibration model, controlled physical configuration, and prospective statistical analysis plan. The formal validation study therefore evaluated whether that frozen system produced OAL measurements with acceptable agreement, repeated-measurement behavior, availability, and classification performance relative to an independent manual reference measurement process on the prospectively selected specimen sample.

The literature review in Chapter 2 establishes how the present manufacturing OAL problem relates to prior vision-based dimensional-metrology research and to the broader cartridge-case imaging literature. Accordingly, this thesis does not make a categorical claim that optical or computer-assisted cartridge-case dimensional inspection is unprecedented.

## 1.3 Purpose of the Study

The purpose of this study is to evaluate the dimensional performance of the frozen CaseMetrology computer-vision system for static measurement of cartridge-case overall length under controlled inspection conditions. The evaluation compares specimen-level computer-vision measurements with independently acquired manual reference measurements and applies prospectively defined criteria for agreement, repeated-measurement behavior, system availability, and classification performance.

The study is limited to validation of the documented OAL measurement method. It does not attempt to validate all cartridge-case dimensions or an inline production inspection system.

## 1.4 Research Question

The primary research question is:

> **Can the frozen CaseMetrology computer-vision system measure cartridge-case overall length with acceptable agreement and repeated-measurement performance relative to an independent manual reference measurement process under the documented static inspection conditions?**

Acceptable performance was defined by prospectively established validation criteria rather than by thresholds selected after formal data were observed.

## 1.5 Research Objectives

The study has five objectives:

1. Define and freeze the static backlit imaging configuration, acquisition settings, segmentation procedure, PCA/extreme-mask OAL estimator, and software environment before formal validation.
2. Characterize spatial and directional image scale using a certified gauge-block reference and freeze the physical-unit calibration model and angle convention before formal validation.
3. Establish a controlled manual reference measurement procedure incorporating calibration-certificate review, certified check-standard controls, repeated measurements, and documented session-acceptance criteria.
4. Screen the eligible source population, select a 60-specimen stratified random validation sample, and acquire three manual reference measurements and three computer-vision attempts per selected specimen using independently randomized run orders.
5. Quantify repeated-measurement behavior, availability, measurement agreement, error magnitude, and classification performance using the prospectively frozen statistical analysis plan and acceptance criteria.

## 1.6 Scope and Delimitations

The formal thesis evaluates cartridge-case overall length only. Rim geometry, primer-pocket dimensions, concentricity, and other case characteristics are outside the validation scope and are reserved for future research.

The measurement system is evaluated in a static configuration. The study does not validate conveyor-based inspection, moving workpieces, robotic handling, or high-speed inline manufacturing operation. The validation conclusion is specific to the documented camera, 16 mm CS-mount lens, illumination, measurement-plane geometry, installed clear Lexan measurement assembly, segmentation pipeline, estimator, calibration model, and software configuration used during the study.

The source population consisted of 235 uniquely laser-etched cases. Five specimens previously used during estimator prevalidation were excluded from formal eligibility, leaving 230 eligible specimens. Following screening, 60 unique specimens were selected using the prospectively defined stratified random procedure.

The manual reference study used a single operator. Consequently, the design characterizes within-operator repeated-measurement behavior under the specified conditions but does not estimate between-operator measurement reproducibility (Joint Committee for Guides in Metrology, 2012b). Results are interpreted as empirical findings for the selected population and documented study configuration rather than universal worst-case limits.

## 1.7 Significance of the Study

Industrial machine vision can support dimensional inspection and automated extraction of manufacturing-quality information, but application-specific measurement definitions, controlled image acquisition, calibration, and performance evaluation remain necessary for defensible dimensional use (Malamas et al., 2003; Hashmi et al., 2022).

The contribution of CaseMetrology is therefore the development and prospective evaluation of a complete embedded computer-vision metrology workflow rather than image processing alone. The study integrates physical configuration control, a certified calibration reference, a frozen segmentation and OAL estimator, an independent manual reference process, prospective specimen selection, explicit failure accounting, prespecified statistical analysis, and research-evidence preservation.

The formal validation showed that the documented V1 configuration did not satisfy the overall prespecified validation criteria under the tested conditions. This result nevertheless provides empirical evidence about the performance and limitations of the frozen measurement architecture, while the methodology and preserved evidence record provide a basis for future research involving additional cartridge-case dimensions, operators, optical configurations, or dynamic production inspection.

The present thesis does not claim that CaseMetrology is lower cost, faster than manual inspection, production-ready, or suitable for full-rate inline inspection because those questions are outside the formal study design.

## 1.8 Organization of the Thesis

Chapter 1 introduces the research problem, purpose, research question, objectives, scope, and significance. Chapter 2 reviews relevant literature in industrial machine vision, vision-based dimensional metrology, calibration and uncertainty, measurement-method agreement, and cartridge-case imaging where applicable to the research context.

Chapter 3 describes the CaseMetrology hardware and software configuration, frozen OAL measurement method, spatial and directional calibration, prevalidation and method-freeze controls, specimen population and sample-selection method, manual reference procedure, computer-vision validation procedure, randomization, environmental and measurement-assurance controls, data governance, statistical analysis plan, acceptance criteria, and methodological limitations.

Chapter 4 reports the formal validation results generated from the prospective study. Chapter 5 interprets those findings, answers the research question, states the resulting conclusions and limitations, and identifies appropriate directions for future work.

---

---

# Chapter 2 — Literature Review

## 2.1 Introduction

Machine vision is widely used in industrial inspection to obtain information
about manufactured parts without relying exclusively on manual visual or
contact-based inspection. Applications include dimensional inspection, surface
evaluation, feature recognition, process monitoring, and automated
classification (Malamas et al., 2003; Hashmi et al., 2022). When the objective
is dimensional measurement rather than detection or classification, however,
the production of a numerical value from an image is not by itself sufficient
to establish measurement quality. The result also depends on the relationship
among image formation, calibration, physical geometry, feature localization,
reference standards, repeated-measurement behavior, and the intended
measurement decision.

This distinction is central to the CaseMetrology research problem. The present
study concerns static computer-vision measurement of cartridge-case overall
length (OAL), but the relevant literature extends beyond cartridge cases alone.
Prior work in dimensional machine vision provides guidance regarding optical
measurement architecture, calibration, uncertainty, edge and contour
localization, specimen presentation, and reference comparison. Historical cartridge-case inspection research also establishes that
electro-optical dimensional measurement of cartridge cases, including total
length, predates the present system (Swinth et al., 1979; Coleman & Swinth, 1977; Coleman et al., 1974).

Accordingly, this chapter reviews four related bodies of literature:
industrial machine vision and dimensional inspection; vision-based dimensional
metrology; calibration, traceability, uncertainty, and measurement-system
evaluation; and optical or computational analysis of cartridge cases. The
chapter concludes by positioning CaseMetrology within that established
research space without assuming that optical cartridge-case dimensional
measurement itself is novel.

## 2.2 Industrial Machine Vision and Dimensional Inspection

Industrial machine vision combines image acquisition, computation, and
application-specific interpretation to extract information about manufactured
objects and processes. Malamas et al. described industrial vision systems as
supporting a broad range of inspection functions and emphasized that useful
systems require clear definitions of inspection objectives, inputs, outputs,
and operating conditions (Malamas et al., 2003). More recent manufacturing
literature similarly demonstrates the continued use of cameras and image
processing for process monitoring and measurement-oriented applications
(Hashmi et al., 2022).

For dimensional inspection, the important transition is from recognizing an
object or feature to assigning a defensible physical dimension. A dimensional
machine-vision system must relate image coordinates to physical units and must
define how the relevant physical boundaries are located in the image. The measurement is therefore influenced by both the physical imaging
system and the computational procedure used to interpret the image
(Hemming, 2007; Lazzari & Iuculano, 2004).

This complete-system view distinguishes dimensional metrology from a purely
algorithmic computer-vision task. Sensor resolution alone does not define
dimensional accuracy, and successful segmentation alone does not establish the
relationship between a measured image feature and a traceable physical
dimension. Optical geometry, illumination, calibration, object presentation,
boundary localization, and reference comparison become part of the
measurement problem (Hemming, 2007; Lazzari & Iuculano, 2004).

For CaseMetrology, this distinction motivates evaluation of the complete frozen
OAL method rather than evaluation of segmentation performance in isolation.
The relevant research question is therefore not simply whether a cartridge
case can be detected or measured computationally, but whether the complete
computer-vision measurement process demonstrates acceptable dimensional
behavior relative to an independent reference process under defined conditions.

## 2.3 Vision-Based Dimensional Metrology

### 2.3.1 Backlit and silhouette-based dimensional measurement

Backlighting is a well-established image-formation approach for dimensional
inspection because it can produce high contrast between a manufactured object
and its background. In such systems, dimensional information is derived from the location and
geometric interpretation of the resulting object boundary
(Shin et al., 2002; Xiang et al., 2018; Che & Ratnam, 2018).

Shin, Han, and Moon developed a machine-vision system for dimensional
inspection of ball studs using silhouetted images generated by backlighting
(Shin et al., 2002). Object outlines were extracted at subpixel resolution and
modeled using geometric primitives. The system also incorporated jig fixtures
and servo-controlled motion to position and rotate the inspected component.
This work provides a useful example of the integration of illumination,
boundary localization, geometric modeling, and controlled specimen
presentation in dimensional machine vision.

Xiang et al. used a two-camera backlit system for dimensional measurement of
automobile brake-pad bayonets (Xiang et al., 2018). Their method incorporated a
specially designed dimensional standard, relative edge-position measurement,
edge detection, and line fitting. The study is particularly relevant because
measurement behavior was evaluated in terms of both systematic dimensional
difference and repeatability rather than only whether the vision algorithm
could identify the measured feature.

Che and Ratnam similarly used LED backlighting and subpixel edge localization
for real-time monitoring of workpiece diameter during turning (Che & Ratnam, 2018). Their image-derived measurements were compared quantitatively with
digital-caliper measurements. Although the machining geometry and reference
process differed from the CaseMetrology study, the work provides useful
precedent for evaluating machine-vision dimensions against an independent
physical measurement method.

Together, these studies show that backlit dimensional vision can involve
more than thresholding an object silhouette. Physical presentation, edge
location, dimensional calibration, and an external basis for evaluating the
result can be integral components of the measurement process
(Shin et al., 2002; Xiang et al., 2018; Che & Ratnam, 2018).

### 2.3.2 Optical geometry and measurement-plane effects

The geometric relationship between the camera, calibrated coordinate system,
and measured object can materially influence monocular dimensional
measurement.

Wang et al. analyzed measurement error arising when the physical measurement
plane differs from the plane associated with camera calibration (Wang et al., 2024). Their theoretical and experimental work considered translation and
rotation between calibration and measurement geometry and demonstrated that
external camera parameters can influence dimensional results. The experiments
included both conventional industrial and telecentric optics.

The importance of Wang et al. is broader than any specific error equation. The study demonstrates that dimensional accuracy can depend on the
geometric relationship represented during calibration and that departures
from that relationship can introduce measurement error even when the
image-processing algorithm itself remains unchanged (Wang et al., 2024).

This principle is relevant to any monocular dimensional measurement system.
The physical configuration of the camera, lens, measurement plane, and
specimen cannot be treated as incidental to the dimensional result. At the same time, a general geometric mechanism identified in the
literature should not be assumed to explain the behavior of another system
unless the relevant physical variable has been experimentally isolated
(Wang et al., 2024).

### 2.3.3 Telecentric and high-precision dimensional vision

Modern high-precision vision systems often use telecentric optics to reduce
perspective sensitivity and maintain comparatively stable magnification over a
limited depth range. Lai et al. developed a telecentric dimensional-vision
system that jointly addressed calibration, distortion correction, contour
geometry, subpixel edge localization, and illumination variation (Lai et al., 2026).

Their work demonstrates several principles relevant beyond telecentric systems.
First, the calibration model should correspond to the optical architecture
being modeled. Second, dimensional calibration may benefit from geometric
information distributed across object contours rather than relying only on
isolated calibration points. Third, dimensional measurement can require
subpixel localization of boundaries when the required physical discrimination
is finer than one image pixel. Finally, illumination behavior can influence the estimated position of an
image boundary (Lai et al., 2026).

Telecentric performance cannot be transferred directly to a conventional-lens
system such as CaseMetrology. Nevertheless, the study provides contemporary evidence that high-precision
dimensional vision can require integrated treatment of optics, calibration,
distortion, image formation, and feature localization rather than a single
image-processing operation (Lai et al., 2026).

## 2.4 Calibration, Traceability, and Measurement Uncertainty

### 2.4.1 Metrological framework

The International Vocabulary of Metrology distinguishes concepts including
measurement result, calibration, metrological traceability, measurement
repeatability, and measurement reproducibility (Joint Committee for Guides in Metrology, 2012b). The Guide to
the Expression of Uncertainty in Measurement provides a general framework for
evaluating and combining uncertainty contributions associated with a
measurement result (Joint Committee for Guides in Metrology, 2008).

These principles are particularly important for computer-vision dimensional
measurement because the observed image is not itself a physical dimension.
Image information must be connected to physical units through a defined
measurement model and appropriate dimensional references
(Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b).

A calibrated artifact or scale relationship therefore provides only one part
of the measurement chain. Additional contributions may arise from optical geometry, image formation,
localization of the measured feature, mechanical relationships,
environmental influence quantities, repeated-observation variation, and
characteristics of the measured object
(Hemming, 2007; Lazzari & Iuculano, 2004).

### 2.4.2 Machine-vision traceability and complete-system uncertainty

Hemming examined dimensional machine-vision applications specifically from the
perspective of traceability and measurement uncertainty (Hemming, 2007). His
work considered two-dimensional camera-based systems and demonstrated that the
dominant uncertainty source can differ among applications. In some cases,
camera, lens, and edge-finding behavior can make an important contribution,
while in other applications mechanical or geometrical factors can dominate.

A major implication is that the principal source of dimensional error should
not be assumed from intuition. Different components of the complete
measurement system may need to be evaluated independently.

Hemming's treatment is directly relevant to the distinction between an
image-processing result and a metrologically characterized measurement
process. It supports consideration of illumination, optics, geometry, mechanical
behavior, edge localization, object characteristics, and calibration as
potentially interacting contributors to dimensional measurement
(Hemming, 2007).

### 2.4.3 Optical vision machines and uncertainty evaluation

Lazzari and Iuculano similarly treated a camera-equipped optical measurement
machine as a metrological system rather than only an imaging device (Lazzari & Iuculano, 2004). Their work developed a GUM-oriented mathematical model for
measurement uncertainty and conceptually separated contributions associated
with the physical measuring machine from those associated with the vision or
survey subsystem.

An important conclusion of this research is that verification of instrument
performance and evaluation of measurement uncertainty are related but distinct
activities. Demonstrating that a measurement system operates within an observed range
does not by itself establish the uncertainty associated with each measurement
result (Lazzari & Iuculano, 2004).

Related work from the same research program also used certified dimensional
standards, repeated measurements, and experimental separation of machine and
camera-related behavior (Lazzari et al., 2001). This provides useful precedent
for isolating potential contributors to complete-system dimensional behavior
rather than assigning all observed disagreement to one assumed source.

These works also establish an important boundary for the present thesis.
CaseMetrology evaluates a calibrated manual reference process and empirically
characterizes the CV system through agreement and repeated-measurement metrics,
but the formal study does not claim to provide a complete GUM uncertainty
budget for the entire computer-vision measurement system.

## 2.5 Measurement-System Evaluation and Method Agreement

A dimensional measurement system may produce highly correlated values with
another method while still exhibiting systematic or practically important
disagreement. Bland and Altman demonstrated that correlation is not an
appropriate substitute for agreement analysis when two measurement methods are
being compared (Bland & Altman, 1986). Difference-based analysis is therefore
important when the scientific question concerns whether two methods return
sufficiently similar measurement results.

For the present CaseMetrology study, measurement-system evaluation includes
several distinct properties:

- measurement availability or failure behavior;
- systematic difference or bias relative to a reference process;
- absolute dimensional error;
- repeated-measurement variation;
- behavior across the measurement range;
- classification performance when dimensions are used for conformance
  decisions; and
- uncertainty associated with the reference and decision process.

These properties answer different questions. A system can exhibit strong
linear association while failing an engineering agreement criterion, or it can
produce measurements reliably while exhibiting excessive dimensional error.

The NIST/SEMATECH Engineering Statistics Handbook also emphasizes the roles of
randomization and replication in experimental work (NIST/SEMATECH, n.d.). Replication provides information about repeated
observations, while randomized run sequencing can reduce systematic coupling
between measurement order and uncontrolled temporal effects.

Sampling design likewise affects the interpretation of a validation study.
Stratified sampling can preserve representation across predefined portions of
a population when simple convenience sampling would not adequately represent
the measurement range (Lohr, 2022).

These statistical and experimental principles support treating dimensional
machine-vision validation as a prospective measurement-system study rather
than as an informal comparison of selected example images.

## 2.6 Historical Cartridge-Case Dimensional Inspection

Optical dimensional inspection of cartridge cases predates modern
general-purpose computer vision.

Historical work at Pacific Northwest Laboratory and Battelle developed
high-speed electro-optical inspection systems for manufactured cartridge
cases. These systems measured multiple case dimensions, including total
length, and integrated dimensional measurement with automated inspection,
process monitoring, and rejection (Swinth et al., 1979; Coleman & Swinth, 1977; Coleman et al., 1974).

Swinth, Walker, and Nedrow described a high-throughput profile-monitor system
that used transmitted illumination, projected cartridge-case shadows,
fiber-optic image transfer, linear sensing arrays, and precision mechanical
gauging features (Swinth et al., 1979). The
system measured several cartridge-case dimensions, including total length.

Coleman and Swinth described an automatic cartridge-case inspection and process
control system incorporating electro-optical dimensional measurement,
calibration and quality-assurance functions, automatic rejection, and
comparison with conventionally gauged case dimensions (Coleman & Swinth, 1977).

Earlier work by Coleman and colleagues similarly documented an on-line
automatic high-speed cartridge-case inspection system using electro-optical
profile measurement, computer control, calibration standards, and automatic
classification (Coleman et al., 1974).

These sources have two important implications for the present thesis.

First, optical or electro-optical measurement of cartridge-case total length is
not a new concept. Historical manufacturing systems had already demonstrated
total-length measurement, multiple dimensional measurements, calibration
checks, computer-assisted inspection, and automatic rejection.

Second, those historical systems used substantially different architectures
from CaseMetrology. They relied heavily on dedicated mechanical handling,
gauging fixtures, optical projection, and linear sensor arrays. CaseMetrology
instead employs a modern two-dimensional area camera, embedded computation,
software-defined image processing, preserved raw imagery, and an explicit
prospective validation framework.

The historical literature therefore establishes relevant prior art while also
helping define the narrower research space occupied by the present study.

## 2.7 Modern Cartridge-Case Optical and Computational Analysis

Modern cartridge-case imaging literature is dominated by forensic applications
rather than manufacturing dimensional metrology.

Computerized optical analysis has been used to acquire and compare breech-face,
firing-pin, ejector, and related surface features on cartridge cases. NIST
Standard Reference Material 2461 provides a cartridge-case reference artifact
for quality assurance in computerized optical topography and forensic
comparison systems (National Institute of Standards and Technology, n.d.).

Additional research has addressed automated cartridge-case image matching and
automatic identification of regions of interest in cartridge-case imagery
(Yammen & Muneesawang, 2013; Sakarya et al., 2012).

This literature establishes that controlled optical acquisition and
computational analysis of cartridge cases are established research topics.
However, the measurement targets represented by these sources are principally
forensic surface marks and topographic comparison rather than manufacturing
OAL measurement (National Institute of Standards and Technology, n.d.; Yammen & Muneesawang, 2013; Sakarya et al., 2012).

Accordingly, forensic cartridge-case literature is relevant contextual
evidence but should not be interpreted as validation of dimensional
manufacturing inspection or cartridge-case OAL accuracy.

## 2.8 Literature Synthesis and Research Position

The reviewed literature establishes several consistent principles relevant to
CaseMetrology.

First, dimensional machine vision is a complete measurement-system problem.
Optical geometry, illumination, specimen presentation, calibration, boundary
localization, dimensional conversion, reference comparison, and statistical
evaluation can all influence the measurement result
(Hemming, 2007; Lazzari & Iuculano, 2004; Wang et al., 2024; Lai et al., 2026).

Second, calibration is necessary but does not by itself establish complete
measurement quality. Hemming and Lazzari and Iuculano demonstrate the
importance of traceability and uncertainty across the full measurement chain,
while Wang et al. shows that physical geometry relative to the calibrated
measurement condition can affect monocular dimensional results
(Hemming, 2007; Lazzari & Iuculano, 2004; Wang et al., 2024).

Third, backlit silhouette measurement is an established technique for
dimensional inspection. Shin et al., Xiang et al., and Che and Ratnam provide
examples in which transmitted illumination, boundary localization, geometric
measurement, and reference comparison are integrated into industrial
measurement systems. Lai et al. provides a contemporary high-precision example
showing the continued importance of calibration, distortion, and subpixel
boundary localization (Shin et al., 2002; Xiang et al., 2018; Che & Ratnam, 2018; Lai et al., 2026).

Fourth, optical cartridge-case dimensional inspection itself is not novel.
Historical electro-optical inspection systems measured total cartridge-case
length and other case dimensions decades before the present work
(Swinth et al., 1979; Coleman & Swinth, 1977; Coleman et al., 1974).

The research position of CaseMetrology must therefore be narrower than a claim
of first optical or computer-assisted cartridge-case measurement.

The present study instead evaluates a modern embedded area-camera approach to
static cartridge-case OAL measurement using a defined physical configuration,
software-defined silhouette and dimensional estimator, spatial and directional
calibration, independent manual reference process, repeated measurements,
prospective specimen selection, randomized acquisition, explicit failure
accounting, predefined engineering acceptance criteria, and preserved software
and data provenance.

The contribution lies in the integration and prospective evaluation of this
particular measurement architecture and research methodology rather than in
the invention of optical cartridge-case dimensional inspection.

The literature also identifies several factors that may be relevant to future
system development, including controlled specimen presentation, optical
architecture, measurement-plane geometry, distortion, subpixel boundary
localization, illumination stability, and complete-system uncertainty
evaluation. These factors represent experimentally testable directions for future work.
Their identification in prior literature does not, by itself, establish the
cause of any observed behavior in the present measurement system
(Hemming, 2007; Shin et al., 2002; Wang et al., 2024; Lai et al., 2026).

---

---

# Chapter 3 — Methodology

## 3.1 Research Methodology Overview

The CaseMetrology study evaluates a static computer-vision system for dimensional measurement of cartridge-case overall length (OAL). The research is structured as a prospective engineering validation in which a frozen computer-vision measurement method is compared with an independently acquired manual reference measurement process.

Development, calibration characterization, estimator comparison, and prevalidation engineering are treated as method-development activities and are analytically separated from formal validation. The formal validation plan, acquisition procedures, failure definitions, randomization rules, and primary statistical analysis were specified before formal validation data collection. Prevalidation observations are used to explain method selection and configuration freeze but are not reported as formal validation results. This prospective separation is consistent with established experimental-design principles emphasizing preplanned experimental structure and randomized run sequencing (NIST/SEMATECH, n.d.).

The formal thesis validation is limited to OAL. Other cartridge-case dimensional characteristics are outside the present validation scope and are reserved for future research.

---

## 3.2 System Architecture

CaseMetrology is implemented as a static backlit vision-metrology system in which image acquisition, segmentation, dimensional computation, and primary measurement-artifact creation occur on the Jetson embedded platform. The Jetson-local measurement record is authoritative for the dimensional result.

Supporting network services transfer completed artifacts to an office computer for persistence, engineering review, and read-only dashboard display. Network transfer is intentionally outside the dimensional-computation path; temporary loss of the office connection does not alter an OAL result already computed and preserved locally. A durable local outbox records pending and delivered transfer state, while the office receiver verifies the received record and artifact before acknowledging delivery.

The office engineering dashboard provides read-only access to receiver status and recent measurements. It contains no measurement-control path capable of modifying segmentation, calibration, endpoint logic, or the formal study result. These network and monitoring components are therefore treated as supporting systems-engineering infrastructure rather than as evidence of dimensional accuracy.

---

## 3.3 Hardware and Software Configuration

### 3.3.1 Embedded Computing Platform

The measurement system is executed on an NVIDIA Jetson Orin Nano Super Developer Kit (NVIDIA Corporation, 2026). The actual study runtime was verified directly on August 15, 2026. The platform reported aarch64 NVIDIA L4T R39 revision 2.0 with kernel `6.8.12-1021-tegra` and was operating in the 15 W power mode. The verified software environment included Python 3.12.3, OpenCV 4.6.0, and NumPy 1.26.4.

Manufacturer documentation is used to identify the hardware platform, whereas the repository runtime record is used to describe the software and power configuration actually present during the study. Current NVIDIA software releases are therefore not substituted for the verified experimental environment.

### 3.3.2 Camera and Optical Configuration

Image acquisition uses an Arducam B0499 USB 3 camera based on the Sony IMX296 sensor. Arducam manufacturer documentation identifies the B0499 as a 1.58-MP global-shutter camera with a 1456 × 1088 active image area and a listed maximum YUY2 USB 3 frame rate of 44 fps at that resolution (Arducam, 2024). CaseMetrology acquisition records establish use of 1456 × 1088 images at 44 fps.

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

With the physical and software configuration established, the measurement sequence begins with controlled image acquisition and silhouette extraction. Images used for OAL measurement are acquired using the locked CaseMetrology camera configuration and processed as grayscale images by the frozen segmentation pipeline. For each measurement image, the corresponding blank reference is subtracted using `cv2.subtract(blank, image)` so that regions darkened by the specimen are emphasized relative to the illuminated background.

The resulting darkening image is smoothed with a 5 × 5 Gaussian filter before thresholding. Gaussian smoothing is commonly used to attenuate localized high-frequency variation prior to segmentation (Gonzalez & Woods, 2018). The blurred image is then converted to a binary mask using Otsu thresholding. Otsu's method determines an image threshold from the gray-level histogram by maximizing separation between the resulting classes (Otsu, 1979).

The binary mask is processed using 3 × 3 morphological opening followed by 3 × 3 morphological closing. These operations are used to suppress small binary irregularities and stabilize the segmented object region (Gonzalez & Woods, 2018). Connected components are then evaluated, and only the largest connected foreground component is retained as the candidate cartridge-case silhouette.

The segmentation stage also produces quality information used by downstream measurement logic. During formal validation, threshold values, morphology parameters, and component-selection behavior are not adjusted on a specimen-by-specimen basis. The frozen implementation is maintained in `src/image_processing/oal_segmentation.py` and is incorporated into the verified OAL measurement pipeline.

---

## 3.5 Overall-Length Measurement Algorithm

The primary OAL pixel-length estimator selected for formal validation is the PCA/extreme-mask method implemented in `src/measurement/topdown_oal.py`. Principal component analysis constructs orthogonal principal directions from the observed data, with successive components selected to account for decreasing amounts of variation (Jolliffe & Cadima, 2016). In CaseMetrology, PCA is used geometrically to establish an initial longitudinal direction for the segmented cartridge-case point set rather than as a general dimensionality-reduction stage.

The implementation subsequently refines the longitudinal axis using exposed specimen points. OAL in pixel space is defined from the minimum and maximum accepted-mask projections along the refined measurement axis. This endpoint definition is specific to the CaseMetrology measurement method. The estimator additionally records the specimen centroid, measurement-axis angle, endpoint coordinates, component-size information, and pass/fail state required by the integrated physical-unit pipeline.

Alternative endpoint methods, including binary-geometry and grayscale subpixel approaches, were evaluated during prevalidation engineering. The resulting estimator-selection chronology, development-specimen exclusions, and method-freeze boundary are described in Section 3.7. Selection of the final estimator during prevalidation does not itself constitute evidence of formal dimensional accuracy.

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

Accordingly, the calibration characterization supports the frozen spatial and directional conversion within the tested measurement region and physical configuration. It is not interpreted as evidence of universal sub-0.001-in calibration accuracy at arbitrary image positions or orientations. Measurement-uncertainty and traceability terminology in the final thesis should follow the JCGM Guide to the Expression of Uncertainty in Measurement and the International Vocabulary of Metrology (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b).

---

## 3.7 Prevalidation Engineering and Method Freeze

The preceding sections define the final image-processing, measurement, and calibration methods. Before those methods were applied to formal validation, development and prevalidation activities were completed before formal validation and included segmentation development, estimator comparison, spatial calibration characterization, integrated-pipeline verification, and measurement-assurance checks. These activities were used to select and freeze the measurement method; their numerical outcomes are not treated as formal validation results.

The development record was intentionally preserved under version control. PCA/extreme-mask initially served as the development baseline, a geometry-based estimator was temporarily selected during the August 7, 2026 development stage, and subsequent physical-unit comparison favored PCA/extreme-mask for aggregate dimensional agreement. PCA/extreme-mask was therefore selected and frozen as the primary formal-validation estimator on August 13, 2026. Specimens 121, 146, 178, 187, and 197, which were used during that comparison, are excluded from the formal validation sample.

The frozen method includes the segmentation sequence and parameters, endpoint and axis logic, spatial/directional calibration mapping, quality gates, physical-unit conversion, and formal failure-status behavior. Any subsequent change capable of affecting dimensional output is subject to explicit validation change control. Once formal validation begins, validation outcomes cannot be used to retune the measurement method, acceptance criteria, or prespecified primary statistical analysis. This prospective separation between method development and validation is consistent with established principles of preplanned experimental design (NIST/SEMATECH, n.d.).

---

## 3.8 Specimen Population and Screening

After method freeze, the study proceeds from algorithm development to prospective specimen selection. The available study population consists of 235 cartridge cases previously laser etched with unique integer identifiers from 1 through 235. The existing laser-etched identifier is used directly as the specimen `part_id`, avoiding the introduction of a second identification system. The population contains specimens spanning the available OAL range, including specimens intentionally prepared shorter or longer than nominal during earlier study preparation.

The five specimens previously used during estimator prevalidation—121, 146, 178, 187, and 197—are excluded from eligibility for formal validation. All other eligible specimens remain in the screening population regardless of whether they appear nominal, short, or long.

Before formal sample selection, the eligible population is screened using the designated manual screening process to characterize its dimensional distribution for stratification. Screening measurements are population-characterization measurements only and are not substituted for the three-replicate formal manual reference measurements subsequently obtained from selected validation specimens.

The screening record preserves specimen identity, screening reading, date, time, operator, caliper identity, session identity, reference-check information, screening classification, selection status, and explanatory notes. Screening sessions were bracketed by reference checks against the certified 1-in gauge block under the frozen measurement-assurance procedure. The final numerical session-acceptance limits were established before formal specimen measurement.

Screening was completed before the formal validation sample was selected. The resulting screened population and frozen stratum definitions were preserved as part of the formal selection record.

---

## 3.9 Formal Validation Sample Selection

The formal validation sample contained 60 unique specimens selected from the 230-specimen eligible screened population using the prospectively defined stratified random procedure. The procedure was intended to preserve representation across the observed OAL distribution rather than rely on convenience or discretionary specimen selection. Stratified random sampling partitions a population into defined subgroups and applies random selection within those groups (Lohr, 2022).

The five prevalidation specimens were removed from the eligible sampling frame before selection. The frozen screening-based strata and formal allocation were:

| Stratum | Screening definition | Selected specimens |
|---|---|---:|
| Below LSL | OAL < 0.9900 in | 8 |
| Near LSL, in specification | 0.9900 <= OAL <= 0.9950 in | 14 |
| Central nominal | 0.9950 < OAL < 1.0050 in | 16 |
| Near USL, in specification | 1.0050 <= OAL <= 1.0100 in | 14 |
| Above USL | OAL > 1.0100 in | 8 |

Selection used frozen seed `2026090301` with deterministic SHA-256 ranking. The screened population input, eligibility rules, stratum definitions, allocation, selection logic, final specimen identifiers, and reserve population were preserved so that the sample draw could be reproduced and audited.

---

## 3.10 Manual Reference Measurement Method

Formal manual reference measurements used a Mitutoyo digital caliper, model 500-196-30 / CD-6"ASX, serial number B24254849, with 0.0005-in (0.01-mm) display resolution. Calibration certificate DDJ25P23P identifies the instrument as a 0–6 in digital caliper and reports an as-left indication error of 0.0000 in at 1 in. The reported expanded uncertainty at 1 in is 0.000126 in at approximately 95% confidence. The formal reference-system review accepted the caliper with documented session-control limitations before formal specimen measurement.

No calibration correction is applied to formal manual observations because the accepted certificate reports zero as-left indication error at 1 in. Metrological traceability and uncertainty are treated using the certificate evidence and the applicable VIM/GUM framework (Joint Committee for Guides in Metrology, 2012b; Joint Committee for Guides in Metrology, 2008).

Before and after each formal manual measurement session, five readings of the certified gauge block were obtained with full removal and repositioning between readings. The gauge block has a certified central length of 1.0000024 in under certificate T26A06624. Session acceptance was based on the prospectively frozen reference-error, within-check-spread, and pre-to-post-drift criteria. The frozen limits are 0.0005 in for absolute mean indication error, five-reading range, and pre-to-post mean drift.

Each selected validation specimen was measured manually three times. The specimen was fully removed and repositioned between replicate readings so that the repeated-measurement series included positioning variation inherent in the stated manual procedure. Formal run-order randomization is described in Section 3.12.

The formal manual study was conducted by a single operator. Accordingly, the repeated manual measurements characterize within-operator behavior under the specified measurement conditions; they do not estimate between-operator measurement reproducibility. This distinction follows the VIM separation of measurement repeatability from measurement reproducibility (Joint Committee for Guides in Metrology, 2012b).

The manual process is treated as the study's reference measurement process rather than as an error-free determination of “true” OAL. Its calibration status, resolution, repeatability, and measurement uncertainty remain relevant to interpretation of agreement with the computer-vision method. The calibration-correction policy was frozen as no correction at 1 in.

The prospectively frozen specimen-level reference-uncertainty model combined the calibration, display-resolution, and pooled manual-repeatability contributions. The standard calibration contribution was defined as \(u_{cal}=U_{cal}/2\), the resolution contribution as \(u_{res}=0.0005/\sqrt{12}\), and the repeatability contribution as \(u_{rep}=s_p/\sqrt{3}\), where \(s_p\) is the pooled within-specimen manual repeated-measurement standard deviation. Combined standard uncertainty was defined as \(u_{ref}=\sqrt{u_{cal}^2+u_{res}^2+u_{rep}^2}\), with expanded reference uncertainty \(U_{ref}=2u_{ref}\). The gauge-block uncertainty was used for session assurance and was not added as a specimen-level component, and no separate numerical environmental-uncertainty term was added.

Primary specification classification used the formal manual-reference point estimate and the inclusive nominal limits. A secondary uncertainty-overlap flag identified specimens whose reference interval reached or crossed a specification limit; that flag did not alter primary classification, create an indeterminate category, remove a specimen, or impose a retrospective guard band (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012a).

Raw manual replicate readings are preserved individually. Any specimen-level manual reference mean used in the agreement analysis is derived from those preserved observations rather than replacing the underlying measurements.

---

## 3.11 Computer-Vision Validation Measurement Method

Formal computer-vision validation used the frozen PCA/extreme-mask OAL pipeline after completion of the manual reference measurement phase. The formal study included 60 unique specimens with three CV acquisition attempts per specimen, yielding 180 planned acquisition opportunities. Each specimen was fully removed from the measurement surface between replicate acquisitions and independently replaced for the subsequent randomized round. The clear Lexan measurement assembly remained installed, but the nominal Lexan locator was not used to mechanically register or constrain specimen position. Consequently, the three formal CV observations per specimen characterize placement-dependent repeatability under independent free placement with consistent gross base-to-mouth orientation rather than repeatability under mechanically constrained location.

The CV run order was randomized independently of the manual reference-measurement order as described in Section 3.12. Each formal CV attempt was assigned one of three prospectively defined statuses: `VALID`, `SYSTEM_FAILURE`, or `PROTOCOL_INVALID`. A system failure represents a genuine failure of the system to produce a valid result during an otherwise valid attempt and remains part of formal system-performance accounting. It is not automatically repeated merely to replace an unsuccessful result. A protocol-invalid attempt represents a documented procedural nonconformance rather than measurement-system performance; when permitted by the prospective deviation procedure, such an attempt may receive a documented replacement while the original invalid record remains preserved.

No CV result is imputed for a system failure. At least two valid CV replicates are required for calculation of the specimen-level CV mean used in the primary agreement analysis. Specimens with fewer than two valid CV replicates remain represented in availability and failure reporting but are excluded from the primary specimen-level agreement analysis. The experimental unit for the primary between-method analysis is the unique specimen rather than the individual replicate acquisition.

---

## 3.12 Randomization and Replication

Manual and computer-vision measurements used independently randomized run orders. The manual sequence used seed `2026081901`, whereas the CV sequence used seed `2026081902`. Each method obtained three repeated measurements per selected specimen with full removal and repositioning between replicates.

Randomization and replication are established experimental-design principles that support control of run-order effects and characterization of repeated-observation behavior (NIST/SEMATECH, n.d.). Within the present study, the replicate measurements are used to characterize repeated-measurement behavior and to construct specimen-level means for the primary agreement analysis. Replicates obtained from one specimen are not treated as independent specimens; the principal agreement dataset contains at most 60 unique specimen-level pairs.

---

## 3.13 Environmental and Measurement-Assurance Controls

Formal measurement sessions included environmental observations and reference-standard checks to document measurement conditions and identify material changes during data collection. Environmental monitoring used the WD-20250-91 thermocouple thermometer and WD-08519-54 Type-T self-adhesive surface probes identified in the formal equipment record. The thermometer calibration documentation was reviewed before formal validation; the Type-T probes were not individually calibrated and this limitation was retained in the research record.

Environmental conditions were treated as potential influence quantities (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b). The formal protocol recorded temperature observations but did not apply an automatic thermal correction to the cartridge-case or CV measurement, and no separate numerical environmental-uncertainty contribution was introduced into the specimen-level reference model.

The reference-check procedure defined in Section 3.10 served as the primary session-level measurement-assurance control. The final acceptance limits were 0.0005 in for absolute mean reference error, five-reading range, and pre-to-post mean drift. Formal temperature observations, session-check results, and documented deviations were preserved with the validation dataset.

---

## 3.14 Data Integrity, Research Provenance, and Protocol Deviations

Formal study records preserve raw observations separately from derived summaries. Manual replicate readings, CV attempt-level records, status codes, specimen identifiers, timestamps, and applicable acquisition artifacts are retained so that specimen-level results can be regenerated from the underlying evidence.

Research-relevant software, protocols, calibration records, methodological decisions, and corrections are preserved under version control. The OAL evidence index and method decision log provide an additional claim-to-evidence and chronology layer over the underlying artifacts. Where SHA-256 manifests or transport records are used, they provide integrity checks for preserved or transferred artifacts.

Formal observations are not deleted solely because they are statistically inconvenient or appear to be outliers. Questionable observations are retained and dispositioned using the prospective failure/deviation framework. Material protocol deviations are documented and assessed for their effect on study validity. Methodological corrections preserve both the original evidence and the later correction rather than silently rewriting the research history.

---

## 3.15 Statistical Analysis

The statistical analysis was specified prospectively so that formal outcomes would be evaluated against a fixed analysis plan. The primary unit of between-method agreement analysis is the unique validation specimen. For each specimen with sufficient valid CV replicates, the specimen-level CV mean is compared with the corresponding specimen-level manual reference mean. Signed error is defined as

\[
e_i = \bar{x}_{CV,i} - \bar{x}_{REF,i},
\]

such that positive values indicate CV measurements greater than the reference value and negative values indicate CV measurements less than the reference value.

The prespecified primary statistical summaries include mean bias, mean absolute error, root mean squared error, empirical 95th percentile of absolute specimen error, and maximum absolute specimen error. The empirical P95 is calculated using the prespecified nearest-rank convention; with 60 evaluable specimen-level observations, the 57th ordered absolute error represents the nearest-rank P95.

Repeated-measurement behavior is examined separately from between-method agreement using absolute differences among replicate measurements. The term repeatability is used consistently with the International Vocabulary of Metrology (Joint Committee for Guides in Metrology, 2012b). Error is also examined as a function of measurement magnitude and the final screening-defined strata.

Agreement between the two measurement methods is further examined using a Bland–Altman-style difference-versus-magnitude analysis. Bland and Altman showed that correlation can be misleading when the scientific question concerns agreement between measurement methods (Bland & Altman, 1986). Correlation, if included, is therefore supplementary and does not replace the prespecified error and agreement metrics.

Classification performance was evaluated relative to the project OAL specification limits of 0.9900 in and 1.0100 in, inclusive. Primary classification used the formal manual-reference point estimate. Reference uncertainty was incorporated through the prospectively frozen secondary uncertainty-overlap flag rather than through a guard band or indeterminate primary category (Joint Committee for Guides in Metrology, 2012a).

Computer-vision availability is defined as

\[
Availability =
\frac{N_{\mathrm{VALID}}}
{N_{\mathrm{VALID}} + N_{\mathrm{SYSTEM\_FAILURE}}}.
\]

Protocol-invalid attempts were not counted as system failures because they represent invalid procedure rather than system performance; however, the original invalid records and any permitted replacements remain documented. No observation was removed solely because its inclusion worsened the statistical performance metrics. Formal numerical results are reported in Chapter 4.

---

## 3.16 Validation Acceptance Criteria

The primary validation acceptance criteria were defined before formal validation data collection and were not revised after formal results were observed. The frozen criteria were:

- CV availability of at least 99%;
- P95 absolute repositioning difference no greater than 0.002 in (operationalized in formal V1 as the pairwise difference among independent free placements);
- absolute mean specimen-level bias no greater than 0.001 in;
- specimen-level RMSE no greater than 0.002 in;
- empirical P95 absolute specimen error no greater than 0.003 in; and
- maximum absolute specimen error no greater than 0.004 in.

With 180 planned CV acquisition opportunities, 179 valid attempts correspond to approximately 99.44% availability and satisfy the 99% requirement, whereas 178 valid attempts correspond to approximately 98.89% and do not.

The prospective plan specified zero false-pass classifications as the desired outcome and defined any confirmed false pass as a material validation result because false acceptance is a recognized conformity-assessment risk (Joint Committee for Guides in Metrology, 2012a). Primary reference classification used the formal manual-reference point estimate and the inclusive nominal specification limits; the prospectively frozen uncertainty-overlap flag was reported secondarily and did not change that primary classification.

Unresolved material protocol deviations prevent an unconditional validation conclusion even when numerical performance thresholds are otherwise met. The numerical acceptance criteria above are CaseMetrology-specific prospective criteria and are not attributed to external standards or manufacturer specifications.

---

## 3.17 Methodological Limitations

The formal study is limited to cartridge-case overall length. It does not validate rim geometry, primer-pocket dimensions, concentricity, or other dimensional characteristics. The study evaluates a static, backlit measurement configuration in which specimens were independently placed on the clear Lexan working surface with consistent gross base-to-mouth orientation but without mechanical registration by the installed locator. It does not directly establish performance for conveyor-based, robotic, or otherwise dynamic production acquisition.

The validation conclusion applies to the documented camera, 16 mm CS-mount lens, measurement-plane geometry, illumination, fixture, software, segmentation, estimator, and calibration configuration used during the formal study. A materially changed optical, mechanical, lighting, calibration, or software configuration should not automatically inherit the validation conclusion without an appropriate verification or revalidation assessment.

The manual comparator is a reference measurement process rather than an error-free value. Its resolution, repeatability, calibration status, and measurement uncertainty limit the interpretation of agreement (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b). Because the manual study is performed by one operator, the study does not estimate between-operator reproducibility.

The formal agreement analysis contains 60 unique specimens and therefore provides a finite empirical characterization of the selected study population rather than proof of worst-case performance for every possible cartridge case. The empirical P95 and maximum observed error describe the formal sample and are not interpreted as universal physical bounds. Although the sampling population includes intentionally short and long specimens, generalization to future manufacturing populations remains constrained by the source population, sampling design, and documented study configuration.

The formal study was therefore designed to determine whether the frozen CaseMetrology OAL system satisfied its prespecified validation criteria under the documented conditions. Broader dimensional, operational, and production-line claims are reserved for future research.

---

---

---

# Chapter 4 — Results

## 4.1 Formal OAL Validation Overview

Formal validation of the CaseMetrology overall-length (OAL) measurement system was conducted using the prospectively frozen set of 60 uniquely identified cartridge-case specimens. The same retained specimen set was used throughout the manual-reference and computer-vision (CV) phases.

Three randomized manual-reference measurement rounds and three randomized CV measurement rounds were completed. The resulting formal dataset contained 180 valid manual-reference measurements and 180 valid CV measurements, for a total of 360 formal specimen measurements.

The primary statistical unit was the unique specimen rather than the individual replicate. Accordingly, primary dimensional agreement was evaluated using 60 paired specimen-level means, with each manual and CV mean based on three valid measurements.

Formal V1 CV acquisition used independent free placement on the clear Lexan measurement surface. The installed Lexan locator was not used to mechanically constrain specimen position. Gross base-to-mouth orientation was maintained, while exact image-plane position and small angular variation were otherwise unconstrained. Detailed acquisition conditions are described in Chapter 3.

## 4.2 Formal Dataset Integrity and Measurement Availability

All three manual-reference sessions satisfied the frozen session-acceptance criteria and were classified as accepted.

Two manual-reference measurements obtained during the second manual round were designated protocol-invalid after a temporary run-order sequence displacement was detected. The two observations were preserved in the raw dataset for traceability, excluded from formal analysis, and replaced by measurements obtained in the correct frozen sequence. The resulting formal manual-reference analysis population contained exactly 180 valid measurements, with three valid observations for each of the 60 specimens.

All 180 planned formal CV observations returned a `VALID` measurement status. No CV observation was classified as a system failure. Formal CV measurement availability was therefore:

\[
Availability = 100.0\%
\]

which exceeded the prespecified minimum criterion of 99%.

## 4.3 Manual Reference Repeatability and Reference Uncertainty

For specimen \(i\), the formal manual reference was calculated from the three valid randomized manual observations:

\[
\bar{M}_i =
\frac{M_{i1}+M_{i2}+M_{i3}}{3}
\]

Screening measurements used during sample selection were not included in the formal reference value.

The pooled within-specimen manual repeated-measurement standard deviation was:

\[
s_p = 0.000553\text{ in}
\]

The prospectively frozen reference-uncertainty model combined the accredited calibration uncertainty contribution, digital display-resolution contribution, and pooled repeated-measurement contribution.

The resulting expanded formal reference uncertainty was:

\[
U_{ref}=0.000712\text{ in}
\]

using a coverage factor of \(k=2\).

The expanded uncertainty did not alter the primary specification classification. Instead, the frozen analysis plan required a secondary uncertainty-overlap flag when a specimen's reference-uncertainty interval reached or crossed either nominal specification limit. Thirteen of the 60 formal specimens met this secondary overlap criterion.

## 4.4 CV Repeatability Under Independent Free Placement

Formal CV repeatability was evaluated using the three independent specimen placements obtained for each of the 60 specimens. For each specimen, the absolute differences between CV Rounds 1 and 2, Rounds 1 and 3, and Rounds 2 and 3 were calculated, producing 180 pairwise differences.

The empirical nearest-rank 95th-percentile pairwise difference was:

\[
P_{95}=0.004831\text{ in}
\]

The maximum observed pairwise difference was:

\[
0.007081\text{ in}
\]

The prospectively specified criterion required:

\[
P_{95}\le0.002\text{ in}
\]

Therefore, the V1 independent-placement repeatability criterion was not met.

The largest observed pairwise difference occurred for specimen 70. Its three CV measurements were 1.003218, 1.010299, and 1.008805 in, yielding a maximum pairwise difference of 0.007081 in.

These pairwise differences therefore quantify V1 placement-dependent repeatability under the independent free-placement acquisition condition defined in Chapter 3.

Figure 4.1 summarizes CV repeated-measurement variation under the independent free-placement acquisition condition.

![Figure 4.1. CV repeatability under independent free placement.](../../../../data/oal_validation/derived/figures/figure_v1_independent_placement_repeatability.png)

Source file: `data/oal_validation/derived/figures/figure_v1_independent_placement_repeatability.pdf`

## 4.5 Primary Dimensional Agreement

For each specimen, signed measurement error was prospectively defined as:

\[
e_i=\bar{C}_i-\bar{M}_i
\]

where \(\bar{C}_i\) is the mean formal CV OAL and \(\bar{M}_i\) is the mean formal manual-reference OAL.

Positive error indicates that the CV method reported a longer OAL than the corresponding manual reference.

The observed mean signed error was:

\[
Bias=+0.001613\text{ in}
\]

with a 95% confidence interval of:

\[
[+0.001222,\,+0.002005]\text{ in}
\]

The median signed error was:

\[
+0.001345\text{ in}
\]

The mean absolute error was:

\[
MAE=0.001815\text{ in}
\]

and root mean square error was:

\[
RMSE=0.002205\text{ in}
\]

The empirical nearest-rank 95th-percentile absolute specimen error was:

\[
P_{95}(|e|)=0.003960\text{ in}
\]

and the maximum absolute specimen error was:

\[
E_{max}=0.004799\text{ in}
\]

The observed mean signed error was positive.

Figure 4.2 shows signed specimen-level OAL error as a function of formal manual-reference OAL.

![Figure 4.2. Signed specimen-level OAL error versus formal manual-reference OAL.](../../../../data/oal_validation/derived/figures/figure_v1_signed_error_vs_reference.png)

Source file: `data/oal_validation/derived/figures/figure_v1_signed_error_vs_reference.pdf`

Figure 4.3 shows the distribution of absolute specimen-level OAL error.

![Figure 4.3. Distribution of absolute specimen-level OAL error.](../../../../data/oal_validation/derived/figures/figure_v1_absolute_error_distribution.png)

Source file: `data/oal_validation/derived/figures/figure_v1_absolute_error_distribution.pdf`

## 4.6 Prespecified Formal Validation Criteria

Table 4.1 summarizes the primary prespecified V1 validation criteria and observed outcomes.

### Table 4.1. Prespecified V1 formal OAL validation criteria

| Metric | Observed | Prespecified criterion | Status |
|---|---:|---:|---|
| CV measurement availability | 100.000% | >= 99% | MET |
| Independent-placement pairwise P95 | 0.004831 in | <= 0.002 in | NOT MET |
| Absolute mean bias | 0.001613 in | <= 0.001 in | NOT MET |
| RMSE | 0.002205 in | <= 0.002 in | NOT MET |
| P95 absolute specimen error | 0.003960 in | <= 0.003 in | NOT MET |
| Maximum absolute specimen error | 0.004799 in | <= 0.004 in | NOT MET |
| False passes | 1 | Zero preferred | NOT MET |

The system therefore met the measurement-availability requirement but did not satisfy the prespecified V1 targets for placement-dependent repeatability, absolute mean bias, RMSE, 95th-percentile absolute specimen error, maximum absolute specimen error, or the preferred zero-false-pass condition.

Under the frozen statistical analysis plan, failure of one or more criteria did not authorize retrospective adjustment of the validation dataset, calibration model, estimator, acceptance thresholds, or specimen classifications.

## 4.7 CV Versus Manual Reference Relationship

Linear regression of specimen-level CV mean OAL against formal manual-reference mean OAL produced:

\[
Slope=1.002761
\]

and:

\[
Intercept=-0.001148\text{ in}
\]

Pearson correlation was:

\[
r=0.992737
\]

with:

\[
R^2=0.985526
\]

Correlation and \(R^2\) were prospectively defined as secondary diagnostic measures rather than primary agreement criteria.

Figure 4.4 compares CV specimen-level mean OAL with formal manual-reference mean OAL and includes the 1:1 identity line and ordinary least-squares fit.

![Figure 4.4. CV specimen mean OAL versus formal manual-reference mean OAL with 1:1 identity line and ordinary least-squares fit.](../../../../data/oal_validation/derived/figures/figure_v1_cv_vs_manual.png)

Source file: `data/oal_validation/derived/figures/figure_v1_cv_vs_manual.pdf`

## 4.8 Bland–Altman Agreement

Bland–Altman analysis was performed using the 60 paired specimen-level means.

The mean paired difference was:

\[
+0.001613\text{ in}
\]

The calculated 95% limits of agreement were:

\[
LOA_{lower}=-0.001357\text{ in}
\]

and:

\[
LOA_{upper}=+0.004583\text{ in}
\]

The specimen-level paired differences were distributed around the positive mean bias within these calculated limits of agreement.

Figure 4.5 presents the Bland–Altman difference-versus-magnitude assessment for the paired specimen-level means.

![Figure 4.5. Bland–Altman agreement plot for specimen-level CV and formal manual-reference OAL means.](../../../../data/oal_validation/derived/figures/figure_v1_bland_altman.png)

Source file: `data/oal_validation/derived/figures/figure_v1_bland_altman.pdf`

## 4.9 Specification Classification Performance

The frozen nominal specification limits were:

\[
0.9900\le OAL\le1.0100\text{ in}
\]

inclusive.

Primary reference classification was determined from the formal three-reading manual-reference mean. CV classification used the corresponding three-reading CV mean and the same nominal limits.

The formal confusion-matrix results were:

- true conforming: 37 specimens;
- false fails: 8 specimens;
- false passes: 1 specimen;
- true nonconforming: 14 specimens.

Sensitivity for detecting nonconforming specimens was:

\[
93.33\%
\]

and specificity for conforming specimens was:

\[
82.22\%
\]

The single false-pass specimen was part 143. Its formal manual-reference mean was 0.989833 in, while its CV mean was 0.992173 in. The resulting signed error was +0.002340 in. Part 143 also met the prospectively frozen uncertainty-overlap criterion.

Eight specimens were classified as false fails. Seven of the eight occurred on the upper side of the nominal specification region. Six of the eight false fails also carried the secondary uncertainty-overlap flag.

The overlap flag did not change the frozen primary classification.

Figure 4.6 summarizes the formal specification-classification outcomes.

![Figure 4.6. Formal OAL specification-classification confusion matrix.](../../../../data/oal_validation/derived/figures/figure_v1_classification_confusion_matrix.png)

Source file: `data/oal_validation/derived/figures/figure_v1_classification_confusion_matrix.pdf`

## 4.10 Error by Frozen Sampling Stratum

The five frozen sampling strata were retained for stratified analysis. Strata reflected the original screening-based sampling design and were not reassigned using the final formal manual-reference means.

Table 4.2 summarizes specimen-level dimensional error and classification outcomes across the five frozen sampling strata.

### Table 4.2. V1 dimensional error by frozen sampling stratum

| Frozen sampling stratum | n | Mean signed error (in) | MAE (in) | Maximum absolute error (in) | False passes | False fails |
|---|---:|---:|---:|---:|---:|---:|
| Below LSL | 8 | +0.001109 | 0.001355 | 0.003853 | 0 | 0 |
| Near LSL, in specification | 14 | +0.001615 | 0.001725 | 0.003567 | 1 | 1 |
| Central nominal | 16 | +0.002182 | 0.002189 | 0.004799 | 0 | 0 |
| Near USL, in specification | 14 | +0.001480 | 0.001609 | 0.004126 | 0 | 5 |
| Above USL | 8 | +0.001210 | 0.002049 | 0.004124 | 0 | 2 |

Mean signed error was positive in all five frozen sampling strata.

The central-nominal stratum exhibited the greatest mean signed error at +0.002182 in and the largest observed specimen-level absolute error at 0.004799 in. No classification errors occurred in that stratum.

Classification errors occurred in the near-LSL, near-USL, and above-USL strata, with the largest count occurring in the near-USL stratum.

Figure 4.7 shows signed specimen-level OAL error across the five frozen sampling strata.

![Figure 4.7. Signed specimen-level OAL error by frozen sampling stratum.](../../../../data/oal_validation/derived/figures/figure_v1_error_by_stratum.png)

Source file: `data/oal_validation/derived/figures/figure_v1_error_by_stratum.pdf`

## 4.11 Manual and CV Within-Specimen Repeatability

Within-specimen standard deviations were calculated separately for the three formal manual-reference measurements and three formal CV measurements for each specimen.

The manual-reference repeatability results characterize the single-operator calibrated manual method. They do not constitute a multi-operator Gage R&R study.

The CV within-specimen results characterize repeatability across three independent free placements within the camera viewing field rather than repeatability at one mechanically fixed position.

Figure 4.8 compares within-specimen repeated-measurement behavior for the manual-reference and CV methods.

![Figure 4.8. Comparison of manual-reference and CV within-specimen repeatability across the three formal rounds.](../../../../data/oal_validation/derived/figures/figure_v1_repeatability_comparison.png)

Source file: `data/oal_validation/derived/figures/figure_v1_repeatability_comparison.pdf`

## 4.12 Signed-Error Distributional Assessment

The frozen statistical analysis plan included distributional assessment of signed specimen-level differences.

A normal Q-Q assessment was produced for the 60 signed specimen-level errors. This diagnostic was used to assess the shape of the error distribution and did not provide a basis for deleting or excluding observations.

Figure 4.9 provides the normal Q-Q assessment of signed specimen-level OAL errors.

![Figure 4.9. Normal Q-Q assessment of signed specimen-level OAL errors.](../../../../data/oal_validation/derived/figures/figure_v1_signed_error_qq.png)

Source file: `data/oal_validation/derived/figures/figure_v1_signed_error_qq.pdf`

## 4.13 Post-Validation Exploratory Diagnostics

Following completion, preservation, and interpretation of the primary V1 formal analysis, limited exploratory diagnostics were conducted to characterize the observed failure pattern.

These analyses were not prospectively defined acceptance criteria and did not change the V1 formal outcome.

### 4.13.1 Error by CV Round

Mean signed error differed across the three CV rounds.

Table 4.3 summarizes the exploratory round-specific CV error statistics for the three formal acquisition rounds.

### Table 4.3. Exploratory CV round-specific error

| CV round | n | Mean signed error (in) | Median signed error (in) | SD (in) | MAE (in) |
|---|---:|---:|---:|---:|---:|
| Round 1 | 60 | +0.000764 | +0.000820 | 0.001976 | 0.001697 |
| Round 2 | 60 | +0.001721 | +0.001499 | 0.001988 | 0.002186 |
| Round 3 | 60 | +0.002355 | +0.002519 | 0.001830 | 0.002521 |

The difference between the mean Round 3 and Round 1 errors was:

\[
+0.001591\text{ in}
\]

No meaningful relationship was observed between within-round acquisition sequence and signed measurement error. The sequence-based regressions produced \(R^2\) values of 0.0060, 0.0010, and 0.0027 for Rounds 1, 2, and 3, respectively.

The round-specific means differed, whereas the within-round sequence regressions showed minimal linear association with acquisition sequence.

### 4.13.2 Placement Variability Versus Specimen Agreement Error

The association between each specimen's maximum independent-placement pairwise difference and its specimen-level absolute agreement error was negligible.

Pearson correlation was:

\[
r=-0.083989
\]

and Spearman rank correlation was:

\[
\rho=-0.113087
\]

The observed correlations between maximum placement-dependent variation and specimen-level absolute agreement error were near zero.

### 4.13.3 Signed Error Versus Formal OAL

Signed specimen-level error showed essentially no linear relationship with formal manual-reference OAL.

The error-versus-OAL regression produced:

\[
R^2=0.000516
\]

with:

\[
p=0.863
\]

The fitted relationship between signed error and formal manual-reference OAL was negligible over the observed validation range.

### 4.13.4 Effective PPI

Individual CV observation error showed a moderate negative association with effective pixels per inch (PPI), with Pearson \(r=-0.374732\) and Spearman \(\rho=-0.369283\).

However, effective PPI is an endogenous component of the frozen CaseMetrology dimensional conversion. The production pipeline calculates effective PPI from the spatial calibration planes and specimen orientation and then calculates OAL by dividing measured pixel length by effective PPI.

Because effective PPI is part of the dimensional conversion equation, the observed association is reported as exploratory rather than causal evidence.

Mean effective PPI was similar across the three CV rounds.

## 4.14 Summary of V1 Formal Validation

The V1 CaseMetrology system produced valid OAL measurements for all 180 planned formal CV observations, satisfying the prespecified measurement-availability criterion.

The CV method also exhibited strong linear association with the calibrated manual reference across the validation range.

However, the V1 system did not meet the prospectively defined criteria for independent-placement repeatability, absolute mean bias, RMSE, 95th-percentile absolute specimen error, maximum absolute specimen error, or the preferred zero-false-pass condition.

The formal specimen-level mean bias was +0.001613 in, and the empirical 95th-percentile independent-placement pairwise difference was 0.004831 in.

Classification performance consisted of 37 true-conforming specimens, 14 true-nonconforming specimens, eight false fails, and one false pass.

Signed error was positive in all five frozen sampling strata. Exploratory diagnostics additionally identified an increase in mean signed error across CV rounds but no meaningful progressive within-round sequence trend, no meaningful relationship between signed error and formal OAL, and little association between maximum specimen placement variation and absolute specimen-mean agreement error.

These results constitute the preserved V1 formal validation outcome under the prospectively frozen protocol.

---

# Chapter 5 — Discussion

## 5.1 Overview

The purpose of the formal CaseMetrology validation study was to determine whether the frozen computer-vision overall-length (OAL) measurement system satisfied prospectively established performance criteria relative to an independently acquired calibrated manual reference process. The evaluation addressed measurement availability, repeated-measurement behavior under independent specimen placement, dimensional agreement, error magnitude, and specification-classification performance.

The formal study produced a clear answer to that research question. CaseMetrology achieved complete measurement availability and exhibited strong linear association with the formal manual reference, but the frozen V1 system did not satisfy the complete set of prespecified dimensional-agreement and placement-dependent repeatability criteria. The formal outcome therefore does not support unconditional acceptance of the V1 configuration as a validated OAL conformance-measurement system.

This finding does not represent a failure of the experimental design. The prospective protocol, randomized repeated measurements, preserved raw observations, independent manual-reference process, frozen analysis rules, and predefined performance criteria allowed system limitations to be identified without retrospective adjustment of the estimator, calibration, thresholds, or dataset.

The principal V1 findings requiring interpretation are the positive CV-minus-manual bias, placement-dependent repeated-measurement variation, specification-classification errors near the nominal limits, and the observed round-associated shift in signed error.

## 5.2 Interpretation of Dimensional Agreement

The formal specimen-level mean signed error was +0.001613 in, exceeding the prespecified absolute mean-bias criterion of 0.001 in. The 95% confidence interval for mean bias, +0.001222 to +0.002005 in, remained entirely positive. In addition, mean signed error was positive within each of the five frozen sampling strata.

Taken together, these results provide evidence that the V1 CV method exhibited a systematic positive measurement tendency under the formal validation conditions. This tendency is important because a dimensional measurement system may track relative differences among specimens while still disagreeing materially with the reference measurement process.

The formal regression results illustrate this distinction. Pearson correlation was 0.992737 and the coefficient of determination was 0.985526, demonstrating strong linear association between the two measurement methods. However, strong correlation does not establish measurement agreement. The Bland–Altman results showed a mean difference of +0.001613 in with limits of agreement from -0.001357 to +0.004583 in. Thus, the formal results demonstrate that high correlation and acceptable measurement-system agreement are separate properties, consistent with the methodological distinction described by Bland and Altman (Bland & Altman, 1986).

The additional specimen-level metrics led to the same overall conclusion. RMSE was 0.002205 in compared with a prespecified limit of 0.002 in, the empirical 95th-percentile absolute specimen error was 0.003960 in compared with a limit of 0.003 in, and maximum absolute specimen error was 0.004799 in compared with a limit of 0.004 in.

The positive bias alone therefore does not fully describe V1 performance. Both systematic disagreement and specimen-to-specimen error dispersion contributed to failure of the formal dimensional-agreement criteria.

## 5.3 Placement-Dependent Repeatability

The largest departure from the prespecified repeatability target occurred under the independent free-placement condition used for formal V1 acquisition.

The empirical 95th-percentile absolute pairwise difference among the three CV rounds was 0.004831 in, more than twice the prespecified 0.002-in criterion. The maximum observed pairwise difference was 0.007081 in.

As documented in Chapter 3, the clear Lexan measurement assembly remained installed during formal acquisition, but the nominal Lexan locator was not used to mechanically register specimen position. Each case was placed freely on the clear measurement surface, gross base-to-mouth orientation was maintained, and exact image-plane position and small angular variation were otherwise unconstrained.

The formal repeated-measurement result must therefore be interpreted as placement-dependent repeatability under independent free placement rather than repeatability at a mechanically fixed position.

This result demonstrates that the complete V1 measurement system was sensitive to repeated physical presentation of the specimen under the tested acquisition condition. It does not identify which individual component of the measurement chain produced that sensitivity.

Maximum specimen-level placement variation showed little association with specimen-level absolute CV-versus-manual agreement error. Pearson correlation was -0.083989 and Spearman correlation was -0.113087.

These near-zero correlations do not establish statistical independence between the two quantities. They do show that, within the formal V1 sample, specimens with the greatest placement-dependent variation were not systematically the same specimens with the largest specimen-mean dimensional disagreement.

Accordingly, improved control of specimen placement is a plausible engineering target for reducing repeated-placement variation, but the V1 evidence does not justify assuming that positioning control alone would eliminate the positive mean bias or all specimen-level agreement error.

## 5.4 Consequences for Specification Classification

The nominal OAL acceptance interval was 0.9900 through 1.0100 in, inclusive. Using the formal manual-reference mean as the reference classification, the V1 results included 37 true-conforming specimens, 14 true-nonconforming specimens, eight false fails, and one false pass.

The single false pass is particularly important from a conformance-assessment perspective because the CV method classified a reference-nonconforming specimen as acceptable. The frozen statistical analysis plan prospectively identified zero false passes as the preferred result and required any confirmed false pass to prevent an unconditional acceptance conclusion absent a prospectively established alternative decision rule.

Part 143 produced the false-pass outcome. Its formal manual-reference mean was 0.989833 in, below the 0.9900-in lower specification limit, whereas its CV mean was 0.992173 in. The corresponding signed error was +0.002340 in.

The eight false fails represent a different operational consequence. A false fail rejects a specimen that the reference process classifies as conforming. Seven of the eight false fails occurred on the upper side of the specification region. This pattern is directionally consistent with the positive CV-minus-manual bias observed across the dataset, although the formal study does not establish bias as the sole cause of those individual classification outcomes.

The classification results demonstrate why agreement metrics and decision performance must both be evaluated. Measurement error that appears small relative to the complete dimensional range may still alter pass/fail decisions for specimens located close to a specification boundary.

## 5.5 Reference Uncertainty and Near-Limit Interpretation

The formal manual reference was treated as a calibrated measurement process rather than an error-free determination of true OAL. The prospectively defined uncertainty model produced an expanded reference uncertainty of 0.000712 in using a coverage factor of \(k=2\).

Thirteen of the 60 formal specimens met the secondary uncertainty-overlap criterion because the reference uncertainty interval reached or crossed one of the nominal specification limits.

Seven of the nine classification errors occurred among uncertainty-overlap specimens, including the single false pass. However, six uncertainty-overlap specimens were classified concordantly by the CV and reference methods, and two classification errors occurred among specimens that did not carry the uncertainty-overlap flag.

Within this formal sample, uncertainty overlap was therefore neither necessary nor sufficient for a classification error. It was an important indicator of proximity to a specification boundary, but it did not account for all observed disagreement.

Under the frozen analysis plan, the uncertainty-overlap designation remained secondary. Primary classification was based on the formal manual-reference point estimate and the inclusive nominal specification limits. The overlap flag did not create an indeterminate category, alter a specimen's primary classification, remove a specimen from analysis, or impose a retrospective guard band.

This treatment preserves the distinction between measurement uncertainty and the prospectively defined conformity decision rule. Reference uncertainty is therefore relevant context for interpreting near-limit cases, but it cannot be used retrospectively to redefine unfavorable formal outcomes (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012a).

## 5.6 Round-Associated Shift in Signed Error

Post-validation exploratory analysis identified a round-specific pattern in mean signed error.

Mean signed error was:

- +0.000764 in in Round 1;
- +0.001721 in in Round 2; and
- +0.002355 in in Round 3.

The difference between the Round 3 and Round 1 means was +0.001591 in.

Within each round, however, signed error showed essentially no linear relationship with acquisition sequence. The sequence regressions produced \(R^2\) values of 0.0060, 0.0010, and 0.0027 for Rounds 1, 2, and 3, respectively.

The observed pattern was therefore manifested primarily as a difference among rounds rather than as a detectable monotonic trend across acquisition sequence within an individual 60-specimen round.

The study design does not permit the source of that between-round difference to be isolated. Round identity, acquisition session, elapsed time, and other conditions that could vary between sessions were not independently manipulated as separate experimental factors. Consequently, the observed pattern should not be interpreted as proof of a causal round effect.

Additional exploratory diagnostics also did not establish a mechanism. Maximum placement-dependent variation showed negligible association with specimen-level absolute agreement error. Signed specimen error showed essentially no linear dependence on formal OAL. Effective PPI was associated with individual observation error, but effective PPI is an endogenous component of the frozen dimensional-conversion equation, and its mean values remained similar across the three rounds.

The mechanism responsible for the round-associated shift therefore remains unresolved. The formal evidence does not justify assigning the shift specifically to specimen placement, spatial calibration, effective PPI, environmental conditions, segmentation, estimator behavior, or another individual source.

The unresolved between-round behavior is a limitation of the V1 measurement system characterization and identifies session-to-session dimensional stability as an appropriate subject for subsequent investigation.

## 5.7 Measurement Availability Versus Measurement Quality

CaseMetrology produced a valid result for all 180 planned formal CV observations, giving a measurement availability of 100%.

This result demonstrates that the frozen V1 image-acquisition, segmentation, measurement, and data-recording pipeline operated without formal system failures during the validation study.

Availability, however, addresses whether the system produces a measurement; it does not establish whether the measurement is sufficiently accurate or repeatable for the intended dimensional decision.

The V1 study illustrates this distinction clearly. Availability exceeded the 99% requirement while multiple agreement and repeatability criteria were not met.

For an automated or semi-automated inspection system, both properties are required. A system that produces measurements reliably but with excessive agreement error or placement sensitivity cannot be judged adequate solely on the basis of high measurement availability.

## 5.8 Study Limitations

Several limitations define the scope within which the formal V1 results should be interpreted.

First, the study used one operator for both the manual-reference and CV acquisition processes. The manual repeated measurements therefore characterize within-operator behavior and do not quantify between-operator reproducibility (Joint Committee for Guides in Metrology, 2012b).

Second, formal validation was performed using one frozen hardware and software configuration. The results apply to the tested CaseMetrology V1 configuration and should not be generalized automatically to different cameras, lenses, lighting systems, calibration geometries, image-processing algorithms, or physical positioning arrangements.

Third, the formal sample contained 60 specimens selected using prospectively defined strata that intentionally represented the dimensional range and specification-boundary regions required for validation. The resulting classification counts therefore characterize this designed validation sample and should not be interpreted as estimates of production defect prevalence.

Fourth, the formal V1 CV measurements used independent free specimen placement rather than mechanically constrained location. The observed repeated-placement performance is specific to that acquisition condition.

Fifth, the formal manual reference had finite calibration uncertainty, display resolution, and repeated-measurement variation. Although these components were incorporated prospectively into the reference-uncertainty analysis, the manual reference should not be interpreted as error-free truth.

Sixth, the empirical 95th-percentile and maximum-error statistics are based on the finite formal sample. They characterize the observed validation population but do not establish a universal worst-case error bound for all possible cartridge cases or operating conditions.

Finally, the post-validation round-associated shift was identified descriptively but its causal mechanism was not established.

These limitations constrain the breadth of the conclusions but do not invalidate the formal comparison. Rather, they define the conditions under which the conclusions are supported.

## 5.9 Implications for CaseMetrology System Development

The V1 results identify two related but experimentally distinct development questions.

The first concerns control of specimen presentation. The formal placement-dependent repeatability result substantially exceeded the prospectively defined target under independent free placement. A subsequent CaseMetrology configuration could therefore test whether a more controlled and reproducible specimen-positioning method reduces repeated-placement variation.

Such a positioning change would constitute a new measurement-system configuration. Its performance would need to be evaluated prospectively rather than treated as a correction to the preserved V1 result.

The second question concerns dimensional agreement and between-round stability. Because the specimens with the greatest placement-dependent variation were not systematically the specimens with the greatest specimen-mean agreement error, improved positioning should not be assumed to eliminate the positive bias or the observed round-associated pattern.

A subsequent development program should therefore evaluate these questions separately:

1. whether controlled specimen positioning reduces repeated-placement variation; and
2. whether the modified system also improves dimensional agreement and session-to-session stability relative to the manual reference.

The preserved V1 results may appropriately inform engineering development. However, if V1 specimens or V1 measurement outcomes are used to choose, tune, or select a later configuration, those data become development evidence for that configuration and cannot simultaneously provide independent confirmation of its performance.

Any later V2 claim of independent validation should therefore be supported by prospectively defined confirmatory data that were not used to optimize or select the V2 measurement system.

## 5.10 Answer to the Research Question

The formal research question asked whether the frozen CaseMetrology OAL method satisfied the prespecified criteria for measurement availability, placement-related repeated-measurement behavior, dimensional agreement, error magnitude, and classification performance relative to an independent calibrated manual reference process.

The answer is **no for the complete V1 validation criterion set**.

The system met the measurement-availability criterion, producing valid measurements for all 180 formal CV acquisition opportunities. It also exhibited strong linear association with the manual reference.

However, it did not meet the prespecified limits for independent-placement P95 difference, absolute mean bias, RMSE, empirical 95th-percentile absolute specimen error, or maximum absolute specimen error. It also produced one false pass, contrary to the prospectively preferred zero-false-pass outcome.

The V1 configuration therefore cannot be described as having satisfied the complete formal OAL validation requirements.

At the same time, the formal study successfully quantified the magnitude and structure of the observed disagreement and identified specific engineering limitations that can guide subsequent system development.

## 5.11 Conclusions and Future Work

The CaseMetrology V1 configuration completed all 180 planned formal CV acquisitions with 100% measurement availability and exhibited strong specimen-to-specimen linear association with the calibrated manual reference.

Those characteristics were not sufficient to establish metrological adequacy. Under independent free specimen placement, placement-dependent variation exceeded the prospective repeatability criterion, the CV method exhibited a positive specimen-level bias, multiple dimensional-agreement criteria were not met, and specification classification included both false-fail and false-pass outcomes.

The formal V1 results therefore do not support unconditional acceptance of the tested configuration as a validated OAL conformance-measurement system.

At the same time, the study established a preserved quantitative baseline for subsequent CaseMetrology development. Future work should prioritize more controlled specimen positioning, investigation of the unresolved round-associated measurement shift, and evaluation of whether any modified configuration improves both repeated-placement behavior and dimensional agreement relative to the manual reference.

Other cartridge-case dimensions, multiple operators, alternative optical configurations, and dynamic manufacturing inspection remain outside the formal scope of the present study and may be evaluated separately in later work.

The V1 formal result should remain an immutable baseline. Any subsequent CaseMetrology configuration should be identified as a new system version and evaluated prospectively rather than used to reinterpret, modify, or replace the preserved V1 validation outcome.

---

# References

Arducam. (2024). *B0499 datasheet: 1.58MP IMX296 global shutter USB3.0 camera module* (Version 1.0).

Bland, J. M., & Altman, D. G. (1986). Statistical methods for assessing agreement between two methods of clinical measurement. *The Lancet, 327*(8476), 307–310. https://doi.org/10.1016/S0140-6736(86)90837-8

Che, J. K., & Ratnam, M. M. (2018). Real-time monitoring of workpiece diameter during turning by vision method. *Measurement, 126*, 369–377. https://doi.org/10.1016/j.measurement.2018.05.089

Coleman, W. J., & Swinth, K. L. (1977). Automatic cartridge case inspection and process control monitor. *Proceedings of SPIE, 129*, 74–89. https://doi.org/10.1117/12.956017

Coleman, W. J., Reich, F. R., Erickson, M. D., & Kelly, W. S. (1974). *On-line automatic high speed inspection of cartridge cases*. Pacific Northwest Laboratory.

Gonzalez, R. C., & Woods, R. E. (2018). *Digital image processing* (4th ed.). Pearson.

Hashmi, A. W., Mali, H. S., Meena, A., Khilji, I. A., Hashmi, M. F., & Saffe, S. N. B. M. (2022). Machine vision for the measurement of machining parameters: A review. *Materials Today: Proceedings, 56*(4), 1939–1946. https://doi.org/10.1016/j.matpr.2021.11.271

Hemming, B. (2007). *Measurement traceability and uncertainty in machine vision applications* [Doctoral dissertation, Helsinki University of Technology].

Joint Committee for Guides in Metrology. (2008). *Evaluation of measurement data—Guide to the expression of uncertainty in measurement* (JCGM 100:2008). https://doi.org/10.59161/JCGM100-2008E

Joint Committee for Guides in Metrology. (2012a). *Evaluation of measurement data—The role of measurement uncertainty in conformity assessment* (JCGM 106:2012). https://doi.org/10.59161/JCGM106-2012

Joint Committee for Guides in Metrology. (2012b). *International vocabulary of metrology—Basic and general concepts and associated terms (VIM)* (3rd ed., JCGM 200:2012). https://doi.org/10.59161/JCGM200-2012

Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: A review and recent developments. *Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences, 374*(2065), 20150202. https://doi.org/10.1098/rsta.2015.0202

Lai, Z., Li, H., Wang, N., & Zhang, X. (2026). A telecentric vision system tailored for high-precision dimensional measurement: Calibration and subpixel edge detection. *Measurement, 274*, 121239. https://doi.org/10.1016/j.measurement.2026.121239

Lazzari, A., & Iuculano, G. (2004). Evaluation of the uncertainty of an optical machine with a vision system for contact-less three-dimensional measurement. *Measurement, 36*(3–4), 215–231. https://doi.org/10.1016/j.measurement.2004.09.003

Lazzari, A., Iuculano, G., & Ponterio, A. (2001). Uncertainty analysis on an optical machine with vision system for three-dimensional measuring without contact. In *Proceedings of the 11th IMEKO TC4 Symposium on Trends in Electrical Measurements and Instrumentation and 6th IMEKO TC4 Workshop on ADC Modelling and Testing* (pp. 396–400). Lisbon, Portugal.

Lohr, S. L. (2022). *Sampling: Design and analysis* (3rd ed.). Chapman & Hall/CRC Press.

Malamas, E. N., Petrakis, E. G. M., Zervakis, M., Petit, L., & Legat, J.-D. (2003). A survey on industrial vision systems, applications and tools. *Image and Vision Computing, 21*(2), 171–188. https://doi.org/10.1016/S0262-8856(02)00152-X

National Institute of Standards and Technology. (n.d.). *Standard Reference Material 2461: Standard cartridge case*.

NIST/SEMATECH. (n.d.). *e-Handbook of statistical methods*. National Institute of Standards and Technology. https://doi.org/10.18434/M32189

NVIDIA Corporation. (2026). *Jetson Orin Nano Developer Kit—User guide*.

Otsu, N. (1979). A threshold selection method from gray-level histograms. *IEEE Transactions on Systems, Man, and Cybernetics, 9*(1), 62–66. https://doi.org/10.1109/TSMC.1979.4310076

Sakarya, U., Topçu, O., Leloğlu, U. M., Soysal, M., & Tunalı, E. (2012). Automated region segmentation on cartridge case base. *Forensic Science International, 222*(1–3), 277–287. https://doi.org/10.1016/j.forsciint.2012.07.004

Shin, D., Han, C., & Moon, Y. S. (2002). Ball stud inspection system using machine vision. *ISA Transactions, 41*(1), 3–11. https://doi.org/10.1016/S0019-0578(07)60197-9

Swinth, K. L., Walker, R. A., & Nedrow, N. G. (1979). High throughput dimensional measurements with electro-optics. *Proceedings of SPIE, 193*, 282–290. https://doi.org/10.1117/12.957902

Wang, S., Li, X., Zhang, Y., & Xu, K. (2024). Effects of camera external parameters error on measurement accuracy in monocular vision. *Measurement, 229*, 114413. https://doi.org/10.1016/j.measurement.2024.114413

Xiang, R., He, W., Zhang, X., Wang, D., & Shan, Y. (2018). Size measurement based on a two-camera machine vision system for the bayonets of automobile brake pads. *Measurement, 122*, 106–116. https://doi.org/10.1016/j.measurement.2018.03.017

Yammen, S., & Muneesawang, P. (2013). Cartridge case image matching using effective correlation area based method. *Forensic Science International, 229*(1–3), 27–42. https://doi.org/10.1016/j.forsciint.2013.03.015
