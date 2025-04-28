# SolarSentinel - LoRa to AI Integration

## Purpose

Connect low-power ESP32 LoRa field nodes to SolarSentinel's AI for real-time field awareness.

## Process

1. LoRa Field Node sends text packet (e.g., solar voltage, GPS, custom status)
2. SolarSentinel Pi receives packet via LoRa gateway
3. LoRa Listener logs message into Field Logs
4. AI periodically ingests logs and creates:
   - Waypoint updates
   - Solar warnings
   - Node presence tracking
5. Dashboard displays AI summaries on-demand

---

## Sample LoRa Messages

```
SOLAR:12.7V
GPS:42.3942,-71.1223
NODE:Tracker-03 ONLINE
```

---