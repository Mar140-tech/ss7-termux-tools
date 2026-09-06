#!/usr/bin/env python3

"""
SS7 Termux Tools - Logging Utilities

Handles all logging for the SS7 tools with optimized performance.
"""

import logging
import os
from datetime import datetime


class CachedLogger:
    """Wrapper to cache logger configuration and avoid repeated datetime calls"""
    
    _instance = None
    _logger = None
    _log_file_date = None
    _log_file_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @staticmethod
    def setup_logger(name: str = 'ss7_tools', level: int = logging.INFO) -> logging.Logger:
        """Set up and return a configured logger with caching"""
        
        # Return cached logger if already configured
        if CachedLogger._logger is not None:
            return CachedLogger._logger
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Prevent duplicate handlers
        if logger.handlers:
            CachedLogger._logger = logger
            return logger
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        try:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
        except OSError as e:
            print(f"Warning: Could not create logs directory: {e}")
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler with cached date
        try:
            current_date = datetime.now().strftime("%Y%m%d")
            log_file = os.path.join(log_dir, f'ss7_tools_{current_date}.log')
            
            # Cache the log file date and path
            CachedLogger._log_file_date = current_date
            CachedLogger._log_file_path = log_file
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except OSError as e:
            print(f"Warning: Could not create file handler: {e}")
        
        CachedLogger._logger = logger
        return logger


def setup_logger(name: str = 'ss7_tools', level: int = logging.INFO) -> logging.Logger:
    """Public function to setup and return a configured logger"""
    return CachedLogger.setup_logger(name, level)


def get_logger(name: str = 'ss7_tools') -> logging.Logger:
    """Get an already configured logger without re-initialization"""
    return logging.getLogger(name)
