# Chapter 2 Literature Audit and Rebuild Record

**Project:** CaseMetrology  
**Date:** 2026-09-17  
**Purpose:** Record the source audit and framing decisions used to rebuild Chapter 2 of the authoritative thesis manuscript.

## Audit Basis

The September 7 Chapter 2 drafts, source matrix, source reviews, bibliography normalization matrix, and working references were reviewed against the final thesis architecture dated September 17.

The September 7 literature review contained a sound core treatment of industrial machine vision, backlit dimensional measurement, calibration, uncertainty, method agreement, and cartridge-case prior art. It was not copied directly because it remained centered on the V1-era research position and did not adequately support the final thesis emphasis on:

- physical presentation and fixturing;
- repeatability versus absolute accuracy;
- dimensional decision rules and guard bands;
- dimensional screening as distinct from precision-metrology replacement; and
- the evidentiary boundary between established literature and findings produced by this thesis.

## Retained Source Set

The rebuilt chapter retains the verified September 7 sources supporting:

- industrial machine vision: Malamas et al. (2003), Hashmi et al. (2022);
- backlit dimensional measurement: Shin et al. (2002), Xiang et al. (2018), Che and Ratnam (2018);
- optical geometry and high-precision vision: Wang et al. (2024), Lai et al. (2026);
- machine-vision metrology and uncertainty: Hemming (2007), Lazzari and Iuculano (2004), Lazzari et al. (2001);
- metrology terminology and uncertainty: JCGM 100:2008 and JCGM 200:2012;
- method agreement and experimental design: Bland and Altman (1986), NIST/SEMATECH, and Lohr (2022);
- historical cartridge-case dimensional inspection: Coleman et al. (1974), Coleman and Swinth (1977), and Swinth et al. (1979); and
- modern cartridge-case optical context: NIST SRM 2461, Sakarya et al. (2012), and Yammen and Muneesawang (2013).

The historical sources remain explicit prior art. Chapter 2 does not claim that CaseMetrology is the first optical, electro-optical, computer-assisted, or automated system to measure cartridge-case total length.

## Added Authoritative Sources

Three sources were added to close final-architecture gaps:

1. Coveney (2014), National Physical Laboratory *Dimensional Measurement Using Vision Systems*, Measurement Good Practice Guide No. 39, Issue 2. This source supports complete-system vision metrology, illumination, optical distortion, pixel calibration, repeatability, and the distinction between repeatability and measurement error.
2. Joint Committee for Guides in Metrology (2012a), JCGM 106:2012. This source supports conformity assessment under measurement uncertainty, acceptance limits, guard bands, and false-acceptance/false-rejection risk.
3. International Organization for Standardization (2017), ISO 14253-1:2017. This source supports dimensional decision rules near specification limits while accounting for measurement uncertainty.

JCGM 106:2012 was already present in the working bibliography but had not been integrated into the September 7 Chapter 2 narrative. It is now used directly.

## Principal Rebuild Decisions

- Chapter 2 now treats physical presentation as part of the measurement architecture. The literature establishes that fixtures, mechanical constraints, calibrated geometry, and controlled motion have been incorporated into prior dimensional systems. The chapter does not claim that prior literature proves the magnitude or cause of CaseMetrology's observed placement effects.
- Repeatability, precision, bias, and accuracy are kept distinct using VIM terminology. The chapter explicitly states that repeatability does not prove absolute accuracy.
- Guard bands are presented as decision-risk tools rather than post hoc error removal. The chapter states that a margin selected retrospectively from one validation cohort is not, by itself, a validated production decision rule.
- Screening is framed as a multistage inspection role in which near-limit results may be referred to secondary inspection. This does not imply precision-gage equivalence.
- The deliberately stratified formal cohort is recognized as useful for challenging near-limit classification but not as a basis for estimating production yield.
- CaseMetrology results are not reported as literature findings. Chapter 2 supplies the interpretive framework; project-specific results remain in Chapters 4 and 5.

## Bibliographic Additions

Coveney, T. (2014). *Dimensional measurement using vision systems* (Measurement Good Practice Guide No. 39, Issue 2). National Physical Laboratory. (Original work published 2001). https://eprintspublications.npl.co.uk/2042/1/mgpg39.pdf

International Organization for Standardization. (2017). *Geometrical product specifications (GPS)—Inspection by measurement of workpieces and measuring equipment—Part 1: Decision rules for verifying conformity or nonconformity with specifications* (ISO 14253-1:2017). https://www.iso.org/standard/70137.html

The existing entry for JCGM 106:2012 remains:

Joint Committee for Guides in Metrology. (2012a). *Evaluation of measurement data—The role of measurement uncertainty in conformity assessment* (JCGM 106:2012). https://doi.org/10.59161/JCGM106-2012

## Remaining Bibliographic Actions

The historical metadata issues already identified on September 7 remain pending final reference-list preparation:

- confirm the formal SPIE volume title for Swinth et al. (1979);
- resolve the final publication-year convention for Coleman and Swinth;
- choose the final report/conference form for Coleman et al. (1974);
- choose the certificate or official documentation record for NIST SRM 2461; and
- choose one consistent final citation form for the NIST/SEMATECH e-Handbook.

These issues do not prevent use of the verified source claims in Chapter 2, but they must be resolved before final thesis submission.

## Outcome

Chapter 2 was integrated into `2026-09-17_thesis_manuscript_rebuild.md` without modifying Chapter 1. The rebuilt chapter supports the frozen final architecture and preserves the distinction among established literature, retrospective analysis, prospective validation, and exploratory industrial-feasibility interpretation.
