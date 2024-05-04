"""Helper functions for images."""
import logging
import os

logger = logging.getLogger()
#Images
picdir = os.path.join(
    os.path.dirname(
        os.path.realpath(__file__)
    ),
    'pic'
)

def get_image_path(filename):
    """Return the full path of the image."""
    return os.path.join(picdir, filename)

def check_image_path(filename):
    """Check if the image path is valid.
        - Must be a .bmp file
        - Must exist in the /pic/ directory"""
    if not filename.endswith(".bmp"):
        logger.error("File must be a .bmp file")
        raise ValueError("File must be a .bmp file")
    if not os.path.exists(get_image_path(filename)):
        logger.error("File not found at pic/%s",filename)
        raise FileNotFoundError()
    return True

def get_all_images():
    """Return a list of all images in the /pic/ directory"""
    return [f for f in os.listdir(picdir) if f.endswith(".bmp")]

def get_weather_icon(icon):
    """Return the full path of the weather icon."""
    if os.path.exists(os.path.join(picdir, "weather", f"{icon}.bmp")):
        return os.path.join(picdir, "weather", f"{icon}.bmp")
    logger.error("Weather icon %s not found", icon)