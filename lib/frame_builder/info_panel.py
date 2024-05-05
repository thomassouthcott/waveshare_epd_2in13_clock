"""InfoPanel Classes for displaying information next to the time on the eInk display."""

import logging
import time

from PIL import Image,ImageOps,ImageFont

from config import get_config
from constants import HorizontalAlignment, InfoTypes
from image_helper import get_weather_icon, get_fitbit_icon
from lib.frame_builder.service_panel import ServicePanel
from lib.services.weather_api import WeatherService
from lib.services.fitbit_api import FitbitService

logger = logging.getLogger()

def get_info_types():
    """Returns a dictionary of InfoPanel child classes."""
    return {
        InfoTypes.TEXT: TextPanel,
        InfoTypes.WEATHER: WeatherPanel
    }

def get_info(panel_type=None, screendimensions=None):
    """Returns an InfoPanel child class based on the panelType."""
    return get_info_types().get(
        panel_type,
        lambda args: logger.debug("panel_type [%s] not recognised. Ignoring Panel.", panel_type)
    )(screendimensions)

##Class for Panels next to the time
class InfoPanel(ServicePanel):
    """Class for panels that display information next to the time."""
    def __init__(self, screen_dimensions, alignment, service = None,
                 logname="Info", fontsize=24):
        super().__init__(
            (
                screen_dimensions[0]-get_config().frame.clock_dimensions[0],
                get_config().frame.clock_dimensions[1]
            ),
            alignment, service, logname=logname, fontsize=fontsize)
        self._drawn = False
        self._description = "This description is given when the panels command is called."
        super().draw()

    def _image_factory(self):
        """Create a new image with missing top or bottom border."""
        border = (0,1,1,1) if (self._alignment[1] == HorizontalAlignment.LEFT) else (1,1,0,1)
        return ImageOps.expand(
            Image.new('1', (self._dimensions[0]-1, self._dimensions[1]-2), 255),
            border=border
        )

class TextPanel(InfoPanel):
    """Class for panels that display text."""
    def __init__(self, screen_dimensions, alignment, logname="Text", fontsize=24):
        super().__init__(screen_dimensions, alignment, logname=logname, fontsize=fontsize)
        self._description = "This panel is used to display text."

    def _draw(self):
        self._imagedraw.text((0,0), self._data, font = self._font, fill = 0)
        self._latest_change = f"Text now displays {self._data}"

    def set_text(self, text):
        """Set the text of the text panel."""
        self._data = text
        self._drawn = False

DATE_FORMAT = "%d/%m/%Y"

class DatePanel(InfoPanel):
    """Class for panels that display the current date."""
    def __init__(self, screen_dimensions, alignment, logname="Date", fontsize=24):
        super().__init__(screen_dimensions, alignment, logname=logname, fontsize=fontsize)
        self._description = "This panel is used to display the current date."

    def _draw(self):
        self._imagedraw.text((26,3), self._data, font = self._font, fill = 0)
        self._latest_change = f"Date now displays {self._data}"

    def update(self):
        if (self._last_refresh is None or self._data != time.strftime(DATE_FORMAT)):
            self._data = time.strftime(DATE_FORMAT)
            self._drawn = False
            self._last_refresh = time.time()

class WeatherPanel(InfoPanel):
    """Class for panels that display the weather."""
    def __init__(self, screen_dimensions, alignment, logname="Weather", fontsize=18):
        super().__init__(screen_dimensions, alignment, WeatherService(), logname, fontsize)
        self._description = "This panel is used to display the weather."

    def _update(self):
        self._last_refresh = time.time()
        response = self._service.get_data()
        if response is None:
            self._drawn = True
            return
        if isinstance(self._data, dict):
            if self._data["icon"] != response["icon"]:
                self._data["icon"] = response["icon"]
                self._drawn = False
            if self._data["temp"] != response["temp"]:
                self._data["temp"] = response["temp"]
                self._drawn = False
            if self._data["description"] != response["conditions"]:
                self._data["description"] = response["conditions"]
                self._drawn = False
        else:
            self._drawn = False
            self._data = dict()
            self._data["icon"] = response["icon"]
            self._data["temp"] = response["temp"]
            self._data["description"] = response["conditions"]

    def _draw(self):
        if isinstance(self._data, dict):
            self._draw_temp()
            self._draw_conditions()
            self._paste_icon()
            self._latest_change = f"Weather now displays {self._convert_temp(self._data['temp'])} and {self._data['description']}"
        else:
            self._imagedraw.text((4,4), 'loading...', font = self._font, fill = 0)
    
    def _paste_icon(self):
        """Paste the weather icon onto the image."""
        #Get the weather icon folder in pic
        icon = Image.open(get_weather_icon(self._data["icon"]))
        self._image.paste(icon, (2,2))

    def _draw_temp(self):
        """Draw the temperature on the image."""
        temp = self._convert_temp(self._data["temp"])
        font = ImageFont.truetype(self._font.path, 26)
        self._imagedraw.text((32,2), temp[0:4], font = font, fill = 0)
        self._imagedraw.text((88,2), temp[4::1], font = self._font, fill = 0)

    def _draw_conditions(self):
        """Draw the weather conditions on the image."""
        ##need to truncate text if too long
        #how too long?
        font = ImageFont.truetype(self._font.path, 14)
        print(f"space available: {self._dimensions[0]-90}, text length: {len(self._data['description'])}")
        self._imagedraw.text((84,16), self._data["description"], font = font, fill = 0)

    def _convert_temp(self, temp):
        """Convert the temperature to the correct units."""
        if self._service.units == "imperial":
            return f"{str(temp)[0:4]}°F"
        return f"{str(float(temp - 32) * 5 / 9)[0:4]}°C"

##GMAIL PANEL (UNREAD EMAILS (UNREAD IMPORTANT), (TOTAL OF) MULTI-ACCOUNT SUPPORT)

class FitbitPanel(InfoPanel):
    """Class for panels that display fitbit data."""
    def __init__(self, screen_dimensions, alignment, logname="Fitbit", fontsize=28):
        super().__init__(screen_dimensions, alignment, FitbitService(), logname=logname, fontsize=fontsize)
        self._description = "This panel is used to display fitbit steps."

    def _update(self):
        self._last_refresh = time.time()
        response = self._service.get_data()
        if response is not None:
            if self._data is not None or self._data['summary']['steps'] != response['summary']['steps']:
                self._drawn = False
            self._data = response
            

    def _draw(self):
        if self._data is None:
            self._imagedraw.text((4,4), 'loading...', font = self._font, fill = 0)
            return
        self._draw_icon()
        self._draw_steps(self._data['summary']['steps'],self._data['goals']['steps'])
        self._latest_change = f"Fitbit now displays {self._data['summary']['steps']}/{self._data['goals']['steps']} steps"

    def _draw_icon(self):
        """Draw the fitbit icon on the image."""
        icon = Image.open(get_fitbit_icon("steps")).resize((24,24))
        self._image.paste(icon, (3,6))

    def _draw_steps(self, actual, goal):
        """Draw the steps on the image."""
        self._imagedraw.text((32,-3), f"{actual:06}", font = self._font, fill = 0)
        font = ImageFont.truetype(self._font.path, 12)
        self._imagedraw.text((112,21), f"of {goal}", font = font, fill = 0)