"""
Interactive D3 rendering of matplotlib images
=============================================

Functions: General Use
----------------------
:func:`plotWithMap`
    renders a Figure on a Leaflet map
"""

__all__ = ['__version__','plotWithMap']

from .__about__ import __version__
from .pyLeaflet import *