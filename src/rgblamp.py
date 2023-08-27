# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""RGB Lamp"""
import time

import board
from rainbowio import colorwheel
import adafruit_fancyled.adafruit_fancyled as fancy
import adafruit_dotstar

from mode_base import ModeBaseClass


class RGBLamp(ModeBaseClass):
    config_defaults = {
        # QT Py ESP32-S3
        "rgblamp": {
            "mode": "nightlight",
            "brightness": 0.01,
        },
    }
    config = {}

    def __init__(self, *, config={}):
        super(RGBLamp, self).__init__(config=config)

        print(42 * "*")
        print("RGBLamp")
        print(42 * "*")

        self.config_extend_with_defaults(defaults=self.config_defaults)
        print(self.__class__, "config extended:")
        self.num_pixels = self.config["hw"]["pixel_count"]

        self.hue = 0
        self.cycle_duration = 1 * 60
        self.cycle_start = 0
        self.last_update = 0

        self.spi_init()
        self.spi_deinit()

    # @brightness.setter
    # def brightness(self, value):
    #     # print("setter of x called")
    #     self._brightness = helper.limit(value, 0.0, 1.0)
    #     if  self._brightness > 0.1

    def spi_init(self):
        self.pixels = adafruit_dotstar.DotStar(
            self.get_pin("pixel_spi_pins","clock"),
            self.get_pin("pixel_spi_pins","data"),
            self.num_pixels,
            brightness=0.01,
            auto_write=False,
        )

        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def spi_deinit(self):
        self.pixels.deinit()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # user interface

    def handle_user_input(self, touch_id, touch):
        if touch.fell:
            # print("RGBLamp - handle_user_input: ", touch_id)
            if touch_id == 0:
                self.pixels.brightness += 0.01
            elif touch_id == 1:
                self.pixels.brightness -= 0.01
            elif touch_id == 2:
                self.pixels.brightness = 0.01
            print("pixels.brightness", self.pixels.brightness)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # animation functions

    def nightlight_update(self):
        self.pixels.fill(0)
        self.pixels[-1] = (255, 0, 255)
        self.pixels[-2] = (255, 0, 255)
        # self.pixels[-2] = (0, 0, 255)
        # self.pixels[-3] = (255, 0, 0)
        self.pixels.show()

    def rainbow_update(self):
        """based on CircuitPython Essentials DotStar example"""
        # TODO: implement FancyLED HSV version.
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#types-conversions-and-other-operations-2981225
        if self.hue > 255:
            self.hue = 0
        else:
            self.hue += 1

        # for i in range(self.num_pixels):
        for i in range((self.num_pixels - 5), self.num_pixels):
            rc_index = (i * 256 // (self.num_pixels * 3)) + self.hue
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()

    def main_loop(self):
        cycle_end = self.cycle_start + self.cycle_duration
        # TODO: implement cycle time thing..
        # map current runtime position to hue range 0..255
        # self.rainbow_update()
        self.nightlight_update()
        # print(time)
