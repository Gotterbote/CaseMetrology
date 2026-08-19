"""Read-only engineering dashboard for CaseMetrology office measurements.

This service reads the existing office receiver SQLite database and received
annotated images. It does not modify measurement rows, calibration, the Jetson
outbox, or the frozen OAL measurement implementation.
"""

from __future__ import annotations

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import sqlite3
from urllib import error, parse, request

RECEIVER_ROOT = Path(
    os.environ.get(
        "CASEMETROLOGY_RECEIVER_ROOT",
        r"C:\CaseMetrologyReceiver",
    )
)
DB_PATH = RECEIVER_ROOT / "casemetrology.sqlite3"

HOST = os.environ.get(
    "CASEMETROLOGY_DASHBOARD_HOST",
    "127.0.0.1",
)
PORT = int(
    os.environ.get(
        "CASEMETROLOGY_DASHBOARD_PORT",
        "8767",
    )
)
RECEIVER_HEALTH_URL = os.environ.get(
    "CASEMETROLOGY_RECEIVER_HEALTH_URL",
    "http://127.0.0.1:8766/health",
)

MAX_RECENT = 100

DASHBOARD_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CaseMetrology Engineering Dashboard</title>
<style>
:root { color-scheme: dark; font-family: Arial, Helvetica, sans-serif; }
body { margin: 0; background: #111418; color: #e7ebef; }
header { padding: 18px 22px; border-bottom: 1px solid #2c333a; }
h1 { margin: 0; font-size: 1.35rem; }
.sub { color: #9ba7b3; margin-top: 5px; font-size: .9rem; }
main { padding: 18px; max-width: 1450px; margin: 0 auto; }
.grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit,minmax(210px,1fr)); }
.card { background: #181d22; border: 1px solid #2b333b; border-radius: 10px; padding: 14px; }
.label { color: #9ba7b3; font-size: .78rem; text-transform: uppercase; letter-spacing: .06em; }
.value { font-size: 1.45rem; margin-top: 6px; font-weight: 600; }
.ok { color: #76d69a; }
.bad { color: #ff8a8a; }
.warn { color: #ffd27a; }
.latest { display: grid; grid-template-columns: minmax(280px,1fr) minmax(320px,1fr); gap: 14px; margin-top: 14px; }
img { width: 100%; max-height: 520px; object-fit: contain; background: #0c0f12; border-radius: 8px; }
dl { display: grid; grid-template-columns: 160px 1fr; gap: 7px 12px; }
dt { color: #9ba7b3; }
dd { margin: 0; overflow-wrap: anywhere; }
table { width: 100%; border-collapse: collapse; font-size: .88rem; }
th, td { padding: 8px 7px; border-bottom: 1px solid #2a3138; text-align: left; }
th { color: #aeb8c2; }
.scroll { overflow-x: auto; margin-top: 14px; }
small { color: #9ba7b3; }
@media (max-width: 800px) { .latest { grid-template-columns: 1fr; } dl { grid-template-columns: 125px 1fr; } }
</style>
</head>
<body>
<header>
  <h1>CaseMetrology Engineering Dashboard</h1>
  <div class="sub">Read-only office view. Jetson measurement artifacts remain authoritative.</div>
</header>
<main>
  <div class="grid">
    <div class="card"><div class="label">Receiver service</div><div id="receiver" class="value">…</div></div>
    <div class="card"><div class="label">Stored measurements</div><div id="count" class="value">…</div></div>
    <div class="card"><div class="label">Mean valid OAL</div><div id="mean" class="value">…</div></div>
    <div class="card"><div class="label">Valid OAL SD</div><div id="sd" class="value">…</div></div>
    <div class="card"><div class="label">Last packet received</div><div id="last" class="value">…</div></div>
  </div>

  <div class="latest">
    <div class="card">
      <div class="label">Latest annotated image</div>
      <div style="margin-top:10px"><img id="image" alt="No annotated image available"></div>
    </div>
    <div class="card">
      <div class="label">Latest measurement</div>
      <dl id="details"><dt>Status</dt><dd>Loading…</dd></dl>
    </div>
  </div>

  <div class="card scroll">
    <div class="label" style="margin-bottom:8px">Recent measurements</div>
    <table>
      <thead>
        <tr>
          <th>Timestamp</th><th>Part</th><th>OAL (in)</th><th>Status</th>
          <th>Measurement ID</th><th>Git commit</th>
        </tr>
      </thead>
      <tbody id="recent"></tbody>
    </table>
  </div>
  <p><small>Dashboard refresh: 2 s. No control or write operations are exposed.</small></p>
</main>
<script>
function esc(v) {
  return String(v ?? "").replace(/[&<>"']/g, c => (
    {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]
  ));
}
function fmtNum(v, digits=6) {
  return (v === null || v === undefined) ? "—" : Number(v).toFixed(digits);
}
function ageText(seconds) {
  if (seconds === null || seconds === undefined) return "No packets";
  if (seconds < 60) return `${Math.round(seconds)} s ago`;
  if (seconds < 3600) return `${Math.round(seconds/60)} min ago`;
  return `${(seconds/3600).toFixed(1)} h ago`;
}
async function refresh() {
  try {
    const [statusResp, recentResp] = await Promise.all([
      fetch("/api/status", {cache:"no-store"}),
      fetch("/api/recent?limit=25", {cache:"no-store"})
    ]);
    const s = await statusResp.json();
    const recent = await recentResp.json();

    const receiver = document.getElementById("receiver");
    receiver.textContent = s.receiver_health === "up" ? "UP" : "DOWN";
    receiver.className = "value " + (s.receiver_health === "up" ? "ok" : "bad");

    document.getElementById("count").textContent = s.measurement_count ?? "0";
    document.getElementById("mean").textContent =
      s.valid_oal_mean_in == null ? "—" : fmtNum(s.valid_oal_mean_in);
    document.getElementById("sd").textContent =
      s.valid_oal_sd_in == null ? "—" : fmtNum(s.valid_oal_sd_in);
    document.getElementById("last").textContent = ageText(s.last_packet_age_seconds);

    const latest = s.latest;
    const details = document.getElementById("details");
    const image = document.getElementById("image");

    if (!latest) {
      details.innerHTML = "<dt>Status</dt><dd>No measurements stored</dd>";
      image.removeAttribute("src");
    } else {
      const fields = [
        ["Measurement ID", latest.measurement_id],
        ["Part ID", latest.part_id],
        ["Characteristic", latest.measurement_characteristic],
        ["Measurement status", latest.measurement_status],
        ["Pipeline passed", latest.pipeline_passed],
        ["OAL", latest.oal_in == null ? "—" : `${fmtNum(latest.oal_in)} in`],
        ["Effective PPI", latest.effective_ppi],
        ["Axis angle", latest.axis_angle_deg],
        ["Measured at", latest.measurement_timestamp],
        ["Received at", latest.received_at],
        ["Receiver status", latest.receiver_status],
        ["Git commit", latest.git_commit]
      ];
      details.innerHTML = fields.map(([k,v]) =>
        `<dt>${esc(k)}</dt><dd>${esc(v ?? "—")}</dd>`
      ).join("");
      image.src = `/image/${encodeURIComponent(latest.measurement_id)}`;
    }

    const tbody = document.getElementById("recent");
    tbody.innerHTML = (recent.measurements || []).map(r => `
      <tr>
        <td>${esc(r.measurement_timestamp ?? r.received_at ?? "—")}</td>
        <td>${esc(r.part_id ?? "—")}</td>
        <td>${esc(r.oal_in == null ? "—" : fmtNum(r.oal_in))}</td>
        <td>${esc(r.measurement_status ?? "—")}</td>
        <td>${esc(r.measurement_id)}</td>
        <td>${esc(r.git_commit ?? "—")}</td>
      </tr>`).join("");
  } catch (e) {
    const receiver = document.getElementById("receiver");
    receiver.textContent = "DASHBOARD ERROR";
    receiver.className = "value bad";
  }
}
refresh();
setInterval(refresh, 2000);
</script>
</body>
</html>
"""


def _connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")
    connection.execute("PRAGMA busy_timeout=5000")
    return connection


def _row_dict(row: sqlite3.Row | None) -> dict[str, object] | None:
    if row is None:
        return None
    return dict(row)


def latest_measurement(db_path: Path = DB_PATH) -> dict[str, object] | None:
    """Return the most recently received measurement without modifying the DB."""

    if not db_path.is_file():
        return None

    with _connect(db_path) as connection:
        row = connection.execute("""
            SELECT *
            FROM measurements
            ORDER BY received_at DESC, measurement_id DESC
            LIMIT 1
            """).fetchone()

    return _row_dict(row)


def recent_measurements(
    db_path: Path = DB_PATH,
    *,
    limit: int = 25,
) -> list[dict[str, object]]:
    """Return recent measurements in reverse receipt order."""

    if not db_path.is_file():
        return []

    limit = max(1, min(int(limit), MAX_RECENT))

    with _connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM measurements
            ORDER BY received_at DESC, measurement_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def measurement_summary(db_path: Path = DB_PATH) -> dict[str, object]:
    """Return read-only aggregate information for engineering display."""

    if not db_path.is_file():
        return {
            "measurement_count": 0,
            "valid_oal_count": 0,
            "valid_oal_mean_in": None,
            "valid_oal_sd_in": None,
        }

    with _connect(db_path) as connection:
        count_row = connection.execute(
            "SELECT COUNT(*) AS count FROM measurements"
        ).fetchone()

        oal_rows = connection.execute("""
            SELECT oal_in
            FROM measurements
            WHERE oal_in IS NOT NULL
              AND (
                    measurement_status IS NULL
                    OR LOWER(measurement_status) IN ('valid', 'pass', 'accepted')
                  )
            """).fetchall()

    values = [float(row["oal_in"]) for row in oal_rows]
    mean = None
    sd = None

    if values:
        mean = sum(values) / len(values)

    if len(values) >= 2:
        variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
        sd = math.sqrt(variance)

    return {
        "measurement_count": int(count_row["count"]) if count_row else 0,
        "valid_oal_count": len(values),
        "valid_oal_mean_in": mean,
        "valid_oal_sd_in": sd,
    }


def _parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None

    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.astimezone(timezone.utc)


def _packet_age_seconds(latest: dict[str, object] | None) -> float | None:
    if latest is None:
        return None

    timestamp = _parse_timestamp(latest.get("received_at"))
    if timestamp is None:
        return None

    return max(
        0.0,
        (datetime.now(timezone.utc) - timestamp).total_seconds(),
    )


def receiver_health(
    health_url: str = RECEIVER_HEALTH_URL,
    *,
    timeout_seconds: float = 1.0,
) -> str:
    """Return 'up' only when the receiver health endpoint answers successfully."""

    try:
        with request.urlopen(health_url, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if response.status == 200 and payload.get("status") == "ok":
            return "up"
    except (
        error.URLError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ):
        pass

    return "down"


def status_payload(
    db_path: Path = DB_PATH,
    *,
    health_url: str = RECEIVER_HEALTH_URL,
) -> dict[str, object]:
    latest = latest_measurement(db_path)
    payload = measurement_summary(db_path)
    payload.update(
        {
            "service": "CaseMetrologyEngineeringDashboard",
            "dashboard_status": "ok",
            "receiver_health": receiver_health(health_url),
            "last_packet_age_seconds": _packet_age_seconds(latest),
            "latest": latest,
        }
    )
    return payload


def annotated_image_path(
    measurement_id: str,
    db_path: Path = DB_PATH,
) -> Path | None:
    """Resolve an image path only through the trusted database index."""

    if not measurement_id or not db_path.is_file():
        return None

    with _connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT annotated_image_path
            FROM measurements
            WHERE measurement_id = ?
            """,
            (measurement_id,),
        ).fetchone()

    if row is None:
        return None

    path = Path(row["annotated_image_path"])
    return path if path.is_file() else None


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_bytes(
        self,
        status: int,
        body: bytes,
        content_type: str,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(
        self,
        status: int,
        payload: object,
    ) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def do_GET(self) -> None:
        parsed = parse.urlparse(self.path)

        if parsed.path in {"/", "/dashboard"}:
            self._send_bytes(
                200,
                DASHBOARD_HTML.encode("utf-8"),
                "text/html; charset=utf-8",
            )
            return

        if parsed.path == "/health":
            self._json(
                200,
                {
                    "status": "ok",
                    "service": "CaseMetrologyEngineeringDashboard",
                    "mode": "read_only",
                },
            )
            return

        if parsed.path == "/api/status":
            self._json(200, status_payload())
            return

        if parsed.path == "/api/recent":
            query = parse.parse_qs(parsed.query)
            raw_limit = query.get("limit", ["25"])[0]

            try:
                limit = int(raw_limit)
            except ValueError:
                self._json(400, {"error": "invalid limit"})
                return

            measurements = recent_measurements(limit=limit)
            self._json(
                200,
                {
                    "measurements": measurements,
                    "count": len(measurements),
                },
            )
            return

        if parsed.path.startswith("/image/"):
            measurement_id = parse.unquote(parsed.path[len("/image/") :])

            if "/" in measurement_id or "\\" in measurement_id:
                self._json(400, {"error": "invalid measurement_id"})
                return

            path = annotated_image_path(measurement_id)
            if path is None:
                self._json(404, {"error": "image not found"})
                return

            self._send_bytes(200, path.read_bytes(), "image/png")
            return

        self._json(404, {"error": "not found"})


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"CaseMetrology engineering dashboard listening on " f"http://{HOST}:{PORT}")
    print(f"Database: {DB_PATH}")
    print("Mode: read-only")
    server.serve_forever()


if __name__ == "__main__":
    main()
