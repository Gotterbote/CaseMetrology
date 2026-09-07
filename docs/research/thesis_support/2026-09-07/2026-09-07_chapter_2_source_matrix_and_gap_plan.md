# Chapter 2 Literature Review — Source Matrix and Gap Plan

**Project:** CaseMetrology
**Date:** 2026-09-07
**Status:** Working literature-review planning record

## 1. Purpose

This record defines the literature categories required to support Chapter 2 of
the CaseMetrology thesis and distinguishes established sources from sources
requiring full review and genuine literature gaps requiring targeted searching.

The literature review shall not assume that CaseMetrology is the first optical,
electro-optical, or computer-assisted system to measure cartridge-case
dimensions. Historical cartridge-case inspection literature already establishes
prior use of electro-optical dimensional measurement.

The final contribution/novelty statement shall be written only after the
literature review is sufficiently complete.

## 2. Proposed Chapter 2 Structure

### 2.1 Industrial Machine Vision and Dimensional Inspection

Purpose:
- establish machine vision as an industrial inspection and measurement method;
- distinguish inspection/detection from defensible dimensional metrology;
- introduce the importance of controlled image acquisition and application-
  specific validation.

Existing sources:
- Malamas et al. (2003), industrial vision systems survey.
- Hashmi et al. (2022), manufacturing-oriented machine-vision context.

Disposition:
- RETAIN.
- Verify the exact claims assigned to each source before final citation.

### 2.2 Vision-Based Dimensional Metrology

Purpose:
- review 2D optical dimensional measurement;
- discuss pixel-to-physical calibration;
- discuss contour/edge localization;
- discuss effects of optical geometry and specimen position;
- place CaseMetrology's conventional-lens area-camera architecture in context.

Existing/candidate sources:
- Shin, Han, and Moon (2002), "Ball stud inspection system using machine
  vision," ISA Transactions, 41(1), 3-11.
  DOI: 10.1016/S0019-0578(07)60197-9
- Lai, Li, Wang, and Zhang (2026), "A telecentric vision system tailored for
  high-precision dimensional measurement: Calibration and subpixel edge
  detection," Measurement, 274, 121239.
  DOI: 10.1016/j.measurement.2026.121239

Disposition:
- FULL-PAPER REVIEW REQUIRED.
- Shin is directly relevant to backlit silhouette dimensional measurement.
- Lai is useful modern dimensional-metrology context but uses telecentric
  imaging and must not be presented as directly equivalent to CaseMetrology.

Remaining gap:
- identify additional peer-reviewed 2D area-camera dimensional-metrology work,
  preferably including conventional non-telecentric imaging, spatial scale
  variation, calibration, or object-position sensitivity.

### 2.3 Image Segmentation, Thresholding, and Geometric Measurement

Purpose:
- support the general image-processing principles used by CaseMetrology;
- distinguish general literature-derived methods from CaseMetrology-specific
  estimator logic.

Existing sources:
- Otsu (1979), histogram-based threshold selection.
- Gonzalez and Woods, Digital Image Processing, 4th ed.
- Jolliffe and Cadima (2016), principal-component-analysis review.

Disposition:
- READY FOR USE.
- Do not attribute CaseMetrology-specific endpoint or calibration logic to
  these general sources.

### 2.4 Calibration, Traceability, and Measurement Uncertainty

Purpose:
- establish that image-derived dimensions require calibration and a defined
  measurement model;
- define uncertainty, traceability, influence quantities, repeatability, and
  reproducibility;
- support treatment of the manual comparator as a reference measurement
  process rather than error-free truth.

Existing sources:
- JCGM 100:2008, GUM.
- JCGM 200:2012, VIM.
- JCGM 106:2012, measurement uncertainty in conformity assessment.
- ISO 5725-2:2019, if selectively retained for precision terminology.

Disposition:
- STRONG CORE SOURCES.
- ISO 5725 must not be used to imply that CaseMetrology performed an ISO
  interlaboratory precision study.

Remaining gap:
- identify one or more applied optical/vision dimensional-metrology sources
  showing practical interaction among camera calibration, edge localization,
  and dimensional uncertainty.

### 2.5 Measurement-Method Agreement and Experimental Design

Purpose:
- justify specimen-level method agreement rather than reliance on correlation;
- support randomized replication and separation of development from formal
  validation.

Existing sources:
- Bland and Altman (1986), measurement-method agreement.
- NIST/SEMATECH Engineering Statistics Handbook.
- Lohr (2022), Sampling: Design and Analysis, 3rd ed.

Disposition:
- READY FOR USE.

### 2.6 Historical Cartridge-Case Dimensional Inspection

Purpose:
- document prior electro-optical cartridge-case dimensional inspection;
- establish that optical cartridge-case dimensional measurement predates
  CaseMetrology;
- distinguish historical high-throughput dedicated inspection systems from
  the present embedded area-camera research architecture.

Existing source set:
- High-throughput dimensional measurements with electro-optics.
- Automatic cartridge case inspection and process control.
- Historical cartridge-case inspection report preserved as 4272487.pdf.
- Coleman and Swinth (1978), Pacific Northwest Laboratory cartridge-case
  measurement/eject system.

Known historical characteristics requiring source-level verification:
- electro-optical dimensional measurement;
- dedicated mechanical handling;
- high-throughput automated inspection;
- multiple cartridge-case dimensions;
- calibration / quality-assurance controls;
- comparison with hand-gauged values.

Disposition:
- CENTRAL CHAPTER 2 SOURCES.
- FULL-PAPER REVIEW REQUIRED.
- Do not claim CaseMetrology is the first optical system to measure
  cartridge-case total length.

### 2.7 Modern Cartridge-Case Optical and Computational Analysis

Purpose:
- establish modern optical/computational analysis of cartridge cases;
- distinguish forensic surface/topography analysis from manufacturing
  dimensional metrology.

Existing sources:
- NIST SRM 2461 Standard Cartridge Case.
- Cartridge-case image matching literature.
- Automated cartridge-case region-of-interest segmentation literature.

Disposition:
- USE AS CONTEXT ONLY.
- NIST SRM 2461 concerns forensic cartridge-case surface/topography
  measurement quality assurance and is not an OAL dimensional standard.
- Forensic image-analysis papers shall not be represented as validation of
  manufacturing OAL measurement.

### 2.8 Literature Synthesis and Research Position

The final synthesis shall answer:

1. What optical and machine-vision methods have previously been used for
   dimensional manufacturing inspection?
2. What prior work specifically measured cartridge-case dimensions?
3. What measurement-system limitations are recognized in vision-based
   dimensional metrology?
4. How have calibration, repeatability, uncertainty, and agreement been
   evaluated in prior work?
5. What specific research contribution remains for CaseMetrology?

A defensible contribution statement is expected to focus on the combination of
the tested architecture and research methodology rather than claiming invention
of optical cartridge-case measurement.

Potential contribution dimensions to evaluate after completing the review:
- embedded area-camera implementation;
- static backlit side-view OAL measurement;
- software-defined spatial/directional calibration;
- prospective method freeze;
- independent calibrated manual-reference comparison;
- stratified formal validation;
- predefined engineering acceptance criteria;
- explicit failure accounting;
- measurement-uncertainty treatment;
- preservation of raw data, derived results, software state, and Git
  provenance.

These attributes shall not be called novel until the literature review confirms
that characterization.

## 3. Targeted Search Gaps

The remaining literature search should concentrate on:

1. peer-reviewed 2D machine-vision dimensional metrology using area cameras;
2. backlit/silhouette dimensional measurement of manufactured components;
3. conventional-lens spatial calibration and image-position sensitivity;
4. measurement uncertainty in camera-based dimensional systems;
5. modern optical dimensional inspection of ammunition or cartridge cases;
6. studies comparing vision-derived dimensions with calibrated contact/manual
   reference measurements.

Broad searches for generic computer vision or deep learning are not a priority
unless they directly support one of these questions.

## 4. Novelty Guardrail

Until the targeted literature review is complete, the thesis shall not claim
that CaseMetrology is:

- the first optical cartridge-case inspection system;
- the first computer-assisted cartridge-case measurement system;
- the first system to measure cartridge-case overall length optically; or
- the first automated cartridge-case dimensional inspection system.

Historical evidence already demonstrates prior electro-optical cartridge-case
dimensional inspection.

The final literature-gap statement shall instead identify the narrower research
space actually supported by the completed review.
