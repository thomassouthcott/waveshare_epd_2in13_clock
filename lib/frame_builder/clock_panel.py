""" This module is responsible for creating the clock panel. 
    It is a subclass of the Panel class and is used to display the current time."""
import logging
import time

from lib.frame_builder.panel import Panel

from config import get_config

logger = logging.getLogger()

class ClockPanel(Panel):
    """Clock Panel class, displays the current time."""
    def __init__(self, alignment):
        super().__init__(get_config().frame.clock_dimensions, alignment, "Clock",
                         time.strftime('%H:%M'), 32)
        self._imagedraw.text((0,0), self._text, font = self._font, fill = 0)

    # Draw the time on the image
    def draw(self):
        """Draw the clock panel image."""
        if self._text == time.strftime('%H:%M'):
            return None, None
        self._text = time.strftime('%H:%M')
        super().draw()
        self._imagedraw.text((0,0), self._text, font = self._font, fill = 0)
        return self._image, f"Clock now displays {self._text}"
