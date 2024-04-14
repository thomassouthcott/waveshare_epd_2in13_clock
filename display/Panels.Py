from lib.waveshare_epd import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont

class Panel:
    def __init__(self):
        self.image = Image.new('1', (168, 35), 255)

    def draw(self):
        self.image = Image.new('1', (168, 35), 255)

class WeatherPanel(Panel):
    def __init__(self):
        super().__init__()

    def draw(self, weather):
        super().draw()