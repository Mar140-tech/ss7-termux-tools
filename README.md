# SS7 Termux Tools 🔧📱

**SS7 Vulnerability Analysis & Testing Toolkit for Termux (Android)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform: Android/Termux](https://img.shields.io/badge/Platform-Android%2FTermux-green.svg)](https://termux.com/)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#)

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Commands Reference](#commands-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

SS7 Termux Tools is a comprehensive security toolkit designed for analyzing, testing, and detecting vulnerabilities in SS7 (Signaling System No. 7) networks. It runs natively on Android devices via Termux, providing:

- **Network Scanning** - Discover SS7 nodes and services
- **Protocol Analysis** - Parse and decode SS7 messages
- **Vulnerability Detection** - Identify known security issues
- **Traffic Analysis** - Analyze captured PCAP files
- **Reporting** - Generate detailed security reports

### What is SS7?

SS7 is the global standard signaling protocol used by telecom networks for call routing, SMS delivery, and subscriber management. Vulnerabilities in SS7 can lead to unauthorized access.

**⚠️ Disclaimer:** This tool is for authorized security testing and educational purposes only.

## ✨ Features

### 🔍 Network Discovery
- Multi-port scanning (8 default SS7/SIP ports)
- CIDR range support
- Response time measurement
- Service identification

### 📊 Protocol Analysis
- SS7 message parsing
- ITU-Q.773 protocol support
- Field extraction

### 🛡️ Vulnerability Detection
- 5 Known SS7 Vulnerabilities
- Confidence scoring
- Report generation

### 📝 Traffic Analysis
- PCAP file parsing
- Packet inspection
- Anomaly detection

## 📋 Requirements

### Hardware
| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Android | 5.0 | 9.0+ |
| RAM | 2GB | 4GB+ |
| Storage | 500MB | 1GB+ |

### Software
- **Termux** (latest version)
- **Python** 3.8+
- **pip** (Python package manager)

## 🚀 Installation

### Step 1: Install Termux
Download from [Google Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/)

### Step 2: Clone Repository

```bash
pkg update && pkg upgrade -y
git clone https://github.com/Mar140-tech/ss7-termux-tools.git
cd ss7-termux-tools
```

### Step 3: Automated Installation

```bash
chmod +x setup.sh
./setup.sh
```

### Step 4: Verify Installation

```bash
bash scripts/check_env.sh
```

### Step 5: Configure

```bash
cp config/config.example.json config/config.json
```

## ⚡ Quick Start

### Basic Network Scan

```bash
python3 src/main.py scan --target 192.168.1.0/24
```

### Detect Vulnerabilities

```bash
python3 src/main.py detect-vuln --report -o vulnerability_report.json
```

### Show Help

```bash
python3 src/main.py --help
```

## 🔧 Commands Reference

### SCAN - Network Scanning

```bash
python3 src/main.py scan [OPTIONS]
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--target` / `-t` | TEXT | **Required** | Target IP or CIDR range |
| `--output` / `-o` | TEXT | `scan_results.json` | Output file |
| `--timeout` | INT | 5 | Connection timeout (seconds) |
| `--retries` | INT | 3 | Retry attempts |
| `--ports` | TEXT | Default | Comma-separated ports |

### DETECT-VULN - Vulnerability Detection

```bash
python3 src/main.py detect-vuln [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--report` / `-r` | Generate detailed report |
| `--output` / `-o` | Output file |

### CONFIG - Configuration Management

```bash
python3 src/main.py config [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--show` | Display configuration |
| `--check` | Validate configuration |

## ⚙️ Configuration

### Configuration File

```bash
config/config.json
```

### Key Settings

```json
{
  "network": {
    "timeout": 30,
    "retries": 3
  },
  "ss7": {
    "protocol_version": "ITUQ773",
    "ports": [5060, 5061, 6060, 6061, 8888, 9999, 14001, 14002]
  },
  "logging": {
    "level": "INFO"
  }
}
```

## 🔧 Troubleshooting

### Issue: "Permission Denied"

```bash
chmod +x setup.sh scripts/*.sh src/main.py
./setup.sh
```

### Issue: "Python Not Found"

```bash
pkg install python3 python3-dev
pip install -r requirements.txt
```

### Issue: "Connection Timeout"

Increase timeout in `config/config.json`:
```json
{"network": {"timeout": 60}}
```

### Issue: "Insufficient Storage"

```bash
pkg autoclean
pkg clean
```

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - See LICENSE file

## 📞 Support

- [GitHub Issues](https://github.com/Mar140-tech/ss7-termux-tools/issues)
- [GitHub Discussions](https://github.com/Mar140-tech/ss7-termux-tools/discussions)

---

**Happy Testing! 🔒🔍**
