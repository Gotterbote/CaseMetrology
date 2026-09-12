#!/usr/bin/env python3

from pathlib import Path
from collections import Counter
from datetime import datetime
import csv
import hashlib
import json
import subprocess

REPO = Path(__file__).resolve().parents[1]

DEVELOPMENT_BASELINE = "cdd76a7"
MANUAL_SEED = "2026091201"
CV_SEED = "2026091202"

SOURCE = REPO / "data/oal_validation/formal_validation_specimens.csv"

OUTDIR = REPO / "data/oal_validation/v3_formal"
DOCDIR = REPO / "docs/research/v3_formal_validation"

EXPECTED_IDS = {
    75,85,123,131,150,152,215,222,
    9,14,40,55,58,61,143,151,163,194,200,221,228,233,
    12,64,72,95,100,120,127,139,161,165,172,189,192,204,230,235,
    15,30,48,69,70,86,104,118,124,135,144,188,193,225,
    35,51,53,106,136,218,219,226
}

EXPECTED_STRATA = {
    "below_lsl": 8,
    "near_lsl_in_spec": 14,
    "central_nominal": 16,
    "near_usl_in_spec": 14,
    "above_usl": 8,
}

DEV_SPECIMENS = {121,146,178,187,197}


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")


def git(*args):
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True
    ).strip()


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def deterministic_order(ids, seed, label):
    return sorted(
        ids,
        key=lambda sid: hashlib.sha256(
            f"{seed}|{label}|{sid}".encode()
        ).hexdigest()
    )


def find_col(fieldnames, candidates):
    lookup = {x.strip().lower(): x for x in fieldnames}
    for candidate in candidates:
        if candidate.lower() in lookup:
            return lookup[candidate.lower()]
    return None


OUTDIR.mkdir(parents=True, exist_ok=True)
DOCDIR.mkdir(parents=True, exist_ok=True)

head = git("rev-parse", "--short=7", "HEAD")

if head != DEVELOPMENT_BASELINE:
    raise SystemExit(
        f"FAIL: expected HEAD {DEVELOPMENT_BASELINE}; found {head}"
    )

status_lines = [
    line for line in git("status", "--porcelain").splitlines()
    if line.strip()
]

# The preparation script itself is expected to be untracked at this point
# because the clean-repository check occurred immediately before it was created.
allowed_status = {
    "?? scripts/prepare_v3_formal_freeze.py",
}

unexpected_status = [
    line for line in status_lines
    if line not in allowed_status
]

if unexpected_status:
    raise SystemExit(
        "FAIL: unexpected repository changes before preparation:\n"
        + "\n".join(unexpected_status)
    )

if not SOURCE.exists():
    raise SystemExit(f"FAIL: missing frozen cohort file: {SOURCE}")

with SOURCE.open(newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    if not reader.fieldnames:
        raise SystemExit("FAIL: frozen cohort file has no header.")

    rows = list(reader)

    id_col = find_col(
        reader.fieldnames,
        ["specimen_id", "part_id", "case_id", "id", "specimen"]
    )

    stratum_col = find_col(
        reader.fieldnames,
        ["stratum", "allocation_stratum", "selection_stratum"]
    )

if id_col is None:
    raise SystemExit(
        f"FAIL: could not identify specimen ID column: {reader.fieldnames}"
    )

ids = []

for row in rows:
    ids.append(int(float(str(row[id_col]).strip())))

if len(ids) != 60:
    raise SystemExit(f"FAIL: expected 60 specimens; found {len(ids)}")

if len(set(ids)) != 60:
    duplicates = sorted(
        sid for sid, n in Counter(ids).items() if n > 1
    )
    raise SystemExit(f"FAIL: duplicate IDs: {duplicates}")

if set(ids) != EXPECTED_IDS:
    raise SystemExit(
        "FAIL: cohort mismatch\n"
        f"Missing: {sorted(EXPECTED_IDS - set(ids))}\n"
        f"Extra:   {sorted(set(ids) - EXPECTED_IDS)}"
    )

if set(ids) & DEV_SPECIMENS:
    raise SystemExit(
        "FAIL: development/prevalidation specimens found in formal cohort."
    )

stratum_text = "NOT AVAILABLE"

if stratum_col:
    normalized = Counter(
        str(row[stratum_col]).strip().lower()
        for row in rows
    )

    if dict(normalized) != EXPECTED_STRATA:
        raise SystemExit(
            "FAIL: stratum allocation mismatch\n"
            f"Expected: {EXPECTED_STRATA}\n"
            f"Actual:   {dict(normalized)}"
        )

    stratum_text = str(dict(normalized))

# ------------------------------------------------------------------
# Manual stability-check order
# ------------------------------------------------------------------

manual_order = deterministic_order(
    sorted(EXPECTED_IDS),
    MANUAL_SEED,
    "V3_MANUAL_STABILITY"
)

manual_path = OUTDIR / "v3_manual_stability_run_order.csv"

with manual_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)

    w.writerow([
        "sequence",
        "specimen_id",
        "seed",
        "planned_session"
    ])

    for seq, sid in enumerate(manual_order, 1):
        w.writerow([
            seq,
            sid,
            MANUAL_SEED,
            "V3-MAN-STAB-S001"
        ])

manual_template = OUTDIR / "v3_manual_stability_observations.csv"

with manual_template.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)

    w.writerow([
        "session_id",
        "sequence",
        "specimen_id",
        "measurement_in",
        "timestamp",
        "validity",
        "review_trigger",
        "notes"
    ])

    for seq, sid in enumerate(manual_order, 1):
        w.writerow([
            "V3-MAN-STAB-S001",
            seq,
            sid,
            "",
            "",
            "",
            "",
            ""
        ])

# ------------------------------------------------------------------
# Three independently randomized formal CV rounds
# ------------------------------------------------------------------

cv_path = OUTDIR / "v3_cv_run_orders.csv"
cv_orders = {}

with cv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)

    w.writerow([
        "round",
        "sequence",
        "specimen_id",
        "seed",
        "planned_session"
    ])

    for rnd in range(1, 4):

        order = deterministic_order(
            sorted(EXPECTED_IDS),
            CV_SEED,
            f"V3_CV_ROUND_{rnd}"
        )

        cv_orders[rnd] = order

        for seq, sid in enumerate(order, 1):
            w.writerow([
                rnd,
                seq,
                sid,
                CV_SEED,
                f"V3-CV-S{rnd:03d}"
            ])

cv_template = OUTDIR / "v3_cv_observations.csv"

with cv_template.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)

    w.writerow([
        "session_id",
        "round",
        "sequence",
        "specimen_id",
        "timestamp",
        "image_path",
        "validity",
        "invalid_reason",
        "endface_hybrid_in",
        "pca_in",
        "geometry_in",
        "notes"
    ])

    for rnd in range(1, 4):

        for seq, sid in enumerate(cv_orders[rnd], 1):
            w.writerow([
                f"V3-CV-S{rnd:03d}",
                rnd,
                seq,
                sid,
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            ])

# ------------------------------------------------------------------
# Prospective formal-validation plan
# ------------------------------------------------------------------

plan_path = DOCDIR / "V3_FORMAL_VALIDATION_PLAN.md"

plan = f"""# CaseMetrology V3 Formal OAL Validation Plan

Generated: {now()}

Development baseline: `{DEVELOPMENT_BASELINE}`

Status: **PROSPECTIVE — PRE-ACQUISITION**

---

## 1. Study Purpose

The V3 formal validation will determine whether the frozen CaseMetrology
configuration provides improved overall-length agreement and
repositioning repeatability when specimen rocking and roll orientation
are mechanically controlled.

V3 is a prospective confirmation study.

Formal V3 observations shall not be used to modify the system.

---

## 2. Formal Measurement Configuration

The planned V3 configuration is:

- Arducam IMX296 global-shutter camera
- 16 mm lens
- existing accepted OAL calibration
- rocking-controlled fixture
- Fixture 2 positively registered
- controlled specimen roll orientation
- specimen engraving used as roll-registration reference
- existing backlight configuration
- existing locked camera controls
- unchanged working geometry

No hardware modification is planned.

---

## 3. Estimator Hierarchy

Primary estimator:

**Endface Hybrid**

Historical comparator:

**PCA**

Secondary/exploratory estimator:

**Geometry**

The exact source files and SHA-256 hashes for these estimators shall be
recorded in the final V3 freeze evidence before formal data acquisition.

No estimator modification is permitted after final freeze.

---

## 4. Development Independence

Development/prevalidation specimens:

121, 146, 178, 187, 197

These specimens remain outside the frozen V3 formal cohort.

The controlled-presentation procedure and V3 estimator work were
developed using prevalidation/development data.

No measurement from the prospective V3 formal acquisition may be used
to tune the V3 system.

---

## 5. Formal Specimen Cohort

The V3 formal cohort is the same retained 60-specimen cohort used in
the completed V1 formal validation.

Allocation:

| Stratum | n |
|---|---:|
| below LSL | 8 |
| near LSL in specification | 14 |
| central nominal | 16 |
| near USL in specification | 14 |
| above USL | 8 |
| Total | 60 |

No specimen shall be replaced because of poor V3 performance.

---

## 6. Manual Reference Strategy

The accepted three-round V1 manual-reference mean remains the primary
reference value for each retained specimen.

Before formal V3 CV acquisition, all 60 specimens shall receive one
new randomized manual stability-check measurement.

The stability check verifies that the retained physical specimens have
not materially changed.

It does not replace the frozen reference means.

Manual stability randomization seed:

`{MANUAL_SEED}`

A difference greater than 0.0015 in from the frozen manual-reference
mean triggers review.

A triggered specimen receives two additional stability-check readings.

A review trigger shall not result in silent exclusion or specimen
replacement.

---

## 7. V3 Formal CV Design

Each of the 60 specimens shall undergo three independent formal
placements.

Total formal CV observations:

**180**

Each observation requires removal and independent replacement of the
specimen.

Repeated images of an untouched specimen do not constitute independent
placements.

CV randomization seed:

`{CV_SEED}`

Formal sessions:

- V3-CV-S001
- V3-CV-S002
- V3-CV-S003

---

## 8. Controlled Presentation

For every formal placement:

1. specimen is removed from the measurement position;
2. specimen is independently replaced;
3. specimen is seated against the established fixture datum;
4. base-to-mouth rocking is mechanically controlled;
5. roll orientation is registered using the frozen presentation rule;
6. proper seating is confirmed;
7. image is acquired.

The presentation procedure shall not be changed because of observed
measurement results.

---

## 9. Primary Statistical Unit

The primary independent experimental unit is the specimen.

Primary agreement sample size:

**n = 60**

For each specimen, the three V3 Endface Hybrid measurements shall be
averaged and compared with the frozen manual-reference mean.

The 180 CV observations shall not be treated as 180 independent
specimens.

---

## 10. Prospective Performance Targets

| Endpoint | Frozen target |
|---|---:|
| Endface Hybrid availability | >= 99% |
| Absolute mean bias | <= 0.0010 in |
| RMSE | <= 0.0020 in |
| P95 absolute error | <= 0.0030 in |
| Maximum absolute error | <= 0.0040 in |
| P95 pairwise repositioning difference | <= 0.0020 in |

Failure of a target is a study result.

It does not authorize system modification.

---

## 11. Agreement Analysis

The formal specimen-level analysis shall report:

- mean signed bias
- 95% confidence interval for bias
- median signed error
- MAE
- RMSE
- P95 absolute error
- maximum absolute error

The P95 calculation shall remain consistent with the V1 analysis
implementation.

---

## 12. Repositioning Analysis

For each specimen, three independent measurements produce three
pairwise absolute differences.

The analysis shall report:

- specimen three-placement range
- pairwise absolute differences
- P95 pairwise absolute difference
- maximum pairwise absolute difference
- worst-performing specimens

---

## 13. Classification Analysis

Frozen specification limits:

LSL = 0.9900 in

USL = 1.0100 in

Each specimen shall be classified as:

- true pass
- true fail
- false pass
- false fail

All misclassified specimens shall be individually reported.

No post-hoc guard band shall be introduced.

---

## 14. V1-to-V3 Comparison

Because V1 and V3 use the same retained specimens and frozen manual
reference, paired comparison is permitted.

Three conditions shall be distinguished:

1. V1 PCA with V1 specimen presentation
2. V3 PCA with controlled presentation
3. V3 Endface Hybrid with controlled presentation

This permits mechanical-presentation effects and estimator effects to
be discussed separately.

---

## 15. Stop Conditions

Formal acquisition shall stop or enter HOLD status for:

- failed required reference checks
- failed calibration verification
- loss of Fixture 2 registration
- fixture movement or modification
- camera movement
- lens movement
- focus change
- working-geometry change
- unintended camera-control change
- physical specimen damage
- systematic acquisition/software failure
- inability to establish the frozen presentation procedure
- loss of specimen/data traceability

These are NOT stop conditions:

- large measurement error
- poor repeatability
- unexpected bias
- false pass
- false fail
- estimator disagreement
- unusual specimen geometry

Those are formal results.

---

## 16. Raw-Data Preservation

All formal images shall be retained.

Blank/reference images shall be retained.

Protocol-invalid attempts shall remain preserved.

A technically valid measurement shall not be repeated merely because
its value is unfavorable.

---

## 17. Configuration-Change Rule

A material change after final freeze to:

- hardware
- calibration
- fixture
- presentation rule
- segmentation
- estimator logic
- camera configuration

ends acquisition under the frozen V3 configuration until the change is
formally dispositioned.

A materially changed system requires a new prospective validation
decision.

---

## 18. Interpretation Boundary

Successful V3 results may support approximately thousandth-inch-class
repositioning performance under the tested controlled-presentation
conditions.

Repeatability shall not be described as equivalent to absolute
accuracy.

Results apply only to the tested system and OAL task.

No claim of automated production-line performance or uncontrolled
specimen orientation is implied.

---

## 19. Final Freeze Requirement

Formal acquisition may begin only after:

- V3 plan exists;
- frozen 60-specimen cohort passes audit;
- manual stability order is frozen;
- all three CV run orders are frozen;
- estimator source files are identified;
- calibration/configuration files are identified;
- all frozen files receive SHA-256 hashes;
- configuration commit is recorded;
- freeze evidence is committed;
- repository is clean.
"""

plan_path.write_text(plan, encoding="utf-8")

# ------------------------------------------------------------------
# Checklist
# ------------------------------------------------------------------

checklist_path = DOCDIR / "V3_PREACQUISITION_CHECKLIST.md"

checklist_path.write_text(f"""# V3 Pre-Acquisition Checklist

Development baseline: `{DEVELOPMENT_BASELINE}`

## Formal Study Definition

- [ ] 60-specimen cohort audit PASS
- [ ] Development specimens excluded
- [ ] Endface Hybrid primary estimator confirmed
- [ ] PCA historical comparator confirmed
- [ ] Geometry secondary estimator confirmed
- [ ] Estimator source files identified
- [ ] Calibration files identified
- [ ] Camera configuration identified
- [ ] SHA-256 manifest generated
- [ ] Configuration commit recorded
- [ ] Repository clean

## Hardware

- [ ] Arducam IMX296 installed
- [ ] 16 mm lens installed
- [ ] camera position unchanged
- [ ] focus unchanged
- [ ] Fixture 2 positively registered
- [ ] rocking-control configuration unchanged
- [ ] fixed-roll presentation rule unchanged
- [ ] backlight configuration unchanged
- [ ] camera controls unchanged

## Manual Stability Check

Seed: `{MANUAL_SEED}`

- [ ] reference-system check accepted
- [ ] 60 specimens measured in frozen order
- [ ] previous reference values not used to guide readings
- [ ] >0.0015-in differences reviewed
- [ ] required follow-up readings documented
- [ ] specimen stability disposition complete

## Formal CV

Seed: `{CV_SEED}`

- [ ] V3-CV-S001 order frozen
- [ ] V3-CV-S002 order frozen
- [ ] V3-CV-S003 order frozen
- [ ] each observation is an independent placement
- [ ] raw images preserved
- [ ] invalid attempts preserved
- [ ] no valid measurement repeated because of result

Formal V3 acquisition shall not begin until the final freeze evidence
has been committed.
""", encoding="utf-8")

# ------------------------------------------------------------------
# Development baseline record
# ------------------------------------------------------------------

baseline_path = DOCDIR / "V3_DEVELOPMENT_BASELINE.txt"

baseline_path.write_text(
    f"""CaseMetrology V3 Development Baseline

Recorded: {now()}

Development-complete commit:
{git("rev-parse", "HEAD")}

Short commit:
{DEVELOPMENT_BASELINE}

Commit subject:
{git("show", "-s", "--format=%s", "HEAD")}

This commit represents the end of exploratory V3 controlled-presentation
development immediately before prospective formal-validation
preparation.

No V3 formal measurements had been collected when this record was
created.
""",
    encoding="utf-8"
)

# ------------------------------------------------------------------
# Metadata
# ------------------------------------------------------------------

metadata_path = DOCDIR / "V3_PREPARATION_METADATA.json"

metadata = {
    "generated_at": now(),
    "development_baseline": git("rev-parse", "HEAD"),
    "development_baseline_short": DEVELOPMENT_BASELINE,
    "source_cohort": str(SOURCE.relative_to(REPO)),
    "source_cohort_sha256": sha256(SOURCE),
    "formal_specimen_count": 60,
    "development_specimens": sorted(DEV_SPECIMENS),
    "manual_seed": MANUAL_SEED,
    "cv_seed": CV_SEED,
    "manual_stability_measurements_planned": 60,
    "formal_cv_measurements_planned": 180,
    "primary_estimator": "Endface Hybrid",
    "historical_comparator": "PCA",
    "secondary_estimator": "Geometry",
    "final_freeze_complete": False
}

metadata_path.write_text(
    json.dumps(metadata, indent=2) + "\n",
    encoding="utf-8"
)

# ------------------------------------------------------------------
# Search for likely estimator / calibration / configuration files.
# These are candidates only. Nothing is frozen by this search.
# ------------------------------------------------------------------

candidate_terms = [
    "endface",
    "hybrid",
    "geometry",
    "pca",
    "calib",
    "ppi",
    "camera",
    "control"
]

candidate_files = []

for root in [REPO / "scripts", REPO / "config", REPO / "configs"]:
    if not root.exists():
        continue

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        low = path.name.lower()

        if any(term in low for term in candidate_terms):
            candidate_files.append(path)

candidate_files = sorted(set(candidate_files))

candidate_path = DOCDIR / "V3_FREEZE_FILE_CANDIDATES.txt"

with candidate_path.open("w", encoding="utf-8") as f:

    f.write("V3 FREEZE FILE CANDIDATES\n")
    f.write("=" * 80 + "\n\n")

    f.write(
        "These are search candidates only. The final freeze must explicitly\n"
        "identify the authoritative estimator, calibration, and configuration\n"
        "files before formal acquisition.\n\n"
    )

    for path in candidate_files:
        f.write(str(path.relative_to(REPO)) + "\n")

# ------------------------------------------------------------------
# Audit
# ------------------------------------------------------------------

audit_path = DOCDIR / "V3_PREACQUISITION_AUDIT.txt"

audit = [
    "=" * 80,
    "CASEMETROLOGY V3 PRE-ACQUISITION AUDIT",
    "=" * 80,
    "",
    f"Generated: {now()}",
    f"Development baseline: {DEVELOPMENT_BASELINE}",
    "",
    "PASS: repository was clean before preparation",
    "PASS: development baseline verified",
    f"PASS: formal cohort count = {len(ids)}",
    f"PASS: unique formal specimens = {len(set(ids))}",
    "PASS: formal IDs exactly match established frozen 60",
    "PASS: development specimens absent from formal cohort",
    f"Stratum audit: {stratum_text}",
    "",
    f"PASS: manual stability run order = {len(manual_order)} specimens",
    f"PASS: manual stability seed = {MANUAL_SEED}",
    "",
]

for rnd in range(1, 4):
    audit.extend([
        f"PASS: V3 CV round {rnd} = {len(cv_orders[rnd])} specimens",
        f"PASS: V3 CV round {rnd} unique = {len(set(cv_orders[rnd]))}",
        f"PASS: V3 CV round {rnd} cohort complete = "
        f"{set(cv_orders[rnd]) == EXPECTED_IDS}",
    ])

audit.extend([
    "",
    "PASS: total planned formal V3 CV placements = 180",
    "",
    "PENDING: exact Endface Hybrid source file identification",
    "PENDING: exact PCA comparator source file identification",
    "PENDING: exact Geometry source file identification",
    "PENDING: exact calibration/configuration file identification",
    "PENDING: SHA-256 final freeze manifest",
    "",
    "NO FORMAL V3 MEASUREMENT DATA WERE GENERATED.",
    "",
    "PREPARATION AUDIT: PASS",
    "FINAL FREEZE: NOT YET COMPLETE",
    "=" * 80,
])

audit_path.write_text(
    "\n".join(audit) + "\n",
    encoding="utf-8"
)

print("=" * 80)
print("V3 FORMAL VALIDATION PREPARATION")
print("=" * 80)
print(f"Development baseline: {DEVELOPMENT_BASELINE}")
print()
print("PASS: frozen formal cohort verified")
print("PASS: development specimens excluded")
print("PASS: manual stability order generated")
print("PASS: three formal CV run orders generated")
print("PASS: observation files generated")
print("PASS: formal validation plan generated")
print("PASS: checklist generated")
print("PASS: preparation audit generated")
print()
print("FINAL FREEZE IS NOT YET COMPLETE.")
print()
print("Next required step:")
print("identify exact estimator/calibration/configuration files.")
