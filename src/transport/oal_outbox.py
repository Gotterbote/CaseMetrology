"""Durable SQLite outbox for locally persisted OAL artifacts.

The local measurement artifacts remain authoritative. Network delivery
state is tracked separately so a failed or interrupted transfer cannot
cause measurement data loss.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3


@dataclass(frozen=True)
class OutboxEntry:
    """One durable OAL artifact delivery record."""

    measurement_id: str
    record_path: str
    annotated_path: str
    record_sha256: str
    annotated_sha256: str
    status: str
    attempt_count: int
    last_error: str | None
    created_at: str
    last_attempt_at: str | None
    delivered_at: str | None
    remote_status: str | None
    remote_sha256: str | None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def _connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_outbox(db_path: Path) -> None:
    """Create the durable outbox database if it does not exist."""

    with _connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS oal_outbox (
                measurement_id TEXT PRIMARY KEY,
                record_path TEXT NOT NULL,
                annotated_path TEXT NOT NULL,
                record_sha256 TEXT NOT NULL,
                annotated_sha256 TEXT NOT NULL,
                status TEXT NOT NULL
                    CHECK (status IN ('pending', 'delivered')),
                attempt_count INTEGER NOT NULL DEFAULT 0,
                last_error TEXT,
                created_at TEXT NOT NULL,
                last_attempt_at TEXT,
                delivered_at TEXT,
                remote_status TEXT,
                remote_sha256 TEXT
            )
            """)


def _row_to_entry(row: sqlite3.Row) -> OutboxEntry:
    return OutboxEntry(
        measurement_id=row["measurement_id"],
        record_path=row["record_path"],
        annotated_path=row["annotated_path"],
        record_sha256=row["record_sha256"],
        annotated_sha256=row["annotated_sha256"],
        status=row["status"],
        attempt_count=row["attempt_count"],
        last_error=row["last_error"],
        created_at=row["created_at"],
        last_attempt_at=row["last_attempt_at"],
        delivered_at=row["delivered_at"],
        remote_status=row["remote_status"],
        remote_sha256=row["remote_sha256"],
    )


def queue_artifact_pair(
    db_path: Path,
    *,
    record_path: Path,
    annotated_path: Path,
) -> OutboxEntry:
    """Register a locally persisted JSON/PNG artifact pair for delivery."""

    if not record_path.is_file():
        raise FileNotFoundError(record_path)

    if not annotated_path.is_file():
        raise FileNotFoundError(annotated_path)

    record = json.loads(record_path.read_text(encoding="utf-8"))

    measurement_id = record.get("measurement_id")

    if not isinstance(measurement_id, str) or not measurement_id:
        raise ValueError("Measurement record has no valid measurement_id.")

    expected_image_hash = record.get("annotated_image_sha256")

    if not isinstance(expected_image_hash, str):
        raise ValueError("Measurement record has no annotated_image_sha256.")

    actual_image_hash = _sha256(annotated_path)

    if actual_image_hash != expected_image_hash:
        raise ValueError("Annotated image SHA-256 does not match measurement record.")

    record_hash = _sha256(record_path)

    record_path = record_path.resolve()
    annotated_path = annotated_path.resolve()

    initialize_outbox(db_path)

    with _connect(db_path) as connection:
        existing = connection.execute(
            """
            SELECT *
            FROM oal_outbox
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

        if existing is not None:
            entry = _row_to_entry(existing)

            if (
                entry.record_sha256 != record_hash
                or entry.annotated_sha256 != actual_image_hash
            ):
                raise ValueError(
                    "Measurement ID already exists with different " "artifact content."
                )

            return entry

        connection.execute(
            """
            INSERT INTO oal_outbox (
                measurement_id,
                record_path,
                annotated_path,
                record_sha256,
                annotated_sha256,
                status,
                attempt_count,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, 'pending', 0, ?)
            """,
            (
                measurement_id,
                str(record_path),
                str(annotated_path),
                record_hash,
                actual_image_hash,
                _utc_now(),
            ),
        )

        row = connection.execute(
            """
            SELECT *
            FROM oal_outbox
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

    if row is None:
        raise RuntimeError("Failed to retrieve newly queued measurement.")

    return _row_to_entry(row)


def get_entry(
    db_path: Path,
    measurement_id: str,
) -> OutboxEntry | None:
    """Return one outbox entry by measurement ID."""

    initialize_outbox(db_path)

    with _connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT *
            FROM oal_outbox
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

    return None if row is None else _row_to_entry(row)


def pending_entries(
    db_path: Path,
) -> list[OutboxEntry]:
    """Return pending entries in creation order."""

    initialize_outbox(db_path)

    with _connect(db_path) as connection:
        rows = connection.execute("""
            SELECT *
            FROM oal_outbox
            WHERE status = 'pending'
            ORDER BY created_at, measurement_id
            """).fetchall()

    return [_row_to_entry(row) for row in rows]


def record_failed_attempt(
    db_path: Path,
    measurement_id: str,
    error: str,
) -> None:
    """Record a failed delivery attempt while leaving the item pending."""

    initialize_outbox(db_path)

    with _connect(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE oal_outbox
            SET attempt_count = attempt_count + 1,
                last_attempt_at = ?,
                last_error = ?
            WHERE measurement_id = ?
              AND status = 'pending'
            """,
            (
                _utc_now(),
                error,
                measurement_id,
            ),
        )

        if cursor.rowcount != 1:
            raise ValueError(f"No pending outbox entry: {measurement_id}")


def mark_delivered(
    db_path: Path,
    measurement_id: str,
    *,
    remote_status: str,
    remote_sha256: str,
) -> None:
    """Mark an artifact pair delivered after a verified receiver ACK."""

    initialize_outbox(db_path)

    with _connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT annotated_sha256, status
            FROM oal_outbox
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

        if row is None:
            raise ValueError(f"Unknown outbox measurement: {measurement_id}")

        if remote_sha256 != row["annotated_sha256"]:
            raise ValueError("Receiver SHA-256 does not match queued artifact.")

        if row["status"] == "delivered":
            return

        connection.execute(
            """
            UPDATE oal_outbox
            SET status = 'delivered',
                attempt_count = attempt_count + 1,
                last_attempt_at = ?,
                last_error = NULL,
                delivered_at = ?,
                remote_status = ?,
                remote_sha256 = ?
            WHERE measurement_id = ?
            """,
            (
                _utc_now(),
                _utc_now(),
                remote_status,
                remote_sha256,
                measurement_id,
            ),
        )
