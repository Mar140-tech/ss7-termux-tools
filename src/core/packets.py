#!/usr/bin/env python3
"""
Packet Module

Handles packet construction and analysis.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import struct

logger = logging.getLogger(__name__)


@dataclass
class PacketHeader:
    """TCP/IP packet header"""
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    flags: str = ""


@dataclass
class PacketPayload:
    """Packet payload"""
    data: bytes
    length: int
    checksum: str = ""


class PacketAnalyzer:
    """Analyzes network packets"""

    PROTOCOLS = {
        6: "TCP",
        17: "UDP",
        1: "ICMP",
    }

    def __init__(self):
        """Initialize packet analyzer"""
        self.packets: List[Dict[str, Any]] = []
        logger.info("PacketAnalyzer initialized")

    def analyze_packet(self, packet_data: bytes, source_ip: str, dest_ip: str,
                      source_port: int = 0, dest_port: int = 0,
                      protocol: str = "TCP") -> Dict[str, Any]:
        """Analyze a packet"""
        try:
            analysis = {
                'source_ip': source_ip,
                'destination_ip': dest_ip,
                'source_port': source_port,
                'destination_port': dest_port,
                'protocol': protocol,
                'packet_size': len(packet_data),
                'checksum': self._calculate_checksum(packet_data),
                'flags': self._extract_flags(packet_data),
                'payload_size': len(packet_data) - 20,  # Assuming 20-byte header
            }
            self.packets.append(analysis)
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing packet: {e}")
            return {}

    def _calculate_checksum(self, data: bytes) -> str:
        """Calculate packet checksum"""
        try:
            checksum = sum(data) & 0xFFFFFFFF
            return f"0x{checksum:08x}"
        except Exception:
            return "0x00000000"

    def _extract_flags(self, data: bytes) -> str:
        """Extract TCP flags from packet"""
        if len(data) < 2:
            return ""

        try:
            flags = []
            byte = data[1]
            if byte & 0x01:
                flags.append("FIN")
            if byte & 0x02:
                flags.append("SYN")
            if byte & 0x04:
                flags.append("RST")
            if byte & 0x08:
                flags.append("PSH")
            if byte & 0x10:
                flags.append("ACK")
            if byte & 0x20:
                flags.append("URG")
            return ",".join(flags) if flags else "NONE"
        except Exception:
            return "NONE"

    def get_packets(self) -> List[Dict[str, Any]]:
        """Get all analyzed packets"""
        return self.packets

    def filter_packets(self, protocol: Optional[str] = None,
                      source_ip: Optional[str] = None) -> List[Dict[str, Any]]:
        """Filter packets by criteria"""
        results = self.packets

        if protocol:
            results = [p for p in results if p['protocol'].upper() == protocol.upper()]

        if source_ip:
            results = [p for p in results if p['source_ip'] == source_ip]

        return results

    def clear_packets(self):
        """Clear all analyzed packets"""
        self.packets = []
        logger.info("Cleared all packets")
