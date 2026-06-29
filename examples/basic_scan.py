#!/usr/bin/env python3

"""
Basic Network Scan Example

This script demonstrates how to use the SS7 scanner.
"""

import sys
sys.path.insert(0, '..')

from src.tools.scanner import SS7Scanner
from src.utils import logger

# Setup logger
log = logger.setup_logger()


def main():
    """Run basic network scan"""
    log.info("Starting basic network scan example")
    
    # Create scanner instance
    scanner = SS7Scanner(timeout=30, retries=3)
    
    # Scan a network
    target_network = "192.168.1.0/24"
    log.info(f"Scanning network: {target_network}")
    
    results = scanner.scan_network(target_network)
    
    # Display results
    print(f"\nFound {len(results)} nodes:")
    for result in results:
        print(f"  - {result['host']}:{result['port']} ({result['status']})")
    
    # Save results
    scanner.save_results('basic_scan_results.json')
    log.info("Results saved to basic_scan_results.json")


if __name__ == '__main__':
    main()
