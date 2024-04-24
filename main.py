"""Main entry point and Cli for the program."""
import argparse
import logging

import asyncio
from aioconsole import AsynchronousCli

from constants import HorizontalAlignment, VerticalAlignment, get_config
import clock
from lib.frame_builder.info_panel import get_info_types

# Set up logging
# from https://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
# thanks https://stackoverflow.com/users/1537951/waterboy
# the first result when I searched "python logging to file and console"
formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s")
logger = logging.getLogger()

fileHandler = logging.FileHandler(get_config().logging.file)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logger.setLevel(get_config().logging.level)

prog= clock.Clock()

def log_input(func):
    """Decorator to log the input of the function."""
    async def wrapper(reader, writer, *args, **kwargs):
        """Wrapper for the function."""
        logger.info("[CLI] [%s] Received input: %s", func.__name__, args)
        await func(*args, **kwargs)
    return wrapper

async def set_background(i):
    """Set the background image of the screen."""
    pass

async def set_text(reader, writer, text):
    """Set the text of the Text Panel."""
    prog.set_text_panel(text)

async def set_panel(reader, writer, panelType):
    """Set the PanelType of the InfoPanel."""
    #if panelType in getPanelTypes().keys():
        #prog.setPanel(panelType)
    #else:
        #prog.setPanel()
    pass

async def align(reader, writer, x, y):
    """Set the alignment of the clock."""
    prog.set_alignment(VerticalAlignment[x], HorizontalAlignment[y])

async def get_info_panel_descriptions(reader, writer):
    """Print the descriptions of the InfoPanels."""
    writer.write(prog.get_info_panel_descriptions())

def make_cli():
    """Create the Command Line Interface for the program."""
    background_parser = argparse.ArgumentParser(
        description="Set the background image of the screen"
    )
    background_parser.add_argument('-i', type=str, help="Filename of the image in /bmp/",
                                  required=True)

    text_parser = argparse.ArgumentParser(description="Set the text of the Text Panel")
    text_parser.add_argument('-t', type=str, help="Text to display", required=True)

    panel_parser = argparse.ArgumentParser(description="Set the PanelType of the InfoPanel")
    panel_parser.add_argument('-p', type=str, help="PanelType to display",
                             required=True, choices=get_info_types().keys())

    align_parser = argparse.ArgumentParser(description="Set the alignment of the clock")
    align_parser.add_argument("-x",type=str, help="Vertical Alignment",
                             required=True, choices=VerticalAlignment.__members__.keys())
    align_parser.add_argument("-y",type=str, help="Horizontal Alignment",
                             required=True, choices=HorizontalAlignment.__members__.keys())

    get_panel_info_parser = argparse.ArgumentParser(
        description="Get the descriptions of the InfoPanels"
    )

    commands = {
        "background": (set_background, background_parser),
        "display": (set_text, text_parser),
        "set-panel": (set_panel, panel_parser),
        "align": (align, align_parser),
        "panels": (get_info_panel_descriptions, get_panel_info_parser)
        #"toggle-panel": (togglepanel, toggleparser), Toggles panel on/off
        #will require adding show logic to the infopanel class
        }
    return AsynchronousCli(commands, prog="Clock")

def main():
    """Main entry point for the program."""
    task = None
    try:
        logger.debug("[Main] Starting main...")
        logger.info(r"""
        __________        _________ .__                 __    
        \______   \___.__.\_   ___ \|  |   ____   ____ |  | __
        |     ___<   |  |/    \  \/|  |  /  _ \_/ ___\|  |/ /
        |    |    \___  |\     \___|  |_(  <_> )  \___|    < 
        |____|    / ____| \______  /____/\____/ \___  >__|_ \
                  \/             \/                 \/     \/
        """)
        logger.info("Version: %s", get_config().version)
        logger.info("Author: %s", get_config().author)
        loop = asyncio.get_event_loop()
        task = loop.create_task(prog.run_clock())
        loop.run_until_complete(make_cli().interact())
        loop.run_forever()
    except SystemExit:
        logger.info("[Main] Exiting...")
        if not task.done():
            task.cancel()
        loop.run_until_complete(task)
        loop.stop()
        loop.close()

main()
