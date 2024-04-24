"""Clear and Shutdown the e-paper display."""

import logging

from lib.waveshare_epd import epd2in13_V4

from config import get_config

log_formatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
logger = logging.getLogger("shutdown")

file_handler = logging.FileHandler(get_config().logging.file)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

logger.debug("[Shutdown] Initialising display...")
epd = epd2in13_V4.EPD()
epd.init()
logger.debug("[Shutdown] Clearing display...")
epd.Clear()
logger.debug("[Shutdown] Putting display to sleep...")
epd.sleep()
logger.debug("[Shutdown] Exiting")
