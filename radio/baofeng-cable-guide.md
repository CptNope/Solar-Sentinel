# SolarSentinel - Baofeng Cable Interface Guide

This guide explains how to connect Android phones, ESP32 nodes, and Raspberry Pi devices to Baofeng UV-5R radios for APRS and BBS operations.

## Standard Baofeng Audio Pinout (K1 Connector)

| Pin | Function  |
|:----|:----------|
| Tip | Microphone |
| Ring 1 | Speaker |
| Ring 2 | Ground |
| Sleeve | PTT Trigger (ground to transmit) |

**Note:** Some cheap cables combine Mic and PTT incorrectly — test with multimeter if issues.

---

## Phone to Baofeng Cable

- TRRS (Phone) to K1 (Baofeng)
- Enable VOX on Baofeng (detects audio and auto-transmits)
- Adjust phone volume carefully to avoid overdriving

---

## Raspberry Pi to Baofeng

- Use USB soundcard with 3.5mm input/output
- Simple cables (mic and speaker)
- Use Direwolf software modem to generate/decode APRS tones

---

## ESP32 to Baofeng (Advanced)

- Can directly PWM AFSK tones from ESP32 DAC
- Requires careful level shifting (resistor network)

---