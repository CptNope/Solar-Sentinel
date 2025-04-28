# SolarSentinel - Offline PWA Deployment Guide

## Purpose

Allow field units to install the SolarSentinel Field Node App **off-grid**, directly from the SolarSentinel Pi server, without needing Internet.

---

## Deployment Setup

1. Install a local HTTP server on the Raspberry Pi
```bash
sudo apt install apache2
```
OR use a Flask server if already installed.

2. Place the PWA files inside your web root (example):
```plaintext
/var/www/html/app/
```

3. Place `install-page.html` at root (`/var/www/html/`) to act as the install launcher.

4. Ensure Service Worker and Manifest paths are **relative** (no external CDN links).

5. Optional (for Android): Use a local SSL certificate (self-signed) for true "Add to Home Screen" prompt.

---

## Field Unit Steps

1. Connect to SolarSentinel Wi-Fi network
2. Open browser and visit:
```plaintext
http://solarsentinel.local/
```
3. Click "**Install Field Node App**"
4. PWA installs — even without Internet!

---

## Notes

- PWA assets must be cached fully offline via Service Worker
- Updates to app will automatically propagate when reconnected to SolarSentinel network
- Works on Android immediately; iOS devices may require manual "Add to Home Screen" after loading the page.

---