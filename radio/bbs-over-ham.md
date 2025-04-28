# SolarSentinel - BBS Interface Over HAM Radio (Packet)

## Concept

Use APRS/Packet radio protocols to interact with the SolarSentinel BBS system during low-connectivity conditions.

---

## Legal Considerations

- No encryption allowed over HAM bands (FCC Part 97)
- Identify your station every 10 minutes (callsign)
- Only allow non-sensitive, public commands (e.g., status, waypoints)

---

## Command Examples Over HAM

| Command Sent | Action |
|:-------------|:-------|
| `N1ABC>CMD:STATUS` | Request system status |
| `N1ABC>CMD:WAYPOINT ADD` | Send GPS waypoint |
| `N1ABC>CMD:LOG REQUEST` | Request solar logs |

---

## System Setup

1. Raspberry Pi + USB soundcard + Baofeng
2. Direwolf software TNC (handles packet encoding/decoding)
3. Unified BBS parser listens for incoming packets
4. Replies via packet radio text message

---

## Future Expansion

- Challenge-response lightweight authentication (public phrases)
- Use "grid square" knowledge or "waypoint names" for validation
- Adaptive command menu based on user's session type (LoRa or HAM)

---