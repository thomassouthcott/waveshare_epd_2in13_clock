from lib.waveshare_epd import epd2in13_V4

import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
import time
from PIL import Image,ImageDraw,ImageFont

class Clock:
    def __init__(self):        
        self.font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
        self.image = self.canvas()

    def canvas(self):
        return Image.new('1', (82, 35), 255)

    # Draw the time on the image
    def draw(self, time): 
        self.image = self.canvas()  
        time_draw = ImageDraw.Draw(self.image)
        time_draw.text((0,0), time.strftime('%H:%M'), font = self.font, fill = 0)
        return self.image