"""EPD driver for Waveshare 2.13inch e-Paper V4"""
import logging
import time

from lib.waveshare_epd import epd2in13_V4

from constants import get_config

logger = logging.getLogger()

REFRESH_TIME = 43200

class EPDDriver:
    """Class to handle the e-Paper display."""
    def __init__(self):
        self._epd = epd2in13_V4.EPD()
        logger.info(
            "[epd2in13_V4] (%sx%s)",
            self._epd.height,
            self._epd.width
        )
        self._last_refresh = time.time()
        self._partial_updates = 0
        self._image = None

    def get_dimensions(self):
        """Return the dimensions of the display."""
        return (self._epd.height, self._epd.width)

    def init(self):
        """Send the initialise command to the display."""
        logger.debug("[epd2in13_V4] Initialising the display...")
        self._epd.init()

    def clear(self):
        """Send the clear command to the display."""
        logger.debug("[epd2in13_V4] Clearing the display...")
        self._epd.Clear()

    def sleep(self):
        """Send the sleep command to the display."""
        logger.debug("[epd2in13_V4] Sending sleep command to the display...")
        self._epd.sleep()

    def set_screen(self, image):
        """Set the screen to the frame image."""
        logger.debug(
            "[epd2in13_V4] Setting screen to image dimensions (%s,%s)",
            self._epd.height, self._epd.width
        )
        if self._partial_updates > 0:
            self._epd.TurnOnDisplay()
        self._partial_updates = 0
        self._image = image
        self._epd.displayPartBaseImage(self._epd.getbuffer(image))

    def update_screen(self, image= None):
        """Update the screen with the frame image."""
        if image is None and time.time() - self._last_refresh >= REFRESH_TIME:
            self.refresh_screen()
            return
        if image is None:
            return
        self.init()
        if self._partial_updates > 6 or time.time() - self._last_refresh >= REFRESH_TIME:
            self.set_screen(image)
            self.sleep()
        else:
            logger.debug("[epd2in13_V4] Updating screen...")
            self._epd.TurnOnDisplayPart()
            self._epd.displayPartial(self._epd.getbuffer(image))
            self._partial_updates += 1
            self._image = image
            self.sleep()

    def refresh_screen(self):
        """Refresh the screen with the frame image."""
        logger.debug("[epd2in13_V4] Refreshing screen...")
        self.init()
        self.clear()
        self._partial_updates += 1
        self.set_screen(self._image)
        self._last_refresh = time.time()
        self.sleep()

    def shutdown(self):
        """Clear then sleep the display."""
        logger.debug("[epd2in13_V4] Shutting down the display...")
        self._epd.init()
        self._epd.Clear()
        self._epd.sleep()
        logger.info("[epd2in13_V4] Display shutdown")
