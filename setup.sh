#!/bin/bash

# SS7 Termux Tools - Installation Script
# This script sets up the SS7 tools environment in Termux

set -e

echo "========================================"
echo "SS7 Termux Tools - Installation Script"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if running in Termux
if [ ! -d "$PREFIX" ]; then
    echo -e "${RED}Error: This script should be run in Termux environment${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/5] Updating package manager...${NC}"
pkg update -y > /dev/null 2>&1
pkg upgrade -y > /dev/null 2>&1

echo -e "${YELLOW}[2/5] Installing system dependencies...${NC}"
bash scripts/install_deps.sh

echo -e "${YELLOW}[3/5] Creating directory structure...${NC}"
mkdir -p config src/core src/tools src/utils scripts docs examples tests logs
echo -e "${GREEN}✓ Directory structure created${NC}"

echo -e "${YELLOW}[4/5] Installing Python dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

echo -e "${YELLOW}[5/5] Setting up permissions...${NC}"
chmod +x scripts/*.sh 2>/dev/null || true
chmod +x src/main.py 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Copy config: cp config/config.example.json config/config.json"
echo "  2. Test installation: python3 src/main.py --version"
echo "  3. Read documentation: cat docs/USAGE.md"
echo ""
