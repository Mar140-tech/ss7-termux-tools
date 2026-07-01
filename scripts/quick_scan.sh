#!/bin/bash

# SS7 Termux Tools - Quick Scan Script
# Convenience wrapper for quick network scanning

if [ $# -eq 0 ]; then
    echo "Usage: $0 <target_network>"
    echo "Example: $0 192.168.1.0/24"
    exit 1
fi

TARGET=$1
OUTPUT="quick_scan_$(date +%Y%m%d_%H%M%S).json"

echo "SS7 Quick Scan"
echo "Target: $TARGET"
echo "Output: $OUTPUT"
echo ""

python3 src/main.py scan --target "$TARGET" --output "$OUTPUT" --verbose

echo ""
echo "Results saved to: $OUTPUT"
