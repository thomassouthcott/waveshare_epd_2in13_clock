"""Config Parser Module"""
import configparser
import dataclasses
import logging

from constants import InfoTypes, BannerTypes, VerticalAlignment, HorizontalAlignment
from image_helper import check_image_path

logger = logging.getLogger()

def get_config_item(config, group, key):
    """Returns the value of the key in the group"""
    try:
        return config[group][key]
    except KeyError as exc:
        raise KeyError(f"Key {key} not found in group {group}") from exc

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

        self.prog = get_config_item(config,"DEFAULT","NAME")
        self.version = get_config_item(config,"DEFAULT","VERSION")
        self.author = get_config_item(config,"DEFAULT","AUTHOR")
        self.logging = LoggingConfig(config)
        self.frame = FrameConfig(config)

@dataclasses.dataclass
class LoggingConfig:
    """Class to hold the logging configuration"""
    def __init__(self, config):
        self.level = logging.getLevelName(get_config_item(config,"LOGGING","LEVEL"))
        self.file = get_config_item(config,"LOGGING","FILE")

@dataclasses.dataclass
class FrameConfig:
    """Class to hold the frame configuration"""
    def __init__(self, config):
        self.v_alignment = VerticalAlignment[get_config_item(config,"FRAME","V_ALIGNMENT")]
        self.h_alignment = HorizontalAlignment[get_config_item(config,"FRAME","H_ALIGNMENT")]
        filename=get_config_item(config,"FRAME","DEFAULT_BACKGROUND")
        if filename == "":
            logger.warning("[CONFIG] No default background image specified.")
            self.default_background = None
        elif check_image_path(filename):
            self.default_background = filename
        self.slide_interval = int(get_config_item(config,"FRAME","SLIDE_INTERVAL"))

        self.clock_dimensions = tuple(map(
            int, get_config_item(config,"FRAME","CLOCK_DIMENSIONS").split(",")
        ))
        self.banner_dimensions = tuple(map(
            int, get_config_item(config,"FRAME","BANNER_DIMENSIONS").split(",")
        ))
        panels = get_config_item(config,"FRAME","INFOS_ENABLED").split(",")
        self.infos = [InfoTypes[item] for item in panels]
        panels = get_config_item(config,"FRAME","BANNERS_ENABLED").split(",")
        self.banners = [BannerTypes[item] for item in panels]

@dataclasses.dataclass
class WeatherConfig:
    """Class to hold the weather configuration"""
    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
        except Exception as exc:
            raise FileNotFoundError("Config file not found") from exc
        self.api_key = get_config_item(config,"WEATHER","API_KEY")
        self.api_urls = get_config_item(config,"WEATHER","API_URL").split(",")
        self.api_refresh_interval = int(get_config_item(config,"WEATHER","REFRESH_INTERVAL"))
        self.city = get_config_item(config,"WEATHER","CITY")
        self.units = get_config_item(config,"WEATHER","UNITS")

_config = Config()
_weather_config = WeatherConfig()

def get_config():
    """Returns the currently loaded configuration"""
    return _config

def get_weather_config():
    """Returns the currently loaded weather configuration"""
    return _weather_config
