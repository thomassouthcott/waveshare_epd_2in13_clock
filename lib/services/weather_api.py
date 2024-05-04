"""Class for Weather Service."""
import time
import logging

import requests

from config import get_weather_config
from lib.services.api import APIService

logger = logging.getLogger()

class WeatherService(APIService):
    """Dataclass for API services."""
    def __init__(self):
        super().__init__(get_weather_config().api_key, get_weather_config().api_urls, get_weather_config().api_refresh_interval)
        self.city = get_weather_config().city
        self.units = get_weather_config().units

    def _request(self):
        response = requests.request("GET", self.api_urls[0] + self.city, params={"key": self.api_key, "include":"current", "iconSet":"icons1"}, timeout=10)
        logger.debug("[WEATHER] %i, %s", response.status_code, response.json())
        json = response.json()
        # Check if the API returned an error
        if "error" in json:
            logger.error("[WEATHER] %s", json["error"])
            return None
        return json["currentConditions"]
