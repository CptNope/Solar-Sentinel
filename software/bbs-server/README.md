# SolarSentinel - BBS Server System

## Purpose

Provide a simple text-based interface accessible over:

- LoRa private mesh
- HAM packet radio (APRS/AX.25)

## Key Commands

- `LOGIN:<callsign>`
- `CMD:STATUS`
- `CMD:WAYPOINT ADD`
- `CMD:LOGOUT`

## Flow

1. Receive text command packet
2. Parse using BBS parser
3. Log safe events
4. Forward to AI for deeper analysis

## Security

- LoRa mesh supports private encryption
- HAM radio is public — only safe status commands allowed

---