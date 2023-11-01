# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-dotstar

"""RGB Lamp"""
import time
import math

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
            # "brightness_fade_duration": 10,
            # https://learn.adafruit.com/fancyled-library-for-circuitpython/colors#hsv-colors-2981215
            # only specifying Hue → purple
            "base_color": CHSV(0.75),
            # "base_color": CRGB(255,0,255),
            # effect duration in seconds
            "effect_duration": 10, 
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
        self.brightness_mapped = 0.0

        print(42 * "*")
        print("RGBLamp")
        print(42 * "*")

        self.config_extend_with_defaults(defaults=self.config_defaults)
        # print(self.__class__, "config extended:")
        self.num_pixels = self.config["hw"]["pixel_count"]

        self.base_color = self.config["rgblamp"]["base_color"]
        # print("self.base_color", self.base_color)

        # effect base
        self.effect_duration = self.config["rgblamp"]["effect_duration"]
        self.effect_start_cycle()
        self._offset = 0

        # effect rainbow
        self.hue = 0.0
        self.last_update = 0

        # effect plasma
        # self._hue_base = 0.5
        self._hue_min = 0.0
        self._hue_max = 1.0
        self._contrast = 1
        self._contrast_min = 0.5
        self._contrast_max = 1.0

        self.stepsize = 0.01
        self.hue_base = self.base_color.hue
        self.hue_half_width = 0.06
        self.animation_contrast = 0.99
        self.hue_range_update()
        # print("self.hue_base", self.hue_base)
        # brightness
        self.brightness_map_mask = [
            # in , out
            #      led_count on
            (0.0, 1),
            (0.3, ((0.3 * 2 * 10) + 1)),  # 7
            (0.5, self.num_pixels),
            (1.0, self.num_pixels),
        ]
        self.mask_pixel_active_count = self.num_pixels
        self.mask_pixel_black_count = self.num_pixels - self.mask_pixel_active_count

        self.spi_init()

        # print("brightness mapping test:")
        # for value in range(0, 105, 5):
        #     self.brightness = value / 100

        self.brightness = self.config["rgblamp"]["brightness"]

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
        # self.pixels.brightness = value_mapped
        self.brightness_mapped = value_mapped

        # mask things
        self.mask_pixel_active_count = int(
            helper.multi_map(value, self.brightness_map_mask)
        )
        self.mask_pixel_black_count = self.num_pixels - self.mask_pixel_active_count
        # print("num_pixels", self.num_pixels)
        # print("mask_pixel_active_count", self.mask_pixel_active_count)
        # print("mask_pixel_black_count", self.mask_pixel_black_count)
        # if self.mask_pixel_black_count > 0:
        self.mask_black_array = [(0, 0, 0)] * (self.mask_pixel_black_count)
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

    # @property
    # def hue_base(self):
    #     """Get hue_base value."""
    #     return self._hue_base

    # @hue_base.setter
    # def hue_base(self, value):
    #     """Set hue_base value."""
    #     self._hue_base = value
    #     self.hue_range_update()

    def hue_range_update(self):
        self._hue_min = self.hue_base - self.hue_half_width
        self._hue_max = self.hue_base + self.hue_half_width

    # @property
    # def animation_contrast(self):
    #     """Get animation_contrast value."""
    #     return self._contrast

    # @animation_contrast.setter
    # def animation_contrast(self, value):
    #     """Set animation_contrast value."""
    #     self._contrast = value
    #     # self._contrast_min = self._contrast - 0.5
    #     # self._contrast_max = self._contrast + 0.5
    #     self._contrast_min = 1 - self._contrast
    #     self._contrast_max = 1

    ##########################################
    # hw

    def spi_init(self):
        self.pixels = adafruit_dotstar.DotStar(
            helper.get_pin(
                config=self.config, bus_name="pixel_spi_pins", pin_name="clock"
            ),
            helper.get_pin(
                config=self.config, bus_name="pixel_spi_pins", pin_name="data"
            ),
            self.num_pixels,
            # brightness=0.01,
            auto_write=False,
        )

        self.main_loop()

    def spi_deinit(self):
        self.pixels.deinit()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # user interface

    def handle_user_input(self, touch_id, touch):
        if touch.rose:
            # print("RGBLamp - handle_user_input: ", touch_id)
            if touch_id == 0:
                self.brightness += 0.05
            elif touch_id == 1:
                self.brightness -= 0.05
            elif touch_id == 2:
                self.brightness = 0.01
            print("(touch ", touch_id, ") brightness", self.brightness)
            # print("pixels.brightness", self.pixels.brightness)

    def handle_gesture(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # animation functions

    def effect_start_cycle(self):
        print("effect_start_cycle")
        self.effect_start_ts = time.monotonic()
        self.effect_end_ts = self.effect_start_ts + self.effect_duration
        
    def offset_update(self):
        # stop_ts animation if  brightness is to low / only a view LEDs are on..
        if self.brightness > 0.05:
            if time.monotonic() >= (self.effect_start_ts + self.effect_duration):
                self.effect_start_cycle()
            self._offset = helper.map_to_01(time.monotonic(), self.effect_start_ts, self.effect_end_ts)

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

        if self.hue > 1.0:
            self.hue = 0.0
        else:
            self.hue += 0.001

        for i in range(self.num_pixels):
            pixel_pos = helper.map_to_01(i, 0, self.num_pixels)
            color = CHSV(self.hue + pixel_pos)
            # handle gamma and global brightness
            color_rgb = fancy.gamma_adjust(color, brightness=self.brightness_mapped)
            self.pixels[i] = color_rgb.pack()

    def plasma_update(self):
        """simple plasma animation."""
        # mostly inspired by
        # https://www.bidouille.org/prog/plasma
        # extracted from magic_crystal_animation
        plasma_offset = helper.map_01_to(self._offset, 0.0, (math.pi * 30))
        for i in range(self.num_pixels):
            col = 0.0
            row = helper.map_range(
                i,
                0,
                self.num_pixels - 1,
                # 0, 1.0
                -0.5,
                0.5,
            )

            # moving rings
            cx = col + 0.5 * math.sin(plasma_offset / 5)
            cy = row + 0.5 * math.cos(plasma_offset / 3)
            value = math.sin(math.sqrt(100 * (cx * cx + cy * cy) + 1) + plasma_offset)
            # mapping
            contrast = helper.map_range(
                value, -1, 1, self._contrast_min, self._contrast_max
            )
            hue = helper.map_range(value, -1, 1, self._hue_min, self._hue_max)
            # map to color
            # color = fancy.CHSV(hue, v=contrast)
            color = fancy.CHSV(hue)
            # handle gamma and global brightness
            color_rgb = fancy.gamma_adjust(color, brightness=self.brightness_mapped)
            self.pixels[i] = color_rgb.pack()

    def main_loop(self):
        # TODO: implement cycle time thing..
        self.offset_update()

        # self.rainbow_update()
        self.plasma_update()
        # self.nightlight_update()

        self.handle_brightness_mask()
        self.pixels.show()
        # print(time)
