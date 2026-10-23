# SolarSentinel

**Operate beyond the grid.**

SolarSentinel is an open-source field-network project for local coordination, outdoor training, exploration, and scenario-based exercises. The working application is a browser dashboard for node check-ins and field reports, backed by a local Flask server and SQLite database.

The broader vision combines a solar-powered field server, ESP32/LoRa nodes, radio gateways, offline reference material, and local AI. Those integrations are at different stages: this repository includes working dashboard code, starter firmware, sample data, and design documents. See [project status](#project-status) before planning a deployment.

## Contents

- [Project status](#project-status)
- [What the dashboard does](#what-the-dashboard-does)
- [Quickstart](#quickstart)
- [Using the dashboard](#using-the-dashboard)
- [Architecture](#architecture)
- [Configuration and deployment](#configuration-and-deployment)
- [API examples](#api-examples)
- [Data, backups, and recovery](#data-backups-and-recovery)
- [Hardware and integration guides](#hardware-and-integration-guides)
- [Repository layout](#repository-layout)
- [Development and validation](#development-and-validation)
- [Troubleshooting](#troubleshooting)
- [Roadmap and contributions](#roadmap-and-contributions)
- [License and links](#license-and-links)

## Project status

**Early working implementation.** The dashboard can be run and tested independently of field hardware. Field reliability and the complete off-grid system have not been validated end to end.

| Area | Available in this repository | Current boundary |
| --- | --- | --- |
| Field dashboard | Responsive interface, node check-ins, reports, SQLite persistence, operator-token writes | Working local application |
| Node telemetry | Validated HTTP check-in API, timestamps, freshness and battery indicators | Measurements must be supplied manually or by an adapter |
| Solar monitoring | Example monitoring script and hardware notes | The existing script generates random simulated readings |
| ESP32 / LoRa | Starter Arduino sketches and network plans | No dashboard gateway or verified mesh implementation |
| APRS / packet radio | Setup and integration guides | No connected dashboard adapter |
| Field-node PWA | Specification, deployment notes, and install-page placeholder | No installable app, service worker, or background synchronization |
| Offline knowledge | Kiwix setup guide and Compose example | Separate service; content must be supplied and configured |
| Local AI / RAG | Ollama setup notes and integration plans | No working dashboard AI or retrieval pipeline |
| Missions / RPG | Sample scenario JSON, node profiles, and engine plans | No executable mission engine, XP system, or campaign runner |
| AR / VR | Expansion ideas and AR planning notes | Future work |

The project aims to support training and field coordination. The current implementation is a prototype rather than a validated emergency-response system.

## What the dashboard does

- Shows registered nodes, recent check-ins, nodes needing attention, and the total number of open reports.
- Stores the latest node snapshot, including optional battery, voltage, and coordinates.
- Separates online, stale, and offline nodes using server receipt time.
- Creates field reports with routine, important, or urgent priority; reports can be resolved and reopened.
- Filters the latest 200 reports by open, urgent, or resolved status.
- Saves one report draft in the browser and prevents duplicate submissions when an identical request is retried.
- Uses a shared operator token for updates and keeps the token in page memory.
- Runs with locally served assets and an explicitly labeled demo workspace.

An internet connection is needed to obtain the code and dependencies during setup. Once installed, the dashboard does not need external scripts, fonts, or map services. Browsers still need access to the running field server to load the application and submit updates.

## Quickstart

### Requirements

- Python 3.10 or newer with `pip` and `venv` support.
- Git to clone the repository, or an extracted source archive.
- A modern browser.
- Node.js only if you want to run the JavaScript syntax check.

The dashboard does not require a Raspberry Pi, radio, GPS receiver, solar equipment, Ollama, Docker, or Apache to try it locally. The commands below assume you are starting from a terminal and run subsequent commands in the repository root.

### Windows PowerShell

```powershell
git clone https://github.com/CptNope/Solar-Sentinel.git
cd Solar-Sentinel
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m dashboard.app --demo
```

### Linux / Raspberry Pi

```sh
git clone https://github.com/CptNope/Solar-Sentinel.git
cd Solar-Sentinel
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m dashboard.app --demo
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Keep the terminal running; press `Ctrl+C` there to stop the server. These commands invoke the virtual environment directly, so shell activation is optional.

### Enable operator access

On first startup, the server generates an access token beside its database. For the demo workspace, read it locally:

```powershell
# Windows PowerShell
Get-Content dashboard/instance/demo.token
```

```sh
# Linux / Raspberry Pi
cat dashboard/instance/demo.token
```

Choose **Operator access** in the dashboard, paste the token, and select **Use token**. Reloading the page clears browser access; re-enter the token when needed. **Clear access** locks updates for that page.

### Start an empty live workspace

Stop the demo server and run the same command without `--demo`:

```powershell
# Windows PowerShell
.\.venv\Scripts\python.exe -m dashboard.app
```

```sh
# Linux / Raspberry Pi
.venv/bin/python -m dashboard.app
```

The live workspace starts empty and uses a separate database and token. "Live" selects the normal workspace; it does not connect hardware automatically.

| Workspace | Default database | Generated token file |
| --- | --- | --- |
| Live | `dashboard/instance/sentinel.sqlite3` | `dashboard/instance/sentinel.token` |
| Demo | `dashboard/instance/demo.sqlite3` | `dashboard/instance/demo.token` |

Demo data is seeded once into its database. Its timestamps age naturally, so sample nodes eventually become stale or offline. Restarting preserves existing data rather than resetting the samples.

## Using the dashboard

1. Open the dashboard and enable operator access.
2. Choose **Check in a node**. Give it a stable ID and display name. Battery, voltage, and coordinates are optional.
3. Submit another check-in with the same ID to replace that node's latest snapshot.
4. Choose **New field report**, enter a call sign or team, select a priority, and describe the update.
5. Use the report filter and **Mark resolved** / **Reopen report** to manage activity.

### Reading node health

| Indicator | Meaning |
| --- | --- |
| Online | Last check-in received less than 120 seconds ago |
| Stale | Last check-in received from 120 to under 600 seconds ago |
| Offline | No check-in received for at least 600 seconds |
| Needs attention | A node is overdue or has a fresh battery reading at or below 20%; each node is counted once |
| Dash (`—`) | The node did not supply that measurement |
| Last reported | A measurement belongs to a stale or offline snapshot |

These connection states describe check-in freshness, not a verified radio link. The server does not estimate battery percentage from voltage or distinguish panel voltage from battery voltage. An adapter must supply measurements with the intended meaning.

### Connectivity and drafts

The page refreshes every 10 seconds while visible. If the browser loses contact with the server, it displays a warning and retains the last received data. That data may be outdated.

One report draft is saved in that browser profile's localStorage. Reconnect and submit it manually; successful submission clears the draft. There is no background queue or automatic offline synchronization. Drafts are local to the device, while submitted reports live on the server. Clear browser site data to remove a saved draft.

## Architecture

The implemented dashboard path is:

```text
Browser dashboard                 Manual/API clients
  HTML + CSS + JavaScript            Node measurements / reports
            |                                  |
            +-------------- HTTP --------------+
                            |
                       Waitress server
                            |
                      Flask application
                   Validation + write token
                            |
                       SQLite database
                 Latest nodes + field reports
```

The interface and API are served from the same application. `/` and `/status` open the dashboard. Node snapshots are replaced on check-in; the application does not retain a telemetry history. Reports remain stored even when resolved, while the dashboard lists only the latest 200.

Planned integrations would feed this application through adapters: physical sensors or LoRa/APRS gateways for telemetry, a field-node PWA for offline interaction, and optional Kiwix or Ollama services for reference material and AI assistance. These services are not started by the dashboard command.

## Configuration and deployment

The CLI starts the application through Waitress. Run commands from the repository root.

| Setting | Default | Purpose |
| --- | --- | --- |
| `--host` | `127.0.0.1` | Interface to listen on |
| `--port` | `5000` | HTTP port |
| `--demo` | Off | Select the separate demo database and seed sample data if empty |
| `SENTINEL_DB` | Live database path shown above | Override the live SQLite path; ignored by `--demo` |
| `SENTINEL_TOKEN` | Generated token file | Supply the shared write credential instead of loading/generating a token file |

Relative `SENTINEL_DB` paths are resolved from the process's working directory. Use an absolute path for a service deployment.

### Access from another device

To listen on a trusted local network, add `--host 0.0.0.0`:

```sh
.venv/bin/python -m dashboard.app --host 0.0.0.0 --port 5000
```

On Windows, use `.\.venv\Scripts\python.exe` in place of `.venv/bin/python`. From another device on the same network, open `http://<field-server-IP>:5000`. `0.0.0.0` is a bind address, not a browser destination. Hostname discovery, a Wi-Fi access point, and firewall rules are not configured by this application.

### Access boundary

Anyone who can reach the server can read node positions and reports. Updates require a shared bearer token. The application does not provide individual accounts, roles, token expiry, or a per-operator audit trail.

For shared or untrusted networks, use an HTTPS reverse proxy with appropriate authentication and restrict direct access to the application port. Plain HTTP exposes tokens and field data in transit. Protect the database and token files with host permissions; they are excluded from Git.

The existing [`software/pi-setup.sh`](software/pi-setup.sh) is a starter for broader system setup. It does not replace the dashboard quickstart or install a complete integrated field network.

## API examples

Read endpoints require no token. All writes require `Authorization: Bearer YOUR_TOKEN` and JSON content. The request-body limit is 16 KB.

| Method and route | Behavior |
| --- | --- |
| `GET /api/health` | Check database connectivity and return the demo flag |
| `GET /api/state` | Return nodes, latest 200 reports, total open report count, demo flag, and server timestamp |
| `POST /api/access` | Validate an operator token |
| `POST /api/nodes` | Create or replace a node snapshot |
| `POST /api/reports` | Create a report, or return the existing report for an identical retry |
| `PATCH /api/reports/<id>` | Resolve or reopen a report |

The following examples use a POSIX shell with `curl`. Set a token for the workspace you started; the examples use the default live workspace:

```sh
SENTINEL_API_TOKEN="$(cat dashboard/instance/sentinel.token)"
curl --fail-with-body http://127.0.0.1:5000/api/health
```

If you supplied `SENTINEL_TOKEN` when starting the server, use that credential instead of reading a generated file. For a demo server, use `dashboard/instance/demo.token`.

### Check in a node

```sh
curl --fail-with-body http://127.0.0.1:5000/api/nodes \
  -H "Authorization: Bearer $SENTINEL_API_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"id":"trail-01","name":"Trail team","battery":72,"voltage":12.8,"latitude":35.61,"longitude":-82.55}'
```

`id` and `name` are required. Optional numbers may be omitted or set to `null`. Each check-in replaces the snapshot: omitting a previous measurement clears it to unknown. Supply latitude and longitude together, or neither. Suggested adapter check-in interval: 60 seconds.

| Node field | Accepted value |
| --- | --- |
| `id` | Nonblank string, up to 64 characters |
| `name` | Nonblank string, up to 80 characters |
| `battery` | Number from 0 to 100, or null |
| `voltage` | Number from 0 to 100, or null |
| `latitude` | Number from -90 to 90, or null |
| `longitude` | Number from -180 to 180, or null |

### Submit and resolve a report

```sh
curl --fail-with-body http://127.0.0.1:5000/api/reports \
  -H "Authorization: Bearer $SENTINEL_API_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"request_id":"trail-01-report-001","author":"Trail team","priority":"important","message":"At the north junction. Next check-in in five minutes."}'
```

`author` is required and limited to 80 characters; `message` is required and limited to 2,000 characters. `priority` is `routine` (the default), `important`, or `urgent`. `request_id` is a required nonblank string of up to 64 characters.

Generate a new request ID for each new report. Reuse that ID only to retry the same author, message, and priority after an uncertain response. A new report returns HTTP 201; an identical retry returns the existing ID with HTTP 200. Changed content using an existing request ID returns HTTP 409.

Use the returned report ID in the update route; this example assumes the returned ID was `1`:

```sh
curl --fail-with-body -X PATCH http://127.0.0.1:5000/api/reports/1 \
  -H "Authorization: Bearer $SENTINEL_API_TOKEN" \
  -H 'Content-Type: application/json' \
  --data '{"resolved":true}'
```

Set `resolved` to `false` to reopen it. Common errors are 400 for invalid input, 401 for an invalid/missing token, 404 for an unknown report ID, and 413 for an oversized request. See the [dashboard reference](dashboard/README.md) for further behavior notes.

## Data, backups, and recovery

SQLite data survives application restarts. The application stores the latest snapshot per node and all submitted reports, including resolved reports. It does not automatically expire records or expose a delete operation.

To back up a workspace:

1. Stop its server so no writes are in progress.
2. Copy the database and any adjacent SQLite `-wal` / `-shm` files as one stopped-workspace snapshot, or copy the whole instance directory.
3. Keep the token file with the backup if you want to retain its generated credential. If you use `SENTINEL_TOKEN`, manage that secret separately.
4. Restore files while the server is stopped, preserving permissions and the configured database path, then restart.

To reseed a disposable demo, stop the server and move its database and adjacent SQLite files to a backup location before restarting with `--demo`. Keep the live workspace untouched. Removing only the demo token file generates a new credential on the next start unless `SENTINEL_TOKEN` is set.

Browser drafts are separate from server backups. Clearing site data removes those drafts and does not delete submitted reports.

## Hardware and integration guides

Start with the software dashboard before adding hardware. Existing hardware lists and sketches are starting points; board pinouts, radio drivers, power requirements, and gateway behavior need verification for your chosen components.

| Topic | Starting point |
| --- | --- |
| Field-server equipment | [Parts list](hardware/parts-list.md) and [solar setup notes](hardware/solar-setup-guide.md) |
| ESP32 firmware | [Firmware examples](firmware/) |
| LoRa topology | [Network plan](lora/lora-network-plan.md) |
| Android APRS | [APRSdroid setup](android/aprsdroid-setup.md) |
| Radio integration | [APRS/VHF setup](radio/aprs-vhf-setup.md) and [BBS over radio](radio/bbs-over-ham.md) |
| Field-node app | [PWA specification](pwa/solar-sentinel-pwa-spec.md) |
| Offline reference library | [Kiwix setup](wiki/kiwix-setup.md) and [Compose example](wiki/kiwix-docker-compose.yml) |
| Local AI | [Ollama setup notes](ai/ollama-setup.md) and [RAG plan](ai/rag-system-plan.md) |
| Scenarios and profiles | [Mission samples](scenarios/) and [node profile templates](node-profiles/) |

## Repository layout

```text
dashboard/             Working Flask app, browser assets, and dashboard reference
tests/                 Backend behavior tests
.github/workflows/     Automated dashboard checks
requirements.txt       Dashboard Python dependencies
firmware/              Starter ESP32 / LoRa / GPS sketches
hardware/              Equipment lists and solar setup notes
software/              Pi setup starter, simulated solar monitor, BBS plans
lora/                  LoRa network and AI integration plans
radio/                 APRS, radio-cabling, and BBS guides
android/               Android/APRS setup notes
pwa/                   Field-node specifications and placeholder install page
ai/                    Local-model, categorization, RAG, and mission-engine plans
wiki/                  Kiwix setup and Compose example
scenarios/             Example mission JSON
node-profiles/         Example node-profile JSON
assets/                Project icon
docs/                  Project-site content, launch material, and diagram files
```

## Development and validation

After installing the requirements, run the backend suite from the repository root:

```powershell
# Windows PowerShell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

```sh
# Linux / Raspberry Pi
.venv/bin/python -m unittest discover -s tests -v
```

With Node.js installed:

```sh
node --check dashboard/static/dashboard.js
git diff --check
```

GitHub Actions runs the backend tests and JavaScript syntax check on pushes and pull requests using Python 3.12 and Node.js 22. The tests cover unknown telemetry, authenticated writes, node updates, freshness boundaries, invalid input, report retries, persistence, demo isolation, and response headers.

For interface changes, also verify desktop and phone layouts, keyboard access, report draft recovery after reload, and server-disconnection behavior. Automated checks do not validate physical radios, solar autonomy, or complete field operation.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `ModuleNotFoundError: flask` or `waitress` | Install `requirements.txt` with the same virtual-environment Python used to launch the app. |
| No nodes or reports appear | A live workspace starts empty. Check in a node, submit a report, or restart with `--demo` for samples. |
| Demo nodes become stale/offline | Sample timestamps age naturally. This is expected; demo mode does not emit ongoing check-ins. |
| Updates return 401 | Re-enter the token for the active workspace. An environment-supplied token overrides generated token-file loading. |
| Server unavailable warning | Confirm the server process is running, the URL/port is correct, and the device can reach it. Last displayed readings may be old. |
| Another device cannot connect | Bind to `0.0.0.0`, use the server's actual LAN IP, and check network isolation and host firewall settings. |
| Port is already in use | Stop the other process or start with another port, such as `--port 5001`. |
| A previous measurement disappeared | Check-ins replace the full snapshot. Resend every measurement you want to retain. |
| Open count exceeds the visible reports | The open count includes all persisted reports; the activity list and filters cover only the latest 200. |
| A draft is missing on another phone | Drafts stay in the browser profile where they were composed. They are not server-synchronized. |
| `solarsentinel.local` does not resolve | Automatic hostname discovery is not configured here. Use the field server's IP address. |

## Roadmap and contributions

The next useful milestones are:

1. **Measured telemetry:** connect a real sensor adapter, document units and provenance, and validate it on field hardware.
2. **Gateway ingestion:** bridge LoRa/APRS data into authenticated check-ins with explicit delivery and identity behavior.
3. **Offline field client:** implement an installable app, local storage, and a reliable synchronization protocol.
4. **Operational controls:** add per-operator permissions, audit history, and documented backup/upgrade procedures.
5. **Mission tooling:** validate scenario schemas and build an executable mission workflow.
6. **Optional knowledge and AI:** integrate reference search and local assistance after the core data flow is reliable.

AR/VR overlays and RPG expansion remain longer-term ideas. This is a direction for contributions, not a release schedule.

To contribute, open an issue describing the problem or proposed integration, then submit a focused pull request. Include setup instructions, relevant tests, and the hardware/OS used for integration testing. Keep real field locations, credentials, databases, and personal reports out of commits. New scenario packs and node profiles should identify required capabilities and distinguish examples from tested configurations.

## License and links

SolarSentinel is released under the [MIT License](LICENSE).

- [Source repository and issues](https://github.com/CptNope/Solar-Sentinel)
- [Project site](https://CptNope.github.io/Solar-Sentinel)
- [Dashboard reference](dashboard/README.md)
- Project founder: [Jeremy Anderson](https://github.com/CptNope) · [Website](https://jeremyanderson.tech/)
