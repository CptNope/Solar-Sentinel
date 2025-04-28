# SolarSentinel - Flashing Rootable Android Phones

SolarSentinel supports adding low-cost rooted Android devices for APRS and auxiliary control.

## Rootable Phone Suggestions
- Pixel 3a
- Moto G7
- LG V20
- OnePlus 6

## Steps to Flash Lightweight ROM (LineageOS / AOSP)

1. **Unlock Bootloader**
```bash
adb reboot bootloader
fastboot oem unlock
```

2. **Install Custom Recovery (TWRP)**
```bash
fastboot flash recovery twrp.img
```

3. **Flash ROM**
- Boot into recovery
- Wipe Data
- Flash LineageOS / AOSP ROM zip

4. **Optional: Install Magisk (for root)**

---

## Post-Flash Setup
- Disable all telemetry
- Install lightweight launcher
- Install APRSdroid manually (APK sideload)

---