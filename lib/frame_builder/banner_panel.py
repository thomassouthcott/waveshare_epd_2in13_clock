"""BannerPanel Classes for displaying information opposite the time on the eInk display."""

import logging

from PIL import Image,ImageOps

from config import get_config
from constants import BannerTypes
from lib.frame_builder.service_panel import ServicePanel

logger = logging.getLogger()

def get_banner_types():
    """Returns a dictionary of InfoPanel child classes."""
    return {
        BannerTypes.QOTD: BannerPanel
    }

def get_banner(panel_type=None, screendimensions=None):
    """Returns an BannerPanel child class based on the panelType."""
    return get_banner_types().get(
        panel_type,
        lambda args: logger.debug("panel_type [%s] not recognised. Ignoring Panel.", panel_type)
    )(screendimensions)

##Class for Full-Length Banner panels opposite the time, maybe scrolling text?
class BannerPanel(ServicePanel):
    """Class for panels that display information opposite the time."""
    def __init__(self, alignment, logname="Banner", fontsize=14):
        super().__init__(get_config().frame.banner_dimensions, alignment,
                         logname=logname, fontsize=fontsize)

    def _image_factory(self):
        return ImageOps.expand(
            Image.new('1', (self._dimensions[0]-2, self._dimensions[1]-2), 255),
            border=(1,1,1,1)
        )
##CALENDAR PANEL (NEXT EVENT, MULTI-ACCOUNT SUPPORT NEXT EVENT FROM ALL)

##NEWS PANEL (NEWS HEADLINES, MULTI-ACCOUNT SUPPORT)

##QUOTE OF THE DAY
