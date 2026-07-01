#!/usr/bin/env python3
"""
Input Validators

Validate user inputs and configuration.
"""

import re
import logging

logger = logging.getLogger(__name__)


def validate_ip_address(ip: str) -> bool:
    """Validate IP address format"""
    try:
        import socket
        socket.inet_aton(ip)
        return True
    except socket.error:
        logger.warning(f"Invalid IP address: {ip}")
        return False


def validate_port(port: int) -> bool:
    """Validate port number"""
    if isinstance(port, str):
        try:
            port = int(port)
        except ValueError:
            logger.warning(f"Invalid port: {port}")
            return False

    if 1 <= port <= 65535:
        return True

    logger.warning(f"Port out of range: {port}")
    return False


def validate_cidr(cidr: str) -> bool:
    """Validate CIDR notation"""
    try:
        import ipaddress
        ipaddress.ip_network(cidr, strict=False)
        return True
    except Exception:
        logger.warning(f"Invalid CIDR notation: {cidr}")
        return False


def validate_timeout(timeout: int) -> bool:
    """Validate timeout value"""
    if isinstance(timeout, str):
        try:
            timeout = int(timeout)
        except ValueError:
            logger.warning(f"Invalid timeout: {timeout}")
            return False

    if 1 <= timeout <= 300:
        return True

    logger.warning(f"Timeout out of range: {timeout}")
    return False


def validate_file_path(path: str) -> bool:
    """Validate file path"""
    import os
    try:
        # Check if path is valid (doesn't need to exist)
        if len(path) == 0 or len(path) > 255:
            logger.warning(f"Invalid file path: {path}")
            return False
        return True
    except Exception:
        logger.warning(f"Invalid file path: {path}")
        return False


def validate_output_format(format_type: str) -> bool:
    """Validate output format"""
    valid_formats = ['json', 'csv', 'txt', 'xml']
    if format_type.lower() in valid_formats:
        return True

    logger.warning(f"Invalid output format: {format_type}")
    return False
