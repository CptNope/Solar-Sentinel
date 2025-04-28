# SolarSentinel - Android APRS to AI Integration

## Purpose

Use rooted Android devices with APRSdroid to report field data over HAM radio into the AI assistant.

## Process

1. APRSdroid sends GPS or text packet via VHF (144.390 MHz)
2. Baofeng radio transmits
3. SolarSentinel Pi receives via Direwolf software TNC
4. Packet parsed and logged
5. AI analyzes messages for:
   - New waypoints
   - Field status changes
   - System events

---

## Sample APRSdroid Messages

```
/cmd wp add 42.3942,-71.1223 "New Stream Crossing"
/cmd solar low 11.8V
```

---