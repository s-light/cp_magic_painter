# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

"""Mode Base Class"""

import board

import helper
from config_base import ConfigBaseClass
class ModeBaseClass(ConfigBaseClass):

    config_defaults = {
        "hw": {
            "pixel_color_order": "bgr",
            "pixel_count": 36,
            "pixel_spi_pins": {
                "clock": "SCK",
                "data": "MOSI",
            },
            "accel_i2c_pins": {
                "clock": "SCL1",
                "data": "SDA1",
            },
        },

    }
    config = {}

    def __init__(self, *, config={}):
        super(ModeBaseClass, self).__init__(config=config)
        # print("__init__ of ModeBaseClass....")
        # prepare internals
        self._brightness = None

        # all other init things
        # self.load_config()
        self.config_extend_with_defaults(defaults=ModeBaseClass.config_defaults)
        # print("ModeBaseClass", "config extended:")
        # self.config_print()

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

    def get_pin(self, bus_name, pin_name):
        board_pin_name = self.config["hw"][bus_name][pin_name]
        return getattr(board, board_pin_name)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # user interface

    def handle_user_input(self, touch_id, touch):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main

    def main_loop(self):
        pass
