# SolarSentinel Solar Power Setup Guide

## Basic Diagram

[SOLAR PANEL] → [MPPT CONTROLLER] → [LiFePO4 BATTERY] → [12V to 5V Step-Down Converter] → [Raspberry Pi]

## Key Tips:
- Always fuse between battery and load.
- Use MPPT controllers for maximum solar efficiency.
- Monitor voltage levels to avoid over-discharging LiFePO4 battery.
- Plan for nighttime operation with enough battery reserve (at least 1x daily draw).
- Optional: Add a separate 5V rail for ESP32 nodes to increase efficiency.

---

## Example Parts
- BigBlue 28W Solar Panel
- Renogy Wanderer MPPT Controller
- Bioenno 12V 12Ah LiFePO4 battery
- DROK Buck Converter (12V to 5V 5A)

---
