#!/bin/bash

# SS7 Termux Tools - System Dependencies Installation
# Installs required system packages for Termux

echo "Installing system dependencies for SS7 tools..."

# Update package manager
echo "[*] Updating package manager"
pkg update -y

# Core development tools
echo "[*] Installing development tools"
pkg install -y python3 python3-dev clang make

# Network tools
echo "[*] Installing network utilities"
pkg install -y netcat tcpdump libpcap git wget curl

# Build essentials
echo "[*] Installing build essentials"
pkg install -y pkg-config

# Additional utilities
echo "[*] Installing additional utilities"
pkg install -y nano vim git openssh

echo "[✓] System dependencies installation completed"
