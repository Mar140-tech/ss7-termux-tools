#!/usr/bin/env python3

"""
Helper Functions

Utility functions for common tasks with optimized performance.
"""

import re
from ipaddress import IPv4Address, IPv4Network, AddressValueError
from typing import Optional, List, Tuple


# Precompiled regex for hex validation (O(1) pattern matching)
HEX_PATTERN = re.compile(r'^[0-9a-fA-F]*$')


def is_valid_ip(ip: str) -> bool:
    """
    Check if a string is a valid IPv4 address.
    Faster than socket.inet_aton() for bulk validation.
    """
    if not isinstance(ip, str) or not ip:
        return False
    
    try:
        IPv4Address(ip)
        return True
    except (AddressValueError, TypeError):
        return False


def is_valid_ipv6(ip: str) -> bool:
    """
    Check if a string is a valid IPv6 address.
    """
    if not isinstance(ip, str) or not ip:
        return False
    
    try:
        from ipaddress import IPv6Address
        IPv6Address(ip)
        return True
    except (AddressValueError, TypeError):
        return False


def parse_network_range(network: str) -> Optional[Tuple[str, int]]:
    """
    Parse a network range in CIDR notation.
    
    Args:
        network: Network in CIDR notation (e.g., '192.168.0.0/24')
        
    Returns:
        Tuple of (base_ip: str, mask: int) or None if invalid
    """
    if not isinstance(network, str) or not network:
        return None
    
    if '/' not in network:
        return None
    
    try:
        parts = network.split('/')
        if len(parts) != 2:
            return None
        
        base, mask_str = parts
        
        # Validate base IP
        if not is_valid_ip(base):
            return None
        
        # Validate and parse mask
        try:
            mask = int(mask_str)
        except ValueError:
            return None
        
        if not 0 <= mask <= 32:
            return None
        
        # Validate using ipaddress module for comprehensive check
        IPv4Network(network, strict=False)
        
        return (base, mask)
    
    except (ValueError, AttributeError, TypeError):
        return None


def expand_cidr(network: str) -> Optional[List[str]]:
    """
    Expand a CIDR network range to individual IP addresses.
    Use with caution on large ranges (e.g., /16 = 65,536 IPs).
    
    Args:
        network: Network in CIDR notation
        
    Returns:
        List of IP addresses or None if invalid
    """
    try:
        net = IPv4Network(network, strict=False)
        return [str(ip) for ip in net.hosts()] if net.num_addresses > 2 else [str(net.network_address), str(net.broadcast_address)]
    except (ValueError, AttributeError, TypeError):
        return None


def bytes_to_hex(data: bytes) -> str:
    """
    Convert bytes to hex string.
    
    Args:
        data: Bytes object
        
    Returns:
        Hexadecimal string representation
    """
    if not isinstance(data, bytes):
        return ''
    return data.hex()


def hex_to_bytes(hex_str: str) -> Optional[bytes]:
    """
    Convert hex string to bytes with validation.
    
    Args:
        hex_str: Hexadecimal string (with or without spaces/colons)
        
    Returns:
        Bytes object or None if invalid
    """
    if not isinstance(hex_str, str):
        return None
    
    # Remove common separators
    cleaned = hex_str.replace(' ', '').replace(':', '').replace('-', '')
    
    if not cleaned:
        return None
    
    # Validate hex string format (even length, valid characters)
    if len(cleaned) % 2 != 0:
        return None
    
    if not HEX_PATTERN.match(cleaned):
        return None
    
    try:
        return bytes.fromhex(cleaned)
    except ValueError:
        return None


def hex_to_bytes_silent(hex_str: str) -> bytes:
    """
    Convert hex string to bytes, returning empty bytes on error (backward compatible).
    
    Args:
        hex_str: Hexadecimal string
        
    Returns:
        Bytes object (empty bytes if invalid)
    """
    result = hex_to_bytes(hex_str)
    return result if result is not None else b''


def validate_hex_string(hex_str: str) -> bool:
    """
    Validate if a string is a valid hexadecimal sequence.
    
    Args:
        hex_str: String to validate
        
    Returns:
        True if valid hex, False otherwise
    """
    if not isinstance(hex_str, str) or not hex_str:
        return False
    
    cleaned = hex_str.replace(' ', '').replace(':', '').replace('-', '')
    
    if len(cleaned) % 2 != 0:
        return False
    
    return bool(HEX_PATTERN.match(cleaned))


def ip_in_range(ip: str, network: str) -> bool:
    """
    Check if an IP address is in a CIDR network range.
    
    Args:
        ip: IP address to check
        network: Network in CIDR notation
        
    Returns:
        True if IP is in range, False otherwise
    """
    if not is_valid_ip(ip):
        return False
    
    try:
        ip_obj = IPv4Address(ip)
        net_obj = IPv4Network(network, strict=False)
        return ip_obj in net_obj
    except (AddressValueError, ValueError, TypeError):
        return False
