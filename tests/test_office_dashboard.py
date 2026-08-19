"""Tests for the read-only CaseMetrology office engineering dashboard."""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
from pathlib import Path
import sqlite3
import sys

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "services"
    / "office_receiver"
    / "dashboard.py"
)

SPEC = importlib.util.spec_from_file_location(
    "casemetrology_office_dashboard",
    MODULE_PATH,
)
assert SPEC is not None and SPEC.loader is not None
dashboard = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dashboard
SPEC.loader.exec_module(dashboard)


def _make_db(tmp_path: Path) -> Path:
    db_path = tmp_path / "casemetrology.sqlite3"

    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE measurements (
                measurement_id TEXT PRIMARY KEY,
                schema_version TEXT,
                part_id TEXT,
                measurement_characteristic TEXT NOT NULL,
                measurement_status TEXT,
                pipeline_passed INTEGER,
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

    return db_path


def _insert_measurement(
    db_path: Path,
    *,
    measurement_id: str,
    oal_in: float,
    received_at: str,
    image_path: Path,
) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            """
            INSERT INTO measurements (
                measurement_id,
                part_id,
                measurement_characteristic,
                measurement_status,
                pipeline_passed,
                oal_in,
                annotated_image_sha256,
                record_sha256,
                git_commit,
                measurement_timestamp,
                received_at,
                record_path,
                annotated_image_path,
                receiver_status
            )
            VALUES (?, ?, 'OAL', 'valid', 1, ?, ?, ?, ?, ?, ?, ?, ?, 'stored')
            """,
            (
                measurement_id,
                measurement_id.replace("measurement-", ""),
                oal_in,
                "imagehash",
                "recordhash",
                "abc1234",
                received_at,
                received_at,
                str(image_path.with_suffix(".json")),
                str(image_path),
            ),
        )


def test_latest_and_recent_measurements_are_read_only(tmp_path: Path) -> None:
    db_path = _make_db(tmp_path)
    image1 = tmp_path / "1.png"
    image2 = tmp_path / "2.png"
    image1.write_bytes(b"one")
    image2.write_bytes(b"two")

    _insert_measurement(
        db_path,
        measurement_id="measurement-001",
        oal_in=1.000,
        received_at="2026-08-19T20:00:00+00:00",
        image_path=image1,
    )
    _insert_measurement(
        db_path,
        measurement_id="measurement-002",
        oal_in=1.002,
        received_at="2026-08-19T20:01:00+00:00",
        image_path=image2,
    )

    latest = dashboard.latest_measurement(db_path)
    recent = dashboard.recent_measurements(db_path, limit=10)

    assert latest is not None
    assert latest["measurement_id"] == "measurement-002"
    assert [row["measurement_id"] for row in recent] == [
        "measurement-002",
        "measurement-001",
    ]

    with sqlite3.connect(db_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]

    assert count == 2


def test_summary_calculates_sample_sd(tmp_path: Path) -> None:
    db_path = _make_db(tmp_path)

    for index, value in enumerate((0.999, 1.000, 1.001), 1):
        image = tmp_path / f"{index}.png"
        image.write_bytes(b"x")
        _insert_measurement(
            db_path,
            measurement_id=f"measurement-{index:03d}",
            oal_in=value,
            received_at=f"2026-08-19T20:0{index}:00+00:00",
            image_path=image,
        )

    summary = dashboard.measurement_summary(db_path)

    assert summary["measurement_count"] == 3
    assert summary["valid_oal_count"] == 3
    assert abs(summary["valid_oal_mean_in"] - 1.000) < 1e-12
    assert abs(summary["valid_oal_sd_in"] - 0.001) < 1e-12


def test_image_path_is_resolved_from_database(tmp_path: Path) -> None:
    db_path = _make_db(tmp_path)
    image = tmp_path / "annotated.png"
    image.write_bytes(b"png")

    _insert_measurement(
        db_path,
        measurement_id="measurement-001",
        oal_in=1.000,
        received_at=datetime.now(timezone.utc).isoformat(),
        image_path=image,
    )

    assert (
        dashboard.annotated_image_path(
            "measurement-001",
            db_path,
        )
        == image
    )

    assert (
        dashboard.annotated_image_path(
            "missing",
            db_path,
        )
        is None
    )
