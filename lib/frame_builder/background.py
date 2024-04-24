"""Class to represent background images."""
import logging
import time

from PIL import Image, ImageOps

from constants import check_image_path, get_image_path, get_all_images, get_config

logger = logging.getLogger()

class Background:
    """Class to represent background images."""
    def __init__(self, screen_dimensions):
        self._image = None
        self._drawn = True
        self._name = None
        self._slideshow = None
        self._screen_dimensions = screen_dimensions

    def get_image(self):
        """Return the background image."""
        if self._image is None:
            logger.error("[Background] No background image set.")
            return Image.new('1', self._screen_dimensions, 255)
        return self._image

    def set_image(self, filename, top, bottom):
        """Set the background of the frame. Black and White, uncompressed BMP."""
        if check_image_path(filename) is False:
            logger.error("Invalid image path: %s", filename)
            return
        self._name = filename
        border = (1,0,1,0)
        image = Image.open(get_image_path(filename)).resize(self._screen_dimensions, Image.BICUBIC)
        self._image=ImageOps.expand(
            image.crop(
                (1, top, self._screen_dimensions[0] - 1, self._screen_dimensions[1] - bottom)
            ),
            border=border
        )
        self._drawn = False

    def draw(self):
        """Draw the background image to the frame."""
        if not self._drawn:
            self._drawn = True
            logger.debug("[Frame] Drawing background.")
            return self._image, f"Drawing pic/{self._name} as background"
        return None, None

class Slideshow(Background):
    """Class to represent a slideshow of background images."""
    def __init__(self, screen_dimensions, top, bottom):
        super().__init__(screen_dimensions)
        self._top = top
        self._bottom = bottom
        self._slideshow = []
        self._current = 0
        self._last_change = None
        for image in get_all_images():
            self._slideshow.append(image)
        logger.info("[Slideshow] %d images found.", len(self._slideshow))
        self.draw()

    def draw(self):
        """Move to the next image in the slideshow."""
        if self._last_change is not None:
            if time.time() - self._last_change < get_config().frame.slide_interval:
                return None, None
        if len(self._slideshow) == 0:
            logger.warning("[Slideshow] No images in slideshow.")
            return None, None
        if self._current < len(self._slideshow) - 1:
            self._current += 1
        else:
            self._current = 0
        self._last_change = time.time()
        self.set_image(self._slideshow[self._current], self._top, self._bottom)
        return super().draw()
