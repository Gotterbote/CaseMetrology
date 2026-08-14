"""Tests for the durable OAL transport outbox."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from src.transport.oal_outbox import (
    get_entry,
    mark_delivered,
    pending_entries,
    queue_artifact_pair,
    record_failed_attempt,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _make_artifacts(tmp_path: Path) -> tuple[Path, Path]:
    image_path = tmp_path / "annotated.png"
    image_path.write_bytes(b"test annotated image")

    record_path = tmp_path / "record.json"
    record_path.write_text(
        json.dumps(
            {
                "measurement_id": "measurement-001",
                "annotated_image_sha256": _sha256(image_path),
            }
        ),
        encoding="utf-8",
    )

    return record_path, image_path


def test_queue_survives_database_reopen(tmp_path: Path) -> None:
    db_path = tmp_path / "outbox.sqlite3"
    record_path, image_path = _make_artifacts(tmp_path)

    queued = queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    reopened = get_entry(
        db_path,
        "measurement-001",
    )

    assert reopened == queued
    assert reopened is not None
    assert reopened.status == "pending"
    assert reopened.attempt_count == 0


def test_queue_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "outbox.sqlite3"
    record_path, image_path = _make_artifacts(tmp_path)

    first = queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    second = queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    assert first == second
    assert len(pending_entries(db_path)) == 1


def test_failed_attempt_remains_pending(tmp_path: Path) -> None:
    db_path = tmp_path / "outbox.sqlite3"
    record_path, image_path = _make_artifacts(tmp_path)

    queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    record_failed_attempt(
        db_path,
        "measurement-001",
        "receiver unavailable",
    )

    entry = get_entry(
        db_path,
        "measurement-001",
    )

    assert entry is not None
    assert entry.status == "pending"
    assert entry.attempt_count == 1
    assert entry.last_error == "receiver unavailable"


def test_verified_ack_marks_delivered(tmp_path: Path) -> None:
    db_path = tmp_path / "outbox.sqlite3"
    record_path, image_path = _make_artifacts(tmp_path)

    queued = queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    mark_delivered(
        db_path,
        "measurement-001",
        remote_status="stored",
        remote_sha256=queued.annotated_sha256,
    )

    entry = get_entry(
        db_path,
        "measurement-001",
    )

    assert entry is not None
    assert entry.status == "delivered"
    assert entry.attempt_count == 1
    assert entry.remote_status == "stored"
    assert entry.remote_sha256 == queued.annotated_sha256
    assert pending_entries(db_path) == []
