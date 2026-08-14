"""Run one live CaseMetrology OAL acquisition and production cycle.

The established research-acquisition script remains authoritative for
camera capture. This wrapper invokes it, reads the resulting acquisition
metadata, and passes the captured image into the integrated OAL workflow.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import subprocess
import sys

import cv2

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DEFAULT_RECEIVER_URL = "http://100.71.13.87:8766"
DEFAULT_RUNTIME_ROOT = Path.home() / ".local" / "share" / "casemetrology"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one live cartridge case and run the complete "
            "CaseMetrology OAL production workflow."
        )
    )

    parser.add_argument(
        "--part-id",
        required=True,
        help="Laser-etched specimen identifier.",
    )

    parser.add_argument(
        "--blank-image",
        required=True,
        type=Path,
        help="Current controlled blank-reference image.",
    )

    parser.add_argument(
        "--receiver-url",
        default=DEFAULT_RECEIVER_URL,
        help=("CaseMetrology receiver base URL " f"(default: {DEFAULT_RECEIVER_URL})."),
    )

    return parser.parse_args()


def capture_case(part_id: str) -> tuple[Path, Path, str]:
    """Run the established research acquisition for one live case."""

    label = f"oal_live_case_{part_id}"

    command = [
        sys.executable,
        "src/acquisition/capture_research.py",
        "--label",
        label,
        "--count",
        "1",
    ]

    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    print(completed.stdout, end="")

    metadata_match = re.search(
        r"^Metadata saved to:\s+(.+)$",
        completed.stdout,
        flags=re.MULTILINE,
    )

    if metadata_match is None:
        raise RuntimeError(
            "Could not determine acquisition metadata path " "from capture output."
        )

    metadata_path = Path(metadata_match.group(1).strip())

    if not metadata_path.is_file():
        raise RuntimeError(f"Acquisition metadata does not exist: {metadata_path}")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    session_id = metadata.get("session_id")
    images = metadata.get("images")

    if not isinstance(session_id, str) or not session_id:
        raise RuntimeError("Acquisition metadata has no valid session_id.")

    if not isinstance(images, list) or len(images) != 1:
        raise RuntimeError("Expected exactly one acquired image.")

    image_path_value = images[0].get("relative_path")

    if not isinstance(image_path_value, str):
        raise RuntimeError("Acquisition metadata has no valid image path.")

    image_path = Path(image_path_value)

    if not image_path.is_file():
        raise RuntimeError(f"Captured image does not exist: {image_path}")

    return image_path, metadata_path, session_id


def main() -> None:
    from src.workflows.oal_production_cycle import run_oal_production_cycle

    args = parse_args()

    if not args.blank_image.is_file():
        raise FileNotFoundError(f"Blank reference does not exist: {args.blank_image}")

    print("===== LIVE OAL CYCLE =====")
    print(f"Part ID: {args.part_id}")
    print(f"Blank:   {args.blank_image}")
    print()

    image_path, metadata_path, session_id = capture_case(args.part_id)

    blank = cv2.imread(
        str(args.blank_image),
        cv2.IMREAD_GRAYSCALE,
    )

    image = cv2.imread(
        str(image_path),
        cv2.IMREAD_GRAYSCALE,
    )

    if blank is None:
        raise RuntimeError(f"Could not load blank reference: {args.blank_image}")

    if image is None:
        raise RuntimeError(f"Could not load captured image: {image_path}")

    result = run_oal_production_cycle(
        blank=blank,
        image=image,
        source_image_path=image_path,
        blank_reference_path=args.blank_image,
        artifact_root=DEFAULT_RUNTIME_ROOT / "artifacts",
        outbox_db_path=DEFAULT_RUNTIME_ROOT / "oal_outbox.sqlite3",
        part_id=args.part_id,
        measurement_id=session_id,
        receiver_url=args.receiver_url,
        timeout_seconds=5.0,
    )

    print()
    print("===== OAL RESULT =====")
    print(f"Part ID:              {args.part_id}")
    print(f"Acquisition session:  {session_id}")
    print(f"Acquisition metadata: {metadata_path}")
    print(f"Measurement passed:   {result.measurement.passed}")

    if result.measurement.passed:
        print(f"OAL inches:           " f"{result.measurement.length_inches:.9f}")
        print(f"OAL pixels:           " f"{result.measurement.pca.length_pixels:.9f}")
        print(
            f"Effective PPI:        "
            f"{result.measurement.calibration.effective_ppi:.9f}"
        )
    else:
        print(f"Failure stage:        " f"{result.measurement.failure_stage}")
        print(f"Failure reason:       " f"{result.measurement.failure_reason}")

    print(f"Record:               {result.record_path}")
    print(f"Annotated:            {result.annotated_path}")
    print(f"Outbox status:        {result.outbox_entry.status}")
    print(f"Delivery attempts:    {result.outbox_entry.attempt_count}")

    if result.delivery is None:
        print("Delivery:              not attempted")
    else:
        print(f"Delivery success:     {result.delivery.success}")
        print(f"Remote status:        {result.delivery.remote_status}")
        print(f"Delivery error:       {result.delivery.error}")


if __name__ == "__main__":
    main()
