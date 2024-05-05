"""Config Parser Module"""
import configparser
import dataclasses
import logging
from secrets import token_hex

from constants import InfoTypes, BannerTypes, VerticalAlignment, HorizontalAlignment
from image_helper import check_image_path

logger = logging.getLogger()

def get_config_item(config, group, key):
    """Returns the value of the key in the group"""
    try:
        return config[group][key]
    except KeyError as exc:
        raise KeyError(f"Key {key} not found in group {group}") from exc
    
def set_config_item(config, group, key, value):
    """Sets the value of the key in the group"""
    try:
        config[group][key] = value
        config.write(open("config.ini", "w"))
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
            logger.debug("[CONFIG] No default background image specified.")
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
        self.api_urls = get_config_item(config,"WEATHER","API_URL").split(" ")
        self.api_refresh_interval = int(get_config_item(config,"WEATHER","REFRESH_INTERVAL"))
        self.city = get_config_item(config,"WEATHER","CITY")
        self.units = get_config_item(config,"WEATHER","UNITS")

@dataclasses.dataclass
class TextBoxConfig:
    """Class to hold the text box configuration"""
    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
        except Exception as exc:
            raise FileNotFoundError("Config file not found") from exc
        self.text = get_config_item(config,"TEXTBOX","TEXT")

@dataclasses.dataclass
class FitbitConfig:
    """Class to hold the fitbit configuration"""
    def __init__(self):
        try:
            config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            config.read("config.ini")
        except Exception as exc:
            raise FileNotFoundError("Config file not found") from exc
        self.api_client_id = get_config_item(config,"FITBIT","API_CLIENT_ID")
        self.api_secret = get_config_item(config,"FITBIT","API_SECRET")
        self.api_urls = get_config_item(config,"FITBIT","API_URL").split(" ")
        self.api_refresh_interval = int(get_config_item(config,"FITBIT","REFRESH_INTERVAL"))
        self.api_key = get_config_item(config,"FITBIT","API_KEY")
        self.api_access_token = get_config_item(config,"FITBIT","API_ACCESS_TOKEN")
        self.api_refresh_token = get_config_item(config,"FITBIT","API_REFRESH_TOKEN")
        expiry = get_config_item(config,"FITBIT","API_EXPIRY")
        if expiry == "":
            self.api_expiry = 0
        else:
            self.api_expiry = float(get_config_item(config,"FITBIT","API_EXPIRY"))
        self.user_id = get_config_item(config,"FITBIT","USER_ID")
        self.units = get_config_item(config,"FITBIT","UNITS")
        self.scope = get_config_item(config,"FITBIT","API_SCOPE")
        try:
            self.code_verifier = get_config_item(config,"FITBIT","CODE_VERIFIER")
            if self.code_verifier == "":
                logger.warning("[CONFIG] No code verifier found in config.ini")
                self.code_verifier = token_hex(32)
                set_config_item(config,"FITBIT","CODE_VERIFIER",self.code_verifier)
        except KeyError:
            logger.warning("[CONFIG] No code verifier found in config.ini")
            self.code_verifier = token_hex(32)
            set_config_item(config,"FITBIT","CODE_VERIFIER",self.code_verifier)
    
    def set_tokens(self, access_token, refresh_token, expiry, user_id):
        """Sets the access token and refresh token"""
        try:
            config = configparser.ConfigParser()
            config.read("config.ini")
        except Exception as exc:
            raise FileNotFoundError("Config file not found") from exc
        self.api_access_token = access_token
        self.api_refresh_token = refresh_token
        self.api_expiry = expiry
        self.user_id = user_id
        if expiry is not str:
            expiry = str(expiry)
        set_config_item(config,"FITBIT","API_ACCESS_TOKEN",access_token)
        set_config_item(config,"FITBIT","API_REFRESH_TOKEN",refresh_token)
        set_config_item(config,"FITBIT","API_EXPIRY",expiry)
        set_config_item(config,"FITBIT","USER_ID",user_id)

_CONFIG = Config()
_TEXTBOX_CONFIG = TextBoxConfig()
_WEATHER_CONFIG = WeatherConfig()
_FITBIT_CONFIG = FitbitConfig()

def get_config():
    """Returns the currently loaded configuration"""
    return _CONFIG

def get_textbox_config():
    """Returns the currently loaded textbox configuration"""
    return _TEXTBOX_CONFIG

def get_weather_config():
    """Returns the currently loaded weather configuration"""
    return _WEATHER_CONFIG

def get_fitbit_config():
    """Returns the currently loaded fitbit configuration"""
    return _FITBIT_CONFIG
