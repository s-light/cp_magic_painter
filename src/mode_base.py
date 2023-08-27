# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

"""Mode Base Class"""

import helper
class ModeBaseClass(object):
    def __init__(self):
        super(ModeBaseClass, self).__init__()
        
        # prepare internals
        self._brightness = None


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

    def handle_user_input(self, touch_id, touch):
        pass

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # main

    def main_loop(self):
        pass
