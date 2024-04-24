""" This module is responsible for creating a panel. 
    Is used to display a white box with black border."""

import logging
import os

from PIL import Image,ImageDraw,ImageFont, ImageOps

from constants import get_config, picdir
logger = logging.getLogger()


class Panel:
    """Panel class, displays a box with 1px border."""
    def __init__(self, dimensions, alignment, logname = "Base Panel",
                 text= "loading...", fontsize=24):
        self._font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), fontsize)
        self._alignment = alignment
        self._dimensions = dimensions
        self._image = self._image_factory()
        self._imagedraw = ImageDraw.Draw(self._image)
        self._text = text
        self._logname= logname
        logger.debug(
            "[%s Panel] [Dimensions: %s, Text: %s, FontSize: %s]",
            self._logname,
            self._dimensions,
            self._text,
            fontsize
        )

    def _image_factory(self):
        """Create a new image with the dimensions of the panel."""
        return ImageOps.expand(
            Image.new('1', (self._dimensions[0]-2, self._dimensions[1]-2), 255),
            border=(1,1,1,1)
        )

    def get_image(self):
        """Return the image of the panel."""
        return self._image

    def get_dimensions(self):
        """Return the dimensions of the panel."""
        return self._dimensions

    def set_vertical_alignment(self, alignment):
        """Set the vertical alignment of the panel."""
        self._alignment = (
            alignment,
            self._alignment[1]
        )
        logger.debug("[%s Panel] Vertical alignment changed to %s", self._logname, alignment)

    def set_horizontal_alignment(self, alignment):
        """Set the horizontal alignment of the panel."""
        self._alignment = (
            self._alignment[0],
            alignment
        )
        logger.debug("[%s Panel] Horizontal alignment changed to %s", self._logname, alignment)

    def get_font(self):
        """Return the font used by the panel."""
        return self._font

    def set_font(self, font):
        """Set the font used by the panel."""
        self._font = font
        logger.debug("[%s Panel] Font changed to %s", self._logname, font)

    def reset_canvas(self):
        """Reset the canvas base image."""
        logger.debug("[%s Panel] Resetting the canvas to %s", self._logname, self._dimensions)
        self._image = self._image_factory()
        self._imagedraw = ImageDraw.Draw(self._image)

    def draw(self):
        """Draw the blank panel on the canvas."""
        logger.debug("[%s Panel] Drawing the canvas", self._logname)
        self.reset_canvas()
