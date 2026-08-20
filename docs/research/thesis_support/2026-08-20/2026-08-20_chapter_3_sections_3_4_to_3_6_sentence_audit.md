# Chapter 3 Sentence-Level Evidence Audit — Sections 3.4–3.6

**Project:** CaseMetrology
**Researcher:** Timmy D. Bell
**Date:** 2026-08-20
**Scope:** K-State M.S. Integrated Systems Design & Dynamics thesis — cartridge-case OAL only
**Status:** Working audited draft; formal validation has not begun.

## Tag legend

- `[REPO]` — supported by CaseMetrology repository evidence.
- `[LITERATURE]` — general scientific concept requiring scholarly citation.
- `[STANDARD]` — supported by a recognized metrology/engineering standard or guide.
- `[CERTIFICATE]` — supported by the actual calibration certificate.
- `[PENDING]` — cannot be finalized until future evidence exists.
- `[CORRECTION]` — reconciles an earlier draft statement with the frozen repository evidence.

---

# A. Annotated evidence-audit version

## 3.4 Image Acquisition and Segmentation

`[REPO]` Images used for OAL measurement are acquired using the locked CaseMetrology camera configuration and processed as grayscale images by the frozen OAL segmentation pipeline.

`[REPO]` For each measurement image, the corresponding blank reference is subtracted using `cv2.subtract(blank, image)` so that regions darkened by the specimen are emphasized relative to the illuminated background.

`[REPO]` The resulting darkening image is smoothed using a 5 × 5 Gaussian filter before thresholding.

`[LITERATURE]` Gaussian smoothing is a standard image-processing operation used to attenuate local high-frequency variation prior to subsequent segmentation operations.
**Source still to finalize:** standard image-processing text, preferably Gonzalez and Woods or an equivalent authoritative source.

`[REPO] [LITERATURE]` The blurred image is converted to a binary mask using Otsu thresholding. The CaseMetrology implementation uses OpenCV's Otsu mode, while the general threshold-selection principle is attributed to Otsu's histogram-based method.
**Primary source:** Otsu (1979), DOI `10.1109/TSMC.1979.4310076`.

`[REPO]` The binary mask is then processed using 3 × 3 morphological opening followed by 3 × 3 morphological closing.

`[LITERATURE]` In the thesis explanation, opening and closing should be described only at a general level as morphological operations used to suppress small binary irregularities and stabilize object regions; the exact 3 × 3 implementation is a CaseMetrology design choice.
**Source still to finalize:** standard digital-image-processing text.

`[REPO]` Connected components are evaluated after morphology, and only the largest connected foreground component is retained as the candidate cartridge-case silhouette.

`[REPO]` The segmentation stage also produces quality information used by downstream measurement logic, including component size and failure status.

`[REPO]` No threshold value is tuned manually on a specimen-by-specimen basis during formal validation; the frozen Otsu-based procedure is used consistently.

`[REPO]` The segmentation implementation used for formal-validation preparation is contained in `src/image_processing/oal_segmentation.py` and is incorporated into the verified OAL production pipeline.

### Audit disposition for Section 3.4

**Supported now:** exact processing sequence, parameter sizes, component-selection rule, frozen status.
**External citations required:** Otsu; one standard source for Gaussian filtering/morphology/connected-component explanation.
**Formal-data dependency:** none for the method description.

---

## 3.5 Overall-Length Measurement Algorithm

`[REPO]` The primary OAL pixel-length estimator selected for formal validation is the PCA/extreme-mask method implemented in `src/measurement/topdown_oal.py`.

`[LITERATURE]` Principal component analysis (PCA) constructs orthogonal principal directions from the observed data, with successive components chosen to account for decreasing amounts of variance.
**Recommended source:** Jolliffe and Cadima (2016), DOI `10.1098/rsta.2015.0202`.

`[REPO]` Within CaseMetrology, PCA is not used as a general dimensionality-reduction stage; it is used geometrically to establish an initial longitudinal direction for the segmented cartridge-case point set.

`[REPO]` The implementation subsequently refines the axis using exposed specimen points so that the final measurement direction better represents the accepted cartridge-case silhouette.

`[REPO]` OAL in pixel space is defined from the minimum and maximum accepted-mask projections along the refined measurement axis.

`[REPO]` This endpoint definition is specific to the CaseMetrology estimator and should not be attributed to the general PCA literature.

`[REPO]` The estimator also records the specimen centroid, measurement-axis angle, endpoint coordinates, component-size information, and pass/fail state required by the integrated physical-unit pipeline.

`[REPO]` Several alternative endpoint methods were evaluated during prevalidation engineering, including a binary-geometry estimator and grayscale subpixel approaches.

`[REPO]` The development record must preserve the actual chronology: PCA/extreme-mask was initially retained as the development baseline; a geometry-based estimator was temporarily selected on August 7, 2026; subsequent five-specimen prevalidation comparison favored PCA/extreme-mask for dimensional agreement; and PCA/extreme-mask was selected and frozen as the primary formal-validation estimator on August 13, 2026.

`[REPO]` The five specimens used in that comparison—121, 146, 178, 187, and 197—are development/prevalidation specimens and are excluded from the formal 60-specimen validation sample.

`[REPO]` Selection of PCA/extreme-mask as the formal-validation estimator does not itself constitute validation of the estimator's accuracy; formal validation remains a separate prospective study.

`[REPO]` Once formal validation begins, the estimator's segmentation behavior, endpoint definition, axis logic, quality gates, and pixel-length calculation are prohibited from being retuned against the validation results.

### Audit disposition for Section 3.5

**Supported now:** implementation, estimator selection, chronology, prevalidation exclusions, frozen state.
**External citation required:** PCA concept only.
**Important guardrail:** do not rewrite history to imply PCA was always the final choice.

---

## 3.6 Spatial Calibration Method

`[CERTIFICATE]` Pixel measurements are converted to physical units using a Mitutoyo Grade 0 steel gauge block, identification number 253568, as the certified dimensional reference.

`[CERTIFICATE]` Certificate T26A06624 reports a nominal length of 1.0000000 in and a certified central length of 1.0000024 in.

`[CERTIFICATE]` The certificate reports expanded uncertainty for central deviation of 2.4 microinches for lengths up to 4 in and identifies the inspection basis as ASME B89.1.9-2002.

`[STANDARD]` When the thesis describes the actual gauge-block certificate, the stated 2002 standard must be retained because it is the basis named on the certificate. A newer standard revision must not be substituted retrospectively.

`[REPO]` Formal calibration characterization was performed at the installed OAL measurement plane using the permanent clear Lexan measurement/locator surface.

`[REPO]` A coordinate-controlled 2 × 2 calibration grid, designated positions A through D, was measured using two principal gauge-block orientations.

`[REPO]` Independent holdout position E was withheld from fitting and used to evaluate calibration-model behavior at principal and oblique orientations.

`[REPO]` The accepted calibration results demonstrated that effective image scale varied with both image position and measurement direction; therefore a single global pixels-per-inch value was not retained as the final calibration model.

`[REPO]` Separate first-order spatial calibration planes were fitted to the accepted A–D calibration observations:

\[
PPI_0(x,y)
=
516.907045
+
0.00843326411x
+
0.000817091863y
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

`[CORRECTION]` The coefficient `0.00442714650` is the supported Y coefficient for `PPI_90`; any earlier thesis draft containing `0.000436889756` is incorrect and must be replaced.

`[REPO]` The historical labels `PPI_0` and `PPI_90` are retained because they identify the corresponding gauge-block acquisition orientations.

`[REPO]` A prevalidation audit on August 13, 2026 identified that the gauge-block analyzer reported the long-axis orientation while the certified short dimension was measured perpendicular to that reported direction.

`[REPO]` Because the cartridge-case PCA estimator reports the OAL measurement direction itself, the original direct label-to-angle interpretation was corrected before formal validation.

`[REPO]` For a cartridge-case centroid \((x_c,y_c)\) and PCA OAL direction \(\theta\), the frozen physical-unit implementation resolves effective scale as

\[
PPI_{\mathrm{effective}}
=
\sqrt{
\left[PPI_{90}(x_c,y_c)\cos\theta\right]^2
+
\left[PPI_0(x_c,y_c)\sin\theta\right]^2
}.
\]

`[REPO]` Under this convention, a horizontal cartridge-case OAL direction resolves to the historical `PPI_90` calibration plane and a vertical OAL direction resolves to the historical `PPI_0` plane.

`[REPO]` Physical OAL is then calculated as

\[
L_{\mathrm{OAL}}
=
\frac{L_{\mathrm{px}}}{PPI_{\mathrm{effective}}},
\]

where \(L_{\mathrm{px}}\) is the frozen PCA/extreme-mask pixel-length result.

`[REPO]` The August 13 correction changed only the mapping between measurement direction and the existing principal-direction calibration surfaces; it did not refit the A–D calibration data or alter segmentation, PCA endpoint logic, or the frozen pixel-length estimator.

`[REPO]` Reinterpretation of the preserved oblique holdout under the corrected dimensional-direction convention produced an equivalent dimensional residual of approximately -0.000412622 in over the approximately 1-in reference.

`[REPO]` The calibration evidence should therefore be described as supporting the frozen spatial/directional conversion within the tested measurement region and configuration, not as demonstrating universal sub-0.001-in calibration accuracy at arbitrary position or orientation.

`[STANDARD]` Measurement-uncertainty and traceability terminology should follow the JCGM Guide to the Expression of Uncertainty in Measurement and the International Vocabulary of Metrology rather than treating the certified reference value as error-free truth.
**Sources:** JCGM 100:2008 and JCGM 200:2012.

### Audit disposition for Section 3.6

**Supported now:** gauge-block identity/value, calibration design, plane coefficients, holdouts, corrected directional mapping, physical conversion equation, correction chronology.
**External/standard support:** certificate basis; GUM/VIM for uncertainty and traceability terminology.
**Critical correction:** `PPI_90` Y coefficient must be `0.00442714650`.
**Formal-data dependency:** none for the optical calibration method itself; the manual-reference calibration certificate remains separate and pending.

---

# B. Clean thesis-ready version

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

# C. Reference-placement record

## Otsu
Otsu, N. (1979). A Threshold Selection Method from Gray-Level Histograms. *IEEE Transactions on Systems, Man, and Cybernetics*, 9(1), 62–66. DOI: 10.1109/TSMC.1979.4310076.

**Placement:** first substantive explanation of Otsu thresholding in Section 3.4.

## PCA
Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: a review and recent developments. *Philosophical Transactions of the Royal Society A*, 374(2065), 20150202. DOI: 10.1098/rsta.2015.0202.

**Placement:** first substantive explanation of PCA in Section 3.5.

## GUM
Joint Committee for Guides in Metrology. (2008). *Evaluation of measurement data — Guide to the expression of uncertainty in measurement*. JCGM 100:2008(E). DOI: 10.59161/JCGM100-2008E.

**Placement:** Section 3.6 uncertainty framing and later reference-measurement sections.

## VIM
Joint Committee for Guides in Metrology. (2012). *International Vocabulary of Metrology — Basic and general concepts and associated terms (VIM), 3rd edition*. JCGM 200:2012.

**Placement:** Section 3.6 traceability/measurement terminology; Sections 3.10, 3.13, and 3.17 for repeatability, reproducibility, and uncertainty.

## Certificate/standard
CaseMetrology gauge-block certificate T26A06624; inspection basis stated as ASME B89.1.9-2002.

**Placement:** Section 3.6 certified reference description.

---

# D. Open items after this audit

1. Select and verify one authoritative image-processing source for Gaussian smoothing, binary morphology, and connected-component terminology.
2. Confirm the thesis citation style required by the K-State program/ETDR template before final reference formatting.
3. Ensure every existing Chapter 3 draft instance of the `PPI_90` equation uses Y coefficient `0.00442714650`.
4. Ensure every existing Chapter 3 draft uses the 16 mm CS2316ZM02 optical configuration.
5. Keep manual-reference calibration-certificate claims outside Section 3.6 unless clearly distinguished from the already certified gauge-block evidence.
6. Do not populate Chapter 4 with prevalidation numerical results.
