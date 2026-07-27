"""Guided acquisition for gauge-block removal-and-replacement testing."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2

DEVICE = "/dev/case-metrology-camera"
WIDTH = 1456
HEIGHT = 1088
FPS = 44
WARMUP_FRAMES = 20

CONTROL_NAMES = [
    "brightness",
    "contrast",
    "saturation",
    "white_balance_automatic",
    "gain",
    "white_balance_temperature",
    "auto_exposure",
    "exposure_time_absolute",
]

EXPECTED_CONTROLS = {
    "brightness": 0,
    "contrast": 10,
    "saturation": 0,
    "white_balance_automatic": 0,
    "gain": 100,
    "white_balance_temperature": 2498,
    "auto_exposure": 1,
    "exposure_time_absolute": 5,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Guide an operator through independent gauge-block removal, "
            "replacement, seating, and image-capture cycles."
        )
    )
    parser.add_argument(
        "--test-name",
        default="lexan_gauge_block_repositioning",
        help="Meaningful test name.",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=10,
        help="Number of independent repositioning cycles (default: 10).",
    )
    parser.add_argument(
        "--mode",
        choices=["workflow_validation", "removal_and_replacement"],
        default="removal_and_replacement",
        help=(
            "Session purpose recorded in metadata "
            "(default: removal_and_replacement)."
        ),
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("raw_images/repositioning"),
        help="Root directory for captured images.",
    )
    parser.add_argument(
        "--metadata-root",
        type=Path,
        default=Path("measurements/repositioning"),
        help="Directory for session metadata.",
    )
    return parser.parse_args()


def run_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sanitize_name(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip())
    sanitized = sanitized.strip("_").lower()

    if not sanitized:
        raise ValueError("The test name contains no usable characters.")

    return sanitized


def get_git_state() -> tuple[str, bool]:
    commit = run_command(["git", "rev-parse", "HEAD"])
    dirty = bool(run_command(["git", "status", "--porcelain"]))
    return commit, dirty


def get_camera_controls() -> dict[str, int]:
    output = run_command(
        [
            "v4l2-ctl",
            f"--device={DEVICE}",
            f"--get-ctrl={','.join(CONTROL_NAMES)}",
        ]
    )

    controls: dict[str, int] = {}

    for line in output.splitlines():
        match = re.match(r"^([a-zA-Z0-9_]+):\s+(-?\d+)", line.strip())

        if match:
            controls[match.group(1)] = int(match.group(2))

    missing = sorted(set(CONTROL_NAMES) - set(controls))

    if missing:
        raise RuntimeError(
            "Could not read required camera controls: " + ", ".join(missing)
        )

    return controls


def verify_controls(controls: dict[str, int]) -> None:
    mismatches = [
        f"{name}: expected {expected}, found {controls.get(name)}"
        for name, expected in EXPECTED_CONTROLS.items()
        if controls.get(name) != expected
    ]

    if mismatches:
        raise RuntimeError(
            "Camera controls are not in the locked research state:\n  "
            + "\n  ".join(mismatches)
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def warm_up_camera(camera: cv2.VideoCapture) -> None:
    for _ in range(WARMUP_FRAMES):
        success, _ = camera.read()

        if not success:
            raise RuntimeError("Camera warmup frame capture failed.")


def capture_fresh_frame(camera: cv2.VideoCapture) -> Any:
    frame = None

    for _ in range(5):
        success, frame = camera.read()

        if not success:
            raise RuntimeError("Camera frame capture failed.")

    return frame


def main() -> None:
    args = parse_args()

    if args.cycles < 2:
        raise ValueError("--cycles must be at least 2.")

    if not Path(DEVICE).exists():
        raise RuntimeError(
            f"Camera device does not exist: {DEVICE}\n"
            "Reconnect the camera and rerun the research preflight."
        )

    test_name = sanitize_name(args.test_name)
    controls_before = get_camera_controls()
    verify_controls(controls_before)

    git_commit, git_dirty = get_git_state()

    if git_dirty:
        raise RuntimeError(
            "Git working tree is not clean. Commit or discard changes "
            "before beginning the repositioning experiment."
        )

    started_at = datetime.now().astimezone()
    timestamp = started_at.strftime("%Y%m%d_%H%M%S")
    session_id = f"{test_name}_{timestamp}"

    image_dir = args.output_root / session_id
    metadata_path = args.metadata_root / f"{session_id}.json"

    image_dir.mkdir(parents=True, exist_ok=False)
    args.metadata_root.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)

    if not camera.isOpened():
        raise RuntimeError(f"Could not open camera at {DEVICE}")

    records: list[dict[str, Any]] = []

    try:
        camera.set(
            cv2.CAP_PROP_FOURCC,
            cv2.VideoWriter_fourcc(*"YUYV"),
        )
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, FPS)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        warm_up_camera(camera)

        actual_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = float(camera.get(cv2.CAP_PROP_FPS))

        print("CaseMetrology Guided Repositioning Acquisition")
        print(f"Session ID: {session_id}")
        print(f"Cycles planned: {args.cycles}")
        print()
        print(
            "For each cycle, remove the gauge block completely, replace it "
            "in the Lexan locator, seat it gently against both datum faces, "
            "confirm it rests flat, and then press Enter."
        )

        for cycle in range(1, args.cycles + 1):
            print()
            input(
                f"Cycle {cycle:02d}/{args.cycles:02d}: "
                "reposition and seat the gauge block, then press Enter..."
            )

            controls_at_capture = get_camera_controls()
            verify_controls(controls_at_capture)

            frame = capture_fresh_frame(camera)
            captured_at = datetime.now().astimezone()

            filename = (
                f"{test_name}_cycle_{cycle:02d}_"
                f"{captured_at.strftime('%Y%m%d_%H%M%S_%f')}.png"
            )
            image_path = image_dir / filename

            if not cv2.imwrite(str(image_path), frame):
                raise RuntimeError(f"Could not save image: {image_path}")

            record = {
                "cycle": cycle,
                "filename": filename,
                "relative_path": str(image_path),
                "captured_at": captured_at.isoformat(timespec="microseconds"),
                "size_bytes": image_path.stat().st_size,
                "sha256": sha256_file(image_path),
                "camera_controls": controls_at_capture,
            }
            records.append(record)

            print(f"Captured cycle {cycle:02d}: {image_path}")

    finally:
        camera.release()

    controls_after = get_camera_controls()
    verify_controls(controls_after)

    metadata = {
        "schema_version": 1,
        "session_id": session_id,
        "test_name": test_name,
        "test_mode": args.mode,
        "started_at": started_at.isoformat(timespec="seconds"),
        "completed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "git_commit": git_commit,
        "git_working_tree_dirty": git_dirty,
        "camera": {
            "device": DEVICE,
            "width": actual_width,
            "height": actual_height,
            "fps": actual_fps,
            "pixel_format": "YUYV",
            "warmup_frames": WARMUP_FRAMES,
        },
        "expected_camera_controls": EXPECTED_CONTROLS,
        "camera_controls_before": controls_before,
        "camera_controls_after": controls_after,
        "cycles_requested": args.cycles,
        "cycles_completed": len(records),
        "captures": records,
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print("Guided repositioning acquisition complete")
    print(f"Cycles captured: {len(records)}")
    print(f"Images directory: {image_dir}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
