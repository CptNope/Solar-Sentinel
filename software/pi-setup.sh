#!/bin/bash
# SolarSentinel - Raspberry Pi Initial Setup Script

echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "Installing essential packages..."
sudo apt install -y python3 python3-pip git screen gpsd gpsd-clients python3-gps mosquitto mosquitto-clients

echo "Installing Flask for dashboard..."
pip3 install Flask

echo "Setting up Kiwix Server (Wikipedia Offline)..."
# Download or setup Kiwix-server manually here
# Example: wget https://download.kiwix.org/release/kiwix-tools/kiwix-tools_linux-arm64.tar.gz

echo "Setting up Ollama AI (local install)..."
# Instructions inside /ai/ollama-setup.md

echo "Enabling I2C and SPI interfaces..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

echo "Initial setup complete. Please reboot the system."
