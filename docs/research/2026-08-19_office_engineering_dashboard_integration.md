# CaseMetrology Office Engineering Dashboard Integration

**Date:** 2026-08-19  
**Subsystem:** Networked metrology data and engineering visualization  
**Status:** Supporting integration development; not part of frozen dimensional computation

## Purpose

This increment adds a read-only engineering dashboard for measurement artifacts
already persisted by the CaseMetrology Windows office receiver.

The dashboard does not perform dimensional measurement and does not modify:

- the frozen segmentation implementation;
- the PCA/extreme-mask OAL estimator;
- the spatial calibration models;
- the Jetson measurement artifact;
- the Jetson durable delivery outbox; or
- existing rows in the office measurement database.

The Jetson-side locally persisted artifacts remain the authoritative originals.

## Existing verified architecture retained

The existing implementation already provides:

1. local Jetson artifact persistence;
2. SHA-256 integrity checks before queueing;
3. durable SQLite outbox storage;
4. HTTP transfer to the office receiver;
5. receiver-side annotated-image SHA-256 verification;
6. durable file storage;
7. SQLite indexing;
8. idempotent duplicate handling; and
9. verified acknowledgment before the Jetson marks an item delivered.

This dashboard consumes the resulting office-side database and images without
changing the transport contract.

## Dashboard implementation

`services/office_receiver/dashboard.py`

The service uses only the Python standard library. By default it listens on:

`http://127.0.0.1:8767`

The default loopback binding intentionally limits the dashboard to the office
computer unless the operator explicitly changes
`CASEMETROLOGY_DASHBOARD_HOST`.

The dashboard exposes:

- `/` and `/dashboard` — browser dashboard;
- `/health` — dashboard-service health;
- `/api/status` — receiver health, counts, aggregate valid-OAL information,
  last packet age, and latest measurement;
- `/api/recent?limit=N` — recent measurements;
- `/image/<measurement_id>` — the annotated image indexed by the existing
  office database.

The service opens SQLite connections with `PRAGMA query_only=ON`.

## Displayed information

The first version displays:

- receiver service health;
- stored measurement count;
- mean and sample standard deviation of stored valid OAL values;
- age of the most recently received packet;
- latest annotated image;
- latest part/measurement identifier;
- OAL and measurement status;
- pipeline status;
- effective PPI;
- axis angle;
- measurement and receipt timestamps;
- receiver status;
- associated Git commit; and
- a recent-measurement table.

A two-second browser refresh interval is used for the prototype.

## Deliberate exclusions

The first dashboard increment does not display the Jetson pending-queue count
because that state currently exists only in the Jetson outbox. No new telemetry
contract is introduced merely to populate a dashboard field.

The architecture requirement already qualifies pending queue count as
"when available." A later integration increment may add read-only Jetson
transport telemetry without changing measurement semantics.

The dashboard also contains no commands for:

- changing calibration;
- changing quality gates;
- modifying segmentation;
- changing the OAL estimator;
- editing measurement records;
- deleting measurements;
- changing formal-validation status; or
- forcing retransmission.

## Receiver health

The dashboard checks the existing receiver `/health` endpoint separately from
the age of the most recently received packet. This avoids treating a quiet
measurement period as a communication failure.

## Research interpretation

This subsystem is supporting systems-engineering infrastructure. It demonstrates
that measurement computation, local persistence, network delivery, remote
storage, and human visualization are separated concerns.

A network or office-dashboard outage cannot change an already computed OAL
measurement and does not remove the locally persisted Jetson artifact.

Formal validation conclusions remain based on the frozen measurement system
and formal validation records, not on dashboard operation.

## Verification

Automated tests verify:

- latest/recent measurement queries;
- database reads do not alter measurement row count;
- aggregate mean and sample standard deviation;
- annotated-image lookup through the database index.

A later live Windows verification should additionally confirm:

1. the receiver task is running;
2. `http://127.0.0.1:8766/health` returns healthy status;
3. the dashboard task is running;
4. `http://127.0.0.1:8767/health` returns healthy status;
5. the dashboard renders the latest previously stored measurement;
6. a new Jetson measurement appears without manual refresh;
7. the displayed annotated image matches the stored artifact;
8. stopping the receiver changes receiver health to DOWN without altering
   stored measurements; and
9. restarting the receiver restores health.

## Thesis use

The implementation may support a Chapter 3 subsection describing networked
data persistence and engineering monitoring. It should remain explicitly
separate from the dimensional measurement algorithm and primary validation
method.
