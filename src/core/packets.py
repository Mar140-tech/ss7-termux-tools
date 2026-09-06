"""
Packet Handling

Defines and processes protocol packets.
"""

from typing import Optional, Dict, Any


class Packet:
    """Base class for protocol packets"""
    
    def __init__(self, data: Optional[bytes] = None):
        """
        Initialize packet.
        
        Args:
            data: Raw packet data
        """
        self.data = data or b''
        self.parsed = False
    
    def parse(self) -> bool:
        """
        Parse packet data.
        
        Returns:
            True if parsing successful, False otherwise
        """
        raise NotImplementedError("Packet parsing not yet implemented")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert packet to dictionary representation.
        
        Returns:
            Dictionary representation of packet
        """
        return {
            'data_length': len(self.data),
            'parsed': self.parsed
        }
