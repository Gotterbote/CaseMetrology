# Chapter 3 Source-Gap Closure and K-State ETDR Alignment

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Status:** Working thesis-support record; repository commit intentionally deferred.

# 1. Purpose

This record closes the three external-source gaps remaining after the Chapter 3 sentence-level evidence audit:

1. general image-processing support for Gaussian filtering, morphology, and segmentation;
2. a defensible stratified-sampling source;
3. current Kansas State University ETDR guidance on citation/formatting responsibility and thesis reproducibility.

---

# 2. Final image-processing source

## Selected source

Rafael C. Gonzalez and Richard E. Woods.
*Digital Image Processing*, 4th ed. Pearson.

A verified Pearson listing identifies the fourth edition and describes its coverage of spatial filtering and image-processing fundamentals. The book's table of contents and associated bibliographic records include morphological image processing and image segmentation.

## Use in CaseMetrology Chapter 3

Use this source in Section 3.4 for general explanations of:

- Gaussian/spatial smoothing;
- binary morphological opening and closing;
- connected-region / segmentation concepts.

## Evidence boundary

This textbook supports what those image-processing operations mean in general.

It does **not** prove that CaseMetrology used:

- a 5 × 5 Gaussian kernel;
- Otsu thresholding;
- 3 × 3 opening;
- 3 × 3 closing;
- largest-component retention.

Those exact choices remain repository-supported implementation facts.

## Citation strategy

Use Otsu (1979) for the named Otsu thresholding method and Gonzalez & Woods for the surrounding standard image-processing operations. This avoids asking one citation to support the entire CaseMetrology pipeline.

**Source gap status:** CLOSED.

---

# 3. Final stratified-sampling source

## Selected source

Sharon L. Lohr.
*Sampling: Design and Analysis*, 3rd ed. Chapman & Hall/CRC Press, 2022.

The publisher's table of contents identifies Chapter 3 as **Stratified Sampling**.

## Use in CaseMetrology Chapter 3

Use in Section 3.9 only if the thesis gives a general explanation of why stratified random sampling is used.

Recommended role:

> General sampling literature supports partitioning a finite population into defined strata and performing probability selection within those strata; the actual CaseMetrology stratum boundaries, allocation rules, exclusions, and selection implementation are prospective project-specific decisions.

## Evidence boundary

Lohr does not establish:

- the final CaseMetrology stratum boundaries;
- the final number drawn from each stratum;
- the final 60 selected IDs;
- the project's excluded prevalidation specimens.

Those remain repository/formal-data facts.

**Source gap status:** CLOSED.

---

# 4. NIST experimental-design source

## Selected source

NIST/SEMATECH e-Handbook of Statistical Methods.

Use selectively for:

- prospective experimental planning;
- randomization of run sequence;
- replication terminology and rationale.

NIST describes experimental design as planning an experiment in advance so the resulting data can support valid and objective conclusions. Its DOE terminology identifies randomization as randomized run scheduling and replication as repeating an experimental condition.

## CaseMetrology qualification

The formal OAL study should **not** be labeled a factorial DOE merely because NIST experimental-design terminology is cited. NIST is being used for general design principles applicable to the prospective validation structure.

**Source gap status:** CLOSED.

---

# 5. K-State ETDR citation-style finding

## Current K-State position

Kansas State University's current ETDR guidance requires consistent formatting of the references/bibliography but does not establish one universal citation style for every graduate program.

The 2026–2027 Graduate Handbook states that individual graduate programs should establish policies for thesis/dissertation style and general format. If the program does not provide detailed requirements, the supervisory committee is responsible for specifying the style and general format.

## Consequence for CaseMetrology

Do **not** spend time converting the working source dossier into a final APA, IEEE, Chicago, or other reference style until the program/advisor/committee preference is confirmed.

For now:

- preserve complete bibliographic metadata;
- preserve DOI values;
- preserve exact manufacturer/standard document identity;
- use consistent temporary citation keys/placeholders in the working thesis;
- perform one final bibliography-format conversion once the required style is confirmed.

## ETDR template

K-State strongly encourages use of the current Graduate School master's thesis template and warns against relying on inherited older templates.

The Graduate School's formatting review emphasizes:

- required front matter;
- correct pagination;
- working Table of Contents / Lists of Figures and Tables;
- consistently formatted references;
- overall formatting consistency.

**ETDR style gap status:** CLOSED as a policy question; exact citation style remains a committee/program formatting choice.

---

# 6. K-State reproducibility requirement — important CaseMetrology implication

The 2026–2027 K-State Graduate Handbook states that, regardless of style and format, a thesis or dissertation must contain enough information for an independent investigator to repeat or verify the work leading to the results and conclusions.

The handbook further recognizes that a journal-style manuscript may be too terse and states that additional material may be needed to support independent reproducibility, including tables, derivations, and descriptions of unsuccessful or unproductive explorations.

## Implications for this thesis

This strongly supports the evidence discipline already being applied to CaseMetrology, but the final thesis cannot rely on the existence of the Git repository alone.

The manuscript itself should contain enough methodological information to reproduce the formal OAL study, including at minimum:

- study scope and research question;
- physical measurement configuration;
- camera and optical configuration;
- image-acquisition settings;
- segmentation sequence and parameters;
- frozen estimator definition;
- spatial calibration equations and angle convention;
- certified calibration reference;
- validation specimen population and exclusions;
- screening and sample-selection procedure;
- formal manual reference procedure;
- formal CV acquisition procedure;
- randomization and replication;
- failure and deviation rules;
- environmental and measurement-assurance controls;
- statistical definitions;
- acceptance criteria;
- methodological limitations.

The repository may provide deeper provenance and auditability, but core reproducibility information should remain in the thesis or formally submitted supplementary material.

## Unsuccessful/superseded methods

K-State's reproducibility language also supports retaining a concise account of material unsuccessful or superseded method-development paths when those paths are important for understanding why the final method was chosen.

For CaseMetrology, the thesis need not reproduce every exploratory terminal session, but it should preserve the scientifically relevant chronology:

- PCA development baseline;
- geometry alternative and temporary selection;
- subpixel alternatives;
- physical-unit prevalidation comparison;
- final PCA/extreme-mask selection;
- calibration-angle interpretation correction before formal validation.

This can be concise in Chapter 3 and expanded in an appendix or supplementary research record if needed.

---

# 7. Finalized Chapter 3 external source set

## Core scholarly sources

1. **Otsu, N. (1979)** — threshold selection.
2. **Jolliffe, I. T., & Cadima, J. (2016)** — PCA.
3. **Bland, J. M., & Altman, D. G. (1986)** — measurement-method agreement.
4. **Gonzalez, R. C., & Woods, R. E., 4th ed.** — image-processing fundamentals.
5. **Lohr, S. L. (2022), 3rd ed.** — stratified sampling.
6. **NIST/SEMATECH Engineering Statistics Handbook** — general randomization/replication/DOE principles.

## Metrology sources

7. **JCGM 100:2008** — GUM.
8. **JCGM 200:2012** — VIM.
9. **JCGM 106:2012** — conformity assessment / uncertainty / false acceptance.
10. **ASME B89.1.9-2002** — actual gauge-block certificate basis.

## Manufacturer sources

11. **NVIDIA Jetson Orin Nano Developer Kit User Guide** — platform identity/vendor specifications.
12. **Arducam B0499 IMX296 datasheet** — camera/sensor capability.
13. **Mitutoyo 500-196-30 documentation** — manual caliper model/range/resolution.

## Certificate sources

14. **Gauge-block certificate T26A06624** — certified 1.0000024-in central length and stated uncertainty.
15. **Manual reference caliper certificate** — PENDING.
16. **Formal environmental instrument/probe calibration evidence** — PENDING.

---

# 8. Chapter 3 support state after source-gap closure

## External-source gaps

- Otsu thresholding — CLOSED.
- PCA — CLOSED.
- Bland–Altman — CLOSED.
- Gaussian/spatial filtering — CLOSED.
- Morphology — CLOSED.
- Stratified sampling — CLOSED.
- Experimental randomization/replication — CLOSED.
- uncertainty/VIM/conformity sources — CLOSED.
- Jetson manufacturer source — CLOSED.
- camera manufacturer source — CLOSED.
- caliper model source — CLOSED.
- gauge-block standard basis — CLOSED.

## Dependencies that cannot be closed yet

- manual reference caliper certificate;
- formal environmental calibration documentation;
- completed screening distribution;
- final strata;
- final 60-specimen sample;
- formal manual data;
- formal CV data;
- formal statistical results;
- final validation conclusion.

These are genuine future-evidence dependencies, not literature deficiencies.

---

# 9. Recommended next thesis action

With Chapter 3 sentence-level evidence coverage complete and the planned external-source set closed, the next productive writing step is to assemble one **integrated audited Chapter 3 working draft** from Sections 3.1 through 3.17.

That integrated draft should:

1. remove evidence-audit tags;
2. retain citation placeholders;
3. retain explicit pending statements where evidence does not yet exist;
4. use the corrected calibration equation and angle convention;
5. maintain the 16 mm optical configuration;
6. preserve the development chronology;
7. prevent any Chapter 4 formal-results language from appearing prematurely.

After integration, Chapter 3 can undergo a final consistency/flow review rather than another methodological redesign.
