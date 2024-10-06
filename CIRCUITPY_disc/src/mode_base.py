# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

"""Mode Base Class"""

import board

import helper
from config_base import ConfigBaseClass


class ModeBaseClass(ConfigBaseClass):
    __name__ = "ModeBaseClass"

    config_defaults = {
        "hw": {
            "pixel_color_order": "bgr",
            "pixel_count": 36,
            "pixel_spi_pins": {
                "clock": "SCK",
                "data": "MOSI",
            },
        },
    }
    config = {}

    def __init__(self, *, config={}, print_fn):
        super(ModeBaseClass, self).__init__(config=config)
        self.print = print

        # print("__init__ of ModeBaseClass....")
        # prepare internals
        self._brightness = -42.0

        # all other init things
        # self.load_config()
        self.config_extend_with_defaults(defaults=ModeBaseClass.config_defaults)
        # print("ModeBaseClass", "config extended:")
        # self.config_print()

        # self.statusline_template = "brightness: {brightness: >4.2f} "
        # self.statusline_template = ""

        # we need to to this as last action -
        # otherwise we get into dependency hell as not all things shown in status line are initialized..
        self.print = print_fn

    @property
    def brightness(self):
        """brightness Property. Range: 0..1"""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        # print("setter of x called")
        self._brightness = helper.limit(value, 0.0, 1.0)

    def spi_init(self):
        pass

    def spi_deinit(self):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # user interface

    statusline_template = ""

    def statusline_fn(self):
        """
        Generate statusline.

        NO prints in this function!!
        (leads to infinity loops..)
        """
        statusline = self.statusline_template.format(
            # brightness=self.brightness,
        )

        return statusline

    def handle_user_input(self, event):
        pass

    def handle_gesture(self, event):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main

    def main_loop(self):
        pass
