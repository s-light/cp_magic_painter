# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""RGB Lamp"""
import time

import board
from rainbowio import colorwheel
import adafruit_fancyled.adafruit_fancyled as fancy
from adafruit_fancyled.adafruit_fancyled import CHSV, CRGB
import adafruit_dotstar

import helper

from mode_base import ModeBaseClass


class RGBLamp(ModeBaseClass):
    config_defaults = {
        "rgblamp": {
            "mode": "nightlight",
            "brightness": 0.02,
            # duration for full fade from 0 to 1 in seconds
            "brightness_fade_duration": 10,
            # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
            # only specifying Hue → purple
            "base_color": CHSV(0.75),
            # "base_color": CRGB(255,0,255),
        },
    }

    brightness_map = [
        # in , out
        (0.0, 0.02),
        # in this range use brightness_mask
        (0.5, 0.02),
        (0.7, 0.1),
        (1.0, 0.7),
    ]
    # brightness_map_mask = [
    #     (0.0, 1),
    #     (1.0, 1),
    # ]

    def __init__(self, *, config={}):
        super(RGBLamp, self).__init__(config=config)

        self._brightness = 0.0

        print(42 * "*")
        print("RGBLamp")
        print(42 * "*")

        self.config_extend_with_defaults(defaults=self.config_defaults)
        # print(self.__class__, "config extended:")
        self.num_pixels = self.config["hw"]["pixel_count"]

        self.base_color = self.config["rgblamp"]["base_color"]

        # effect rainbow
        self.hue = 0.0
        self.cycle_duration = 1 * 60
        self.cycle_start = 0
        self.last_update = 0

        self.brightness_map_mask = [
            # in , out
            #      led_count on
            (0.0, 1),
            (0.3, ((0.3*2*10)+1)), # 7
            (0.5, self.num_pixels),
            (1.0, self.num_pixels),
        ]
        self.mask_pixel_active_count = self.num_pixels

        self.spi_init()

        self.brightness = self.config["rgblamp"]["brightness"]
        
        # print("brightness mapping test:")
        # for value in range(0, 105, 5):
        #     self.brightness = value / 100
        # # reset
        # self.brightness = self.config["rgblamp"]["brightness"]
        
        # run animation rendering one time.
        self.main_loop()

        self.spi_deinit()

    ##########################################
    # properties

    @property
    def brightness(self):
        # return ModeBaseClass.brightness
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        # super(POVPainter, self).brightness = value
        # https://github.com/python/cpython/issues/59170#issuecomment-1093581234
        # we need a workaround..
        # ModeBaseClass.brightness = value
        value = helper.limit(value, 0.0, 1.0)
        self._brightness = value
        # Remap brightness from 0.0-1.0 to brightness_range.
        # print("brightness - self.brightness:", self.brightness)
        # test = helper.map_01_to(value, 0.0, 0.7)
        # print("brightness - map_range:", test)
        # print("brightness - test:", test)

        value_mapped = helper.multi_map(value, self.brightness_map)
        self.pixels.brightness = value_mapped

        # mask things
        self.mask_pixel_active_count = int(helper.multi_map(value, self.brightness_map_mask))
        self.mask_pixel_black_count = self.num_pixels - self.mask_pixel_active_count
        # print("num_pixels", self.num_pixels)
        # print("mask_pixel_active_count", self.mask_pixel_active_count)
        # print("mask_pixel_black_count", self.mask_pixel_black_count)
        # if self.mask_pixel_black_count > 0:
        self.mask_black_array = [(0, 0, 0)] * (
            self.mask_pixel_black_count
        )
        # print("mask_black_array", self.mask_black_array)

        # print(
        #     "brightness - "
        #     "input:{: > 6.2f}  "
        #     "mask:{: > 4}  "
        #     "mapped:{: > 7.2f}  "
        #     "".format(
        #         value,
        #         self.mask_pixel_active_count,
        #         value_mapped,
        #     )
        # )

    def spi_init(self):
        self.pixels = adafruit_dotstar.DotStar(
            self.get_pin("pixel_spi_pins", "clock"),
            self.get_pin("pixel_spi_pins", "data"),
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
                self.brightness += 0.05
            elif touch_id == 1:
                self.brightness -= 0.05
            elif touch_id == 2:
                self.brightness = 0.01
            # print("brightness", self.brightness)
            # print("pixels.brightness", self.pixels.brightness)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # animation functions

    def handle_brightness_mask(self):
        if self.mask_pixel_black_count:
            self.pixels[0 : self.mask_pixel_black_count] = self.mask_black_array

    def nightlight_update(self):
        self.pixels.fill(self.base_color.pack())
        # self.pixels.fill(0)
        # self.pixels[-1] = (255, 0, 255)
        # self.pixels[-2] = (255, 0, 255)
        # self.pixels[-2] = (0, 0, 255)
        # self.pixels[-3] = (255, 0, 0)

    def rainbow_update(self):
        """based on CircuitPython Essentials DotStar example"""
        # TODO: implement FancyLED HSV version.
        # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#types-conversions-and-other-operations-2981225
        if self.hue > 255:
            self.hue = 0
        else:
            self.hue += 1

        # for i in range((self.num_pixels - 5), self.num_pixels):
        for i in range(self.num_pixels):
            rc_index = (i * 256 // (self.num_pixels * 3)) + self.hue
            self.pixels[i] = colorwheel(rc_index & 255)
        self.pixels.show()

    def main_loop(self):
        cycle_end = self.cycle_start + self.cycle_duration
        # TODO: implement cycle time thing..
        # map current runtime position to hue range 0..255
        # self.rainbow_update()
        self.nightlight_update()
        self.handle_brightness_mask()
        self.pixels.show()
        # print(time)
