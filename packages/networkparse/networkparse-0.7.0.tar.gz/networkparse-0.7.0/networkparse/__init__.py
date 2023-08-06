"""
A simple network configuration searcher
"""
from pathlib import Path

VERSION = (0, 7, 0, "", 0)
__version__ = ".".join([str(n) for n in VERSION[:3]])

from . import core
from . import parse
