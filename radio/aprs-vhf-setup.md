# SolarSentinel - APRS over VHF Setup

## Basics

- APRS uses 1200 baud AFSK over 2-meter VHF band
- Typical North America APRS frequency: **144.390 MHz**

## Setup Steps

1. Program Baofeng UV-5R:
    - Frequency: 144.390 MHz
    - No tone squelch (disable CTCSS/DCS)
    - Narrowband (12.5 kHz) mode

2. Enable VOX:
    - Menu 4 (VOX)
    - Set VOX Level around 3–5

3. Connect cable to device (phone, Pi, ESP32)
4. Configure APRSdroid, Direwolf, or custom app to use audio interface

---

## Best Practices

- Use low power mode (~1W) for nearby APRS coverage
- Use wideband antennas if possible
- Keep audio levels clean (not distorted)

---

## Optional Enhancements

- External SMA antenna for better range
- Filter capacitors on cables to remove noise
- Use digipeaters to extend message range

---