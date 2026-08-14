"""Integrated production workflow for one OAL measurement cycle.

Sequence:
    1. Run the frozen OAL measurement pipeline.
    2. Persist annotated PNG and JSON locally.
    3. Register the artifact pair in the durable SQLite outbox.
    4. Optionally attempt remote delivery.

Local persistence is authoritative. A network failure leaves the
measurement queued for later retry and does not erase or invalidate it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from src.diagnostics.oal_measurement_artifacts import (
    save_oal_measurement_artifacts,
)
from src.measurement.topdown_oal_pipeline import (
    TopDownOALPipelineResult,
    measure_topdown_oal_image,
)
from src.transport.oal_outbox import (
    OutboxEntry,
    get_entry,
    queue_artifact_pair,
)
from src.transport.oal_sender import (
    DeliveryResult,
    deliver_entry,
)

GrayImage = NDArray[np.uint8]


@dataclass(frozen=True)
class OALProductionCycleResult:
    """Outcome of one integrated OAL production cycle."""

    measurement: TopDownOALPipelineResult
    annotated_path: Path
    record_path: Path
    outbox_entry: OutboxEntry
    delivery: DeliveryResult | None


def run_oal_production_cycle(
    *,
    blank: GrayImage,
    image: GrayImage,
    source_image_path: Path,
    blank_reference_path: Path,
    artifact_root: Path,
    outbox_db_path: Path,
    part_id: str,
    measurement_id: str,
    receiver_url: str | None = None,
    timestamp: datetime | None = None,
    timeout_seconds: float = 5.0,
) -> OALProductionCycleResult:
    """Run one measurement through persistence, queueing, and delivery."""

    measurement = measure_topdown_oal_image(
        blank,
        image,
    )

    annotated_path, record_path = save_oal_measurement_artifacts(
        image=image,
        source_image_path=source_image_path,
        blank_reference_path=blank_reference_path,
        result=measurement,
        output_root=artifact_root,
        part_id=part_id,
        measurement_id=measurement_id,
        timestamp=timestamp,
    )

    outbox_entry = queue_artifact_pair(
        outbox_db_path,
        record_path=record_path,
        annotated_path=annotated_path,
    )

    delivery: DeliveryResult | None = None

    if receiver_url is not None and outbox_entry.status == "pending":
        delivery = deliver_entry(
            outbox_db_path,
            outbox_entry,
            receiver_url=receiver_url,
            timeout_seconds=timeout_seconds,
        )

        refreshed = get_entry(
            outbox_db_path,
            measurement_id,
        )

        if refreshed is None:
            raise RuntimeError("Outbox entry disappeared after delivery attempt.")

        outbox_entry = refreshed

    return OALProductionCycleResult(
        measurement=measurement,
        annotated_path=annotated_path,
        record_path=record_path,
        outbox_entry=outbox_entry,
        delivery=delivery,
    )
