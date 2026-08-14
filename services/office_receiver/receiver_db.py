"""SQLite measurement index for the CaseMetrology office receiver."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3

RECEIVER_ROOT = Path(
    os.environ.get(
        "CASEMETROLOGY_RECEIVER_ROOT",
        r"C:\CaseMetrologyReceiver",
    )
)

DB_PATH = RECEIVER_ROOT / "casemetrology.sqlite3"


def connect_database() -> sqlite3.Connection:
    RECEIVER_ROOT.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=FULL")
    connection.execute("PRAGMA busy_timeout=5000")

    return connection


def initialize_database() -> None:
    with connect_database() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                measurement_id TEXT NOT NULL PRIMARY KEY,

                schema_version TEXT,
                part_id TEXT,

                measurement_characteristic TEXT NOT NULL,
                measurement_status TEXT,

                pipeline_passed INTEGER
                    CHECK (
                        pipeline_passed IS NULL
                        OR pipeline_passed IN (0, 1)
                    ),

                oal_in REAL,
                oal_pixels REAL,
                effective_ppi REAL,
                axis_angle_deg REAL,

                source_image_origin_path TEXT,
                blank_reference_origin_path TEXT,

                source_image_sha256 TEXT,
                annotated_image_sha256 TEXT NOT NULL,
                record_sha256 TEXT NOT NULL,

                git_commit TEXT,
                measurement_timestamp TEXT,
                received_at TEXT NOT NULL,

                record_path TEXT NOT NULL,
                annotated_image_path TEXT NOT NULL,

                receiver_status TEXT NOT NULL,

                line_id TEXT,
                station_id TEXT,
                machine_id TEXT,

                work_order TEXT,
                lot_id TEXT,
                batch_id TEXT,
                cycle_number INTEGER
            )
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_part_id
            ON measurements(part_id)
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_timestamp
            ON measurements(measurement_timestamp)
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_received_at
            ON measurements(received_at)
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_work_order
            ON measurements(work_order)
            """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_measurements_lot_id
            ON measurements(lot_id)
            """)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def index_measurement(
    *,
    record_bytes: bytes,
    image_bytes: bytes,
    record_path: Path,
    image_path: Path,
    receiver_status: str,
) -> str:
    """Insert or verify one received measurement.

    Returns:
        "inserted" if a new database row was created.
        "existing" if the same measurement was already indexed.

    Raises:
        ValueError if an existing measurement_id conflicts with the
        received artifact content.
    """

    initialize_database()

    record = json.loads(record_bytes.decode("utf-8"))

    measurement_id = record.get("measurement_id")

    if not isinstance(measurement_id, str) or not measurement_id:
        raise ValueError("Missing measurement_id")

    characteristic = record.get("measurement_characteristic")

    if not isinstance(characteristic, str) or not characteristic:
        raise ValueError("Missing measurement_characteristic")

    actual_image_hash = sha256_bytes(image_bytes)
    expected_image_hash = record.get("annotated_image_sha256")

    if actual_image_hash != expected_image_hash:
        raise ValueError("Annotated image SHA-256 mismatch")

    record_hash = sha256_bytes(record_bytes)

    pipeline_passed = record.get("pipeline_passed")

    if pipeline_passed is None:
        pipeline_value = None
    else:
        pipeline_value = int(bool(pipeline_passed))

    with connect_database() as connection:
        existing = connection.execute(
            """
            SELECT
                measurement_id,
                annotated_image_sha256,
                record_sha256
            FROM measurements
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

        if existing is not None:
            if (
                existing["annotated_image_sha256"] != actual_image_hash
                or existing["record_sha256"] != record_hash
            ):
                raise ValueError(
                    "Existing database row conflicts with received artifacts"
                )

            return "existing"

        connection.execute(
            """
            INSERT INTO measurements (
                measurement_id,
                schema_version,
                part_id,
                measurement_characteristic,
                measurement_status,
                pipeline_passed,
                oal_in,
                oal_pixels,
                effective_ppi,
                axis_angle_deg,
                source_image_origin_path,
                blank_reference_origin_path,
                source_image_sha256,
                annotated_image_sha256,
                record_sha256,
                git_commit,
                measurement_timestamp,
                received_at,
                record_path,
                annotated_image_path,
                receiver_status,
                line_id,
                station_id,
                machine_id,
                work_order,
                lot_id,
                batch_id,
                cycle_number
            )
            VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                measurement_id,
                str(record.get("schema_version", "")),
                record.get("part_id"),
                characteristic,
                record.get("measurement_status"),
                pipeline_value,
                record.get("oal_in"),
                record.get("oal_pixels"),
                record.get("effective_ppi"),
                record.get("axis_angle_deg"),
                record.get("source_image"),
                record.get("blank_reference"),
                record.get("source_image_sha256"),
                actual_image_hash,
                record_hash,
                record.get("git_commit"),
                record.get("timestamp"),
                datetime.now(timezone.utc).isoformat(),
                str(record_path),
                str(image_path),
                receiver_status,
                record.get("line_id"),
                record.get("station_id"),
                record.get("machine_id"),
                record.get("work_order"),
                record.get("lot_id"),
                record.get("batch_id"),
                record.get("cycle_number"),
            ),
        )

    return "inserted"


if __name__ == "__main__":
    initialize_database()

    with connect_database() as connection:
        row = connection.execute(
            "SELECT COUNT(*) AS count FROM measurements"
        ).fetchone()

    print("CaseMetrology receiver database initialized")
    print(f"Database: {DB_PATH}")
    print(f"Measurement rows: {row['count']}")
    print("part_id nullable: YES")
    print("measurement_id primary key: YES")
