"""Reliable HTTP delivery of queued OAL measurement artifacts.

The sender reads only from the durable SQLite outbox. A measurement is
marked delivered only after the remote receiver returns a verified ACK
containing the expected measurement ID and annotated-image SHA-256.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from io import BytesIO
import json
from pathlib import Path
from urllib import error, request
import zipfile

from src.transport.oal_outbox import (
    OutboxEntry,
    mark_delivered,
    pending_entries,
    record_failed_attempt,
)


@dataclass(frozen=True)
class DeliveryResult:
    """Result of one attempted artifact delivery."""

    measurement_id: str
    success: bool
    http_status: int | None
    remote_status: str | None
    error: str | None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def _build_packet(entry: OutboxEntry) -> bytes:
    """Build the exact ZIP packet expected by the receiver."""

    record_path = Path(entry.record_path)
    annotated_path = Path(entry.annotated_path)

    if not record_path.is_file():
        raise FileNotFoundError(f"Missing measurement record: {record_path}")

    if not annotated_path.is_file():
        raise FileNotFoundError(f"Missing annotated image: {annotated_path}")

    actual_record_hash = _sha256(record_path)
    actual_annotated_hash = _sha256(annotated_path)

    if actual_record_hash != entry.record_sha256:
        raise ValueError("Measurement record SHA-256 no longer matches outbox.")

    if actual_annotated_hash != entry.annotated_sha256:
        raise ValueError("Annotated image SHA-256 no longer matches outbox.")

    buffer = BytesIO()

    with zipfile.ZipFile(
        buffer,
        "w",
        compression=zipfile.ZIP_DEFLATED,
    ) as archive:
        archive.write(
            record_path,
            arcname="record.json",
        )
        archive.write(
            annotated_path,
            arcname="annotated.png",
        )

    return buffer.getvalue()


def _receiver_endpoint(receiver_url: str) -> str:
    return receiver_url.rstrip("/") + "/measurements"


def deliver_entry(
    db_path: Path,
    entry: OutboxEntry,
    *,
    receiver_url: str,
    timeout_seconds: float = 5.0,
) -> DeliveryResult:
    """Attempt delivery of one pending outbox entry."""

    try:
        packet = _build_packet(entry)

        http_request = request.Request(
            _receiver_endpoint(receiver_url),
            data=packet,
            method="POST",
            headers={
                "Content-Type": "application/zip",
                "Content-Length": str(len(packet)),
            },
        )

        with request.urlopen(
            http_request,
            timeout=timeout_seconds,
        ) as response:
            http_status = response.status
            response_bytes = response.read()

        payload = json.loads(response_bytes.decode("utf-8"))

        if not isinstance(payload, dict):
            raise ValueError("Receiver response is not a JSON object.")

        remote_status = payload.get("status")
        remote_measurement_id = payload.get("measurement_id")
        remote_sha256 = payload.get("annotated_image_sha256")

        if http_status not in (200, 201):
            raise ValueError(f"Unexpected HTTP status: {http_status}")

        if remote_status not in {
            "stored",
            "already_stored",
        }:
            raise ValueError(f"Unexpected receiver status: {remote_status!r}")

        if remote_measurement_id != entry.measurement_id:
            raise ValueError(
                "Receiver ACK measurement ID does not match " "queued measurement."
            )

        if remote_sha256 != entry.annotated_sha256:
            raise ValueError(
                "Receiver ACK SHA-256 does not match " "queued annotated image."
            )

        mark_delivered(
            db_path,
            entry.measurement_id,
            remote_status=remote_status,
            remote_sha256=remote_sha256,
        )

        return DeliveryResult(
            measurement_id=entry.measurement_id,
            success=True,
            http_status=http_status,
            remote_status=remote_status,
            error=None,
        )

    except error.HTTPError as exc:
        try:
            body = exc.read().decode(
                "utf-8",
                errors="replace",
            )
        except Exception:
            body = ""

        message = f"HTTP {exc.code}"

        if body:
            message += f": {body}"

        record_failed_attempt(
            db_path,
            entry.measurement_id,
            message,
        )

        return DeliveryResult(
            measurement_id=entry.measurement_id,
            success=False,
            http_status=exc.code,
            remote_status=None,
            error=message,
        )

    except (
        error.URLError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        message = str(exc)

        record_failed_attempt(
            db_path,
            entry.measurement_id,
            message,
        )

        return DeliveryResult(
            measurement_id=entry.measurement_id,
            success=False,
            http_status=None,
            remote_status=None,
            error=message,
        )


def deliver_pending(
    db_path: Path,
    *,
    receiver_url: str,
    timeout_seconds: float = 5.0,
) -> list[DeliveryResult]:
    """Attempt delivery of all currently pending measurements."""

    results: list[DeliveryResult] = []

    for entry in pending_entries(db_path):
        results.append(
            deliver_entry(
                db_path,
                entry,
                receiver_url=receiver_url,
                timeout_seconds=timeout_seconds,
            )
        )

    return results
