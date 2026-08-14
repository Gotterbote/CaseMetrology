# CaseMetrology Office Receiver

The CaseMetrology office receiver accepts validated measurement artifact
packets from the Jetson measurement system and stores them durably on the
office computer.

Each received measurement consists of:

- `record.json`
- `annotated.png`

The receiver verifies the annotated-image SHA-256, stores the artifact pair,
indexes the measurement in SQLite, and only then returns a successful
acknowledgement to the Jetson.

## Architecture

Jetson measurement system:

1. captures and measures the specimen;
2. saves the measurement artifacts locally;
3. registers the artifact pair in the durable SQLite outbox;
4. sends the packet to the office receiver.

Office receiver:

1. receives the packet;
2. validates the ZIP contents;
3. validates the JSON record;
4. verifies the annotated-image SHA-256;
5. stores the JSON and PNG;
6. indexes the measurement in SQLite;
7. returns a verified acknowledgement.

A duplicate transmission with identical content is treated as
`already_stored` and does not create duplicate files or database rows.

## Measurement Identity

`measurement_id` is the authoritative unique identifier and is required.

`part_id` is optional.

This supports both research and production use:

Research:

    measurement_id = unique measurement event
    part_id = laser-etched specimen ID

Production:

    measurement_id = unique machine/cycle measurement event
    part_id = NULL

Production traceability can instead use available process context such as:

- line ID;
- station ID;
- machine ID;
- work order;
- lot ID;
- batch ID; and
- cycle number.

## Default Configuration

Receiver root:

    C:\CaseMetrologyReceiver

Receiver host:

    100.71.13.87

Receiver port:

    8766

Received artifacts:

    C:\CaseMetrologyReceiver\received\<measurement_id>\

Database:

    C:\CaseMetrologyReceiver\casemetrology.sqlite3

## Environment Overrides

The defaults may be changed without modifying source code.

PowerShell example:

    $env:CASEMETROLOGY_RECEIVER_ROOT = "D:\CaseMetrology"
    $env:CASEMETROLOGY_RECEIVER_HOST = "100.x.x.x"
    $env:CASEMETROLOGY_RECEIVER_PORT = "8766"

## Startup

From the receiver directory:

    python receiver.py

Expected startup output:

    CaseMetrology receiver listening on http://<host>:<port>
    Storage root: <receiver-root>\received
    SQLite indexing: ENABLED

## Health Check

From another computer:

    curl http://<host>:<port>/health

Expected response:

    {
      "status": "ok",
      "service": "CaseMetrologyReceiver",
      "database": "enabled"
    }

## SQLite Schema

The `measurements` table uses:

    measurement_id TEXT NOT NULL PRIMARY KEY

`part_id` is nullable by design.

The database stores measurement metadata and paths to the stored artifact
files. PNG files are not stored as SQLite BLOBs.

## Durability

SQLite uses:

- WAL journal mode;
- `synchronous=FULL`;
- a 5-second busy timeout.

The Jetson remains authoritative for locally generated measurement artifacts
until remote delivery is acknowledged.

A receiver acknowledgement is returned only after the artifact files and
SQLite measurement row have been successfully stored or verified as already
existing.

## Current Status

The receiver has been verified for:

- successful new measurement storage;
- SHA-256 verification;
- duplicate retry handling;
- idempotent SQLite indexing;
- persistence across receiver restarts;
- research records containing `part_id`; and
- production-style records with `part_id = NULL`.


## Automatic Startup

The receiver can be registered with Windows Task Scheduler using:

    powershell -ExecutionPolicy Bypass -File install_task.ps1

The installer:

- uses the currently logged-in Windows account;
- discovers the active Python executable unless one is supplied;
- starts the receiver at user logon;
- prevents duplicate receiver instances;
- retries the task after unexpected termination; and
- removes the normal Task Scheduler execution-time limit.

Optional parameters include:

    -ReceiverRoot
    -TaskName
    -PythonPath

Example:

    powershell -ExecutionPolicy Bypass -File install_task.ps1 `
        -ReceiverRoot "C:\CaseMetrologyReceiver"
