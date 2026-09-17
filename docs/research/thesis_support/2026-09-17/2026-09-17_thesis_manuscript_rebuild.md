# Engineering Evaluation of an Embedded Computer-Vision System for Static Dimensional Screening of Cartridge-Case Overall Length

**Researcher:** Timmy D. Bell  
**Degree:** M.S. Integrated Systems Design & Dynamics  
**Institution:** Kansas State University  
**Status:** Rebuilt thesis manuscript based on completed V1-V3 research

# Chapter 1 — Introduction

## 1.1 Background and Motivation

Machine vision is widely used in manufacturing to inspect parts, identify features, monitor processes, and extract dimensional or quality-related information from images. Industrial vision systems can reduce dependence on manual visual inspection and provide repeatable computational methods for evaluating manufactured components when the imaging conditions, measurement objective, and decision process are appropriately defined (Malamas et al., 2003; Hashmi et al., 2022). For dimensional inspection, however, detecting an object or producing a numerical value from an image does not by itself establish that the result is suitable for measurement or manufacturing decisions.

Dimensional machine vision is a measurement-system problem as well as a computer-vision problem. Image formation, optical geometry, calibration, physical presentation of the workpiece, feature localization, reference standards, repeated-measurement behavior, and measurement uncertainty can all influence the reported dimension. Consequently, a computer-vision measurement should be evaluated not only by whether an algorithm successfully detects the intended boundaries, but also by how the resulting physical measurement behaves relative to an appropriate reference process and under repeated measurement conditions (Joint Committee for Guides in Metrology, 2008; Joint Committee for Guides in Metrology, 2012b).

Backlit silhouette imaging provides a useful architecture for this type of dimensional inspection because it can create high contrast between a manufactured component and its background. Previous dimensional machine-vision studies have used backlighting, edge or contour localization, calibrated image scale, geometric modeling, and controlled specimen presentation to measure manufactured parts (Shin et al., 2002; Xiang et al., 2018; Che & Ratnam, 2018). These studies illustrate that measurement performance depends on the complete physical and computational system rather than on image segmentation alone.

Cartridge cases provide a practical test object for investigating these relationships. Optical and computerized analysis of cartridge cases is well established, particularly in forensic applications involving surface-feature acquisition and comparison. Historical work also demonstrates that electro-optical dimensional inspection of cartridge cases, including case-length measurement, predates the present research (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979). The contribution of the present study therefore does not depend on claiming novelty for optical cartridge-case measurement itself. Instead, the research examines the engineering behavior of a specific embedded computer-vision architecture used to measure cartridge-case overall length under controlled static conditions.

Overall length (OAL) was selected as the formal dimensional characteristic because it provides a clearly defined end-to-end measurement while allowing the study to concentrate on one measurement problem. Restricting the formal work to OAL made it possible to evaluate calibration, reference measurement, repeated measurement, physical presentation, estimator behavior, and measurement agreement without simultaneously introducing additional dimensional features and measurement definitions.

An important distinction in this research is the difference between **precision dimensional metrology** and **dimensional screening**. A measurement system intended to replace a precision reference instrument must demonstrate performance appropriate to that metrological role across the intended measurement range. A screening system can serve a different manufacturing function. Rather than requiring every image-derived measurement to function as a final reference-quality dimensional value, a screening system may be used to identify measurements that are comfortably within an acceptance region, distinguish clearly nonconforming measurements, and refer uncertain or near-limit measurements for secondary inspection. Such an architecture still requires quantitative characterization because measurement uncertainty and classification risk must be understood rather than ignored.

CaseMetrology was developed as a static, embedded, backlit computer-vision system for investigating this problem. The research progressed through successive formal validation and engineering iterations. The initial configuration established a prospective measurement baseline. Subsequent diagnostic and fixture-development work investigated sources of repeated-measurement variation, and later configurations introduced improved physical presentation control and a revised OAL estimator. The final prospective configuration provided an opportunity to determine whether improved presentation stability also improved absolute dimensional performance and whether the resulting system behavior supported a defensible industrial-screening interpretation.

Accordingly, the motivation for this thesis extends beyond determining whether a camera and image-processing algorithm can estimate cartridge-case length. The broader engineering question is whether a complete embedded vision system can produce sufficiently stable and characterized dimensional information to support practical inspection decisions, what limitations remain after physical presentation is controlled, and how those limitations affect the role that such a system could reasonably perform in an industrial setting.

## 1.2 Problem Statement

A computer-vision system can produce dimensional values that appear plausible while still being unsuitable for final inspection decisions. For a vision-derived dimension to support manufacturing use, the measurement process must demonstrate acceptable behavior relative to an independent reference, adequate repeatability under repeated presentation, reliable measurement availability, and decision performance appropriate to the intended application.

The CaseMetrology research addressed this problem through successive engineering and validation stages rather than through evaluation of a single image-processing algorithm. The original formal validation established a baseline for measurement agreement and repeated-measurement behavior. Those results showed that the initial system configuration did not satisfy all of the predeclared performance criteria and that placement-dependent variation was a substantial limitation.

Subsequent engineering work therefore focused on understanding and reducing sources of measurement variation. Fixture changes, controlled repositioning studies, estimator development, and controlled-presentation testing were used to determine whether the dominant repeated-measurement limitation could be reduced without changing the fundamental embedded, backlit imaging architecture.

The resulting V3 configuration substantially improved presentation repeatability, but absolute dimensional error remained materially larger than the repositioning error. This created a second engineering problem: improved repeatability alone did not establish that the prototype could be treated as interchangeable with a precision reference instrument across the entire specification interval.

The completed study therefore addresses two related but distinct questions. First, it evaluates whether successive engineering changes improved the measurement behavior of the CaseMetrology system under controlled static conditions. Second, it examines whether the resulting level of performance is more appropriately interpreted as precision metrology or as dimensional screening in which near-limit measurements require secondary inspection.

This distinction is important because the practical value of a dimensional vision system depends on how its demonstrated uncertainty and error characteristics relate to the decision being made. A system that is not suitable as a direct replacement for precision contact measurement may still provide useful screening capability if its measurement behavior is sufficiently stable, its limitations are characterized, and decision rules are designed to account for uncertainty near specification boundaries.

Accordingly, the central problem addressed by this thesis is not simply whether cartridge-case overall length can be estimated from an image. The problem is whether an embedded computer-vision measurement architecture can be engineered and characterized well enough to support defensible dimensional inspection decisions, and what limits remain after major sources of presentation-dependent variation are reduced.

## 1.3 Purpose of the Study

The purpose of this study is to evaluate the engineering performance and practical dimensional-inspection potential of the CaseMetrology embedded computer-vision system for static measurement of cartridge-case overall length.

The study first evaluates the system against prospectively defined measurement-performance criteria using an independent manual reference process. It then examines how successive engineering changes to fixture design, part presentation, and measurement estimation affected repeated-measurement behavior and absolute dimensional performance across V1, V2, and V3.

A further purpose is to determine whether the final demonstrated system behavior is more appropriately interpreted as precision metrology or as dimensional screening. This distinction is evaluated using formal V3 performance results together with an exploratory post-validation guard-band analysis intended to characterize the tradeoff between automatic acceptance and secondary review near specification limits.

The study does not attempt to validate the prototype as a production-ready inline inspection system or as a replacement for precision contact measurement. Instead, it seeks to establish what the demonstrated system can and cannot support under controlled static conditions and to identify the engineering evidence required for any future production-oriented validation.

## 1.4 Research Questions

The completed research is organized around three related questions that reflect the actual chronology of the study. The first question governed the original prospective validation. The second and third questions synthesize the engineering evidence generated after the original validation and are not presented as prospectively defined V1 hypotheses.

### Original Prospective Validation Question

**Can the frozen CaseMetrology computer-vision system measure cartridge-case overall length with acceptable agreement and repeated-measurement performance relative to an independent manual reference measurement process under documented static inspection conditions?**

This question is evaluated using the prospectively established performance criteria and the corresponding formal validation results. The thesis reports explicitly which criteria were satisfied and which were not.

### Engineering Synthesis Question

**What do successive CaseMetrology design iterations reveal about the roles of physical presentation, estimator design, and residual measurement error in the feasibility of embedded computer-vision OAL screening?**

This question synthesizes evidence from V1, the post-V1 diagnostic program, V2, Endface-Hybrid estimator development, controlled-presentation development, and prospective V3 validation. Its purpose is to determine what the completed experimental sequence demonstrates about the principal engineering limitations of the system.

### Exploratory Industrial-Feasibility Question

**Can guarded decision logic provide a practical pathway for using the demonstrated measurement system as a dimensional screening tool while reducing observed false-pass risk near specification limits?**

This question is addressed through post-validation exploratory analysis. It is not used to redefine the original acceptance criteria and does not constitute validation of a production guard-band rule.

## 1.5 Research Objectives

The objectives of the study reflect both the original prospective validation and the subsequent engineering work that followed from the observed results.

### Original Validation Objectives

The original validation objectives were to:

1. establish and freeze the static backlit imaging configuration, acquisition settings, OAL measurement procedure, calibration model, and software environment before formal validation;
2. establish an independent manual reference-measurement process using documented instruments, check-standard controls, repeated measurements, and session-acceptance criteria;
3. select and preserve a formal validation cohort using a documented screening and stratified random-selection procedure;
4. acquire repeated manual-reference and computer-vision measurements under controlled conditions;
5. quantify availability, systematic bias, absolute error, repeated-measurement behavior, and classification performance using prospectively defined statistical criteria; and
6. determine whether the original CaseMetrology configuration satisfied those predefined validation criteria.

### Subsequent Engineering Objectives

Following the original validation, the engineering objectives were expanded to:

7. investigate the principal sources of repeated-measurement variability observed during V1;
8. evaluate whether fixture and presentation changes reduced placement-dependent measurement variation;
9. evaluate the Endface-Hybrid estimator using development data and retrospective V2 analysis while preserving the distinction between retrospective and prospective evidence;
10. prospectively evaluate the frozen Endface-Hybrid estimator under the V3 controlled-presentation configuration;
11. determine whether substantial improvement in presentation repeatability produced a corresponding improvement in absolute dimensional accuracy; and
12. explore whether guarded decision logic could support a practical dimensional-screening architecture while reducing observed false-pass risk near specification boundaries.

These objectives preserve the chronology of the study rather than representing later engineering questions as though they had been part of the original V1 validation plan.

## 1.6 Scope and Delimitations

The formal dimensional characteristic evaluated in this thesis is cartridge-case overall length. Other cartridge-case characteristics, including rim geometry, primer-pocket dimensions, concentricity, wall thickness, and additional dimensional features, are outside the formal validation scope.

The system is evaluated under static inspection conditions. The study does not validate conveyor-based inspection, moving workpieces, robotic handling, automated part loading, or full-rate production operation. Conclusions regarding system performance therefore apply to the documented static measurement configuration rather than to an automated manufacturing line.

The experimental system uses an embedded NVIDIA Jetson Orin Nano Super Developer Kit, an Arducam USB 3.0 IMX296 global-shutter camera, a 16 mm C-mount lens, and LED backlighting. The physical measurement geometry, imaging controls, calibration approach, fixturing, software environment, and frozen estimator configurations are part of the evaluated system. Results should not be generalized automatically to other cameras, lenses, working distances, illumination systems, or processing pipelines.

The source population consisted of 235 uniquely identified cartridge cases. Five specimens used during development were excluded from formal specimen selection. A 60-specimen stratified cohort was then selected for formal validation. The cohort intentionally included specimens distributed around the lower and upper specification limits and therefore was designed to challenge measurement and classification behavior rather than represent natural production yield.

The manual reference process used a single operator for all formal acquisitions. The study therefore characterizes within-operator repeated-measurement behavior under the documented conditions but does not estimate between-operator reproducibility.

The manual reference measurement is treated as the comparison basis for evaluating the computer-vision system, but it is not assumed to be error-free. Reference-measurement uncertainty, instrument resolution, operator influence, and physical case-end geometry remain relevant when interpreting small differences between the two methods.

V2 Endface-Hybrid results are retrospective because the estimator was applied to previously acquired V2 images. Those results are used for comparative and engineering interpretation but are not represented as prospective validation.

The V3 Endface-Hybrid evaluation is prospective with respect to the frozen estimator and controlled-presentation configuration. The estimator and V3 configuration were frozen before formal acquisition, and formal estimator-result interpretation was withheld until completion of the 180-image acquisition.

The guard-band analysis was conducted after the formal V3 results were available. It is therefore exploratory and retrospective. It demonstrates decision-behavior tradeoffs within the formal validation cohort but does not validate a production guard-band rule.

The study does not claim that the demonstrated prototype is production-ready, that it replaces precision contact metrology, or that it has been validated for universal cartridge-case populations or operating environments.

## 1.7 Significance of the Study

The significance of this research lies in the evaluation of dimensional machine vision as a complete engineering measurement system rather than as an image-processing task alone.

The study demonstrates how physical presentation, optical measurement, calibration, reference comparison, estimator behavior, and decision criteria interact in a practical embedded vision system. The successive V1, V2, and V3 configurations provide evidence that a system can become substantially more repeatable without achieving a corresponding proportional improvement in absolute accuracy.

This distinction is important for industrial dimensional inspection. A system that produces highly repeatable results may still contain systematic or residual measurement error that limits its suitability for direct replacement of a precision reference instrument. Conversely, a system that does not satisfy all precision-metrology requirements may still provide useful inspection value if its limitations are understood and incorporated into the decision process.

The V3 results are particularly important because controlled presentation reduced P95 repositioning from 0.004831 in in the V1 configuration to 0.000633 in, an improvement of approximately 86.9%. At the same time, V3 P95 absolute error remained 0.003267 in. The completed experimental sequence therefore provides direct evidence that presentation-dependent repeatability and residual absolute measurement error were separate limitations of the prototype.

This finding shifts the practical interpretation of the system. The completed prototype was not demonstrated as interchangeable with precision contact measurement across the complete specification interval. However, the measured stability, availability, low systematic bias, and exploratory guard-band behavior support further evaluation of the architecture as a dimensional-screening system.

The research also contributes a documented engineering progression in which unsuccessful or partially successful validation results were used to guide subsequent design changes. V1 was not discarded when its criteria were not met. Instead, its results provided evidence that motivated diagnostic testing, fixture improvements, estimator development, and controlled-presentation validation. The resulting sequence illustrates the value of preserving negative and intermediate results as part of an engineering research record.

Finally, the study establishes a traceable evidence base for future work. The formal specimen cohort, acquisition records, estimator freezes, analysis definitions, performance results, and limitations have been preserved so that future studies can evaluate alternative optics, operators, presentation systems, decision rules, additional dimensions, or production-oriented automation without obscuring the basis of the present conclusions.

## 1.8 Organization of the Thesis

Chapter 1 introduces the dimensional-inspection problem, the motivation for the study, the research questions, objectives, scope, delimitations, and significance of the completed V1-through-V3 engineering program.

Chapter 2 reviews literature relevant to industrial machine vision, backlit dimensional inspection, vision-based dimensional metrology, optical geometry, calibration, measurement uncertainty, repeatability, physical presentation, dimensional decision rules, and optical analysis of cartridge cases.

Chapter 3 describes the CaseMetrology hardware and software architecture, calibration and manual reference processes, specimen population and formal cohort, V1 validation methodology, post-V1 diagnostic investigations, V2 engineering iteration, Endface-Hybrid estimator development, V3 controlled-presentation development and freeze, prospective V3 validation, and exploratory guard-band methodology.

Chapter 4 presents the experimental results in chronological order. It reports the V1 formal results, post-V1 diagnostic findings, V2 formal PCA results, retrospective V2 Endface-Hybrid results, controlled-presentation development evidence, prospective V3 formal results, comparative V1-V2-V3 performance, and exploratory guard-band results.

Chapter 5 interprets the findings and answers the research questions. Particular emphasis is placed on the distinction between repeatability and absolute accuracy, the engineering progression from V1 through V3, the practical implications for dimensional screening, the limitations of the demonstrated system, and the requirements for future production-oriented validation.
