"""This module is responsible for the clock display on the e-ink screen.
    It checks changes to the display and updates the screen accordingly."""

import logging

import asyncio

from lib.frame_builder.frame import Frame
from lib.waveshare_epd import epd2in13_V4

from constants import get_config

logger = logging.getLogger(get_config().prog)

class Clock():
    """Class to handle the clock display on the e-ink screen. 
        Use the run_clock method to start the clock."""
    def __init__(self):
        logger.debug("[epd2in13_V4] Initialising Clock...")
        self._epd = epd2in13_V4.EPD()
        self._frame = Frame(
            (
                self._epd.height,
                self._epd.width
            ),
            (
                get_config().frame.v_alignment,
                get_config().frame.h_alignment
            )
        )
        logger.info("[epd2in13_V4] (%sx%s)",self._epd.height, self._epd.width)

    def init(self):
        """Send the initialise command to the display."""
        logger.debug("[epd2in13_V4] Initialising the display...")
        self._epd.init()
        self._epd.Clear()
        logger.info("[epd2in13_V4] Display initialised")

    def shutdown(self):
        """Send the sleep command to the display."""
        logger.debug("[epd2in13_V4] Shutting down the display...")
        self._epd.init()
        self._epd.Clear()
        self._epd.sleep()
        logger.info("[epd2in13_V4] Display shutdown")

    def set_screen(self):
        """Set the screen to the frame image."""
        logger.info(
            "[epd2in13_V4] Setting screen to image dimensions (%s,%s)",
            self._epd.height, self._epd.width
        )
        self._epd.displayPartBaseImage(self._epd.getbuffer(self._frame.get_image()))

    def update_screen(self):
        """Update the screen with the frame image."""
        logger.info("[epd2in13_V4] Updating screen from frame image")
        self._epd.displayPartial(self._epd.getbuffer(self._frame.get_image()))

    def set_text_panel(self, text):
        """Set the text panel to the specified string."""
        self._frame.set_text_panel(text)

    def set_alignment(self, vertical_alignment, horizontal_alignment):
        """Set the alignment of the frame."""
        self._frame.set_vertical_alignment(vertical_alignment)
        self._frame.set_horizontal_alignment(horizontal_alignment)

    def get_info_panel_descriptions(self):
        """Return the descriptions of the info panels."""
        return "\n".join(self._frame.get_info_panel_descriptions())+"\n"

    def get_banner_panel_descriptions(self):
        """Return the descriptions of the banner panels."""
        return "\n".join(self._frame.get_banner_panel_descriptions())+"\n"

    async def run_clock(self):
        """Async function to run the clock. Sleeps for 0.33 seconds to allow for cli."""
        try:
            logger.debug("Initialising display...")
            self.init()
            self.set_screen()
            logger.debug("Display initialised")
            self._frame.set_background(get_config().frame.default_background)
            while True:
                image = self._frame.draw()
                if image is not None:
                    self.update_screen()
                else:
                    await asyncio.sleep(0.33)
        except IOError as e:
            logger.error("\tIOError")
            logger.error(e)
            self.shutdown()
            exit(1)

        except asyncio.CancelledError:
            logger.debug("Cancelled")
            self.shutdown()
            exit()

        except KeyboardInterrupt:
            print()
            self.shutdown()
            exit()

        except SystemExit:
            logger.debug("System Exit")
            self.shutdown()
            exit()

        except e:
            logger.error("Something went wrong...")
            logger.error(e)
            self.shutdown()
            exit()
