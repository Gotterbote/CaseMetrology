from datetime import datetime
from pathlib import Path

import cv2

DEVICE = "/dev/case-metrology-camera"
WIDTH = 1456
HEIGHT = 1088
FPS = 44
WARMUP_FRAMES = 20


def main() -> None:
    output_dir = Path("raw_images/baseline")
    output_dir.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(DEVICE, cv2.CAP_V4L2)

    if not camera.isOpened():
        raise RuntimeError(f"Could not open camera at {DEVICE}")

    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"YUYV"))
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    camera.set(cv2.CAP_PROP_FPS, FPS)

    frame = None

    for _ in range(WARMUP_FRAMES):
        success, frame = camera.read()

        if not success:
            camera.release()
            raise RuntimeError("Camera opened, but frame capture failed")

    actual_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = camera.get(cv2.CAP_PROP_FPS)

    camera.release()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = output_dir / f"baseline_{timestamp}.png"

    if frame is None or not cv2.imwrite(str(image_path), frame):
        raise RuntimeError("Could not save the baseline image")

    print("Baseline capture successful")
    print(f"Resolution: {actual_width} x {actual_height}")
    print(f"Reported frame rate: {actual_fps:.2f}")
    print(f"Image saved to: {image_path}")


if __name__ == "__main__":
    main()
