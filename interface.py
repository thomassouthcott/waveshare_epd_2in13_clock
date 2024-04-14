#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
bmpdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bmp')

import logging
from lib.waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)
epd = epd2in13_V4.EPD()
frame=Image.new('1', (epd.height, epd.width), 255)
draw = ImageDraw.Draw(frame)
# Display Functions
def init(epd, args=None):
    if(args!=None):
        logging.info("No arguments required for init. Ignoring the arguments.")
    epd.init()
    epd.Clear()
    #100x25
def display_current_time(epd, args=None):   
    if(args!=None):
        logging.info("No arguments required for display_current_time. Ignoring the arguments.") 
    logging.info("Displaying the current time...")
    font32 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
    time_image = Image.new('1', (epd.height, epd.width), 255)
    path=os.path.join(bmpdir, "image.bmp")
    time_image.paste(Image.open(path).resize((epd.height, epd.width)))
    logging.info(frame)
    logging.info("calling image draw...")
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    num = 0
    while (True):
        time_panel = Image.new('1', (82, 35), 255)
        time_draw = ImageDraw.Draw(time_panel)
        time_draw.text((0,0), time.strftime('%H:%M'), font = font32, fill = 0)
        time_image.paste(time_panel, (0,0))
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 1500):
            break


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

##Convert anything into a 250x122 image
def display_fullscreen_image(epd, args):
    if(len(line.strip().split("."))>1 and not (args[0].split(".")[1].lower() == "bmp")):
        logging.error("Invalid argument [0]. Please provide a file .bmp file.")
        return
    path=os.path.join(bmpdir, args[0])
    if(not os.path.exists(path)):
        logging.error(f"File not found at bmp/{args[0]}")    
    frame=Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(frame)
    logging.info("2")
    frame.paste(Image.open(path).resize((epd.width, epd.height)))
    logging.info(frame)
    epd.displayPartial(epd.getbuffer(frame))
    logging.info("4")

##Convert anything into a 122x122 image
def display_image(epd, args):
    if(not len(args)<=3):
        logging.error("Invalid number of arguemnts. Please provide a file name and height and width of the image.")
    if(not (args[0].split(".")[1].lower() == "bmp")):
        logging.error("Invalid argument [0]. Please provide a file .bmp file.")
        return    
    
    path=os.path.join(bmpdir, args[0])

    if(not os.path.exists(path)):
        logging.error(f"File not found at bmp/{args[0]}")
        return

    if(not args[1].isdigit()):
        logging.error("Invalid argument [1]. height must be an integer.")
        return
    
    if(not args[2].isdigit()):
        logging.error("Invalid argument [2]. height must be an integer.")
        return 
    h = int(args[1])
    w = int(args[2])
    logging.info(h)
    logging.info(w)
    ##CREATE FRAME FOR WHOLE SCREEN
    frame=Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(frame)
    logging.info("2")
    frame.paste(Image.open(path).resize((w,h), Image.MESH))
    logging.info(frame)
    epd.displayPartial(epd.getbuffer(frame))
    logging.info("4")

def shutdown(epd, args=None):
    if(args!=None):
        logging.info("No arguments required for shutdown. Ignoring the arguments.") 
    epd.init()
    epd.Clear()
    epd.sleep()
    logging.info("Exiting")

def refresh(epd, args=None):
    if(args!=None):
        logging.info("No arguments required for refresh. Ignoring the arguments.") 
    ##CREATE FRAME FOR WHOLE SCREEN
    frame=Image.new('1', (epd.height, epd.width), 255)
    

##TODO: Add more display functions here
##TODO: Add async handler for stdin so i can have the clock running in the background and accept commands from stdin

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
            "display_image": display_image,
            "exit": shutdown
        }
        switcher.get(command, lambda epd, args: logging.info(f'Command not recognised.\n\tValid Commands are: {switcher.keys()}'))(epd, args)
    shutdown(epd)
##change all the commands to the "frame" Image and "draw" ImageDraw 
##have some commands like write text on the image update partial display whatever that means
##have a command to clear the display
##have a command to refresh the display
##have a command to draw the frame on the display

##loop to keep refresh the display periodically
##  
## background Image
##  - panel for current time "box in the bottom left corner"
##   - draw for current time
##  - changing information panels fill the bottom panel from the right
##  - bottom panel page 0
##   - draw for current date
##   - draw for current weather
##   - draw for unread emails (maybe notifications)
##  - bottom panel page 4
##   - draw for fitbit stats
##  - bottom panel page 3
##   - draw for calendar events
##  - bottom panel page 1
##   - draw for inspirational quotes
##  - bottom panel page 2
##   - draw for bbc news headlines

except IOError as e:
    logging.error("\tIOError")
    logging.error(e)
    shutdown(epd)
    exit(1)
    
except Exception as e:
    logging.error("\t" + type(e).__name__)
    logging.error(e)
    shutdown(epd)
    exit(1)

except KeyboardInterrupt:    
    print()
    shutdown(epd)
    exit()

except SystemExit:
    logging.info("System Exit")
    shutdown(epd)
    exit()