"""Verify integrity and traceability of a repositioning acquisition session."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2

EXPECTED_CAMERA = {
    "device": "/dev/case-metrology-camera",
    "width": 1456,
    "height": 1088,
    "fps": 44.0,
    "pixel_format": "YUYV",
    "warmup_frames": 20,
}
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
PROTOCOL = Path(
    "docs/repositioning_session_integrity_verification_protocol_2026-07-28.txt"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Verify a repositioning session before dimensional analysis. "
            "This checks record integrity, not measurement accuracy."
        )
    )
    parser.add_argument("metadata", type=Path, help="Session metadata JSON path.")
    parser.add_argument("--report-path", type=Path)
    parser.add_argument("--manifest-path", type=Path)
    return parser.parse_args()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )


def repo_root() -> Path:
    result = run(["git", "rev-parse", "--show-toplevel"], Path.cwd())
    if result.returncode != 0:
        raise RuntimeError("Run this script from inside the Git repository.")
    return Path(result.stdout.strip()).resolve()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path.resolve())


def resolve_recorded_path(value: Any, root: Path) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value)
    return (root / path).resolve() if not path.is_absolute() else path.resolve()


def controls_match(value: Any) -> bool:
    return isinstance(value, dict) and value == EXPECTED_CONTROLS


def camera_matches(value: Any) -> tuple[bool, str]:
    if not isinstance(value, dict):
        return False, "camera record is not an object"

    mismatches: list[str] = []
    for key, expected in EXPECTED_CAMERA.items():
        actual = value.get(key)
        if key == "fps":
            try:
                matched = math.isclose(
                    float(actual), float(expected), rel_tol=0.0, abs_tol=1e-6
                )
            except (TypeError, ValueError):
                matched = False
        else:
            matched = actual == expected
        if not matched:
            mismatches.append(f"{key}: expected {expected!r}, found {actual!r}")

    return not mismatches, "; ".join(mismatches) or "approved camera state"


def main() -> int:
    args = parse_args()
    root = repo_root()
    metadata_path = args.metadata.resolve()

    if not metadata_path.is_file():
        print(f"ERROR: metadata file not found: {metadata_path}", file=sys.stderr)
        return 2

    report_path = (
        args.report_path
        or metadata_path.with_name(f"{metadata_path.stem}_integrity_verification.txt")
    ).resolve()
    manifest_path = (
        args.manifest_path
        or metadata_path.with_name(f"{metadata_path.stem}_evidence_manifest.sha256")
    ).resolve()

    existing = [path for path in (report_path, manifest_path) if path.exists()]
    if existing:
        print("ERROR: refusing to overwrite existing output:", file=sys.stderr)
        for path in existing:
            print(f"  {path}", file=sys.stderr)
        return 2

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: invalid metadata JSON: {error}", file=sys.stderr)
        return 2

    checks: list[tuple[str, bool, str]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append((name, bool(passed), detail))

    required = {
        "schema_version",
        "session_id",
        "test_name",
        "test_mode",
        "git_commit",
        "git_working_tree_dirty",
        "camera",
        "expected_camera_controls",
        "camera_controls_before",
        "camera_controls_after",
        "cycles_requested",
        "cycles_completed",
        "captures",
    }
    missing = sorted(required - set(metadata)) if isinstance(metadata, dict) else []
    check(
        "Required metadata fields",
        isinstance(metadata, dict) and not missing,
        (
            "all required fields present"
            if not missing
            else "missing: " + ", ".join(missing)
        ),
    )
    if not isinstance(metadata, dict):
        metadata = {}

    check(
        "Metadata schema version",
        metadata.get("schema_version") == 1,
        f"recorded={metadata.get('schema_version')!r}",
    )

    verifier_commit_result = run(["git", "rev-parse", "HEAD"], root)
    verifier_commit = verifier_commit_result.stdout.strip() or "UNKNOWN"
    method_paths = [Path(__file__).resolve(), (root / PROTOCOL).resolve()]
    method_relatives: list[str] = []
    method_failures: list[str] = []

    for path in method_paths:
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            method_failures.append(f"outside repository: {path}")
            continue
        method_relatives.append(relative)
        tracked = (
            run(["git", "ls-files", "--error-unmatch", "--", relative], root).returncode
            == 0
        )
        if not tracked:
            method_failures.append(f"not tracked: {relative}")

    if method_relatives:
        changed = (
            run(
                ["git", "diff", "--quiet", "HEAD", "--", *method_relatives], root
            ).returncode
            != 0
        )
        if changed:
            method_failures.append("method differs from HEAD")

    check(
        "Verification method traceability",
        not method_failures,
        (
            f"tracked and unchanged at {verifier_commit}"
            if not method_failures
            else "; ".join(method_failures)
        ),
    )
    check(
        "Clean acquisition working tree",
        metadata.get("git_working_tree_dirty") is False,
        f"recorded={metadata.get('git_working_tree_dirty')!r}",
    )

    camera_ok, camera_detail = camera_matches(metadata.get("camera"))
    check("Approved camera configuration", camera_ok, camera_detail)
    check(
        "Expected controls record",
        controls_match(metadata.get("expected_camera_controls")),
        "matches locked controls",
    )
    check(
        "Controls before acquisition",
        controls_match(metadata.get("camera_controls_before")),
        "matches locked controls",
    )
    check(
        "Controls after acquisition",
        controls_match(metadata.get("camera_controls_after")),
        "matches locked controls",
    )

    captures = metadata.get("captures")
    captures = captures if isinstance(captures, list) else []
    requested = metadata.get("cycles_requested")
    completed = metadata.get("cycles_completed")
    counts_ok = (
        isinstance(requested, int)
        and isinstance(completed, int)
        and requested > 0
        and requested == completed == len(captures)
    )
    check(
        "Acquisition completeness",
        counts_ok,
        f"requested={requested!r}, completed={completed!r}, records={len(captures)}",
    )

    cycles = [item.get("cycle") for item in captures if isinstance(item, dict)]
    expected_cycles = list(range(1, len(captures) + 1))
    check(
        "Sequential unique cycle numbers",
        cycles == expected_cycles and len(cycles) == len(set(cycles)),
        f"cycles={cycles!r}",
    )

    paths = [item.get("relative_path") for item in captures if isinstance(item, dict)]
    names = [item.get("filename") for item in captures if isinstance(item, dict)]
    records_unique = (
        len(paths) == len(set(paths))
        and len(names) == len(set(names))
        and None not in paths
        and None not in names
    )
    check(
        "Unique image records",
        records_unique,
        "paths and filenames are unique and non-null",
    )

    capture_control_failures = [
        item.get("cycle", index)
        for index, item in enumerate(captures, start=1)
        if not isinstance(item, dict) or not controls_match(item.get("camera_controls"))
    ]
    check(
        "Controls for every capture",
        not capture_control_failures,
        (
            "all capture controls match"
            if not capture_control_failures
            else f"failed cycles={capture_control_failures!r}"
        ),
    )

    image_rows: list[str] = []
    evidence_paths = [metadata_path]
    image_passes: list[bool] = []
    camera = metadata.get("camera") if isinstance(metadata.get("camera"), dict) else {}

    for index, item in enumerate(captures, start=1):
        if not isinstance(item, dict):
            image_rows.append(
                f"FAIL | Record {index:02d} | capture record is not an object"
            )
            image_passes.append(False)
            continue

        cycle = item.get("cycle")
        image_path = resolve_recorded_path(item.get("relative_path"), root)
        exists = image_path is not None and image_path.is_file()
        readable = False
        dimensions_ok = False
        size_ok = False
        hash_ok = False
        filename_ok = image_path is not None and item.get("filename") == image_path.name

        if exists and image_path is not None:
            image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
            readable = image is not None
            dimensions_ok = (
                readable
                and image.shape[1] == camera.get("width")
                and image.shape[0] == camera.get("height")
            )
            size_ok = image_path.stat().st_size == item.get("size_bytes")
            hash_ok = sha256(image_path) == item.get("sha256")
            evidence_paths.append(image_path)

        passed = all((exists, readable, dimensions_ok, size_ok, hash_ok, filename_ok))
        image_passes.append(passed)
        path_text = "UNKNOWN" if image_path is None else display_path(image_path, root)
        image_rows.append(
            f"{'PASS' if passed else 'FAIL'} | Cycle {cycle!r} | "
            f"path={path_text} | exists={exists} | readable={readable} | "
            f"dimensions_ok={dimensions_ok} | size_ok={size_ok} | "
            f"sha256_ok={hash_ok} | filename_ok={filename_ok}"
        )

    check(
        "Image file integrity",
        bool(image_passes) and all(image_passes),
        f"passed={sum(image_passes)} of {len(image_passes)}",
    )

    overall_pass = all(passed for _, passed, _ in checks)
    report_lines = [
        "CaseMetrology Repositioning Session Integrity Verification",
        "",
        f"Verification timestamp: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        f"Metadata file: {display_path(metadata_path, root)}",
        f"Session ID: {metadata.get('session_id', 'UNKNOWN')}",
        f"Test mode: {metadata.get('test_mode', 'UNKNOWN')}",
        f"Acquisition Git commit: {metadata.get('git_commit', 'UNKNOWN')}",
        f"Verification-method Git commit: {verifier_commit}",
        "",
        "AUTOMATED CHECKS",
    ]
    report_lines.extend(
        f"{'PASS' if passed else 'FAIL'} | {name} | {detail}"
        for name, passed, detail in checks
    )
    report_lines.extend(["", "IMAGE RECORDS", *image_rows, ""])
    report_lines.extend(
        [
            "MANUAL REVIEWS NOT ESTABLISHED BY THIS SCRIPT",
            "- Gauge-block orientation",
            "- Physical seating against both datum faces",
            "- Unchanged camera, lens, focus, backlight, and Lexan locator",
            "- Environmental measurement classification",
            "- Diagnostic confirmation of correct measurement-edge fitting",
            "",
            f"OVERALL AUTOMATED RESULT: {'PASS' if overall_pass else 'FAIL'}",
            "",
            "A PASS establishes acquisition-record integrity and traceability only. "
            "It does not establish dimensional accuracy, repeatability, uncertainty, "
            "or overall experimental acceptance.",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    evidence_paths.append(report_path)

    unique_evidence = sorted(
        set(evidence_paths), key=lambda path: display_path(path, root)
    )
    manifest_lines = [
        f"{sha256(path)}  {display_path(path, root)}" for path in unique_evidence
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(report_path.read_text(encoding="utf-8"))
    print(f"Report saved: {display_path(report_path, root)}")
    print(f"Manifest saved: {display_path(manifest_path, root)}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
