#!/usr/bin/env python3
"""
SS7 Network Scanner

Scans networks for SS7 nodes and services.
"""

import logging
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import asdict, dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ScanResult:
    """Result of a scan"""
    host: str
    port: int
    status: str
    protocol: str
    response_time: float
    timestamp: str
    service: str = ""


class SS7Scanner:
    """SS7 Protocol Scanner"""

    # Default SS7 ports
    DEFAULT_PORTS = [5060, 5061, 6060, 6061, 8888, 9999, 14001, 14002]

    # Service mapping
    SERVICE_MAP = {
        5060: "SIP",
        5061: "SIP-TLS",
        6060: "SS7-ISUP",
        6061: "SS7-SCCP",
        8888: "Custom-SS7",
        9999: "Debug-Port",
        14001: "TCAP",
        14002: "MAP",
    }

    def __init__(self, timeout: int = 5, retries: int = 3, ports: Optional[List[int]] = None):
        """Initialize scanner"""
        self.timeout = timeout
        self.retries = retries
        self.ports = ports or self.DEFAULT_PORTS
        self.results: List[ScanResult] = []
        self.scan_start_time = None
        self.scan_end_time = None
        logger.info(f"SS7Scanner initialized with {len(self.ports)} ports")

    def scan_host(self, host: str) -> List[ScanResult]:
        """Scan a single host for SS7 services"""
        logger.info(f"Scanning host: {host}")
        host_results = []

        for port in self.ports:
            result = self._probe_port(host, port)
            if result:
                host_results.append(result)
                self.results.append(result)

        return host_results

    def scan_network(self, cidr: str) -> List[ScanResult]:
        """Scan a network in CIDR notation"""
        import ipaddress

        logger.info(f"Scanning network: {cidr}")
        self.scan_start_time = time.time()
        network_results = []

        try:
            network = ipaddress.ip_network(cidr, strict=False)
            hosts = [str(ip) for ip in network.hosts()]
            logger.info(f"Generated {len(hosts)} hosts from CIDR {cidr}")

            for i, host in enumerate(hosts, 1):
                logger.debug(f"Scanning [{i}/{len(hosts)}] {host}")
                host_results = self.scan_host(host)
                network_results.extend(host_results)

            self.scan_end_time = time.time()
            logger.info(f"Network scan completed in {self.scan_end_time - self.scan_start_time:.2f}s")
        except Exception as e:
            logger.error(f"Error scanning network {cidr}: {e}")

        return network_results

    def _probe_port(self, host: str, port: int) -> Optional[ScanResult]:
        """Probe a single port"""
        import socket

        for attempt in range(self.retries):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)

                start_time = time.time()
                result = sock.connect_ex((host, port))
                response_time = time.time() - start_time
                sock.close()

                if result == 0:
                    service = self.SERVICE_MAP.get(port, "Unknown")
                    scan_result = ScanResult(
                        host=host,
                        port=port,
                        status="open",
                        protocol="TCP",
                        response_time=response_time,
                        timestamp=datetime.now().isoformat(),
                        service=service
                    )
                    logger.info(f"Found open port {port} on {host} ({service}) - {response_time*1000:.2f}ms")
                    return scan_result
            except Exception as e:
                logger.debug(f"Probe attempt {attempt+1}/{self.retries} failed for {host}:{port}: {e}")

        return None

    def get_results(self) -> List[Dict[str, Any]]:
        """Get scan results as dictionaries"""
        return [asdict(r) for r in self.results]

    def get_results_by_port(self, port: int) -> List[ScanResult]:
        """Get results for a specific port"""
        return [r for r in self.results if r.port == port]

    def get_results_by_status(self, status: str) -> List[ScanResult]:
        """Get results by status"""
        return [r for r in self.results if r.status == status]

    def save_results(self, filename: str = "scan_results.json") -> bool:
        """Save scan results to JSON file"""
        try:
            data = {
                'scan_info': {
                    'total_results': len(self.results),
                    'start_time': datetime.fromtimestamp(self.scan_start_time).isoformat() if self.scan_start_time else None,
                    'end_time': datetime.fromtimestamp(self.scan_end_time).isoformat() if self.scan_end_time else None,
                    'duration': (self.scan_end_time - self.scan_start_time) if self.scan_start_time and self.scan_end_time else 0,
                },
                'results': self.get_results()
            }

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Results saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return False

    def clear_results(self):
        """Clear all scan results"""
        self.results = []
        logger.info("Cleared all scan results")
