# SolarSentinel - BBS Mission and Waypoint System

## Purpose

Allow field units to:
- Request Missions
- Accept/Reject Missions
- Report Waypoint discoveries
- Update Mission Status
- All via LoRa or HAM BBS text commands

---

## Key Commands

| Command | Description |
|:--------|:------------|
| `CMD:MISSION REQUEST` | Request a mission assignment |
| `CMD:MISSION ACCEPT` | Acknowledge and accept assigned mission |
| `CMD:MISSION COMPLETE` | Mark mission as completed |
| `CMD:WAYPOINT ADD <lat>,<lon> "Label"` | Report new GPS waypoint |

---

## Typical Mission Packet Example

```
New Mission:
- Task: Deploy Weather Node
- Location: 42.3942N, 71.1223W
- Priority: HIGH
- Due: Before 18:00
```

---

## Mission Logging

- Assigned Time
- Operator (callsign or ID)
- Mission Details
- Acceptance/Completion Times
- Result Summary (optional)

---

## Future Enhancements

- Assign priorities automatically
- Timeout abandoned missions
- Field unit ranking based on completed tasks

---