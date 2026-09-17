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

# Chapter 2 — Literature Review

## 2.1 Introduction

The use of machine vision for dimensional inspection lies at the intersection of industrial automation, computer vision, and measurement science. A camera-based system can detect a workpiece and calculate a dimension, but those functions alone do not establish that the reported value is suitable for a manufacturing decision. Dimensional validity also depends on how the image is formed, how physical boundaries are localized, how image coordinates are related to physical units, how the workpiece is presented, how repeated observations behave, and how measurement uncertainty is incorporated into the eventual decision.

These distinctions are especially important for the present study because its final engineering interpretation concerns dimensional screening rather than unrestricted replacement of precision contact metrology. A screening system and a reference-quality measuring system may use similar image-processing operations, yet their required evidence and permissible decisions are different. The literature therefore must address not only how dimensions can be extracted from images, but also how such measurements are characterized and how uncertainty affects acceptance near specification limits.

This chapter reviews nine connected topics: industrial machine vision and dimensional inspection; backlit silhouette measurement; boundary localization and subpixel methods; optical geometry and lens architecture; physical presentation and fixturing; calibration, traceability, and uncertainty; repeatability, accuracy, and method agreement; conformity decisions and guard bands; and prior optical analysis of cartridge cases. The chapter concludes by defining the research position of CaseMetrology without claiming novelty for optical cartridge-case measurement itself. Findings specific to CaseMetrology are reserved for Chapters 4 and 5.

## 2.2 Industrial Machine Vision and Dimensional Inspection

Industrial machine vision combines image acquisition, computation, and application-specific decision logic to inspect manufactured products and processes. Malamas et al. (2003) described industrial vision systems as supporting tasks such as identification, gauging, assembly verification, surface inspection, and process control. Hashmi et al. (2022) similarly reviewed measurement-oriented applications of machine vision in manufacturing. Across these applications, the usefulness of a vision system depends on a clearly defined inspection objective, appropriate image acquisition, and performance demonstrated under the conditions in which the system will be used.

Dimensional inspection differs from detection or classification because it requires a defensible relationship between image information and a physical measurand. The International Vocabulary of Metrology defines a measurand as the quantity intended to be measured and treats a measurement result as more than an instrument indication alone (Joint Committee for Guides in Metrology, 2012b). In image-based dimensional work, the measurand must therefore be defined independently of the pixels or contours used to estimate it. A segmented silhouette is evidence about a physical boundary; it is not itself the physical dimension.

Coveney's (2014) National Physical Laboratory guide describes dimensional vision systems as integrated arrangements for image formation and sensing, image processing, and communication of results. The guide emphasizes that illumination, lens selection, camera behavior, calibration, edge detection, distortion, and uncertainty all influence dimensional measurement. This complete-system view is consistent with Hemming's (2007) metrological treatment of machine vision and with the uncertainty framework developed for optical vision measuring machines by Lazzari and Iuculano (2004).

Industrial use also requires a defined relationship between the measurement and the action taken from it. Historical manufacturing systems have used optical measurements for automatic classification, rejection, and process feedback, including high-throughput cartridge-case inspection (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979). Such examples demonstrate that image-derived dimensions can support production decisions. They do not establish that every optical measurement architecture has equivalent accuracy, uncertainty, or decision risk. Fitness for purpose remains an application-specific property that must be demonstrated for the implemented system.

This distinction supports two possible roles for dimensional machine vision. In a metrology role, the reported value is expected to perform as a defensible dimensional result across the intended range and operating conditions. In a screening role, the system may instead separate clear cases from measurements that require confirmation. Screening does not eliminate the need for validation. It changes the decision architecture: system limitations are managed through defined acceptance, review, and rejection logic rather than ignored.

## 2.3 Backlit Dimensional Vision and Boundary Localization

### 2.3.1 Backlit silhouette measurement

Backlighting is a widely used arrangement for dimensional vision because transmitted light can create strong contrast between an opaque workpiece and the illuminated background. Coveney (2014) identifies contrast and field uniformity as primary considerations when selecting illumination for dimensional measurement. A high-contrast silhouette can simplify the localization of external boundaries, but the measured dimension still depends on how those boundaries are imaged and interpreted.

Shin et al. (2002) developed a machine-vision system for dimensional inspection of ball studs using backlit silhouetted images. Their system extracted outlines at subpixel resolution, modeled boundary data with geometric primitives, and used jig fixtures and controlled motion to present different regions of the part. The study is relevant because it combines illumination, edge localization, geometric interpretation, and physical presentation within one dimensional measurement architecture.

Xiang et al. (2018) used a two-camera backlit arrangement to measure the spacing of automobile brake-pad bayonets. Their method incorporated a purpose-designed dimensional standard, relative edge-position measurement, edge detection, and line fitting. The work is also important because it evaluated both dimensional bias and repeatability against application-specific requirements. Its numerical results are not directly transferable to a single-camera cartridge-case system, but the experimental structure illustrates that a dimensional vision method should be evaluated as more than an edge-detection algorithm.

Che and Ratnam (2018) applied LED backlighting and subpixel edge localization to monitor workpiece diameter during turning. Vision-derived values were compared quantitatively with digital-caliper measurements. The workpiece remained constrained by the machine tool, so the presentation conditions differ from independent static placement. Nevertheless, the study provides precedent for converting silhouette-edge information into a physical dimension and evaluating it against a conventional contact method.

Collectively, these studies establish that backlit dimensional vision is an integrated measurement approach. Illumination creates the observable boundary, the optical system maps that boundary to the sensor, software estimates its location, calibration converts image position to physical units, and specimen presentation determines the geometry under which those operations occur. Failure or variability in any one of those relationships can affect the final dimension.

### 2.3.2 Thresholding, contours, and subpixel localization

Silhouette processing often begins with separation of the object from its background. Otsu's (1979) method selects a global threshold from the gray-level histogram by optimizing between-class separation. It is a general segmentation method rather than a dimensional estimator. A binary mask produced by thresholding identifies foreground and background regions, but it does not by itself define which points correspond to the intended physical endpoints of a manufactured part.

After segmentation, dimensional systems may use contour extraction, fitted lines or circles, geometric primitives, principal directions, or local edge models. Principal component analysis provides a general method for determining dominant directions in multivariate data (Jolliffe & Cadima, 2016), but the conversion of a component direction into a physical end-to-end measurement remains application specific. Similarly, a fitted geometric model can stabilize a boundary estimate only when the chosen model corresponds appropriately to the measured feature.

Subpixel localization is frequently used when the desired dimensional discrimination is finer than one sensor pixel. Shin et al. (2002) and Che and Ratnam (2018) incorporated subpixel edge methods into backlit dimensional systems. Lai et al. (2026) combined a telecentric calibration framework with distortion correction, contour information, illumination compensation, and subpixel edge detection. Their work demonstrates that image-space localization finer than one pixel is possible under a carefully modeled system.

Subpixel output should not be equated automatically with subpixel physical accuracy. Pixel interpolation or model fitting can produce fractional-pixel coordinates, but the physical accuracy of those coordinates still depends on focus, optical distortion, illumination, threshold or edge model, calibration, workpiece geometry, and presentation. Coveney (2014) likewise treats threshold setting, magnification, distortion, pixel calibration, and measurement uncertainty as connected aspects of dimensional vision. The literature therefore supports subpixel localization as a measurement tool, not as an independent guarantee of metrological performance.

## 2.4 Optical Geometry and Lens Architecture

### 2.4.1 Calibration and measurement-plane geometry

Monocular dimensional measurement depends on the relationship among the camera, lens, calibrated coordinate system, measurement plane, and workpiece. For a conventional perspective lens, changes in object distance or orientation can alter projected size. Lateral field position can also matter when distortion or spatially varying magnification is not adequately controlled or modeled.

Wang et al. (2024) analyzed dimensional error arising when the physical measurement plane differs from the plane represented during camera calibration. Their theoretical and experimental work considered translation and rotation between calibration and measurement geometries and included both conventional industrial and telecentric optics. Under the assumptions evaluated, displacement along the optical axis could produce systematic scale error, while more general nonperpendicular geometry produced more complex relationships. The broader implication is that a calibration is valid within a physical geometry, not merely within a software file.

Coveney (2014) similarly recommends evaluating distortion and magnification across the usable image area and repeating pixel calibration within the area selected for measurement. The guide notes that distortion-related errors are often most apparent near the edge of the field. These principles are relevant to conventional area-camera systems because a single nominal pixels-per-unit value does not automatically describe all image locations and orientations with equal fidelity.

The literature establishes plausible mechanisms by which geometric change can influence a dimensional result. It does not justify assigning a particular error mechanism to another system without an experiment that isolates the relevant displacement, rotation, or field-position effect. In the present thesis, general optical-geometry literature supplies the rationale for controlling and documenting presentation geometry; CaseMetrology-specific causal conclusions must come from the project's own experiments.

### 2.4.2 Conventional and telecentric optics

Telecentric lenses are often used in high-precision dimensional vision because they reduce perspective effects and maintain approximately constant magnification over a defined depth range. Lai et al. (2026) developed a telecentric dimensional system with a calibration model matched to telecentric image formation. Wang et al. (2024) also included telecentric optics when experimentally evaluating external-geometry effects. These sources demonstrate why telecentric systems can be advantageous where object depth and perspective sensitivity are critical.

Telecentric optics do not eliminate the need for calibration, distortion characterization, boundary localization, illumination control, or uncertainty analysis. Lai et al. (2026) treated those elements jointly despite using a telecentric lens. Telecentric and conventional systems also involve different imaging models, fields of view, hardware costs, and physical constraints. Performance reported for a telecentric system cannot therefore be transferred directly to a conventional-lens system.

For conventional optics, dimensional performance can still be evaluated empirically and may be adequate for a defined task. The appropriate conclusion from the literature is not that one optical architecture is universally required, but that the selected architecture, calibration model, working distance, measurement plane, and allowed presentation variation must be mutually consistent with the required measurement and decision performance.

## 2.5 Physical Presentation and Fixturing

Physical presentation determines how the workpiece occupies the calibrated imaging geometry. Relevant degrees of freedom can include translation within the field, rotation within the measurement plane, displacement along the optical axis, tilt relative to the measurement plane, and part-specific roll or seating behavior. Some of these changes may affect scale or distortion; others may alter which physical surface or edge becomes the apparent silhouette boundary.

Prior dimensional systems often controlled presentation as part of the measurement design. Shin et al. (2002) used jig fixtures and servo-controlled rotation and translation in the ball-stud system. Che and Ratnam's (2018) workpiece remained mechanically constrained by the lathe. The historical cartridge-case profile monitors used dedicated mechanical handling, gauging fixtures, and precision reference surfaces rather than treating part placement as incidental (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979).

The value of these examples is architectural. They show that a dimensional vision system can include mechanical registration and controlled motion as integral measurement components. The examples do not establish a universal fixture design, nor do they prove that fixturing alone determines measurement accuracy. Hemming (2007) found that dominant uncertainty contributions differed by application and could arise from optical, mechanical, geometric, algorithmic, environmental, operator, or object-related effects.

A fixture may improve repeated presentation by constraining relevant degrees of freedom, but it can also introduce contact, obstruction, deformation, or a new datum relationship. Fixture evaluation should therefore consider whether the part is seated consistently, whether the measured edges remain visible, whether contact forces change the measurand, and whether the fixture maintains the workpiece within the calibrated geometry. A fixture's purpose is not simply to hold the object still; it is to establish repeatable measurement conditions appropriate to the measurand.

This literature provides the conceptual foundation for investigating presentation-dependent variation. It also establishes an important boundary: the general importance of presentation and fixturing is established in prior work, whereas the magnitude of their effects in CaseMetrology is an experimental finding of this thesis and is not assumed from the literature.

## 2.6 Calibration, Traceability, and Measurement Uncertainty

### 2.6.1 Calibration and traceability

Calibration establishes a relationship between indications and known reference values under specified conditions. Metrological traceability requires a documented, unbroken chain of calibrations linking a measurement result to an appropriate reference, with each link contributing to measurement uncertainty (Joint Committee for Guides in Metrology, 2012b). For dimensional vision, this commonly requires a physical length artifact or calibrated scale together with a defined model relating image coordinates to physical units.

Calibration is necessary but not sufficient. A valid scale factor does not characterize boundary localization, distortion, workpiece geometry, presentation variation, environmental effects, or reference-method behavior. Hemming (2007) demonstrated that machine-vision uncertainty budgets are application specific and that dominant contributions can differ among systems. In some applications, camera, lens, and edge-finding behavior were important; in others, mechanical or geometric effects dominated.

Lazzari and Iuculano (2004) treated a camera-equipped optical measuring machine as a metrological system and developed a GUM-oriented uncertainty model. Their work distinguished verification of instrument performance from evaluation of uncertainty associated with a measurement result. Related work from the same research program used certified dimensional standards and repeated measurements while separating machine-related and vision-related behavior (Lazzari et al., 2001). These studies provide precedent for examining subsystems individually while maintaining a complete-system measurement model.

The practical guidance from Coveney (2014) is consistent with those studies. Pixel calibration, threshold selection, distortion, magnification, repeated observations, calibration-standard uncertainty, and environmental conditions can all contribute to the final result. A manufacturer's accuracy specification or a successful check measurement is not automatically equivalent to the uncertainty of a measurement made on a particular workpiece.

### 2.6.2 Reference measurements and uncertainty

The Guide to the Expression of Uncertainty in Measurement provides a general framework for identifying input quantities, evaluating uncertainty contributions, and combining them into a measurement-uncertainty statement (Joint Committee for Guides in Metrology, 2008). The VIM further distinguishes error, bias, precision, repeatability, reproducibility, and uncertainty (Joint Committee for Guides in Metrology, 2012b). These terms describe different properties and should not be substituted for one another.

An independent comparator used in a validation study is therefore better described as a reference measurement process than as error-free truth. Its calibration, resolution, repeatability, operator procedure, contact force, alignment, environmental conditions, and workpiece geometry can affect the assigned reference value. Che and Ratnam (2018) provide precedent for comparing vision-derived dimensions with digital-caliper measurements, but accessible evidence from that study does not establish a complete uncertainty treatment for the comparator. The literature supports comparison to an external method while also requiring caution about the reference method's limitations.

CaseMetrology's manual reference process and its uncertainty are described in Chapter 3. The literature does not supply the project-specific uncertainty value, nor does the uncertainty of the manual reference process constitute a complete uncertainty budget for the computer-vision system. The latter was characterized empirically in this study through agreement, error, repeated-placement, availability, and classification metrics.

## 2.7 Repeatability, Accuracy, and Measurement-System Agreement

### 2.7.1 Repeatability is not accuracy

The VIM defines measurement precision in terms of agreement among replicate measurements under specified conditions and defines repeatability as precision under repeatability conditions (Joint Committee for Guides in Metrology, 2012b). Measurement accuracy concerns closeness between a measured value and the true value of the measurand; it is related to both trueness and precision and is not itself assigned a numerical quantity value in the VIM framework.

These definitions establish why a repeatable system is not necessarily accurate. A system may return tightly grouped repeated values that share a systematic offset or another stable error. Conversely, a system may show little average bias across a cohort while producing substantial specimen-level scatter. Bias, absolute error, and repeated-measurement dispersion therefore answer different engineering questions.

Coveney (2014) explicitly warns that strong day-to-day repeatability does not preclude measurement error arising from calibration, environment, equipment, procedure, or operator effects. Xiang et al. (2018) likewise reported bias and repeatability as separate performance characteristics. Hemming (2007) and Lazzari and Iuculano (2004) provide the broader metrological basis for evaluating multiple contributions rather than treating one precision statistic as proof of complete measurement quality.

This distinction is central to the final CaseMetrology architecture, but the literature review does not state the project's experimental outcome. It establishes the framework used later to interpret whether changes in repeated-presentation behavior were accompanied by corresponding changes in absolute agreement with the reference process.

### 2.7.2 Method agreement and validation design

Correlation is not a substitute for agreement between measurement methods. Bland and Altman (1986) showed that two methods can be strongly correlated while still differing systematically or by an amount that is unacceptable for the intended use. Difference-based analyses are therefore appropriate when evaluating whether an image-derived dimension agrees sufficiently with an independent reference.

A dimensional validation should also distinguish among measurement availability, mean bias, error magnitude, repeated-measurement variation, range-dependent behavior, and classification outcomes. No single metric answers all of these questions. For example, a low mean bias can coexist with large absolute errors of opposing sign, and perfect measurement availability does not imply acceptable dimensional accuracy.

Replication and randomization help characterize repeated observations and reduce confounding between acquisition order and uncontrolled temporal changes (NIST/SEMATECH, n.d.). The definition of replication is important: repeated processing of the same image evaluates algorithmic determinism, repeated images without moving the part evaluate short-term acquisition variation, and complete removal and replacement evaluate a broader presentation process. Repeatability values from different experimental conditions should not be compared as though they describe the same source of variation.

Sampling design also determines what can be inferred. Stratified sampling can intentionally increase representation in scientifically important regions, such as near specification limits, but results must be interpreted in relation to the design (Lohr, 2022). A cohort deliberately concentrated near decision boundaries is useful for challenging classification behavior; its raw acceptance fraction is not automatically an estimate of natural production yield.

## 2.8 Conformity Decisions, Guard Bands, and Screening

### 2.8.1 Decisions under measurement uncertainty

Dimensional specifications define permissible values of a product characteristic, whereas measurements provide uncertain information about those values. JCGM 106:2012 addresses conformity decisions made from measurement results and distinguishes tolerance limits from acceptance limits (Joint Committee for Guides in Metrology, 2012a). When an acceptance limit is displaced from a tolerance limit, the interval between them is a guard band. The purpose is to manage the probability and consequences of incorrect decisions, not to imply that measurement uncertainty has disappeared.

ISO 14253-1:2017 provides decision rules for verifying conformity or nonconformity of geometrical product specifications while taking measurement uncertainty into account, including cases in which measured values fall near specification limits (International Organization for Standardization, 2017). Together, JCGM 106 and ISO 14253-1 establish that direct comparison of a point estimate with a specification limit is only one possible decision rule.

Two incorrect outcomes are especially relevant. False acceptance occurs when a nonconforming item is accepted, while false rejection occurs when a conforming item is rejected. JCGM 106 relates these outcomes to consumer and producer risks and shows that changing the acceptance limits redistributes those risks. Narrowing the automatic-acceptance interval can reduce false-acceptance risk, but it also increases the number of conforming items that are rejected or withheld from automatic acceptance.

A defensible guard band is therefore not simply the smallest margin that removes errors from one observed dataset. Its selection ordinarily depends on the measurement model, uncertainty, risk tolerance, consequences of each decision error, and the intended operating population. A margin selected retrospectively from a limited validation cohort can demonstrate observed decision behavior, but it cannot by itself establish a validated production decision rule or a general false-acceptance probability.

### 2.8.2 Guarded screening architectures

Guarded decisions can be implemented as either binary or multistage processes. In a binary process, a result within the acceptance interval is accepted and a result outside it is rejected. In a screening process, a third disposition is possible: measurements comfortably within the guarded interval may be accepted automatically, while near-limit measurements are referred to a more capable or independent measurement process. Measurements clearly outside specification may likewise be rejected, confirmed, or investigated according to the production procedure.

This multistage architecture separates screening from final reference measurement. Its value depends on the screened population, the performance of both measurement stages, the disposition of review-zone items, and the cost or consequence of incorrect decisions. The screening system still requires characterized measurement behavior because its acceptance and referral boundaries must be connected to empirical performance and risk.

Historical cartridge-case systems used optical measurements for automatic accept/reject decisions and incorporated calibration or known standards for system assurance (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979). Those systems demonstrate industrial precedent for integrating optical measurement with manufacturing decisions. JCGM 106:2012 and ISO 14253-1:2017 provide the modern metrological framework for understanding why decision limits and measurement uncertainty must be considered explicitly.

For the present thesis, this literature supports evaluation of guarded screening as an engineering pathway. It does not prevalidate any CaseMetrology-specific margin. The status, derivation, cohort dependence, and limitations of the project's exploratory guard-band analysis are addressed separately in Chapters 3 through 5.

## 2.9 Optical and Computational Analysis of Cartridge Cases

### 2.9.1 Historical manufacturing inspection

Electro-optical dimensional inspection of cartridge cases predates modern area-camera computer vision. Work at Pacific Northwest Laboratory and Battelle developed automatic high-speed cartridge-case inspection systems that combined mechanical handling, electro-optical profile measurement, computer processing, process monitoring, and rejection (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979).

The systems measured several cartridge-case characteristics, including total length, head thickness, head diameter, extractor-groove diameter, and gas-seal length. Transmitted illumination created projected shadows that were analyzed with linear diode or CCD arrays. Known or calibrated standards could be inserted for system checks, and automatically measured cases could be compared with conventionally gauged values. The reported systems operated at manufacturing throughput and linked dimensional measurement to automated disposition.

These sources are the most direct prior art for the CaseMetrology application. They establish that optical measurement of cartridge-case total length, computer-assisted inspection, calibration checks, comparison with conventional gauging, and automated classification were demonstrated decades before the present study.

The historical architecture differed materially from CaseMetrology. It used dedicated mechanical handling, precision gauging references, optical projection, fiber-optic image transfer, and linear sensor arrays. CaseMetrology uses a static two-dimensional area camera, embedded processing, software-defined silhouette measurement, and preserved raw images. Those differences define a distinct implementation and experimental study; they do not justify a first-ever claim for optical cartridge-case measurement.

### 2.9.2 Modern forensic imaging context

Modern cartridge-case imaging literature is dominated by forensic surface and topography analysis rather than manufacturing OAL measurement. NIST Standard Reference Material 2461 provides a standard cartridge case for quality assurance and performance evaluation of optical topography systems used in firearm identification (National Institute of Standards and Technology, n.d.). Other research has addressed automated segmentation of cartridge-case base regions and image matching of forensic marks (Sakarya et al., 2012; Yammen & Muneesawang, 2013).

This literature confirms that controlled optical acquisition and computational analysis of cartridge cases are established fields. The measurands and decisions, however, differ from dimensional manufacturing inspection. Surface-topography comparison, region-of-interest extraction, and forensic image matching do not establish OAL accuracy or production conformance performance. These sources therefore provide cartridge-specific optical context but are not substitutes for dimensional-metrology literature.

## 2.10 Literature Synthesis and Research Position

The literature supports six conclusions that frame the CaseMetrology study.

First, dimensional machine vision is a complete measurement-system problem. Image formation, illumination, optical geometry, boundary localization, calibration, mechanical relationships, specimen presentation, reference comparison, and decision logic can all affect the reported result (Hemming, 2007; Lazzari & Iuculano, 2004; Coveney, 2014).

Second, backlit silhouette measurement is an established method for manufacturing dimensions. Prior systems have combined transmitted illumination with edge or contour localization, geometric fitting, calibration, and external comparison (Shin et al., 2002; Xiang et al., 2018; Che & Ratnam, 2018). The research question is therefore not whether a silhouette can yield a dimension, but whether a specific system produces measurement behavior adequate for its intended role.

Third, physical presentation is part of the measurement architecture. Prior systems used fixtures, machine-tool constraints, servo motion, or dedicated handling, while optical-geometry research demonstrates why the relationship between the calibrated plane and the measured object matters (Shin et al., 2002; Wang et al., 2024). The literature justifies controlling and studying presentation, but the quantitative effect of that control in CaseMetrology remains a project-specific experimental result.

Fourth, repeatability and absolute accuracy are distinct. Precision under repeated conditions does not prove closeness to the reference value, and low average bias does not prove small specimen-level error (Joint Committee for Guides in Metrology, 2012b; Coveney, 2014). A defensible evaluation therefore requires separate characterization of bias, absolute error, repeated-measurement behavior, availability, and decision outcomes.

Fifth, manufacturing decisions must account for uncertainty and risk near specification limits. JCGM 106:2012 and ISO 14253-1:2017 distinguish specification limits from acceptance limits and provide the basis for guarded decision rules. A guarded screening architecture can refer near-limit measurements for secondary inspection, but an empirically selected margin is not a validated production guard band without prospective evaluation and an appropriate risk basis.

Sixth, optical cartridge-case dimensional inspection is not novel. Historical systems measured total case length and other dimensions, used calibration and conventional-gauge comparisons, and performed automated rejection (Coleman et al., 1974; Coleman & Swinth, 1977; Swinth et al., 1979). The contribution of CaseMetrology must therefore be stated more narrowly.

CaseMetrology occupies a research space defined by the engineering evaluation of a modern embedded, static, backlit area-camera architecture for cartridge-case OAL. Its contribution lies in the documented progression from prospective baseline validation through diagnostic investigation, fixture and presentation control, estimator development, and prospective evaluation of the final frozen configuration. The research also evaluates the difference between repeated-presentation stability and absolute agreement and explores how measured limitations could be incorporated into a guarded screening process.

This position does not claim that CaseMetrology replaces precision contact metrology, that it is production ready, or that its exploratory decision margins are validated for production. Instead, the literature supports the narrower question answered by the thesis: what a specific embedded dimensional-vision architecture can defensibly support under documented static conditions, what limitations remain, and how those limitations affect its potential role as an industrial screening tool.
