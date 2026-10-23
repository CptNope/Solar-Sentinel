# SolarSentinel field dashboard

A local Flask + SQLite workspace for node check-ins and field reports. All interface assets are served locally. No radio, battery sensor, AI, or GPS adapter is connected automatically.

## Start

From the repository root, with Python 3.10 or newer:

```sh
python -m venv .venv
# Linux / Raspberry Pi:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m dashboard.app
```

Open http://127.0.0.1:5000. The server uses Waitress, not Flask's development server. The live database begins empty.

For a separate sample workspace:

```sh
python -m dashboard.app --demo --port 5001
```

Demo mode uses `dashboard/instance/demo.sqlite3`; live mode uses `dashboard/instance/sentinel.sqlite3`. Demo readings are seeded once and age naturally. They do not simulate live hardware.

## Operator access

The server creates a random token in a `.token` file beside its database (for example `dashboard/instance/sentinel.token`). Read it locally and paste it into **Operator access**. It stays in browser memory and is cleared on reload. Alternatively, set `SENTINEL_TOKEN` before starting the server. Keep the database and token files private; both are excluded from Git.

Reads are available to anyone who can reach the server; writes require the token. The default bind address is localhost. To serve a trusted field LAN, use `--host 0.0.0.0`. For shared or untrusted networks, put an HTTPS/authenticating reverse proxy in front of it; plain HTTP does not protect tokens or reports in transit. This is a shared operator credential, not per-user accounts or an audit trail.

Use `SENTINEL_DB` for a custom live database path. Stop the server before copying its database for backup. The demo flag always selects its separate database.

## API

All writes use `Authorization: Bearer YOUR_TOKEN` and `Content-Type: application/json`. Requests are limited to 16 KB.

| Route | Purpose |
| --- | --- |
| `GET /api/health` | Database availability and demo flag |
| `GET /api/state` | Nodes, latest 200 reports, total open report count, server timestamp |
| `POST /api/access` | Validate operator token |
| `POST /api/nodes` | Create or replace the latest check-in for a node ID |
| `POST /api/reports` | Save a report; duplicate request IDs return the existing report |
| `PATCH /api/reports/<id>` | Resolve or reopen with `{"resolved": true}` or `false` |

Node payload:

```json
{"id":"trail-01","name":"Trail team","battery":72,"voltage":12.8,"latitude":35.61,"longitude":-82.55}
```

Only `id` and `name` are required. Optional numeric values may be null or omitted; each check-in replaces the snapshot, so omitted measurements become unknown. Coordinates must be supplied as a pair. `voltage` is whatever voltage the reporting device measures; it is not automatically identified as panel or battery voltage. Battery percentage must be measured or estimated by the adapter, not inferred by this app.

Freshness is based on server receipt time: online under 120 seconds, stale from 120 to 599 seconds, offline at 600 seconds. Suggested adapter interval: 60 seconds. "Needs attention" counts unique nodes with overdue check-ins or a fresh battery reading at or below 20%.

Report payload:

```json
{"request_id":"unique-client-generated-id","author":"Trail team","priority":"important","message":"At the north junction; next check-in in 5 minutes."}
```

Priority is `routine`, `important`, or `urgent`. Reuse a request ID only for retrying an identical report after an uncertain response; changed content with the same ID returns 409. New reports require new IDs.

## Browser behavior

- Refreshes every 10 seconds while visible.
- Clearly flags failed refreshes; last received data stays visible.
- Saves one report draft in localStorage on the device. Retry after reconnecting; successful submission clears the draft.
- Drafts remain on the browser profile and can contain sensitive field information. Clear browser site data to remove them.
- This release requires the server to load the page. It is **not an installable/offline PWA**, and does not automatically queue or sync reports in the background.
- Report filters cover the latest 200 reports; the open count covers all persisted reports.

## Checks

```sh
python -m unittest discover -s tests -v
node --check dashboard/static/dashboard.js
```

Next integration points: a measured telemetry adapter, authenticated LoRa gateway ingestion, offline PWA delivery, and per-operator permissions.
