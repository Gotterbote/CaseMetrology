"""CaseMetrology office artifact receiver."""

from __future__ import annotations

import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

from receiver_db import (
    RECEIVER_ROOT,
    index_measurement,
    initialize_database,
)

HOST = os.environ.get(
    "CASEMETROLOGY_RECEIVER_HOST",
    "100.71.13.87",
)

PORT = int(
    os.environ.get(
        "CASEMETROLOGY_RECEIVER_PORT",
        "8766",
    )
)

ROOT = RECEIVER_ROOT / "received"
MAX_BODY_BYTES = 25 * 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class ReceiverHandler(BaseHTTPRequestHandler):
    def _reply(
        self,
        status: int,
        payload: dict[str, object],
    ) -> None:
        body = json.dumps(
            payload,
            indent=2,
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._reply(
                200,
                {
                    "status": "ok",
                    "service": "CaseMetrologyReceiver",
                    "database": "enabled",
                },
            )
            return

        self._reply(
            404,
            {"error": "not found"},
        )

    def do_POST(self) -> None:
        if self.path != "/measurements":
            self._reply(
                404,
                {"error": "not found"},
            )
            return

        try:
            length = int(
                self.headers.get(
                    "Content-Length",
                    "0",
                )
            )
        except ValueError:
            self._reply(
                400,
                {"error": "invalid Content-Length"},
            )
            return

        if length <= 0 or length > MAX_BODY_BYTES:
            self._reply(
                413,
                {"error": ("invalid or excessive " "request size")},
            )
            return

        body = self.rfile.read(length)

        try:
            with tempfile.TemporaryDirectory() as temp_name:
                temp_dir = Path(temp_name)
                packet_path = temp_dir / "packet.zip"
                packet_path.write_bytes(body)

                with zipfile.ZipFile(
                    packet_path,
                    "r",
                ) as archive:
                    names = set(archive.namelist())

                    if names != {
                        "record.json",
                        "annotated.png",
                    }:
                        raise ValueError(
                            "Packet must contain exactly "
                            "record.json and annotated.png"
                        )

                    record_bytes = archive.read("record.json")
                    image_bytes = archive.read("annotated.png")

                record = json.loads(record_bytes.decode("utf-8"))

                measurement_id = record.get("measurement_id")

                if (
                    not isinstance(
                        measurement_id,
                        str,
                    )
                    or not measurement_id
                ):
                    raise ValueError("Missing measurement_id")

                expected_hash = record.get("annotated_image_sha256")

                actual_hash = sha256_bytes(image_bytes)

                if expected_hash != actual_hash:
                    self._reply(
                        422,
                        {
                            "status": "rejected",
                            "measurement_id": (measurement_id),
                            "reason": ("annotated image " "SHA-256 mismatch"),
                            "expected": expected_hash,
                            "actual": actual_hash,
                        },
                    )
                    return

                destination = ROOT / measurement_id

                record_destination = destination / "record.json"

                image_destination = destination / "annotated.png"

                # --------------------------------------------------
                # Existing filesystem measurement.
                #
                # Verify that it is exactly the same artifact pair,
                # ensure the SQLite row exists, then ACK safely.
                # --------------------------------------------------

                if destination.exists():
                    if (
                        not record_destination.is_file()
                        or not image_destination.is_file()
                    ):
                        self._reply(
                            409,
                            {
                                "status": "conflict",
                                "measurement_id": (measurement_id),
                                "reason": ("existing destination " "is incomplete"),
                            },
                        )
                        return

                    stored_record_bytes = record_destination.read_bytes()

                    stored_image_bytes = image_destination.read_bytes()

                    if (
                        stored_record_bytes != record_bytes
                        or stored_image_bytes != image_bytes
                    ):
                        self._reply(
                            409,
                            {
                                "status": "conflict",
                                "measurement_id": (measurement_id),
                                "reason": (
                                    "measurement ID already "
                                    "exists with different "
                                    "artifact content"
                                ),
                            },
                        )
                        return

                    index_measurement(
                        record_bytes=stored_record_bytes,
                        image_bytes=stored_image_bytes,
                        record_path=record_destination,
                        image_path=image_destination,
                        receiver_status=("already_stored"),
                    )

                    self._reply(
                        200,
                        {
                            "status": "already_stored",
                            "measurement_id": (measurement_id),
                            "annotated_image_sha256": (actual_hash),
                        },
                    )
                    return

                # --------------------------------------------------
                # New measurement.
                #
                # Persist files first. Only ACK after SQLite indexing
                # also succeeds.
                # --------------------------------------------------

                staging = ROOT / (f".{measurement_id}.staging")

                if staging.exists():
                    shutil.rmtree(staging)

                staging.mkdir(
                    parents=True,
                    exist_ok=False,
                )

                (staging / "record.json").write_bytes(record_bytes)

                (staging / "annotated.png").write_bytes(image_bytes)

                ROOT.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                staging.replace(destination)

                index_measurement(
                    record_bytes=record_bytes,
                    image_bytes=image_bytes,
                    record_path=record_destination,
                    image_path=image_destination,
                    receiver_status="stored",
                )

                self._reply(
                    201,
                    {
                        "status": "stored",
                        "measurement_id": (measurement_id),
                        "annotated_image_sha256": (actual_hash),
                    },
                )

        except (
            ValueError,
            json.JSONDecodeError,
            zipfile.BadZipFile,
        ) as exc:
            self._reply(
                400,
                {
                    "status": "rejected",
                    "reason": str(exc),
                },
            )

        except Exception as exc:
            self._reply(
                500,
                {
                    "status": "error",
                    "reason": str(exc),
                },
            )


if __name__ == "__main__":
    ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    initialize_database()

    server = ThreadingHTTPServer(
        (HOST, PORT),
        ReceiverHandler,
    )

    print("CaseMetrology receiver listening on " f"http://{HOST}:{PORT}")
    print(f"Storage root: {ROOT}")
    print("SQLite indexing: ENABLED")

    server.serve_forever()
