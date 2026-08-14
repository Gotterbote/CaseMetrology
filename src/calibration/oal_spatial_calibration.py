"""Frozen spatial/directional calibration for cartridge-case OAL.

The calibration planes retain their historical PPI_0 and PPI_90 names from
the gauge-block acquisition conditions.

The gauge-block analyzer reports the gauge block's long-axis orientation while
measuring the certified short dimension perpendicular to that axis. Therefore,
for cartridge-case OAL, whose reported PCA angle is the measurement direction
itself, the historical principal-direction calibration labels map as follows:

    horizontal case OAL -> PPI_90
    vertical case OAL   -> PPI_0

This convention is documented in:
docs/research/2026-08-13_oal_calibration_angle_convention_correction.md
"""

from __future__ import annotations

from dataclasses import dataclass
import math

PPI_0_INTERCEPT = 516.907045
PPI_0_X_COEFFICIENT = 0.00843326411
PPI_0_Y_COEFFICIENT = 0.000817091863

PPI_90_INTERCEPT = 518.408825
PPI_90_X_COEFFICIENT = 0.00322556849
PPI_90_Y_COEFFICIENT = 0.00442714650


@dataclass(frozen=True)
class OALSpatialCalibrationResult:
    """Resolved spatial/directional calibration for one OAL measurement."""

    centroid_x_px: float
    centroid_y_px: float
    angle_degrees: float
    ppi_0: float
    ppi_90: float
    effective_ppi: float


def ppi_0_at(x_px: float, y_px: float) -> float:
    """Evaluate the historical gauge-block 0-degree calibration plane."""

    return PPI_0_INTERCEPT + PPI_0_X_COEFFICIENT * x_px + PPI_0_Y_COEFFICIENT * y_px


def ppi_90_at(x_px: float, y_px: float) -> float:
    """Evaluate the historical gauge-block 90-degree calibration plane."""

    return PPI_90_INTERCEPT + PPI_90_X_COEFFICIENT * x_px + PPI_90_Y_COEFFICIENT * y_px


def resolve_oal_spatial_calibration(
    x_px: float,
    y_px: float,
    angle_degrees: float,
) -> OALSpatialCalibrationResult:
    """Resolve effective PPI for a cartridge-case OAL measurement direction."""

    values = (x_px, y_px, angle_degrees)

    if not all(math.isfinite(value) for value in values):
        raise ValueError("Calibration position and angle must be finite.")

    ppi_0 = ppi_0_at(x_px, y_px)
    ppi_90 = ppi_90_at(x_px, y_px)

    theta = math.radians(angle_degrees)

    # Historical gauge-block labels are rotated 90 degrees relative to the
    # certified short-dimension measurement direction.
    effective_ppi = math.hypot(
        ppi_90 * math.cos(theta),
        ppi_0 * math.sin(theta),
    )

    if not math.isfinite(effective_ppi) or effective_ppi <= 0.0:
        raise ValueError("Resolved effective pixels-per-inch must be positive.")

    return OALSpatialCalibrationResult(
        centroid_x_px=float(x_px),
        centroid_y_px=float(y_px),
        angle_degrees=float(angle_degrees),
        ppi_0=float(ppi_0),
        ppi_90=float(ppi_90),
        effective_ppi=float(effective_ppi),
    )
