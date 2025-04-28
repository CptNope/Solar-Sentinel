# SolarSentinel - Ollama AI Server Setup

SolarSentinel uses a local AI server based on [Ollama](https://ollama.com/) to power offline intelligent operations.

## Quick Install (Raspberry Pi)

> Note: Ollama ARM builds are experimental — best results on Pi 5 with active cooling.

1. Update and Install Docker:
```bash
sudo apt update && sudo apt install -y docker.io
```

2. Pull the Ollama Docker Image (example):
```bash
docker pull ollama/ollama
```

3. Start Ollama locally:
```bash
docker run -d --name ollama-server -p 11434:11434 ollama/ollama
```

4. Access via:
```bash
http://localhost:11434
```

5. Load lightweight models optimized for ARM (e.g., `llama2:7b`, `mistral:7b`)

---

## For ARM-only setups

- Alternative: Use a mini local server setup script
- Future plan: Create a custom image tuned for SolarSentinel tasks only.

---