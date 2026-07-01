#!/usr/bin/env python3
"""
SS7 Protocol Parser

Handles parsing and decoding of SS7 protocol messages.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SS7Message:
    """Represents a parsed SS7 message"""
    message_type: str
    source: str
    destination: str
    data: bytes
    timestamp: float
    protocol_version: str = "ITU-Q.773"
    parsed_fields: Dict[str, Any] = None

    def __post_init__(self):
        if self.parsed_fields is None:
            self.parsed_fields = {}


class SS7Parser:
    """Parser for SS7 protocol messages"""

    # SS7 message types
    MESSAGE_TYPES = {
        0x01: "MTP1",
        0x02: "MTP2",
        0x03: "MTP3",
        0x04: "SCCP",
        0x05: "ISUP",
        0x06: "TCAP",
    }

    def __init__(self, protocol_version: str = "ITU-Q.773"):
        """Initialize parser with protocol version"""
        self.protocol_version = protocol_version
        self.messages: List[SS7Message] = []
        logger.info(f"SS7Parser initialized with protocol {protocol_version}")

    def parse_message(self, data: bytes, source: str, destination: str, timestamp: float = 0) -> Optional[SS7Message]:
        """Parse a raw SS7 message"""
        if not data or len(data) < 4:
            logger.warning("Invalid SS7 message: too short")
            return None

        try:
            msg_type = data[0]
            msg_type_name = self.MESSAGE_TYPES.get(msg_type, f"UNKNOWN(0x{msg_type:02x})")

            parsed_fields = self._parse_fields(data)

            message = SS7Message(
                message_type=msg_type_name,
                source=source,
                destination=destination,
                data=data,
                timestamp=timestamp,
                protocol_version=self.protocol_version,
                parsed_fields=parsed_fields
            )

            self.messages.append(message)
            return message
        except Exception as e:
            logger.error(f"Error parsing SS7 message: {e}")
            return None

    def _parse_fields(self, data: bytes) -> Dict[str, Any]:
        """Extract fields from message data"""
        fields = {}
        try:
            if len(data) > 1:
                fields['length'] = data[1]
            if len(data) > 2:
                fields['flags'] = hex(data[2])
            if len(data) > 4:
                fields['checksum'] = hex(int.from_bytes(data[3:4], 'big'))
        except Exception as e:
            logger.debug(f"Error parsing fields: {e}")
        return fields

    def get_messages(self, msg_type: Optional[str] = None) -> List[SS7Message]:
        """Get parsed messages, optionally filtered by type"""
        if msg_type:
            return [m for m in self.messages if m.message_type == msg_type]
        return self.messages

    def clear_messages(self):
        """Clear all parsed messages"""
        self.messages = []
        logger.info("Cleared all parsed messages")
