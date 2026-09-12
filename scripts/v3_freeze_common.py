#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "docs/research/v3_formal_validation/V3_MEASUREMENT_SYSTEM_MANIFEST.sha256"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def verify_freeze_manifest() -> None:
    if not MANIFEST.is_file():
        raise SystemExit(
            f"STOP: V3 freeze manifest does not exist: {MANIFEST.relative_to(REPO)}"
        )

    failures: list[str] = []
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        expected, rel = raw.split(None, 1)
        rel = rel.strip()
        path = REPO / rel
        if not path.is_file():
            failures.append(f"MISSING {rel}")
            continue
        actual = sha256_file(path)
        if actual != expected:
            failures.append(f"HASH MISMATCH {rel}")

    if failures:
        raise SystemExit(
            "STOP: frozen V3 measurement-system verification failed:\n"
            + "\n".join(failures)
        )
