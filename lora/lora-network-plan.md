# SolarSentinel - LoRa Mesh Network Plan

## Purpose

Use LoRa modules for:
- Extremely low-power long-distance communications
- Basic status reporting, commands, and waypoint transmissions
- Offline BBS operation across wide areas

---

## Basic Architecture

| Node Type | Function |
|:----------|:---------|
| Deck Commander (Pi) | Central server, main BBS, AI server |
| Field Node (ESP32) | Sensor data collection, GPS tracking |
| Relay Node (ESP32) | Pure repeater, extends LoRa mesh range |

---

## Frequency Plan (Example)

- **915 MHz Band** (U.S.)
- SF7 or SF9 spreading factor (balance between range and speed)
- Bandwidth: 125 kHz

## Recommended Modules

- Heltec WiFi LoRa 32 v3
- TTGO T-Beam (with GPS)
- Adafruit Feather M0 LoRa

---

## Message Protocol (Simple Start)

- Max 256 bytes per message
- Text-based commands:
  - `LOGIN:<user>`
  - `CMD:STATUS`
  - `WAYPOINT:<lat>,<lon>,<label>`
  - `LOGOUT`

---

## Example Node Behavior

- **Every 5 minutes**: Broadcast battery + solar status
- **Every 15 minutes**: Send GPS position (if available)
- **On-demand**: Respond to BBS commands

---

## Future Expansions

- Mesh Networking (ESP-NOW hybrid, LoRaMesh library)
- AES lightweight encryption for LoRa-only side
- Automatic node discovery
- Ad-hoc network mapping (BBS shows active node map)

---