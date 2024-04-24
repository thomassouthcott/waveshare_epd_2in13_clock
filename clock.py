"""This module is responsible for the clock display on the e-ink screen.
    It checks changes to the display and updates the screen accordingly."""

import logging

import asyncio

from lib.frame_builder.frame import Frame
from lib.epd_driver import EPDDriver

from config import get_config

logger = logging.getLogger()

class Clock():
    """Class to handle the clock display on the e-ink screen. 
        Use the run_clock method to start the clock."""
    def __init__(self):
        logger.debug("[epd2in13_V4] Initialising Clock...")
        self._epd_driver = EPDDriver()
        self._frame = Frame(
            self._epd_driver.get_dimensions(),
            (
                get_config().frame.v_alignment,
                get_config().frame.h_alignment
            ),
            get_config().frame.default_background,
        )
        logger.info("[Clock] Clock Initialised")

    # Command Line Interface Commands
    def set_background(self, image):
        """Set the background of the frame to the specified image."""
        #TODO: Add a slideshow mode for no input
        if image is None:
            logger.info("[Clock] No background image specified. Slideshow mode enabled.")
            self._frame.set_background_slideshow()
        else:
            logger.info("[Clock] Background set to: %s", image)
            self._frame.set_background(image)

    def set_text_panel(self, text):
        """Set the text panel to the specified string."""
        logger.info("[Clock] Text Panel set to: %s", text)
        self._frame.set_text_panel(text)

    def set_alignment(self, vertical_alignment, horizontal_alignment):
        """Set the alignment of the frame."""
        logger.info("[Clock] Alignment set to: %s, %s", vertical_alignment, horizontal_alignment)
        self._frame.set_vertical_alignment(vertical_alignment)
        self._frame.set_horizontal_alignment(horizontal_alignment)

    def get_info_panel_descriptions(self):
        """Return the descriptions of the info panels."""
        logger.info("%s\n","\n".join(self._frame.get_info_panel_descriptions()))

    def get_banner_panel_descriptions(self):
        """Return the descriptions of the banner panels."""
        logger.info("%s\n","\n".join(self._frame.get_banner_panel_descriptions()))

    # Main Clock Function
    async def run_clock(self):
        """Async function to run the clock. Sleeps for 0.33 seconds to allow for cli."""
        try:
            logger.info("[Clock] BEGIN")
            self._epd_driver.init()
            self._epd_driver.clear()
            logger.debug("[Clock] Starting Clock...")
            self._epd_driver.set_screen(self._frame.get_image())
            while True:
                image, changes = self._frame.draw()
                if image is None:
                    self._epd_driver.update_screen(image)
                    await asyncio.sleep(0.33)
                else:
                    logger.info(
                        "[Clock] Updating screen, %s change%s:",
                        len(changes),
                        "s" if len(changes) > 1 else ""
                    )
                    for change in changes:
                        logger.info("[Clock] %s",change)
                    self._epd_driver.update_screen(image)
        except IOError as e:
            logger.error("\tIOError")
            logger.error(e)
            self._epd_driver.shutdown()
            exit(1)

        except asyncio.CancelledError:
            logger.debug("Cancelled")
            self._epd_driver.shutdown()
            exit()

        except KeyboardInterrupt:
            print()
            self._epd_driver.shutdown()
            exit()

        except SystemExit:
            logger.debug("System Exit")
            self._epd_driver.shutdown()
            exit()
