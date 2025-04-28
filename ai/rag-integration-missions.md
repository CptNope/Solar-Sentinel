# SolarSentinel - RAG Integration for Missions and Waypoints

## Purpose

Enable AI-driven organization and summarization of field activities.

---

## How it Works

1. Missions, Waypoints, and System Status Updates are logged into local JSON.
2. Logs are periodically embedded and stored in a local Vector Store (ChromaDB, FAISS, or similar).
3. Ollama AI queries the vector store to:
   - Summarize ongoing missions
   - Highlight incomplete missions
   - Report recent waypoints
   - Detect coverage gaps (e.g., no nodes in specific areas)

---

## Example AI Prompts

- "*List active missions and their due times.*"
- "*Show all new waypoints added today.*"
- "*Identify any nodes that missed check-in schedules.*"

---

## Future Features

- Auto-generate new mission suggestions (e.g., cover unmonitored areas)
- Predictive failure analysis (battery levels too low, overdue missions)

---