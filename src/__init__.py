# SS7 Termux Tools - Main Package

__version__ = "0.1.0"
__author__ = "Mar140-tech"
__description__ = "SS7 vulnerability analysis tools for Termux (Android)"

# Lazy import to prevent errors if modules not yet fully implemented
_core_available = False
_tools_available = False

try:
    from src import core
    from src.core import ss7_parser, network, packets
    _core_available = True
except (ImportError, AttributeError) as e:
    pass

try:
    from src import tools
    from src.tools import scanner, analyzer
    _tools_available = True
except (ImportError, AttributeError) as e:
    pass

# Export utilities unconditionally
from src.utils import logger, validators, helpers

__all__ = [
    # Metadata
    '__version__',
    '__author__',
    '__description__',
    # Utilities
    'logger',
    'validators',
    'helpers',
    # Conditionally available
    'core',
    'tools',
]

# Add core modules if available
if _core_available:
    __all__.extend(['ss7_parser', 'network', 'packets'])

# Add tools if available
if _tools_available:
    __all__.extend(['scanner', 'analyzer'])
