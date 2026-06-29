#!/usr/bin/env python3

"""
Input Validation

Validates user input and configuration.
"""

from typing import Any, Dict, Optional


def validate_port(port: Any) -> bool:
    """Validate port number"""
    try:
        port_int = int(port)
        return 0 < port_int < 65536
    except (ValueError, TypeError):
        return False


def validate_timeout(timeout: Any) -> bool:
    """Validate timeout value"""
    try:
        timeout_int = int(timeout)
        return 0 < timeout_int < 3600  # Max 1 hour
    except (ValueError, TypeError):
        return False


def validate_config(config: Dict[str, Any]) -> tuple:
    """Validate configuration dictionary"""
    
    required_keys = ['network', 'ss7', 'logging']
    
    # Check required keys
    for key in required_keys:
        if key not in config:
            return False, f"Missing required config section: {key}"
    
    # Validate network section
    network_config = config.get('network', {})
    if 'timeout' in network_config:
        if not validate_timeout(network_config['timeout']):
            return False, "Invalid network timeout value"
    
    return True, "Configuration is valid"
