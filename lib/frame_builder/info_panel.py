"""InfoPanel Classes for displaying information next to the time on the eInk display."""

import logging

from PIL import Image,ImageOps

from constants import HorizontalAlignment, get_config, InfoTypes
from lib.frame_builder.service_panel import ServicePanel

logger = logging.getLogger(get_config().prog)

def get_info_types():
    """Returns a dictionary of InfoPanel child classes."""
    return {
        InfoTypes.TEXT: TextPanel,
        InfoTypes.WEATHER: WeatherPanel
    }

def get_info(panelType=None, screendimensions=None):
    """Returns an InfoPanel child class based on the panelType."""
    return get_info_types().get(
        panelType,
        lambda args: logger.debug("panelType [%s] not recognised. Ignoring Panel.", panelType)
    )(screendimensions)

##Class for Panels next to the time
class InfoPanel(ServicePanel):
    """Class for panels that display information next to the time."""
    def __init__(self, screen_dimensions, alignment,
                 logname="InfoPanel", fontsize=24):
        super().__init__(
            (
                screen_dimensions[0]-get_config().frame.clock_dimensions[0],
                get_config().frame.clock_dimensions[1]
            ),
            alignment, logname=logname, fontsize=fontsize)
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
    def __init__(self, screen_dimensions, alignment, logname="TextPanel", fontsize=24):
        super().__init__(screen_dimensions, alignment, logname, fontsize)
        self._description = "This panel is used to display text."

    def _draw(self):
        self._imagedraw.text((0,0), self._text, font = self._font, fill = 0)

    def set_text(self, text):
        """Sets the text of the panel."""
        logger.info(
            "[%s Panel] Setting text to %s",
            self._logname.replace("Panel", ""), text.replace("\n", " ")
        )
        self._text = text
        self._drawn = False

class WeatherPanel(InfoPanel):
    """Class for panels that display the weather."""
    def __init__(self, screen_dimensions, alignment, logname="WeatherPanel", fontsize=24):
        super().__init__(screen_dimensions, alignment, logname, fontsize)
        self._description = "This panel is used to display the weather."

##GMAIL PANEL (UNREAD EMAILS (UNREAD IMPORTANT), (ALTENATES BETWEEN) MULTI-ACCOUNT SUPPORT)

##DATE PANEL (DATE, MULTI-ACCOUNT SUPPORT)
