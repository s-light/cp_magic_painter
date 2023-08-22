# SPDX-FileCopyrightText: 2023 Stefan Krüger s-light.eu
# SPDX-License-Identifier: MIT

"""Mode Base Class"""

class ModeBaseClass(object):
    def __init__(self):
        super(ModeBaseClass, self).__init__()

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
