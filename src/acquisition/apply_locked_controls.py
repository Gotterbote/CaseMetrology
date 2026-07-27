"""Apply and verify the locked CaseMetrology camera-control state."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

DEFAULT_DEVICE = "/dev/case-metrology-camera"

LOCKED_CONTROLS = {
    "auto_exposure": 1,
    "white_balance_automatic": 0,
    "exposure_time_absolute": 5,
    "gain": 100,
    "white_balance_temperature": 2498,
    "brightness": 0,
    "contrast": 10,
    "saturation": 0,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Restore and verify the locked camera-control settings used "
            "for CaseMetrology research acquisition."
        )
    )
    parser.add_argument(
        "--device",
        default=DEFAULT_DEVICE,
        help=f"Camera device path (default: {DEFAULT_DEVICE}).",
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


def read_controls(device: str) -> dict[str, int]:
    control_names = ",".join(LOCKED_CONTROLS)

    output = run_command(
        [
            "v4l2-ctl",
            f"--device={device}",
            f"--get-ctrl={control_names}",
        ]
    )

    values: dict[str, int] = {}

    for line in output.splitlines():
        match = re.match(
            r"^([a-zA-Z0-9_]+):\s+(-?\d+)",
            line.strip(),
        )

        if match:
            values[match.group(1)] = int(match.group(2))

    missing = sorted(set(LOCKED_CONTROLS) - set(values))

    if missing:
        raise RuntimeError("Could not read required controls: " + ", ".join(missing))

    return values


def main() -> None:
    args = parse_args()
    device_path = Path(args.device)

    if not device_path.exists():
        raise RuntimeError(
            f"Camera device does not exist: {args.device}\n"
            "Reconnect the Arducam USB cable and try again."
        )

    # Automatic modes must be disabled before dependent manual values
    # can be applied.
    run_command(
        [
            "v4l2-ctl",
            f"--device={args.device}",
            "--set-ctrl=auto_exposure=1,white_balance_automatic=0",
        ]
    )

    manual_controls = ",".join(
        f"{name}={value}"
        for name, value in LOCKED_CONTROLS.items()
        if name not in {"auto_exposure", "white_balance_automatic"}
    )

    run_command(
        [
            "v4l2-ctl",
            f"--device={args.device}",
            f"--set-ctrl={manual_controls}",
        ]
    )

    actual = read_controls(args.device)

    mismatches = [
        (
            name,
            expected,
            actual.get(name),
        )
        for name, expected in LOCKED_CONTROLS.items()
        if actual.get(name) != expected
    ]

    if mismatches:
        details = "\n".join(
            f"  {name}: expected {expected}, found {found}"
            for name, expected, found in mismatches
        )
        raise RuntimeError("Camera-control verification failed:\n" + details)

    print("Locked research camera controls applied and verified")
    print(f"Device: {args.device}")

    for name, value in LOCKED_CONTROLS.items():
        print(f"{name}: {value}")

    print("Status: PASS")


if __name__ == "__main__":
    main()
