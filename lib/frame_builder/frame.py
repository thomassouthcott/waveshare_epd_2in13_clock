""" This module is responsible for creating a frame for the screen. 
    Is used to display a white box with black border."""

import logging
import os

from PIL import Image, ImageOps

from constants import HorizontalAlignment, VerticalAlignment, get_config, picdir
from lib.frame_builder.clock_panel import ClockPanel
import lib.frame_builder.info_panel as InfoPanels
import lib.frame_builder.banner_panel as BannerPanels

logger = logging.getLogger()

class Frame:
    """Frame class, creates frames for the screen."""
    def __init__(self, dimensions, alignment):
        #Alignment
        self._alignment = alignment
        self._alignment_changed = True

        #Base image to paste onto
        self._dimensions = dimensions
        self._image = Image.new('1', self._dimensions, 255)

        #Background image
        self._background = ImageOps.expand(
            Image.new('1', (self._dimensions[0]-2, self._dimensions[1]-1), 255),
            border=(1,0,1,1)
        )
        self._backgrounddrawn = True

        #Panels
        self._clock_panel = ClockPanel(self._alignment)
        self._info_panels = []
        self._info_panels.append(InfoPanels.TextPanel(self._dimensions,self._alignment))
        #Fiddle
        self._info_panels[0].set_text("Weather Panel")
        self._info_panels[0].draw()
        ##Dee dee
        self._banner_panels = []
        self._banner_panels.append(BannerPanels.BannerPanel(self._alignment))
        #Draw!
        logger.debug("[Frame] Initialising...")
        self.draw(True)
        logger.debug("[Frame] Initialised.")

    def set_vertical_alignment(self, alignment):
        """Set the vertical alignment of the clock in frame."""
        self._alignment = (
            alignment,
            self._alignment[1]
        )
        self._clock_panel.set_vertical_alignment(alignment)
        for panel in self._info_panels:
            panel.set_vertical_alignment(alignment)
        for panel in self._banner_panels:
            panel.set_vertical_alignment(alignment)

        self._alignment_changed = True

    def set_horizontal_alignment(self, alignment):
        """Set the horizontal alignment of the clock in frame."""
        self._alignment = (
            self._alignment[0],
            alignment
        )
        self._clock_panel.set_horizontal_alignment(alignment)
        for panel in self._info_panels:
            panel.set_horizontal_alignment(alignment)
        for panel in self._banner_panels:
            panel.set_horizontal_alignment(alignment)

        self._alignment_changed = True

    def set_background(self, filename):
        """Set the background of the frame. Black and White, uncompressed BMP."""
        path=os.path.join(picdir, filename)
        if not os.path.exists(path):
            logging.error("[Frame] File not found at pic/%s", filename)
            raise FileNotFoundError()

        border = (1,0,1,0)
        clock_height = self._clock_panel.get_dimensions()[1]
        banner_height = self._banner_panels[0].get_dimensions()[1]
        panels_height = clock_height + banner_height
        self._background=ImageOps.expand(
            Image.open(path).resize(
                (
                    self._dimensions[0]-2,
                    self._dimensions[1]-panels_height
                ),
                Image.Resampling.BOX
            ),
            border=border
        )
        self._backgrounddrawn = False

    def set_text_panel(self, text):
        """Set the text of the text panel."""
        #Get the text panel
        self._info_panels[0].set_text(text)
        return text

    def get_info_panel_descriptions(self):
        """Return the descriptions of the info panels."""
        return [panel.getdescription() for panel in self._info_panels]

    def get_banner_panel_descriptions(self):
        """Return the descriptions of the banner panels."""
        return [panel.getdescription() for panel in self._banner_panels]

    def _draw_background(self):
        if not self._backgrounddrawn:
            self._backgrounddrawn = True
            return self._background
        logger.debug("[Frame] Background has not changed. Not drawing the background.")
        return None

    def _paste_background(self, image=None):
        offset = 0
        if self._alignment[0] == VerticalAlignment.BOTTOM:
            offset = self._banner_panels[0].get_dimensions()[1]
        else:
            offset = self._clock_panel.get_dimensions()[1]
        box = (
            0,
            offset
        )
        if image is None:
            self._image.paste(self._background, box)
        else:
            image.paste(self._background, box)

    def _paste_clock(self, image=None):
        x_offset = 0
        y_offset = 0
        if self._alignment[1] == HorizontalAlignment.RIGHT:
            x_offset = self._dimensions[0] - self._clock_panel.get_dimensions()[0]
        if self._alignment[0] == VerticalAlignment.BOTTOM:
            y_offset = self._dimensions[1] - self._clock_panel.get_dimensions()[1]
        box = (
            x_offset,
            y_offset
        )
        if image is None:
            self._image.paste(self._clock_panel.get_image(), box)
        else:
            image.paste(self._clock_panel.get_image(), box)

    def _paste_info_panel(self, image=None):
        #TODO: Get the current panel
        current_info_panel = self._info_panels[0]
        x_offset = 0
        y_offset = 0
        if self._alignment[1] == HorizontalAlignment.LEFT:
            x_offset = self._clock_panel.get_dimensions()[0]
        if self._alignment[0] == VerticalAlignment.BOTTOM:
            y_offset = self._dimensions[1] - self._clock_panel.get_dimensions()[1]
        box = (
            x_offset,
            y_offset
        )
        if image is None:
            self._image.paste(current_info_panel.get_image(), box)
        else:
            image.paste(current_info_panel.get_image(), box)

    def _paste_banner_panel(self, image=None):
        #TODO: Get the current panel
        current_banner_panel = self._banner_panels[0]
        y_offset = 0
        if self._alignment[0] == VerticalAlignment.BOTTOM:
            y_offset = self._dimensions[1] - current_banner_panel.get_dimensions[1]
        box = (
            0,
            y_offset
        )
        if image is None:
            self._image.paste(current_banner_panel.get_image(), box)
        else:
            image.paste(current_banner_panel.get_image(), box)

    def draw(self, override=False):
        """Draw the frame. Returns None if nothing has changed."""
        if(override or self._alignment_changed):
            if self._alignment_changed :
                self._alignment_changed = False
                logger.debug("[Frame] Alignment changed. Redrawing the screen, no panels updated.")
            else:
                logger.debug("[Frame] Override set. Redrawing the screen, no panels updated.")
            self._paste_background()
            self._paste_clock()
            self._paste_info_panel()
            self._paste_banner_panel()
            self._image = self._image.rotate(180)
            return self._image
        ##Library displays upside down, so rotate 180
        frame = self._image.rotate(180)
        background_image = self._draw_background()
        if background_image is not None:
            self._paste_background(frame)

        clock_image = self._clock_panel.draw()
        if clock_image is not None:
            self._paste_clock(frame)

        info_image = self._info_panels[0].draw()
        if info_image is not None:
            self._paste_info_panel(frame)

        banner_image = self._banner_panels[0].draw()
        if banner_image is not None:
            self._paste_banner_panel(frame)

        ##Library displays upside down, so rotate 180
        if(clock_image is not None or background_image is not None or
           info_image is not None or banner_image is not None):
            frame = frame.rotate(180)
            self._image = frame
            return self._image
        return None

    def get_image(self):
        """Return the image of the frame."""
        return self._image
