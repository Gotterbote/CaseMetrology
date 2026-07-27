"""Controlled research-image acquisition for CaseMetrology."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2

DEFAULT_DEVICE = "/dev/case-metrology-camera"
DEFAULT_WIDTH = 1456
DEFAULT_HEIGHT = 1088
DEFAULT_FPS = 44
DEFAULT_WARMUP_FRAMES = 20

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
            "Capture one or more controlled research images while recording "
            "camera settings, timestamps, Git state, and SHA-256 hashes."
        )
    )
    parser.add_argument(
        "--label",
        required=True,
        help=("Meaningful filename label, such as " "'gauge_block_repositioning_01'."),
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of images to capture (default: 1).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Seconds between captures (default: 1.0).",
    )
    parser.add_argument(
        "--device",
        default=DEFAULT_DEVICE,
        help=f"Camera device path (default: {DEFAULT_DEVICE}).",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("raw_images/acquisition"),
        help="Root directory for captured images.",
    )
    parser.add_argument(
        "--metadata-root",
        type=Path,
        default=Path("measurements/acquisition"),
        help="Directory for session metadata.",
    )
    parser.add_argument(
        "--allow-control-mismatch",
        action="store_true",
        help="Capture even when camera controls differ from expected values.",
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


def get_git_information() -> tuple[str, bool]:
    commit = run_command(["git", "rev-parse", "HEAD"])
    dirty = bool(run_command(["git", "status", "--porcelain"]))
    return commit, dirty


def get_camera_controls(device: str) -> dict[str, int]:
    output = run_command(
        [
            "v4l2-ctl",
            f"--device={device}",
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
            "Could not read all required camera controls: " + ", ".join(missing)
        )

    return controls


def validate_controls(
    actual: dict[str, int],
    allow_mismatch: bool,
) -> list[str]:
    mismatches = []

    for name, expected_value in EXPECTED_CONTROLS.items():
        actual_value = actual.get(name)

        if actual_value != expected_value:
            mismatches.append(
                f"{name}: expected {expected_value}, found {actual_value}"
            )

    if mismatches and not allow_mismatch:
        raise RuntimeError(
            "Camera controls are not in the locked research state:\n  "
            + "\n  ".join(mismatches)
        )

    return mismatches


def sanitize_label(label: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]+", "_", label.strip())
    sanitized = sanitized.strip("_")

    if not sanitized:
        raise ValueError("The supplied label does not contain usable characters.")

    return sanitized.lower()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> None:
    args = parse_args()

    if args.count < 1:
        raise ValueError("--count must be at least 1")

    if args.interval < 0:
        raise ValueError("--interval cannot be negative")

    device_path = Path(args.device)

    if not device_path.exists():
        raise RuntimeError(f"Camera device does not exist: {args.device}")

    label = sanitize_label(args.label)
    start_time = datetime.now().astimezone()
    session_timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    session_id = f"{label}_{session_timestamp}"

    image_dir = args.output_root / session_id
    metadata_path = args.metadata_root / f"{session_id}.json"

    image_dir.mkdir(parents=True, exist_ok=False)
    args.metadata_root.mkdir(parents=True, exist_ok=True)

    git_commit, git_dirty = get_git_information()
    controls_before = get_camera_controls(args.device)
    control_mismatches = validate_controls(
        controls_before,
        args.allow_control_mismatch,
    )

    camera = cv2.VideoCapture(args.device, cv2.CAP_V4L2)

    if not camera.isOpened():
        raise RuntimeError(f"Could not open camera at {args.device}")

    images: list[dict[str, Any]] = []

    try:
        camera.set(
            cv2.CAP_PROP_FOURCC,
            cv2.VideoWriter_fourcc(*"YUYV"),
        )
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, DEFAULT_WIDTH)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, DEFAULT_HEIGHT)
        camera.set(cv2.CAP_PROP_FPS, DEFAULT_FPS)
        camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        for _ in range(DEFAULT_WARMUP_FRAMES):
            success, _ = camera.read()

            if not success:
                raise RuntimeError("Camera opened, but warmup frame capture failed")

        actual_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = float(camera.get(cv2.CAP_PROP_FPS))

        next_capture_time = time.monotonic()
        capture_number = 0

        while capture_number < args.count:
            success, frame = camera.read()

            if not success:
                raise RuntimeError("Camera frame capture failed")

            current_time = time.monotonic()

            if current_time < next_capture_time:
                continue

            capture_number += 1
            captured_at = datetime.now().astimezone()
            filename = (
                f"{label}_{captured_at.strftime('%Y%m%d_%H%M%S_%f')}"
                f"_{capture_number:02d}.png"
            )
            image_path = image_dir / filename

            if not cv2.imwrite(str(image_path), frame):
                raise RuntimeError(f"Could not save image: {image_path}")

            images.append(
                {
                    "sequence": capture_number,
                    "filename": filename,
                    "relative_path": str(image_path),
                    "captured_at": captured_at.isoformat(timespec="microseconds"),
                    "size_bytes": image_path.stat().st_size,
                    "sha256": sha256_file(image_path),
                }
            )

            print(f"Captured {capture_number}/{args.count}: " f"{image_path}")

            next_capture_time = current_time + args.interval

    finally:
        camera.release()

    controls_after = get_camera_controls(args.device)

    metadata = {
        "schema_version": 1,
        "session_id": session_id,
        "label": label,
        "started_at": start_time.isoformat(timespec="seconds"),
        "completed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "git_commit": git_commit,
        "git_working_tree_dirty": git_dirty,
        "camera": {
            "device": args.device,
            "requested_width": DEFAULT_WIDTH,
            "requested_height": DEFAULT_HEIGHT,
            "requested_fps": DEFAULT_FPS,
            "actual_width": actual_width,
            "actual_height": actual_height,
            "actual_fps": actual_fps,
            "warmup_frames": DEFAULT_WARMUP_FRAMES,
            "pixel_format": "YUYV",
        },
        "camera_controls_before": controls_before,
        "camera_controls_after": controls_after,
        "expected_camera_controls": EXPECTED_CONTROLS,
        "control_mismatches": control_mismatches,
        "capture_count": args.count,
        "requested_interval_seconds": args.interval,
        "images": images,
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print("Research acquisition complete")
    print(f"Session ID: {session_id}")
    print(f"Images captured: {len(images)}")
    print(f"Resolution: {actual_width} x {actual_height}")
    print(f"Reported frame rate: {actual_fps:.2f}")
    print(f"Git commit: {git_commit}")
    print(f"Git working tree dirty: {git_dirty}")
    print(f"Metadata saved to: {metadata_path}")


if __name__ == "__main__":
    main()
