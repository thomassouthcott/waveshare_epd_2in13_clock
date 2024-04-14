from lib.waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new('1', (self.height, self.width), 255)

        ##Add Background to Image
        ##Clock and Panel v-align and Clock h-align