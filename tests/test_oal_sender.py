"""Tests for reliable OAL artifact HTTP delivery."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib import error

from src.transport.oal_outbox import (
    get_entry,
    queue_artifact_pair,
)
from src.transport.oal_sender import deliver_entry


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _make_queued_entry(tmp_path: Path):
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

    db_path = tmp_path / "outbox.sqlite3"

    entry = queue_artifact_pair(
        db_path,
        record_path=record_path,
        annotated_path=image_path,
    )

    return db_path, entry, record_path, image_path


class _FakeResponse:
    def __init__(
        self,
        *,
        status: int,
        payload: dict[str, object],
    ) -> None:
        self.status = status
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self) -> bytes:
        return self._body


def test_stored_ack_marks_entry_delivered(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path, entry, _, _ = _make_queued_entry(tmp_path)

    response = _FakeResponse(
        status=201,
        payload={
            "status": "stored",
            "measurement_id": entry.measurement_id,
            "annotated_image_sha256": entry.annotated_sha256,
        },
    )

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        lambda *args, **kwargs: response,
    )

    result = deliver_entry(
        db_path,
        entry,
        receiver_url="http://receiver.test:8766",
    )

    stored = get_entry(db_path, entry.measurement_id)

    assert result.success
    assert result.http_status == 201
    assert result.remote_status == "stored"

    assert stored is not None
    assert stored.status == "delivered"
    assert stored.attempt_count == 1
    assert stored.remote_sha256 == entry.annotated_sha256


def test_already_stored_ack_is_successful(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path, entry, _, _ = _make_queued_entry(tmp_path)

    response = _FakeResponse(
        status=200,
        payload={
            "status": "already_stored",
            "measurement_id": entry.measurement_id,
            "annotated_image_sha256": entry.annotated_sha256,
        },
    )

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        lambda *args, **kwargs: response,
    )

    result = deliver_entry(
        db_path,
        entry,
        receiver_url="http://receiver.test:8766",
    )

    stored = get_entry(db_path, entry.measurement_id)

    assert result.success
    assert result.http_status == 200
    assert result.remote_status == "already_stored"

    assert stored is not None
    assert stored.status == "delivered"


def test_network_failure_remains_pending(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path, entry, _, _ = _make_queued_entry(tmp_path)

    def fail(*args, **kwargs):
        raise error.URLError("receiver unavailable")

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        fail,
    )

    result = deliver_entry(
        db_path,
        entry,
        receiver_url="http://receiver.test:8766",
    )

    stored = get_entry(db_path, entry.measurement_id)

    assert not result.success
    assert result.http_status is None

    assert stored is not None
    assert stored.status == "pending"
    assert stored.attempt_count == 1
    assert stored.last_error is not None
    assert "receiver unavailable" in stored.last_error


def test_modified_artifact_is_not_transmitted(
    tmp_path: Path,
    monkeypatch,
) -> None:
    db_path, entry, _, image_path = _make_queued_entry(tmp_path)

    image_path.write_bytes(b"tampered image")

    network_called = False

    def unexpected_network_call(*args, **kwargs):
        nonlocal network_called
        network_called = True
        raise AssertionError("Network should not be called.")

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        unexpected_network_call,
    )

    result = deliver_entry(
        db_path,
        entry,
        receiver_url="http://receiver.test:8766",
    )

    stored = get_entry(db_path, entry.measurement_id)

    assert not result.success
    assert not network_called

    assert stored is not None
    assert stored.status == "pending"
    assert stored.attempt_count == 1
    assert stored.last_error is not None
    assert "SHA-256" in stored.last_error
