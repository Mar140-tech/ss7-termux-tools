# Installation Guide - SS7 Termux Tools

## Prerequisites

- Android device with Termux installed
- Stable internet connection
- Minimum 500MB free storage
- Basic familiarity with command line

## Step-by-Step Installation

### 1. Update Termux

```bash
pkg update && pkg upgrade -y
```

### 2. Clone Repository

```bash
git clone https://github.com/Mar140-tech/ss7-termux-tools.git
cd ss7-termux-tools
```

### 3. Automated Installation

Run the automatic setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Update package manager
- Install system dependencies
- Create directory structure
- Install Python dependencies
- Set up permissions

### 4. Manual Installation (Alternative)

If the automated script doesn't work:

```bash
# Install system dependencies
bash scripts/install_deps.sh

# Create directories
mkdir -p config src/core src/tools src/utils scripts docs examples tests logs

# Install Python packages
pip install -r requirements.txt

# Set permissions
chmod +x scripts/*.sh
chmod +x src/main.py
```

### 5. Verify Installation

```bash
bash scripts/check_env.sh
```

Expected output:
```
Checking Python 3... ✓ Found (Python 3.x.x)
Checking pip... ✓ Found
Checking Git... ✓ Found
All checks passed!
```

### 6. Configuration

Create your configuration file:

```bash
cp config/config.example.json config/config.json
```

Edit the configuration as needed:

```bash
nano config/config.json
```

### 7. Test Installation

```bash
python3 src/main.py --help
```

You should see the help menu with available commands.

## Troubleshooting

### Issue: Permission Denied

```bash
chmod +x setup.sh scripts/*.sh src/main.py
./setup.sh
```

### Issue: Python Not Found

Install Python:
```bash
pkg install python3 python3-dev
```

### Issue: Missing Dependencies

Reinstall all packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: Low Storage Space

Free up space and try again:
```bash
pkg autoclean
pkg clean
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Android Version | 5.0 | 9.0+ |
| RAM | 2GB | 4GB+ |
| Storage | 500MB | 1GB+ |
| Python | 3.8 | 3.10+ |

## Next Steps

1. Read the [USAGE.md](USAGE.md) guide
2. Check out [TOOLS.md](TOOLS.md) for specific tool documentation
3. Review [SS7_BASICS.md](SS7_BASICS.md) for protocol information
4. Run example scripts in `examples/`
