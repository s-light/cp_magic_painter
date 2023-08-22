# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""RGB Lamp"""
import time

from rainbowio import colorwheel
import adafruit_dotstar
import board

from mode_base import ModeBaseClass 

class RGBLamp(ModeBaseClass):
    def __init__(self):
        super(RGBLamp, self).__init__()
        self.num_pixels = 36

        self.hue = 0
        self.cycle_duration = 1 * 60
        self.cycle_start = 0
        self.last_update = 0

        self.spi_init()
        self.spi_deinit()

    def spi_init(self):
        self.pixels = adafruit_dotstar.DotStar(
            board.SCK,
            board.MOSI,
            self.num_pixels,
            brightness=0.03,
            # brightness=0.4,
            auto_write=False,
        )

        self.pixels.fill((0, 0, 1))
        self.pixels.show()

    def spi_deinit(self):
        self.pixels.deinit()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # user interface

    def handle_user_input(self, touch_id, touch):
        if touch.fell:
            print("RGBLamp - handle_user_input: ", touch_id)
            if touch_id == 0:
                self.pixels.brightness += 0.01
            elif touch_id == 1:
                self.pixels.brightness -= 0.01
            elif touch_id == 2:
                self.pixels.brightness = 0.009
            print("pixels.brightness", self.pixels.brightness)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # animation functions

    def rainbow_update(self):
        """based on CircuitPython Essentials DotStar example"""
        if self.hue > 255:
            self.hue = 0
        else:
            self.hue += 1

        # for i in range((self.num_pixels-5), self.num_pixels):
        for i in range(self.num_pixels):
            rc_index = (i * 256 // (self.num_pixels * 3)) + self.hue
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()

    def main_loop(self):
        cycle_end = self.cycle_start + self.cycle_duration
        # TODO: map current runtime position to hue range 0..255
        self.rainbow_update()
        # print(time)
