#!/usr/bin/env python3
"""
Network Module

Handles network operations and connectivity.
"""

import socket
import logging
import ipaddress
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)


class NetworkManager:
    """Manages network operations"""

    def __init__(self, timeout: int = 5, retries: int = 3):
        """Initialize network manager"""
        self.timeout = timeout
        self.retries = retries
        self.open_ports: List[Tuple[str, int]] = []
        logger.info(f"NetworkManager initialized (timeout={timeout}s, retries={retries})")

    def is_host_up(self, host: str) -> bool:
        """Check if a host is reachable"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, 80))
            sock.close()
            return result == 0
        except Exception as e:
            logger.debug(f"Host check failed for {host}: {e}")
            return False

    def port_is_open(self, host: str, port: int) -> bool:
        """Check if a port is open on a host"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                self.open_ports.append((host, port))
                return True
            return False
        except Exception as e:
            logger.debug(f"Port check failed for {host}:{port}: {e}")
            return False

    def scan_ports(self, host: str, ports: List[int]) -> List[int]:
        """Scan multiple ports on a host"""
        open_ports = []
        for port in ports:
            if self.port_is_open(host, port):
                open_ports.append(port)
                logger.info(f"Found open port {port} on {host}")
        return open_ports

    def get_network_range(self, cidr: str) -> List[str]:
        """Generate list of IPs from CIDR notation"""
        try:
            network = ipaddress.ip_network(cidr, strict=False)
            hosts = [str(ip) for ip in network.hosts()]
            logger.info(f"Generated {len(hosts)} hosts from CIDR {cidr}")
            return hosts
        except Exception as e:
            logger.error(f"Invalid CIDR notation: {cidr} - {e}")
            return []

    def get_open_ports(self) -> List[Tuple[str, int]]:
        """Get list of discovered open ports"""
        return self.open_ports

    def clear_discoveries(self):
        """Clear discovery results"""
        self.open_ports = []
        logger.info("Cleared network discoveries")
