# SolarSentinel - Kiwix Offline Wikipedia Setup

SolarSentinel includes a fully offline Wikipedia mirror using Kiwix.

## Install Kiwix Server

1. Download and install Kiwix tools:
```bash
sudo apt install kiwix-tools
```

OR manually:
```bash
wget https://download.kiwix.org/release/kiwix-tools/kiwix-tools_linux-arm64.tar.gz
tar -xvzf kiwix-tools_linux-arm64.tar.gz
```

2. Download a ZIM file (compressed Wikipedia data):
- Example:
```bash
wget https://download.kiwix.org/zim/wikipedia_en_all_maxi.zim
```
*(Or a smaller "mini" version if storage limited.)*

3. Start the server:
```bash
./kiwix-serve --port=8080 wikipedia_en_all_maxi.zim
```

4. Access locally:
```bash
http://localhost:8080
```

---

## Notes
- You can host multiple ZIM files (Wikipedia, Wiktionary, medical textbooks, etc.).
- Best to store ZIM files on external SSD if possible.

---