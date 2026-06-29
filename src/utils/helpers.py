#!/usr/bin/env python3

"""
Helper Functions

Utility functions for common tasks.
"""

import socket
from typing import Optional, List


def is_valid_ip(ip: str) -> bool:
    """Check if a string is a valid IP address"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def parse_network_range(network: str) -> Optional[tuple]:
    """Parse a network range in CIDR notation"""
    try:
        if '/' not in network:
            return None
        
        base, mask = network.split('/')
        if not is_valid_ip(base):
            return None
        
        mask = int(mask)
        if not 0 <= mask <= 32:
            return None
        
        return (base, mask)
    except Exception:
        return None


def bytes_to_hex(data: bytes) -> str:
    """Convert bytes to hex string"""
    return data.hex()


def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes"""
    try:
        return bytes.fromhex(hex_str)
    except ValueError:
        return b''
