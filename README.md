# SolarSentinel ⚡ - Tactical AI Field Network

**The First Fully Modular, Solar-Powered, AI-Enhanced Off-Grid Network.**  
Built for real-world missions, survival operations, field training, tactical gaming, and exploration.

---

# 📜 Overview

SolarSentinel is a resilient, autonomous field operations system.  
Combining solar power, LoRa mesh, HAM APRS radio, offline AI, PWA field nodes, and a modular mission system —  
SolarSentinel allows **full tactical command, even beyond the grid**.

It is **open source**, **community-driven**, and **future expandable** with RPG missions, AR overlays, and VR dashboards.

---

# 🌟 Key Features

- ☀️ **Solar-Powered Raspberry Pi Field Server**
- 🛰️ **LoRa Mesh Communication via ESP32 Nodes**
- 📡 **HAM Radio APRS/Packet Integration**
- 🧠 **Self-Hosted AI Field Awareness (Ollama + RAG)**
- 📚 **Offline Wikipedia / Knowledge Bases (Kiwix)**
- 📱 **Installable Field Node PWA App (Offline Deployable)**
- 🧩 **Modular Mission Scenarios (Training, SAR, RPG, Milsim)**
- 🎮 **RPG XP, Gear Unlocks, Branching Mission Chains**
- 🕶️ **Future AR Recon Overlays (WebXR)**
- 🧠 **Future VR Tactical Dashboards (Quest 2 Compatible)**
- 🛡️ **Fully Offline, Resilient Field Operations**

---

# 🎯 Tactical Goals

- Survive and operate beyond communication blackouts.
- Organize field missions dynamically without centralized control.
- Deploy rapid tactical networks for training, SAR, exploration, or simulation.
- Augment real-world ops with RPG and story-driven layers.
- Expand into VR/AR tactical overlays for next-gen ops.

---

# 🛰️ System Architecture

```
[Field Units (PWA, ESP32, Phones)]
    ↓
[LoRa + APRS Radio Mesh]
    ↓
[SolarSentinel Core (Raspberry Pi)]
    ↓
[Offline AI (Ollama RAG) + Field Mission Manager]
    ↓
[Optional Kiwix Wikipedia Server / VR/AR Dashboard / GitHub Sync]
```

---

# ⚙️ Core Components

| Component | Role |
|:----------|:----|
| Raspberry Pi 4/5 | Solar-powered command deck |
| ESP32 Modules | LoRa low-power mesh field nodes |
| Android Phones (optional) | APRSdroid field beacons |
| Baofeng UV-5R Radios | HAM APRS transmission |
| Flask + Apache | Serve PWA Apps and Dashboards |
| Ollama Models | Local AI Summarization and RAG search |
| Kiwix | Offline Wikipedia server |
| A-Frame / AR.js | Future AR expansion (scenarios + clues) |

---

# 📂 Folder Structure

```
/scenarios/              # Mission Packs (Training, Gaming, RPG)
/pwa/                    # PWA App Specs and AR Mode Planning
/software/bbs-server/     # Tactical BBS Server Interface
/ai/                      # Field AI + RAG Summarization Specs
/docs/                    # Launch Posts, Social Posts, Flowcharts
/lora/                    # LoRa Field Node Configs
/android/                 # Android APRS Setup Guides
/radio/                   # Baofeng UV-5R Field Integration
/node-profiles/           # Field Node Type Templates
```

---

# 🔥 RPG and AR Expansion

- XP awarded for missions completed
- Gear unlocks, secret missions, branching campaigns
- AR clues embedded at GPS coordinates (future)
- VR tactical ops dashboard under development (future)

---

# 🚀 Deployment Instructions

1. Deploy Raspberry Pi + Solar Panel + Battery Pack.
2. Install Raspberry Pi OS Lite.
3. Clone SolarSentinel repository.
4. Install Python requirements (Flask, etc.).
5. Deploy Apache2 or Flask to serve `/app/` (PWA) and `/docs/`.
6. Connect ESP32 LoRa nodes (or use Android phones as nodes).
7. Launch Offline AI (Ollama) and configure RAG for field logs.
8. Set up local Kiwix Wikipedia mirror (optional but recommended).
9. Test PWA field installs by connecting phones to Wi-Fi and visiting `http://solarsentinel.local/`.

---

# 🤝 How to Contribute

SolarSentinel is open to:

- Tactical hardware engineers
- Python, JavaScript, Web developers
- LoRa and Radio Ops specialists
- AI Engineers (Vector search, RAG ops)
- VR and AR Developers
- Field testers, SAR experts, Survival trainers

**Contribute New:**
- Node profiles
- Scenario mission packs
- PWA field app extensions
- AR markers and overlays
- Dashboard expansions

---

# 💬 Contact & Links

- GitHub Repository: [https://github.com/CptNope/Solar-Sentinel](https://github.com/CptNope/Solar-Sentinel)
- Official GitHub Pages Site: [https://CptNope.github.io/Solar-Sentinel](https://CptNope.github.io/Solar-Sentinel)
- Project Founder: [Jeremy Anderson](https://github.com/CptNope)[https://jeremyanderson.tech/](https://jeremyanderson.tech/)

---

# 🛡️ License

MIT License — Free for survival, training, and expansion.  
Build, modify, survive, thrive.

---

# 🚀 Inspirational

> "Operate Beyond the Grid.  
> Adapt Beyond the Mission.  
> SolarSentinel Leads the Way."

---