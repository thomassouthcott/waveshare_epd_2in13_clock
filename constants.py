"""constants.py: Constants and Enums"""
import configparser
import dataclasses
from enum import Enum
import logging
import os

logger = logging.getLogger()
#Images
picdir = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'pic'
)

def get_image_path(filename):
    """Return the full path of the image."""
    return os.path.join(picdir, filename)

def check_image_path(filename):
    """Check if the image path is valid.
        - Must be a .bmp file
        - Must exist in the /pic/ directory"""
    if not filename.endswith(".bmp"):
        logger.error("File must be a .bmp file")
        raise ValueError("File must be a .bmp file")
    if not os.path.exists(get_image_path(filename)):
        logger.error("File not found at pic/%s",filename)
        raise FileNotFoundError()
    return True

def get_all_images():
    """Return a list of all images in the /pic/ directory"""
    return [f for f in os.listdir(picdir) if f.endswith(".bmp")]

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

# Configuration Constants
@dataclasses.dataclass
class Config:
    """Class to hold the configuration of the program"""
    def __init__(self, path="config.ini"):
        try:
            config = configparser.ConfigParser()
            config.read(path)
        except Exception as exc:
            raise FileNotFoundError(f"Config file not found at {path}") from exc

        self.prog = config["DEFAULT"]["NAME"]
        self.version = config["DEFAULT"]["VERSION"]
        self.author = config["DEFAULT"]["AUTHOR"]
        self.logging = LoggingConfig(config)
        self.frame = FrameConfig(config)

@dataclasses.dataclass
class LoggingConfig:
    """Class to hold the logging configuration"""
    def __init__(self, config):
        self.level = logging.getLevelName(config["LOGGING"]["LEVEL"])
        self.file = config["LOGGING"]["FILE"]

@dataclasses.dataclass
class FrameConfig:
    """Class to hold the frame configuration"""
    def __init__(self, config):
        self.v_alignment = VerticalAlignment[config["FRAME"]["V_ALIGNMENT"]]
        self.h_alignment = HorizontalAlignment[config["FRAME"]["H_ALIGNMENT"]]
        filename=config["FRAME"]["DEFAULT_BACKGROUND"]
        if filename == "":
            logger.warning("[CONFIG] No default background image specified.")
            self.default_background = None
        elif check_image_path(filename):
            self.default_background = filename
        self.slide_interval = int(config["FRAME"]["SLIDE_INTERVAL"])

        self.clock_dimensions = tuple(map(int, config["FRAME"]["CLOCK_DIMENSIONS"].split(",")))
        self.banner_dimensions = tuple(map(int, config["FRAME"]["BANNER_DIMENSIONS"].split(",")))

        self.infos = [InfoTypes[item] for item in config["FRAME"]["INFOS_ENABLED"].split(",")]
        self.banners = [BannerTypes[item] for item in config["FRAME"]["BANNERS_ENABLED"].split(",")]

_config = Config()

def get_config():
    """Returns the currently loaded configuration"""
    return _config
