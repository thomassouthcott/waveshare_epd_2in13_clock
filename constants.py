"""constants.py: Constants and Enums"""
import configparser
import dataclasses
from enum import Enum
import logging
import os


picdir = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'pic'
)

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

        path=os.path.join(picdir, filename)
        if not os.path.exists(path):
            logging.error("File not found at pic/%s",path)
            raise FileNotFoundError()
        self.default_background = filename

        self.clock_dimensions = tuple(map(int, config["FRAME"]["CLOCK_DIMENSIONS"].split(",")))
        self.banner_dimensions = tuple(map(int, config["FRAME"]["BANNER_DIMENSIONS"].split(",")))

        self.infos = [InfoTypes[item] for item in config["FRAME"]["INFOS_ENABLED"].split(",")]
        self.banners = [BannerTypes[item] for item in config["FRAME"]["BANNERS_ENABLED"].split(",")]

_config = Config()

def get_config():
    """Returns the currently loaded configuration"""
    return _config
