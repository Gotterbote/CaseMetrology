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
