#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import cv2
import sys
import time

CAMERA = "/dev/case-metrology-camera"
WIDTH = 1456
HEIGHT = 1088

OUTDIR = Path(
    "data/oal_validation/post_v1_diagnostics/"
    "fixture_rocking_test/specimen178_repeat1"
)
OUTDIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(CAMERA, cv2.CAP_V4L2)

if not cap.isOpened():
    print(f"ERROR: Could not open {CAMERA}")
    sys.exit(1)

# Set only image dimensions.
# Do NOT alter exposure, gain, brightness, focus, etc.
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print("=" * 72)
print("FIXTURE ROCKING DEVELOPMENT TEST")
print("=" * 72)
print(f"Camera:      {CAMERA}")
print(f"Resolution:  {actual_width} x {actual_height}")
print(f"Output dir:  {OUTDIR}")
print()
print("Specimen: 178 — REPEAT 1")
print("One image per independent placement.")
print("No camera-control changes are made by this script.")
print("=" * 72)

if actual_width != WIDTH or actual_height != HEIGHT:
    print(
        f"WARNING: Requested {WIDTH}x{HEIGHT}, "
        f"but camera reports {actual_width}x{actual_height}"
    )

for placement in range(1, 11):

    print()
    print(f"PLACEMENT {placement}/10")
    print("1. Completely remove specimen 178.")
    print("2. Re-place it naturally in the fixture.")
    print("3. Confirm there is no base-to-mouth rocking.")

    response = input(
        "Press ENTER to capture, or type q then ENTER to stop: "
    ).strip().lower()

    if response == "q":
        print("Capture stopped by operator.")
        break

    # Allow the newly placed specimen/image stream to settle.
    time.sleep(0.5)

    # Flush several buffered frames so the saved image is current.
    frame = None
    for _ in range(8):
        ok, frame = cap.read()
        if not ok:
            print("ERROR: Camera frame acquisition failed.")
            cap.release()
            sys.exit(1)

    timestamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%f")
    filename = (
        OUTDIR /
        f"specimen178_repeat1_placement_{placement:02d}_{timestamp}.png"
    )

    if not cv2.imwrite(str(filename), frame):
        print(f"ERROR: Failed to save {filename}")
        cap.release()
        sys.exit(1)

    print(f"SAVED: {filename}")

cap.release()

print()
print("=" * 72)
print("CAPTURE COMPLETE")
print("=" * 72)
