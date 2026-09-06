#!/usr/bin/env python3

"""
Input Validation

Validates user input and configuration with optimized performance.
"""

from typing import Any, Dict, Optional, Tuple


class ConfigValidator:
    """Cache-aware configuration validator"""
    
    REQUIRED_KEYS = frozenset(['network', 'ss7', 'logging'])
    _validation_cache = {}
    
    @staticmethod
    def validate_port(port: Any) -> bool:
        """Validate port number (1-65535)"""
        try:
            port_int = int(port)
            return 0 < port_int < 65536
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_timeout(timeout: Any) -> bool:
        """Validate timeout value (1-3600 seconds)"""
        try:
            timeout_int = int(timeout)
            return 0 < timeout_int < 3600  # Max 1 hour
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_retry_count(retries: Any) -> bool:
        """Validate retry count (1-10)"""
        try:
            retry_int = int(retries)
            return 0 < retry_int <= 10
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate configuration dictionary with caching.
        
        Args:
            config: Configuration dictionary to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        
        # Check if config dict is empty
        if not config:
            return False, "Configuration dictionary is empty"
        
        if not isinstance(config, dict):
            return False, "Configuration must be a dictionary"
        
        # Use frozenset for O(1) lookups instead of linear search
        config_keys = frozenset(config.keys())
        missing_keys = ConfigValidator.REQUIRED_KEYS - config_keys
        
        if missing_keys:
            return False, f"Missing required config sections: {', '.join(sorted(missing_keys))}"
        
        # Validate network section
        network_config = config.get('network', {})
        if not isinstance(network_config, dict):
            return False, "Network config must be a dictionary"
        
        if 'timeout' in network_config:
            if not ConfigValidator.validate_timeout(network_config['timeout']):
                return False, f"Invalid network timeout value: {network_config['timeout']}"
        
        if 'retries' in network_config:
            if not ConfigValidator.validate_retry_count(network_config['retries']):
                return False, f"Invalid retry count value: {network_config['retries']}"
        
        # Validate SS7 section
        ss7_config = config.get('ss7', {})
        if not isinstance(ss7_config, dict):
            return False, "SS7 config must be a dictionary"
        
        # Validate logging section
        logging_config = config.get('logging', {})
        if not isinstance(logging_config, dict):
            return False, "Logging config must be a dictionary"
        
        if 'level' in logging_config:
            valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
            if logging_config['level'].upper() not in valid_levels:
                return False, f"Invalid logging level: {logging_config['level']}"
        
        return True, "Configuration is valid"


# Public API functions for backward compatibility
def validate_port(port: Any) -> bool:
    """Validate port number"""
    return ConfigValidator.validate_port(port)


def validate_timeout(timeout: Any) -> bool:
    """Validate timeout value"""
    return ConfigValidator.validate_timeout(timeout)


def validate_config(config: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate configuration dictionary"""
    return ConfigValidator.validate_config(config)
