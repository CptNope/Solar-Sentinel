# SolarSentinel - Field Node PWA Specification

## Purpose

Create a Progressive Web App (PWA) that:
- Installs on any smartphone (Android/iPhone)
- Accesses phone sensors (GPS, accelerometer, battery, motion)
- Acts as a network field node
- Connects via LoRa (optional BLE/USB gateway) or Wi-Fi local server
- Allows field mission participation without custom hardware

---

## Core Features

- Offline installable
- Local mission storage (IndexedDB)
- GPS coordinate reporting
- Waypoint adding interface
- Field status reports
- View assigned missions
- Minimalist tactical UI
- Optional training mode for Airsoft/SAR/milsim exercises
- Background Sync attempt when LoRa/Wi-Fi available

---

## Connection Options

| Method | Purpose |
|:-------|:--------|
| Wi-Fi Direct to Pi Server | Direct BBS access |
| BLE to ESP32 LoRa Gateway | Broadcast LoRa packets |
| Offline Storage | Cache reports if no immediate connection |

---

## Future Expansions

- Camera integration (photo waypoints)
- Vibration alerts (new mission received)
- Live mesh mapping via GPS
- Customizable mission types
- Training stats and scoring system

---

## Frameworks and Tools

- Vanilla JavaScript / Bootstrap frontend
- IndexedDB for local data
- Service Worker for offline caching
- Web Bluetooth (optional future for LoRa bridges)

---

## Potential Usage Scenarios

- SAR Field Team Ops
- Airsoft/Milsim Tactical Simulations
- Disaster Recovery Drills
- Environmental Mapping Expeditions

---