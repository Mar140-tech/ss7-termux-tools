# Usage Guide - SS7 Termux Tools

## Getting Started

After installation, start using the tools:

```bash
cd ss7-termux-tools
python3 src/main.py --help
```

## Main Commands

### 1. Scan Command

Scan a network for SS7 nodes:

```bash
python3 src/main.py scan --target 192.168.1.0/24 --output results.json
```

**Options:**
- `--target`: Network range to scan (CIDR notation)
- `--output`: Output file for results (default: scan_results.json)
- `--verbose`: Enable verbose output

**Example:**
```bash
python3 src/main.py scan --target 10.0.0.0/24 --output my_scan.json --verbose
```

### 2. Analyze Command

Analyze captured protocol traffic:

```bash
python3 src/main.py analyze --pcap traffic.pcap
```

**Options:**
- `--pcap`: Path to PCAP file
- `--verbose`: Enable verbose output

**Example:**
```bash
python3 src/main.py analyze --pcap ./captures/traffic.pcap --verbose
```

### 3. Detect Vulnerabilities

Detect known SS7 vulnerabilities:

```bash
python3 src/main.py detect-vuln --report
```

**Options:**
- `--report`: Generate detailed report

### 4. Configuration Management

Manage tool configuration:

```bash
python3 src/main.py config --check
```

## Quick Start Scripts

### Fast Network Scan

```bash
bash scripts/quick_scan.sh 192.168.1.0/24
```

### Check Environment

```bash
bash scripts/check_env.sh
```

## Example Workflows

### Workflow 1: Basic Network Scan

```bash
# 1. Run a quick scan
python3 src/main.py scan --target 192.168.1.0/24

# 2. View results
cat scan_results.json | jq

# 3. Analyze specific targets
python3 src/main.py analyze --pcap traffic.pcap
```

### Workflow 2: Vulnerability Assessment

```bash
# 1. Scan network
python3 src/main.py scan --target 10.0.0.0/24 --output network_scan.json

# 2. Detect vulnerabilities
python3 src/main.py detect-vuln --report

# 3. Generate report
ls -la results/
```

## Configuration File

Edit `config/config.json` to customize behavior:

```json
{
  "network": {
    "timeout": 30,
    "retries": 3
  },
  "ss7": {
    "protocol_version": "ITUQ773",
    "debug": false
  },
  "logging": {
    "level": "INFO",
    "file": "logs/ss7_tools.log"
  }
}
```

### Configuration Options

- **timeout**: Connection timeout in seconds
- **retries**: Number of retry attempts
- **debug**: Enable debug logging
- **level**: Logging level (DEBUG, INFO, WARNING, ERROR)

## Logging

Logs are automatically saved to `logs/` directory:

```bash
# View today's logs
cat logs/ss7_tools_20260629.log

# Follow logs in real-time
tail -f logs/ss7_tools_*.log
```

## Output Files

Results are saved in the current directory:

```
.
├── scan_results.json       # Network scan results
├── analysis_results.json   # Traffic analysis
└── vulnerability_report.json  # Vulnerability assessment
```

## Tips & Tricks

### Run Commands in Background

```bash
nohup python3 src/main.py scan --target 192.168.1.0/24 > scan.log &
```

### Use tmux for Long Operations

```bash
pkg install tmux
tmux new-session -d -s scan 'python3 src/main.py scan --target 192.168.1.0/24'
tmux attach -t scan
```

### Process Large Result Files

```bash
cat scan_results.json | jq '.[] | select(.status=="open")'
```

## Common Issues

### "Module not found" error

```bash
pip install -r requirements.txt
```

### "Permission denied" error

```bash
chmod +x src/main.py scripts/*.sh
```

### "Connection timeout" error

Increase timeout in config:
```json
{
  "network": {
    "timeout": 60
  }
}
```

## Performance Optimization

- Reduce timeout for faster scans (faster = less reliable)
- Increase retries for unstable networks
- Use screen resolution-appropriate logging
- Monitor RAM usage during large scans
