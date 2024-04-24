"""constants.py: Constants and Enums"""
from enum import Enum

# Enums
class InfoTypes(Enum):
    """Enum for the different types of panels that can be displayed on the Info Panel"""
    TEXT = "text"
    WEATHER = "weather"

class BannerTypes(Enum):
    """Enum for the different types of panels that can be displayed on the Banner Panel"""
    QOTD="qotd"

class VerticalAlignment(Enum):
    """Enum for Vertical Alignment of the Clock Panel"""
    TOP = 0
    BOTTOM = 1

class HorizontalAlignment(Enum):
    """Enum for Horizontal Alignment of the Clock Panel"""
    LEFT = 0
    RIGHT = 1
