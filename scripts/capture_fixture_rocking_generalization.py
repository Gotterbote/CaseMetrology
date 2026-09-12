#!/usr/bin/env python3

from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile


REPO = Path.home() / "CaseMetrology"

REFERENCE_SCRIPT = (
    REPO / "scripts" / "capture_fixture_rocking_test.py"
)

BASE_OUTPUT = (
    REPO
    / "data"
    / "oal_validation"
    / "post_v1_diagnostics"
    / "fixture_rocking_test"
)

SPECIMENS = [121, 178, 187, 197]
PLACEMENTS_REQUIRED = 10


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)

    return h.hexdigest()


def placement_files(specimen: int):
    output_dir = BASE_OUTPUT / f"specimen{specimen}"

    return sorted(
        output_dir.glob(
            f"specimen{specimen}_placement_*.png"
        )
    )


def main():
    if not REFERENCE_SCRIPT.exists():
        raise SystemExit(
            f"STOP: reference script not found:\n"
            f"{REFERENCE_SCRIPT}"
        )

    source = REFERENCE_SCRIPT.read_text()

    if "146" not in source:
        raise SystemExit(
            "STOP: expected specimen identifier 146 "
            "was not found in the reference script."
        )

    print("=" * 78)
    print("V3 FIXTURE-STABILITY GENERALIZATION CAPTURE")
    print("=" * 78)
    print()
    print(f"Reference script: {REFERENCE_SCRIPT}")
    print(
        "Reference SHA256:",
        sha256_file(REFERENCE_SCRIPT),
    )
    print()
    print(
        "Specimens:",
        ", ".join(str(x) for x in SPECIMENS),
    )
    print(
        f"Placements per specimen: "
        f"{PLACEMENTS_REQUIRED}"
    )
    print()
    print(
        "The original specimen-146 capture script "
        "will NOT be modified."
    )
    print(
        "Only the specimen identifier and resulting "
        "output path/filename are changed."
    )
    print("=" * 78)

    # --------------------------------------------------
    # PRE-RUN COLLISION CHECK
    # --------------------------------------------------

    print()
    print("Pre-run output check:")

    for specimen in SPECIMENS:
        files = placement_files(specimen)

        if files:
            print()
            print(
                f"STOP: specimen {specimen} already has "
                f"{len(files)} placement image(s):"
            )

            for file in files:
                print(f"  {file}")

            print()
            print(
                "Existing test data will not be mixed "
                "with a new acquisition."
            )

            return 1

        print(
            f"  specimen {specimen}: "
            "no existing placement images"
        )

    print()
    print("=" * 78)
    print("PRE-RUN CHECK PASSED")
    print("=" * 78)

    # --------------------------------------------------
    # CAPTURE EACH SPECIMEN
    # --------------------------------------------------

    for index, specimen in enumerate(SPECIMENS, start=1):

        print()
        print()
        print("#" * 78)
        print(
            f"SPECIMEN {specimen} "
            f"({index}/{len(SPECIMENS)})"
        )
        print("#" * 78)
        print()
        print(
            f"Remove the previous specimen and prepare "
            f"specimen {specimen}."
        )
        print()
        print(
            "Do NOT adjust the camera, 16 mm lens, "
            "focus, lighting, fixture, calibration, "
            "or camera controls."
        )
        print()

        response = input(
            f"Type {specimen} and press ENTER "
            f"when specimen {specimen} is ready, "
            "or q to stop: "
        ).strip()

        if response.lower() == "q":
            print("Capture stopped by operator.")
            return 1

        if response != str(specimen):
            print()
            print(
                "STOP: specimen confirmation did not "
                "match the requested specimen."
            )
            return 1

        # Make an in-memory specimen-specific version
        # of the already-tested 146 capture script.
        modified_source = source.replace(
            "146",
            str(specimen),
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix=f"fixture_capture_{specimen}_",
            delete=False,
        ) as temp:
            temp.write(modified_source)
            temp_path = Path(temp.name)

        try:
            result = subprocess.run(
                [sys.executable, str(temp_path)],
                cwd=str(REPO),
            )
        finally:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass

        if result.returncode != 0:
            print()
            print(
                f"STOP: capture script for specimen "
                f"{specimen} returned code "
                f"{result.returncode}."
            )
            return 1

        files = placement_files(specimen)

        print()
        print(
            f"Specimen {specimen} placement images "
            f"found: {len(files)}"
        )

        if len(files) != PLACEMENTS_REQUIRED:
            print()
            print(
                "STOP: expected exactly "
                f"{PLACEMENTS_REQUIRED} placement "
                f"images but found {len(files)}."
            )
            print(
                "Do not continue to the next specimen."
            )
            return 1

        print(
            f"PASS: specimen {specimen} has exactly "
            f"{PLACEMENTS_REQUIRED} placement images."
        )

    # --------------------------------------------------
    # FINAL VERIFICATION
    # --------------------------------------------------

    print()
    print()
    print("=" * 78)
    print("GENERALIZATION CAPTURE COMPLETE")
    print("=" * 78)

    total = 0

    for specimen in SPECIMENS:
        files = placement_files(specimen)
        total += len(files)

        print(
            f"Specimen {specimen}: "
            f"{len(files)}/"
            f"{PLACEMENTS_REQUIRED} images"
        )

    print("-" * 78)
    print(
        f"Total new placement images: "
        f"{total}/"
        f"{len(SPECIMENS) * PLACEMENTS_REQUIRED}"
    )

    if total != len(SPECIMENS) * PLACEMENTS_REQUIRED:
        print("FINAL STATUS: STOP / INCOMPLETE")
        return 1

    print("FINAL STATUS: PASS")
    print()
    print(
        "Do not modify or recapture any images before "
        "the analysis step."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
