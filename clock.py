"""This module is responsible for the clock display on the e-ink screen.
    It checks changes to the display and updates the screen accordingly."""

import logging

import asyncio

from lib.frame_builder.frame import Frame
from lib.waveshare_epd import epd2in13_V4

from constants import get_config

logger = logging.getLogger()

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
        logger.info("[Clock] Clock Initialised")

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
            self.init()
            self.set_screen()
            logger.debug("[Clock] Starting Clock...")
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
