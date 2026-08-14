"""Tests for the integrated OAL production-cycle workflow."""

from __future__ import annotations

import json
from pathlib import Path
from urllib import error

import cv2
import numpy as np

from src.transport.oal_outbox import pending_entries
from src.workflows.oal_production_cycle import (
    run_oal_production_cycle,
)


def _synthetic_blank_and_case() -> tuple[np.ndarray, np.ndarray]:
    blank = np.full((500, 700), 240, dtype=np.uint8)
    image = blank.copy()

    cv2.rectangle(
        image,
        (250, 100),
        (390, 400),
        40,
        thickness=-1,
    )

    return blank, image


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

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        return False

    def read(self) -> bytes:
        return self._body


def _write_source_images(
    tmp_path: Path,
    blank: np.ndarray,
    image: np.ndarray,
) -> tuple[Path, Path]:
    blank_path = tmp_path / "blank.png"
    image_path = tmp_path / "case.png"

    assert cv2.imwrite(str(blank_path), blank)
    assert cv2.imwrite(str(image_path), image)

    return blank_path, image_path


def test_cycle_persists_and_delivers_when_receiver_available(
    tmp_path: Path,
    monkeypatch,
) -> None:
    blank, image = _synthetic_blank_and_case()

    blank_path, image_path = _write_source_images(
        tmp_path,
        blank,
        image,
    )

    # Keep the test independent of the repository's current Git SHA.
    monkeypatch.setattr(
        "src.diagnostics.oal_measurement_artifacts._git_commit",
        lambda: "test-commit",
    )

    def fake_urlopen(http_request, timeout):
        record = json.loads(
            next(path for path in (tmp_path / "artifacts").rglob("*.json")).read_text(
                encoding="utf-8"
            )
        )

        return _FakeResponse(
            status=201,
            payload={
                "status": "stored",
                "measurement_id": record["measurement_id"],
                "annotated_image_sha256": (record["annotated_image_sha256"]),
            },
        )

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        fake_urlopen,
    )

    db_path = tmp_path / "outbox.sqlite3"

    result = run_oal_production_cycle(
        blank=blank,
        image=image,
        source_image_path=image_path,
        blank_reference_path=blank_path,
        artifact_root=tmp_path / "artifacts",
        outbox_db_path=db_path,
        part_id="test-part",
        measurement_id="cycle-success-001",
        receiver_url="http://receiver.test:8766",
    )

    assert result.measurement.passed
    assert result.annotated_path.is_file()
    assert result.record_path.is_file()

    assert result.delivery is not None
    assert result.delivery.success
    assert result.delivery.http_status == 201
    assert result.delivery.remote_status == "stored"

    assert result.outbox_entry.status == "delivered"
    assert result.outbox_entry.attempt_count == 1

    assert pending_entries(db_path) == []


def test_cycle_preserves_local_measurement_when_receiver_unavailable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    blank, image = _synthetic_blank_and_case()

    blank_path, image_path = _write_source_images(
        tmp_path,
        blank,
        image,
    )

    monkeypatch.setattr(
        "src.diagnostics.oal_measurement_artifacts._git_commit",
        lambda: "test-commit",
    )

    def fail_urlopen(*args, **kwargs):
        raise error.URLError("receiver unavailable")

    monkeypatch.setattr(
        "src.transport.oal_sender.request.urlopen",
        fail_urlopen,
    )

    db_path = tmp_path / "outbox.sqlite3"

    result = run_oal_production_cycle(
        blank=blank,
        image=image,
        source_image_path=image_path,
        blank_reference_path=blank_path,
        artifact_root=tmp_path / "artifacts",
        outbox_db_path=db_path,
        part_id="test-part",
        measurement_id="cycle-offline-001",
        receiver_url="http://receiver.test:8766",
    )

    # Measurement itself remains valid.
    assert result.measurement.passed

    # Local evidence survives regardless of network state.
    assert result.annotated_path.is_file()
    assert result.record_path.is_file()

    # Network delivery failed cleanly.
    assert result.delivery is not None
    assert not result.delivery.success
    assert result.delivery.error is not None
    assert "receiver unavailable" in result.delivery.error

    # The item remains durably queued for retry.
    assert result.outbox_entry.status == "pending"
    assert result.outbox_entry.attempt_count == 1
    assert result.outbox_entry.last_error is not None

    pending = pending_entries(db_path)

    assert len(pending) == 1
    assert pending[0].measurement_id == "cycle-offline-001"

    # Re-reading the locally persisted JSON confirms that the actual
    # measurement was retained even though delivery failed.
    record = json.loads(result.record_path.read_text(encoding="utf-8"))

    assert record["measurement_id"] == "cycle-offline-001"
    assert record["pipeline_passed"] is True
    assert record["oal_in"] is not None
