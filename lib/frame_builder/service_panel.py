"""ServicePanel class for panels that seed from APIs."""
import logging

from lib.frame_builder.panel import Panel

from constants import get_config

logger = logging.getLogger(get_config().prog)

##Class for Panels which seed from APIs
class ServicePanel(Panel):
    """Class for panels that seed from APIs."""
    def __init__(self, dimensions, alignment, logname="ServicePanel", text="loading...",
                 fontsize=24):
        super().__init__(dimensions, alignment, logname, text, fontsize)
        self._drawn = False
        self._description = "This description is given when the panels command is called."
        super().draw()

    def draw(self):
        """Draws the panel."""
        if self._drawn:
            logger.debug("[%s Panel] Text has not changed. Not drawing the text", self._logname)
            return None
        super().draw()
        self._draw()
        self._drawn = True
        return self._image

    def _draw(self):
        pass

    def get_description(self):
        """Returns the description of the panel."""
        name = self._logname.replace("Panel", "")
        return f"{name} Panel: {self._description}"
