# CaseMetrology Formal OAL Reference-Standard and Manual-Session Acceptance Protocol

**Project:** CaseMetrology
**Measurement characteristic:** Cartridge-case overall length (OAL)
**Study phase:** Formal validation
**Designated operator:** Timmy D. Bell
**Status:** Prospective protocol; formal validation measurements have not begun

## 1. Purpose

This protocol defines the measurement-assurance procedure used to determine whether a formal manual-reference session is suitable for specimen measurement and subsequent use in the CaseMetrology validation study.

## 2. Reference Instrument

The formal manual-reference instrument is:

- Mitutoyo CD-8"ASX
- Code 500-197-30
- Serial B23090910
- Resolution 0.0005 in / 0.01 mm

Formal validation shall not begin until the accredited calibration certificate has been reviewed and accepted.

## 3. Designated Check Standard

The CaseMetrology dimensional check standard currently has a certified dimension of:

\[
L_{cert}=1.0000024\ \text{in}
\]

The complete artifact identity shall be documented from its calibration certificate before formal validation begins.

Pending certificate fields include:

- manufacturer;
- artifact type/grade;
- serial or unique ID;
- certificate number;
- calibration date/status;
- calibration laboratory/accreditation;
- measurement uncertainty;
- coverage factor;
- reference temperature;
- limitations or corrections.

The full certified value shall be retained in the research record.

## 4. Role of the Check Standard

The check standard is used to monitor the behavior of the manual measurement process immediately before and after formal specimen measurements.

A passing check-standard result shall not be interpreted as a new calibration of the caliper.

## 5. Definition of a Formal Manual Session

A formal manual session is a continuous group of formal specimen measurements performed:

- by Timmy D. Bell;
- using Mitutoyo B23090910;
- under the applicable environmental protocol;
- under one `session_id`; and
- between required pre-session and post-session check-standard measurements.

Each new formal manual round shall begin with a new pre-session check.

## 6. Events Requiring a New Session

A new session and new pre-session check shall be required when:

- beginning a new formal measurement round;
- continuing on a different calendar day;
- the caliper is removed from the controlled area;
- the caliper sustains an impact;
- battery replacement or instrument malfunction occurs;
- significant corrective cleaning is required;
- environmental conditions leave established limits;
- measurement-system condition becomes questionable.

## 7. Pre-Session Check Procedure

Before formal specimen measurement begins:

1. verify caliper identity and calibration status;
2. inspect measuring surfaces;
3. verify operation in inches;
4. verify environmental requirements;
5. verify check-standard identity;
6. obtain five independent measurements with complete removal/repositioning.

No reading shall be discarded because another reading appears more desirable.

## 8. Pre-Session Calculations

For readings \(P_1,\ldots,P_5\):

\[
\bar{P}=\frac{P_1+P_2+P_3+P_4+P_5}{5}
\]

\[
R_P=\max(P_1,\ldots,P_5)-\min(P_1,\ldots,P_5)
\]

\[
E_P=\bar{P}-L_{ref}
\]

The raw five readings shall remain permanently preserved.

## 9. Pre-Session Go/No-Go Decision

A formal session may begin only when all required conditions pass:

\[
|E_P|\le E_{limit}
\]

and

\[
R_P\le R_{limit}
\]

together with acceptable caliper condition, calibration status, check-standard condition, environmental status, and no unresolved abnormality.

**PENDING CERTIFICATE REVIEW:** final values for `E_limit` and `R_limit`.

## 10. Failed Pre-Session Check

If the pre-session check fails:

**FORMAL SPECIMEN MEASUREMENT SHALL NOT BEGIN.**

The failed check shall remain in the research record.

A subsequent check may occur only after a documented reason/corrective action. Both attempts shall be retained.

## 11. Post-Session Check

Immediately following the session, obtain five additional independent check-standard measurements.

For readings \(Q_1,\ldots,Q_5\):

\[
\bar{Q}=\frac{Q_1+Q_2+Q_3+Q_4+Q_5}{5}
\]

\[
R_Q=\max(Q_1,\ldots,Q_5)-\min(Q_1,\ldots,Q_5)
\]

\[
E_Q=\bar{Q}-L_{ref}
\]

## 12. Pre-to-Post Drift

\[
D=\bar{Q}-\bar{P}
\]

with criterion:

\[
|D|\le D_{limit}
\]

**PENDING CERTIFICATE REVIEW:** final value for `D_limit`.

## 13. Complete Session Acceptance

A completed session shall be `PASS` when:

\[
|E_P|\le E_{limit}
\]

\[
R_P\le R_{limit}
\]

\[
|E_Q|\le E_{limit}
\]

\[
R_Q\le R_{limit}
\]

and

\[
|D|\le D_{limit}
\]

with all other protocol requirements satisfied.

Use `HOLD_FOR_REVIEW` when a post-session check fails, environmental excursion occurs, required information is missing, or another condition prevents automatic acceptance.

## 14. Failed Post-Session Check

A failed post-session check shall not automatically erase or invalidate specimen measurements.

Instead:

1. retain all specimen measurements;
2. retain all check readings;
3. mark the session `HOLD_FOR_REVIEW`;
4. suspend further formal manual measurement;
5. investigate;
6. document findings;
7. assign final disposition.

## 15. Missing Post-Session Check

If the required post-session check cannot be obtained, classify the session `HOLD_FOR_REVIEW`.

## 16. Check-Standard Repetition Rules

Exactly five pre-session and five post-session readings are required per normal formal manual session.

Additional readings shall not be taken to improve a mean, reduce a range, or convert a failed check to passing.

## 17. No Retrospective Adjustment of Limits

After formal measurements begin, acceptance limits shall not be widened based on validation results.

Any unavoidable change shall be a documented protocol amendment/deviation.

## 18. Treatment of Certified Reference Value

The currently documented certified dimension is:

\[
1.0000024\ \text{in}
\]

The final value used as \(L_{ref}\) shall be determined after certificate and environmental-protocol review.

No thermal or dimensional correction shall be introduced after validation results are examined.

## 19. Required Session Record

Each session record shall preserve at minimum:

- `session_id`;
- manual round;
- operator;
- caliper identity;
- calibration certificate ID;
- check-standard identity and certificate ID;
- certified dimension;
- start/end times;
- five pre readings;
- pre statistics and status;
- five post readings;
- post statistics and status;
- pre-to-post drift;
- environmental record ID;
- final session status;
- review-required flag;
- deviation ID, if applicable;
- notes.

## 20. Data Precision

Individual caliper observations shall be recorded exactly as displayed. Calculated means/errors/drift may retain additional computational precision.

## 21. Certificate-Review Gate

Before formal validation:

1. review caliper certificate;
2. review check-standard certificate;
3. establish `E_limit`;
4. establish `R_limit`;
5. establish `D_limit`;
6. document technical basis;
7. verify environmental consistency;
8. commit finalized protocol.

## 22. Protocol Lock

No formal OAL validation specimen measurements shall begin until the certificate-review gate is complete and numerical limits are frozen.
