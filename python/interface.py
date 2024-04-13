#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
bmpdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bmp')

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)
# Display Functions
def init(epd, args=None):
    if(args!=None):
        logging.info("No arguments required for init. Ignoring the arguments.")
    epd.init()
    epd.Clear()
    
def display_current_time(epd, args=None):   
    if(args!=None):
        logging.info("No arguments required for display_current_time. Ignoring the arguments.") 
    logging.info("Displaying the current time...")
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    logging.info("calling image draw...")
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font24, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image))


def display_time(epd, args):
    if(len(args[0].split(":")) < 3 or len(args[0].split(":")) > 3 or not all([x.isdigit() for x in args[0].split(":")])):
        logging.error("Invalid arguments. Please provide time in HH:MM:SS format.")
        return
    
    logging.info("Displaying the current time...")
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    logging.info("calling image draw...")
    time_draw.text((120, 80), args[0], font = font24, fill = 0)
    epd.displayPartial(epd.getbuffer(time_image))

def display_fullscreen_image(epd, args):
    if(len(line.strip().split("."))>1 and not (args[0].split(".")[1].lower() == "bmp")):
        logging.error("Invalid arguments. Please provide a file .bmp file.")
        return
    path=os.path.join(bmpdir, args[0])
    if(not os.path.exists(path)):
        logging.error(f"File not found at bmp/{args[0]}")
    image = Image.open(path)
    epd.display_fast(epd.getbuffer(image))

def shutdown(epd, args=None):
    if(args!=None):
        logging.info("No arguments required for shutdown. Ignoring the arguments.") 
    epd.init()
    epd.Clear()
    epd.sleep()

##TODO: Add more display functions here
##TODO: Add async handler for stdin so i can have the clock running in the background and accept commands from stdin

epd = epd2in13_V4.EPD()
try:
    logging.info(f"epd2in13_V4 {epd.width} x {epd.height}")    
    logging.info("Initialising the display")    
    init(epd)
    logging.info("Ready to accept commands. Enter 'exit' to exit.")
    for line in sys.stdin:
        command = line.strip().split(" ")[0]
        if(command == "exit"):
            break
        if(len(line.strip().split(" "))>1):
            args = line.strip().split(" ")[1:]
        else:
            args = None

        logging.info(f"Command: {command} Args: {args}")
        
        switcher = {
            "display_current_time": display_current_time,
            "display_time": display_time,
            "display_fullscreen_image": display_fullscreen_image,
            "exit": shutdown
        }
        switcher.get(command, lambda epd, args: logging.info(f'Command not recognised.\n\tValid Commands are: {switcher.keys()}'))(epd, args)
    shutdown(epd)

except IOError as e:
    logging.error("\tIOError")
    logging.error(e)
    shutdown(epd)
    logging.info("Exiting")
    exit(1)
    
except Exception as e:
    logging.error("\t" + type(e).__name__)
    logging.error(e)
    shutdown(epd)
    logging.info("Exiting")
    exit(1)

except KeyboardInterrupt:    
    print()
    shutdown(epd)
    exit()

except SystemExit:
    logging.info("System Exit")
    shutdown(epd)
    logging.info("Exiting")
    exit()