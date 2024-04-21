""" This module is responsible for creating the clock panel. 
    It is a subclass of the Panel class and is used to display the current time."""
import logging
import time

from lib.FrameBuilder.panel import Panel

from constants import get_config

logger = logging.getLogger(get_config().prog)

class ClockPanel(Panel):
    """Clock Panel class, displays the current time."""
    def __init__(self, v_align, h_align):
        super().__init__(
            get_config().frame.clock_dimensions,
            v_align,
            h_align,
            "Clock",
            time.strftime('%H:%M'),
            32)
        self._imagedraw.text((0,0), self._text, font = self._font, fill = 0)

    # Draw the time on the image
    def draw(self):
        """Draw the clock panel image."""
        if self._text == time.strftime('%H:%M'):
            logger.debug("[%s Panel] Time has not changed. Not drawing the time.", self._logname)
            return None
        self._text = time.strftime('%H:%M')
        super().draw()
        self._imagedraw.text((0,0), self._text, font = self._font, fill = 0)
        return self._image
