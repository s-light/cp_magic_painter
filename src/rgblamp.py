# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""CircuitPython Essentials DotStar example"""
import time
from rainbowio import colorwheel
import adafruit_dotstar
import board


class RGBLamp(object):
    def __init__(self):
        super(RGBLamp, self).__init__()
        self.num_pixels = 36
        self.pixels = adafruit_dotstar.DotStar(
            board.SCK,
            board.MOSI,
            self.num_pixels,
            brightness=0.03,
            # brightness=1,
            auto_write=False,
        )

        self.pixel.fill((0, 0, 1))
        self.pixels.show()

    def rainbow_cycle(wait):
        for j in range(255):
            for i in range((self.num_pixels-5), self.num_pixels):
                rc_index = (i * 256 // (num_pixels * 3)) + j
                pixels[i] = colorwheel(rc_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def main_loop():
        rainbow_cycle(0.6)
        # print(time)
