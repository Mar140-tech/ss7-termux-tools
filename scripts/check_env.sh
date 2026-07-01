#!/bin/bash

# SS7 Termux Tools - Environment Checker
# Verifies all required dependencies are installed

echo "Checking SS7 Termux Tools Environment"
echo "======================================"
echo ""

CHECKS_PASSED=0
CHECKS_FAILED=0

# Check Python 3
echo -n "Checking Python 3... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Found (Python $PYTHON_VERSION)"
    ((CHECKS_PASSED++))
else
    echo "✗ Not found"
    ((CHECKS_FAILED++))
fi

# Check pip
echo -n "Checking pip... "
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version 2>&1 | awk '{print $2}')
    echo "✓ Found (pip $PIP_VERSION)"
    ((CHECKS_PASSED++))
else
    echo "✗ Not found"
    ((CHECKS_FAILED++))
fi

# Check Git
echo -n "Checking Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo "✓ Found (Git $GIT_VERSION)"
    ((CHECKS_PASSED++))
else
    echo "✗ Not found"
    ((CHECKS_FAILED++))
fi

# Check Click
echo -n "Checking Click... "
if python3 -c "import click" 2>/dev/null; then
    CLICK_VERSION=$(python3 -c "import click; print(click.__version__)" 2>/dev/null)
    echo "✓ Found (Click $CLICK_VERSION)"
    ((CHECKS_PASSED++))
else
    echo "✗ Not found"
    ((CHECKS_FAILED++))
fi

# Check Scapy
echo -n "Checking Scapy... "
if python3 -c "import scapy" 2>/dev/null; then
    SCAPY_VERSION=$(python3 -c "import scapy; print(scapy.__version__)" 2>/dev/null)
    echo "✓ Found (Scapy $SCAPY_VERSION)"
    ((CHECKS_PASSED++))
else
    echo "⚠ Not found"
    ((CHECKS_FAILED++))
fi

# Check directory structure
echo -n "Checking directory structure... "
if [ -d "src" ] && [ -d "config" ] && [ -d "scripts" ]; then
    echo "✓ OK"
    ((CHECKS_PASSED++))
else
    echo "✗ Missing directories"
    ((CHECKS_FAILED++))
fi

# Check src/main.py
echo -n "Checking main entry point... "
if [ -f "src/main.py" ]; then
    echo "✓ Found"
    ((CHECKS_PASSED++))
else
    echo "✗ Not found"
    ((CHECKS_FAILED++))
fi

echo ""
echo "======================================"
echo "Results: $CHECKS_PASSED passed, $CHECKS_FAILED failed"

if [ $CHECKS_FAILED -eq 0 ]; then
    echo "✓ All checks passed!"
    echo ""
    echo "Ready to use. Try:"
    echo "  python3 src/main.py --help"
    exit 0
else
    echo "✗ Some checks failed"
    echo ""
    echo "To fix missing dependencies:"
    echo "  bash scripts/install_deps.sh"
    echo "  pip install -r requirements.txt"
    exit 1
fi
