"""ServicePanel class for panels that seed from APIs."""
import logging
import time

from lib.frame_builder.panel import Panel


logger = logging.getLogger()

##Class for Panels which seed from APIs
class ServicePanel(Panel):
    """Class for panels that seed from APIs."""
    def __init__(self, dimensions, alignment, service=None, logname="Service", text="loading...",
                 fontsize=24):
        super().__init__(dimensions, alignment, logname, text, fontsize)
        self._drawn = False
        self._latest_change = None
        self._last_refresh = None
        self._description = "This description is given when the panels command is called."
        self._service = service
        super().draw()

    def draw(self):
        """Draws the panel."""
        self.update()
        if self._drawn:
            return None, None
        super().draw()
        self._draw()
        self._drawn = True
        return self._image, self._latest_change

    def _draw(self):
        pass

    def update(self):
        """Updates the panel."""
        if self._service is None:
            return
        if self._last_refresh is None:
            self._update()
            return
        if time.time() - self._last_refresh < self._service.api_refresh_interval:
            return
        self._update()

    def _update(self):
        pass

    def get_description(self):
        """Returns the description of the panel."""
        name = self._logname.replace("Panel", "")
        return f"{name} Panel: {self._description}"
