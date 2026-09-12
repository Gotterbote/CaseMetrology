#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path.home() / "CaseMetrology"

REFERENCE = REPO / "scripts" / "capture_fixture_rocking_test.py"

BASE = (
    REPO
    / "data"
    / "oal_validation"
    / "post_v1_diagnostics"
    / "fixture_rocking_test"
)

SPECIMENS = [187, 197]

source = REFERENCE.read_text()

for specimen in SPECIMENS:
    outdir = BASE / f"specimen{specimen}_fixedroll"

    existing = sorted(
        outdir.glob(
            f"specimen{specimen}_fixedroll_placement_*.png"
        )
    )

    if existing:
        raise SystemExit(
            f"STOP: specimen {specimen} already has "
            f"{len(existing)} fixed-roll image(s)."
        )

print("=" * 76)
print("FIXED-ROLL DIAGNOSTIC — SPECIMENS 187 AND 197")
print("=" * 76)
print("10 independent placements per specimen")
print("Engraving faces camera in SAME roll orientation each time.")
print("Do NOT move Fixture 2 or the rubber spacer.")
print("=" * 76)

for specimen in SPECIMENS:

    print()
    print("#" * 76)
    print(f"SPECIMEN {specimen}")
    print("#" * 76)

    confirm = input(
        f"Type {specimen} when specimen {specimen} is ready, "
        "or q to stop: "
    ).strip()

    if confirm.lower() == "q":
        raise SystemExit("Stopped by operator.")

    if confirm != str(specimen):
        raise SystemExit(
            "STOP: specimen confirmation mismatch."
        )

    modified = source

    modified = modified.replace(
        "fixture_rocking_test/specimen146",
        f"fixture_rocking_test/specimen{specimen}_fixedroll"
    )

    modified = modified.replace(
        'print("Specimen: 146")',
        f'print("Specimen: {specimen} — FIXED ROLL")'
    )

    modified = modified.replace(
        "specimen 146",
        f"specimen {specimen}"
    )

    modified = modified.replace(
        "specimen146_placement_",
        f"specimen{specimen}_fixedroll_placement_"
    )

    modified = modified.replace(
        'print("2. Re-place it naturally in the fixture.")',
        'print("2. Orient engraving toward camera in the SAME roll orientation.")\n'
        '    print("3. Re-place it naturally in the fixture.")'
    )

    modified = modified.replace(
        'print("3. Confirm there is no base-to-mouth rocking.")',
        'print("4. Confirm there is no base-to-mouth rocking.")'
    )

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix=f"_fixedroll_{specimen}_",
            dir=REPO / "scripts",
            delete=False,
        ) as f:
            f.write(modified)
            temp_path = Path(f.name)

        result = subprocess.run(
            [sys.executable, str(temp_path)],
            cwd=REPO,
        )

        if result.returncode != 0:
            raise SystemExit(
                f"STOP: specimen {specimen} capture failed."
            )

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

    files = sorted(
        (
            BASE / f"specimen{specimen}_fixedroll"
        ).glob(
            f"specimen{specimen}_fixedroll_placement_*.png"
        )
    )

    if len(files) != 10:
        raise SystemExit(
            f"STOP: specimen {specimen} has "
            f"{len(files)}/10 images."
        )

    print(f"PASS: specimen {specimen} = 10/10")

print()
print("=" * 76)
print("FIXED-ROLL CAPTURE COMPLETE")
print("=" * 76)

for specimen in SPECIMENS:
    files = sorted(
        (
            BASE / f"specimen{specimen}_fixedroll"
        ).glob(
            f"specimen{specimen}_fixedroll_placement_*.png"
        )
    )

    print(
        f"Specimen {specimen}: {len(files)}/10"
    )
